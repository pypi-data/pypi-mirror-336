import json
import time
from typing import Dict, Any, Optional, List, Union, Type, TypeVar, get_type_hints
from threading import Lock
import contextlib
import sys, os

# Import needed modules
from cloudweave.utilities import Singleton
from cloudweave.logging_manager import Logger, LoggerType

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from bson import ObjectId
from pydantic import BaseModel, Field, create_model

T = TypeVar('T', bound=BaseModel)

class MongoDBDoc:
    """
    Dictionary-like wrapper for MongoDB documents.
    Provides a seamless interface similar to dictionary access.
    """
    
    def __init__(self, manager: 'MongoDBManager', model_class: Type[BaseModel], doc_id: str, data: Dict[str, Any] = None):
        """
        Initialize a new MongoDB document wrapper.
        
        Args:
            manager: MongoDBManager instance
            model_class: Pydantic model class
            doc_id: Document ID
            data: Optional data to initialize with
        """
        self.manager = manager
        self.model_class = model_class
        self.doc_id = doc_id
        self.collection_name = manager._get_collection_name(model_class)
        self._data = data or self._load_data()
        
    def _load_data(self) -> Dict[str, Any]:
        """Load document data from MongoDB."""
        data = self.manager.get_document(self.doc_id, self.collection_name)
        if data is None:
            error_msg = f"Document with ID {self.doc_id} not found in collection {self.collection_name}"
            self.manager.logger.error(error_msg)
            raise KeyError(error_msg)
        return data
        
    def __getitem__(self, key: str) -> Any:
        """Get an attribute value."""
        if key not in self._data:
            self._data = self._load_data()  # Refresh data
        return self._data.get(key)
        
    def __setitem__(self, key: str, value: Any) -> None:
        """Set an attribute value and update in MongoDB."""
        self._data[key] = value
        self.manager.update_document(self.doc_id, self.collection_name, {key: value})
        
    def get(self, key: str, default: Any = None) -> Any:
        """Get an attribute value with a default."""
        try:
            return self[key]
        except (KeyError, AttributeError):
            return default
            
    def update(self, updates: Dict[str, Any]) -> None:
        """Update multiple attributes at once."""
        self._data.update(updates)
        self.manager.update_document(self.doc_id, self.collection_name, updates)
        
    def refresh(self) -> None:
        """Refresh data from MongoDB."""
        self._data = self._load_data()
        
    def delete(self) -> None:
        """Delete this document from MongoDB."""
        self.manager.delete_document(self.doc_id, self.collection_name)
        self._data = {}
        
    def to_dict(self) -> Dict[str, Any]:
        """Get a dictionary representation of the document."""
        return self._data.copy()


class PyObjectId(ObjectId):
    """
    Custom ObjectId field for Pydantic models to handle MongoDB _id fields.
    """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class MongoDBManager(Singleton):
    """
    Thread-safe singleton manager for MongoDB operations.
    Provides seamless integration with Pydantic models for collection-like operations.
    """
    
    def _initialize(self, 
                  connection_string: str, 
                  database_name: str,
                  namespace: str,
                  logger_options: Dict[str, Any] = None):
        """
        Initialize MongoDB connection and manager state.
        
        Args:
            connection_string: MongoDB connection string
            database_name: Database name
            namespace: Namespace prefix for collection names
            logger_options: Optional logger configuration
        """
        self.connection_string = connection_string
        self.database_name = database_name
        self.namespace = namespace
        self._client = None
        self._db = None
        self._connection_lock = Lock()
        self._model_collection_map = {}  # Maps model classes to collection names
        self._indexed_fields = {}  # Maps collection names to fields that should be indexed
        
        # Initialize the logger
        self._setup_logger(logger_options or {})
        
        # Initialize MongoDB connection
        self._setup_mongodb()
    
    def _setup_logger(self, logger_options: Dict[str, Any]) -> None:
        """
        Set up the logger for this MongoDBManager instance.
        
        Args:
            logger_options: Logger configuration options
        """
        if 'logger_instance' in logger_options:
            self.logger = logger_options['logger_instance']
            self.logger.info("Using provided logger instance for MongoDBManager")
        else:
            # Create a new logger
            log_level = logger_options.get('log_level', 'info')
            log_namespace = logger_options.get('namespace', f"mongodb-{self.namespace}")
            
            self.logger = Logger(
                logger_type=logger_options.get('logger_type', 'local'),
                namespace=log_namespace,
                instance_id=logger_options.get('instance_id', f"mongodb-manager-{self.namespace}"),
                log_level=log_level,
                **{k: v for k, v in logger_options.items() if k not in ['logger_type', 'namespace', 'instance_id', 'log_level']}
            )
            self.logger.info(f"Created new logger for MongoDBManager with namespace '{log_namespace}'")
    
    def _setup_mongodb(self) -> None:
        """
        Initialize MongoDB connection with proper error handling.
        """
        if self._client is not None and self._db is not None:
            return
            
        with self._connection_lock:
            if self._client is not None and self._db is not None:
                return
                
            try:
                self.logger.info(f"Initializing MongoDB connection to {self.database_name}")
                
                # Initialize MongoDB client
                self._client = MongoClient(self.connection_string)
                
                # Initialize database
                self._db = self._client[self.database_name]
                
                # Test connection
                self._client.admin.command('ping')
                
                self.logger.info(f"MongoDB connection successfully initialized for namespace: {self.namespace}")
                
            except Exception as e:
                self._cleanup()
                error_msg = f"MongoDB initialization failed: {e}"
                self.logger.error(error_msg)
                raise ConnectionError(error_msg) from e
    
    def _cleanup(self) -> None:
        """Clean up MongoDB resources and reset connection state."""
        with self._connection_lock:
            if self._client:
                try:
                    self.logger.debug("Cleaning up MongoDB resources")
                    self._client.close()
                    self.logger.debug("MongoDB connection closed successfully")
                except Exception as e:
                    self.logger.error(f"Error during MongoDB cleanup: {e}")
                finally:
                    self._client = None
                    self._db = None
    
    def __del__(self):
        """Ensure proper cleanup on object deletion."""
        self._cleanup()
    
    @contextlib.contextmanager
    def connection(self):
        """Context manager for safe MongoDB operations."""
        if not self._db:
            error_msg = "MongoDB connection not initialized"
            self.logger.error(error_msg)
            raise ConnectionError(error_msg)
            
        try:
            self.logger.debug("Entering MongoDB connection context")
            yield self._db
        except Exception as e:
            self.logger.error(f"Error during MongoDB operation: {e}")
            raise
        finally:
            self.logger.debug("Exiting MongoDB connection context")
    
    def _get_collection_name(self, model_class: Type[BaseModel]) -> str:
        """
        Get the collection name for a model class.
        
        Args:
            model_class: Pydantic model class
            
        Returns:
            Collection name in MongoDB
        """
        # Check if we have a mapping already
        if model_class in self._model_collection_map:
            return self._model_collection_map[model_class]
        
        # Default to lowercase model name
        collection_name = f"{self.namespace}_{model_class.__name__.lower()}"
        return collection_name
    
    def _get_collection(self, collection_name: str) -> Collection:
        """
        Get a MongoDB collection by name.
        
        Args:
            collection_name: Collection name
            
        Returns:
            MongoDB collection
        """
        if not self._db:
            error_msg = "MongoDB connection not initialized"
            self.logger.error(error_msg)
            raise ConnectionError(error_msg)
            
        # Prepend namespace if not already present
        if not collection_name.startswith(f"{self.namespace}_"):
            full_collection_name = f"{self.namespace}_{collection_name}"
        else:
            full_collection_name = collection_name
            
        return self._db[full_collection_name]
    
    def register_model(self, model_class: Type[BaseModel], collection_name: Optional[str] = None, indexed_fields: Optional[List[str]] = None) -> None:
        """
        Register a model class with a specific collection name.
        
        Args:
            model_class: Pydantic model class to register
            collection_name: Optional custom collection name
            indexed_fields: Optional list of fields to be indexed
        """
        if collection_name:
            full_collection_name = f"{self.namespace}_{collection_name}"
            self._model_collection_map[model_class] = full_collection_name
        else:
            full_collection_name = self._get_collection_name(model_class)
            self._model_collection_map[model_class] = full_collection_name
            
        self.logger.info(f"Registered model {model_class.__name__} with collection {full_collection_name}")
        
        # Store indexed fields
        if indexed_fields:
            self._indexed_fields[full_collection_name] = indexed_fields
            
            # Create indexes
            collection = self._get_collection(full_collection_name)
            for field in indexed_fields:
                self.logger.info(f"Creating index on field '{field}' in collection {full_collection_name}")
                collection.create_index(field)
    
    def ensure_collection_exists(self, model_class: Type[BaseModel], indexed_fields: Optional[List[str]] = None) -> None:
        """
        Ensure a collection exists for the given Pydantic model and create indexes.
        
        Args:
            model_class: Pydantic model class
            indexed_fields: Optional list of fields to create indexes for
        """
        collection_name = self._get_collection_name(model_class)
        
        self.logger.info(f"Ensuring collection {collection_name} exists for model {model_class.__name__}")
        
        # MongoDB creates collections implicitly, but we can create indexes
        if indexed_fields:
            collection = self._get_collection(collection_name)
            for field in indexed_fields:
                self.logger.info(f"Creating index on field '{field}' in collection {collection_name}")
                try:
                    collection.create_index(field)
                except Exception as e:
                    self.logger.error(f"Error creating index on field '{field}': {e}")
                    
            self._indexed_fields[collection_name] = indexed_fields
        
        # Register the model if not already registered
        if model_class not in self._model_collection_map:
            self._model_collection_map[model_class] = collection_name
    
    def _prepare_document(self, item_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare a document for MongoDB storage.
        
        Args:
            item_dict: Dictionary to prepare
            
        Returns:
            Dictionary suitable for MongoDB
        """
        # Convert any Pydantic models to dictionaries
        for key, value in list(item_dict.items()):
            if isinstance(value, BaseModel):
                item_dict[key] = value.model_dump()
                self.logger.debug(f"Converted Pydantic model to dict for field '{key}'")
            elif isinstance(value, dict):
                item_dict[key] = self._prepare_document(value)
                
        return item_dict
    
    def _object_id_to_str(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert MongoDB ObjectId to string.
        
        Args:
            doc: Document with ObjectId
            
        Returns:
            Document with string ID
        """
        if '_id' in doc:
            doc['id'] = str(doc['_id'])
            del doc['_id']
        return doc
    
    def _str_to_object_id(self, doc_id: str) -> ObjectId:
        """
        Convert string ID to MongoDB ObjectId.
        
        Args:
            doc_id: String ID
            
        Returns:
            MongoDB ObjectId
        """
        try:
            return ObjectId(doc_id)
        except Exception:
            return doc_id
    
    def put_item(self, item: BaseModel) -> str:
        """
        Store a Pydantic model instance in MongoDB.
        
        Args:
            item: Pydantic model instance to store
            
        Returns:
            Document ID of the created document
        """
        if not self._db:
            error_msg = "MongoDB connection not initialized"
            self.logger.error(error_msg)
            raise ConnectionError(error_msg)
        
        # Get collection name
        collection_name = self._get_collection_name(item.__class__)
        collection = self._get_collection(collection_name)
        
        self.logger.info(f"Adding document to collection {collection_name}")
        self.logger.debug(f"Model type: {item.__class__.__name__}")
        
        # Convert model to dict
        item_dict = item.model_dump()
        
        # Remove id field if None
        if 'id' in item_dict and item_dict['id'] is None:
            del item_dict['id']
        
        # Rename id to _id if present
        if 'id' in item_dict:
            item_dict['_id'] = self._str_to_object_id(item_dict['id'])
            del item_dict['id']
        
        # Add timestamps if not present
        if 'created_at' not in item_dict:
            item_dict['created_at'] = int(time.time())
        if 'updated_at' not in item_dict:
            item_dict['updated_at'] = int(time.time())
        
        # Prepare the document
        item_dict = self._prepare_document(item_dict)
        
        try:
            # Insert the document
            result = collection.insert_one(item_dict)
            doc_id = str(result.inserted_id)
            self.logger.info(f"Successfully added document with ID {doc_id} to collection {collection_name}")
            return doc_id
        except Exception as e:
            self.logger.error(f"Error adding document to collection {collection_name}: {e}")
            raise
    
    def get_item(self, model_class: Type[T], doc_id: str) -> Optional[MongoDBDoc]:
        """
        Get a document from MongoDB by ID and return as a MongoDBDoc.
        
        Args:
            model_class: Pydantic model class
            doc_id: Document ID
            
        Returns:
            MongoDBDoc instance or None if not found
        """
        if not self._db:
            error_msg = "MongoDB connection not initialized"
            self.logger.error(error_msg)
            raise ConnectionError(error_msg)
        
        collection_name = self._get_collection_name(model_class)
        
        self.logger.debug(f"Getting document with ID {doc_id} from collection {collection_name}")
        
        try:
            # Get the document
            collection = self._get_collection(collection_name)
            doc = collection.find_one({"_id": self._str_to_object_id(doc_id)})
            
            if doc:
                # Convert to dictionary with string ID
                self.logger.debug(f"Document found: {doc_id}")
                doc = self._object_id_to_str(doc)
                # Return as MongoDBDoc for dictionary-like access
                return MongoDBDoc(self, model_class, doc_id, doc)
                
            self.logger.debug(f"Document not found: {doc_id}")
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting document {doc_id}: {e}")
            return None
    
    def get_document(self, doc_id: str, collection_name: str) -> Optional[Dict[str, Any]]:
        """
        Get a document from MongoDB by ID.
        
        Args:
            doc_id: Document ID
            collection_name: Collection name
            
        Returns:
            Document data as dictionary or None if not found
        """
        if not self._db:
            error_msg = "MongoDB connection not initialized"
            self.logger.error(error_msg)
            raise ConnectionError(error_msg)
        
        self.logger.debug(f"Getting document with ID {doc_id} from collection {collection_name}")
        
        try:
            # Get the collection
            collection = self._get_collection(collection_name)
            
            # Get the document
            doc = collection.find_one({"_id": self._str_to_object_id(doc_id)})
            
            if doc:
                # Convert to dictionary with string ID
                self.logger.debug(f"Document found: {doc_id}")
                return self._object_id_to_str(doc)
                
            self.logger.debug(f"Document not found: {doc_id}")
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting document {doc_id}: {e}")
            return None
    
    def update_document(self, doc_id: str, collection_name: str, updates: Dict[str, Any]) -> None:
        """
        Update a document in MongoDB.
        
        Args:
            doc_id: Document ID
            collection_name: Collection name
            updates: Dictionary of fields to update
        """
        if not self._db:
            error_msg = "MongoDB connection not initialized"
            self.logger.error(error_msg)
            raise ConnectionError(error_msg)
        
        self.logger.info(f"Updating document with ID {doc_id} in collection {collection_name}")
        self.logger.debug(f"Update fields: {list(updates.keys())}")
        
        try:
            # Get the collection
            collection = self._get_collection(collection_name)
            
            # Add updated_at timestamp if not already in updates
            if 'updated_at' not in updates:
                updates['updated_at'] = int(time.time())
            
            # Prepare updates
            prepared_updates = self._prepare_document(updates)
            
            # Update the document
            result = collection.update_one(
                {"_id": self._str_to_object_id(doc_id)},
                {"$set": prepared_updates}
            )
            
            if result.modified_count > 0:
                self.logger.info(f"Successfully updated document with ID {doc_id} in collection {collection_name}")
            else:
                self.logger.warning(f"Document with ID {doc_id} not modified (might not exist or no changes made)")
                
        except Exception as e:
            self.logger.error(f"Error updating document {doc_id}: {e}")
            raise
    
    def delete_document(self, doc_id: str, collection_name: str) -> None:
        """
        Delete a document from MongoDB.
        
        Args:
            doc_id: Document ID
            collection_name: Collection name
        """
        if not self._db:
            error_msg = "MongoDB connection not initialized"
            self.logger.error(error_msg)
            raise ConnectionError(error_msg)
        
        self.logger.info(f"Deleting document with ID {doc_id} from collection {collection_name}")
        
        try:
            # Get the collection
            collection = self._get_collection(collection_name)
            
            # Delete the document
            result = collection.delete_one({"_id": self._str_to_object_id(doc_id)})
            
            if result.deleted_count > 0:
                self.logger.info(f"Successfully deleted document with ID {doc_id} from collection {collection_name}")
            else:
                self.logger.warning(f"Document with ID {doc_id} not found for deletion")
                
        except Exception as e:
            self.logger.error(f"Error deleting document {doc_id}: {e}")
            raise
    
    def query(self, model_class: Type[BaseModel], filters: Dict[str, Any] = None) -> List[MongoDBDoc]:
        """
        Query documents based on filter conditions.
        
        Args:
            model_class: Pydantic model class
            filters: Dictionary of field-value pairs to filter by
            
        Returns:
            List of MongoDBDoc instances matching the query
        """
        if not self._db:
            error_msg = "MongoDB connection not initialized"
            self.logger.error(error_msg)
            raise ConnectionError(error_msg)
        
        collection_name = self._get_collection_name(model_class)
        collection = self._get_collection(collection_name)
        
        self.logger.info(f"Querying documents from collection {collection_name}")
        if filters:
            self.logger.debug(f"Filters: {filters}")
        
        # Prepare filter conditions
        query_filter = filters or {}
        
        try:
            # Execute the query
            docs = collection.find(query_filter)
            
            # Convert to MongoDBDoc instances
            results = []
            for doc in docs:
                doc = self._object_id_to_str(doc)
                results.append(MongoDBDoc(self, model_class, doc['id'], doc))
            
            self.logger.info(f"Query returned {len(results)} documents from {collection_name}")
            return results
            
        except Exception as e:
            self.logger.error(f"Error querying documents from {collection_name}: {e}")
            raise
    
    def query_documents(self, collection_name: str, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Query documents based on filter conditions and return raw dictionaries.
        
        Args:
            collection_name: Collection name
            filters: Dictionary of field-value pairs to filter by
            
        Returns:
            List of document dictionaries matching the query
        """
        if not self._db:
            error_msg = "MongoDB connection not initialized"
            self.logger.error(error_msg)
            raise ConnectionError(error_msg)
        
        self.logger.info(f"Querying documents from collection {collection_name}")
        if filters:
            self.logger.debug(f"Filters: {filters}")
        
        collection = self._get_collection(collection_name)
        
        # Prepare filter conditions
        query_filter = filters or {}
        
        try:
            # Execute the query
            docs = collection.find(query_filter)
            
            # Convert to dictionaries with string IDs
            results = []
            for doc in docs:
                results.append(self._object_id_to_str(doc))
            
            self.logger.info(f"Query returned {len(results)} documents from {collection_name}")
            return results
            
        except Exception as e:
            self.logger.error(f"Error querying documents from {collection_name}: {e}")
            raise
    
    def query_with_projection(self, 
                            model_class: Type[BaseModel], 
                            filters: Dict[str, Any] = None,
                            projection: Dict[str, int] = None,
                            sort: List[tuple] = None,
                            limit: int = None) -> List[Dict[str, Any]]:
        """
        Query documents with projection, sorting and limit.
        
        Args:
            model_class: Pydantic model class
            filters: Dictionary of field-value pairs to filter by
            projection: Dictionary specifying which fields to include/exclude
            sort: List of (field, direction) tuples for sorting
            limit: Maximum number of documents to return
            
        Returns:
            List of document dictionaries matching the query
        """
        if not self._db:
            error_msg = "MongoDB connection not initialized"
            self.logger.error(error_msg)
            raise ConnectionError(error_msg)
        
        collection_name = self._get_collection_name(model_class)
        collection = self._get_collection(collection_name)
        
        self.logger.info(f"Executing advanced query on collection {collection_name}")
        if filters:
            self.logger.debug(f"Filters: {filters}")
        if projection:
            self.logger.debug(f"Projection: {projection}")
        if sort:
            self.logger.debug(f"Sort: {sort}")
        if limit:
            self.logger.debug(f"Limit: {limit}")
        
        # Prepare filter conditions
        query_filter = filters or {}
        
        try:
            # Start with basic query
            cursor = collection.find(query_filter, projection)
            
            # Apply sorting if specified
            if sort:
                cursor = cursor.sort(sort)
                
            # Apply limit if specified
            if limit:
                cursor = cursor.limit(limit)
            
            # Convert to dictionaries with string IDs
            results = []
            for doc in cursor:
                results.append(self._object_id_to_str(doc))
            
            self.logger.info(f"Advanced query returned {len(results)} documents from {collection_name}")
            return results
            
        except Exception as e:
            self.logger.error(f"Error executing advanced query on {collection_name}: {e}")
            raise
    
    def query_with_aggregation(self, 
                             model_class: Type[BaseModel], 
                             pipeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Execute an aggregation pipeline.
        
        Args:
            model_class: Pydantic model class
            pipeline: MongoDB aggregation pipeline
            
        Returns:
            List of document dictionaries from the aggregation result
        """
        if not self._db:
            error_msg = "MongoDB connection not initialized"
            self.logger.error(error_msg)
            raise ConnectionError(error_msg)
        
        collection_name = self._get_collection_name(model_class)
        collection = self._get_collection(collection_name)
        
        self.logger.info(f"Executing aggregation pipeline on collection {collection_name}")
        self.logger.debug(f"Pipeline stages: {len(pipeline)}")
        
        try:
            # Execute the aggregation
            results = list(collection.aggregate(pipeline))
            
            # Convert ObjectIds to strings in results
            for doc in results:
                if '_id' in doc and isinstance(doc['_id'], ObjectId):
                    doc['id'] = str(doc['_id'])
                    del doc['_id']
            
            self.logger.info(f"Aggregation returned {len(results)} documents from {collection_name}")
            return results
            
        except Exception as e:
            self.logger.error(f"Error executing aggregation on {collection_name}: {e}")
            raise
    
    def create_model_from_document(self, doc_id: str, collection_name: str, model_name: str = "DynamicModel") -> Optional[BaseModel]:
        """
        Create a Pydantic model instance from a MongoDB document.
        
        Args:
            doc_id: Document ID
            collection_name: Collection name
            model_name: Name for the dynamically created model class
            
        Returns:
            Pydantic model instance or None if document not found
        """
        self.logger.info(f"Creating dynamic model from document {doc_id} in collection {collection_name}")
        
        # Get the document
        doc_data = self.get_document(doc_id, collection_name)
        
        if not doc_data:
            self.logger.warning(f"Document {doc_id} not found in collection {collection_name}")
            return None
        
        try:
            # Create field definitions for the model
            field_definitions = {}
            for key, value in doc_data.items():
                if isinstance(value, str):
                    field_definitions[key] = (str, value)
                elif isinstance(value, int):
                    field_definitions[key] = (int, value)
                elif isinstance(value, float):
                    field_definitions[key] = (float, value)
                elif isinstance(value, bool):
                    field_definitions[key] = (bool, value)
                elif isinstance(value, dict):
                    field_definitions[key] = (dict, value)
                elif isinstance(value, list):
                    field_definitions[key] = (list, value)
                else:
                    # Default to Any type
                    field_definitions[key] = (Any, value)
                    
            self.logger.debug(f"Created field definitions for model {model_name}")
            
            # Create a dynamic Pydantic model
            DynamicModel = create_model(model_name, **field_definitions)
            
            # Create an instance of the model
            self.logger.info(f"Successfully created dynamic model {model_name} from document {doc_id}")
            return DynamicModel(**doc_data)
            
        except Exception as e:
            self.logger.error(f"Error creating dynamic model: {e}")
            return None
    
    def get_or_create(self, model_class: Type[BaseModel], doc_id: str, default_data: Dict[str, Any] = None) -> MongoDBDoc:
        """
        Get a document if it exists or create it with default data.
        
        Args:
            model_class: Pydantic model class
            doc_id: Document ID
            default_data: Default data for new document
            
        Returns:
            MongoDBDoc instance
        """
        if not self._db:
            raise ConnectionError("MongoDB connection not initialized")
        
        collection_name = self._get_collection_name(model_class)
        collection = self._get_collection(collection_name)
        
        # Try to get the document
        doc = collection.find_one({"_id": self._str_to_object_id(doc_id)})
        
        if doc:
            # Return existing document
            doc = self._object_id_to_str(doc)
            return MongoDBDoc(self, model_class, doc_id, doc)
        else:
            # Create new document with default data
            if default_data is None:
                default_data = {}
            
            # Add ID and timestamps
            default_data['_id'] = self._str_to_object_id(doc_id)
            if 'created_at' not in default_data:
                default_data['created_at'] = int(time.time())
            if 'updated_at' not in default_data:
                default_data['updated_at'] = int(time.time())
            
            # Insert the document
            collection.insert_one(default_data)
            
            # Convert to dictionary with string ID
            default_data = self._object_id_to_str(default_data)
            
            # Return the new document
            return MongoDBDoc(self, model_class, doc_id, default_data)
    
    def batch_write(self, operations: List[Dict[str, Any]]) -> None:
        """
        Perform batch write operations on MongoDB.
        
        Args:
            operations: List of operation dictionaries with 'type', 'collection', 'doc_id', and 'data' keys
        """
        if not self._db:
            raise ConnectionError("MongoDB connection not initialized")
        
        for op in operations:
            op_type = op['type']  # 'insert', 'update', 'delete'
            collection_name = op['collection']
            collection = self._get_collection(collection_name)
            
            if op_type == 'insert':
                # Insert operation
                data = op['data'].copy()
                
                # Add timestamps if not present
                if 'created_at' not in data:
                    data['created_at'] = int(time.time())
                if 'updated_at' not in data:
                    data['updated_at'] = int(time.time())
                
                # Insert the document
                collection.insert_one(self._prepare_document(data))
                
            elif op_type == 'update':
                # Update operation
                doc_id = op['doc_id']
                data = op['data'].copy()
                
                # Add updated_at timestamp if not present
                if 'updated_at' not in data:
                    data['updated_at'] = int(time.time())
                
                # Update the document
                collection.update_one(
                    {"_id": self._str_to_object_id(doc_id)},
                    {"$set": self._prepare_document(data)}
                )
                
            elif op_type == 'delete':
                # Delete operation
                doc_id = op['doc_id']
                collection.delete_one({"_id": self._str_to_object_id(doc_id)})
        
        self.logger.info(f"Batch operation completed with {len(operations)} operations")
    
    def model_to_mongo_doc(self, item: BaseModel) -> MongoDBDoc:
        """
        Convert a Pydantic model instance to a MongoDBDoc.
        
        Args:
            item: Pydantic model instance
            
        Returns:
            MongoDBDoc instance
        """
        # Store the item if it doesn't already exist
        item_dict = item.model_dump()
        doc_id = item_dict.get('id')
        
        if not doc_id:
            # Store the item to get an ID
            doc_id = self.put_item(item)
            item_dict['id'] = doc_id
        else:
            # Check if the item exists
            collection_name = self._get_collection_name(item.__class__)
            collection = self._get_collection(collection_name)
            doc = collection.find_one({"_id": self._str_to_object_id(doc_id)})
            
            if not doc:
                # Store the item
                self.put_item(item)
        
        # Return as MongoDBDoc
        return MongoDBDoc(self, item.__class__, doc_id, item_dict)
    
    def count_documents(self, model_class: Type[BaseModel], filters: Dict[str, Any] = None) -> int:
        """
        Count documents matching filter criteria.
        
        Args:
            model_class: Pydantic model class
            filters: Dictionary of field-value pairs to filter by
            
        Returns:
            Number of matching documents
        """
        if not self._db:
            raise ConnectionError("MongoDB connection not initialized")
        
        collection_name = self._get_collection_name(model_class)
        collection = self._get_collection(collection_name)
        
        # Prepare filter conditions
        query_filter = filters or {}
        
        # Count documents
        return collection.count_documents(query_filter)
    
    def drop_collection(self, model_class: Type[BaseModel]) -> None:
        """
        Drop a collection.
        
        Args:
            model_class: Pydantic model class
        """
        if not self._db:
            raise ConnectionError("MongoDB connection not initialized")
        
        collection_name = self._get_collection_name(model_class)
        collection = self._get_collection(collection_name)
        
        # Drop the collection
        collection.drop()
        self.logger.info(f"Dropped collection {collection_name}")


# Example usage
if __name__ == "__main__":
    from pydantic import BaseModel, Field
    
    # Define a Pydantic model
    class User(BaseModel):
        id: Optional[str] = None
        name: str
        email: str
        age: Optional[int] = None
        is_active: bool = True
        metadata: Dict[str, Any] = Field(default_factory=dict)
    
    # Initialize MongoDB manager
    mongo = MongoDBManager(
        connection_string="mongodb://localhost:27017/",
        database_name="myapp",
        namespace="myapp"
    )
    
    # Register the model with indexed fields
    mongo.register_model(User, "users", indexed_fields=["email", "is_active"])
    
    # Create a user
    user = User(name="Test User", email="test@example.com")
    user_id = mongo.put_item(user)
    
    # Get the user as a MongoDBDoc
    user_doc = mongo.get_item(User, user_id)
    
    # Access and update attributes
    print(user_doc["name"])  # Output: Test User
    user_doc["age"] = 30
    
    # Update multiple attributes
    user_doc.update({
        "name": "Updated Name",
        "metadata": {"last_login": "2023-03-15"}
    })
    
    # Query users
    active_users = mongo.query(User, {"is_active": True})
    
    # Delete the user
    user_doc.delete()