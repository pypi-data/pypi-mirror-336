import json
import time
import abc
from typing import Dict, Any, Optional, List, Union, Type, TypeVar, get_type_hints
from threading import Lock
import weakref
import contextlib
import sys
import os

from cloudweave.cloud_session_utils import GCPManager
from cloudweave.utilities import Singleton
from cloudweave.logging_manager import Logger, LoggerType

import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin.auth import Client
from google.cloud import firestore as fs
from google.cloud.firestore_v1.base_query import FieldFilter
from pydantic import BaseModel, create_model

T = TypeVar('T', bound=BaseModel)

class FirestoreItem:
    """
    Dictionary-like wrapper for interacting with Firestore documents.
    Provides a seamless interface similar to dictionary access.
    """
    
    def __init__(self, manager: 'FirestoreManager', model_class: Type[BaseModel], doc_id: str, data: Dict[str, Any] = None):
        """
        Initialize a new Firestore item wrapper.
        
        Args:
            manager: FirestoreManager instance
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
        """Load document data from Firestore."""
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
        """Set an attribute value and update in Firestore."""
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
        """Refresh data from Firestore."""
        self._data = self._load_data()
        
    def delete(self) -> None:
        """Delete this document from Firestore."""
        self.manager.delete_document(self.doc_id, self.collection_name)
        self._data = {}
        
    def to_dict(self) -> Dict[str, Any]:
        """Get a dictionary representation of the document."""
        return self._data.copy()


class FirestoreManager(Singleton):
    """
    Thread-safe singleton manager for Firestore operations.
    Provides seamless integration with Pydantic models for table-like operations.
    Uses GCPManager for authentication.
    """
    
    def _initialize(self, namespace: str, credentials_path: Optional[str] = None, credentials_dict: Optional[Dict[str, Any]] = None, project_id: Optional[str] = None, logger_options: Dict[str, Any] = None) -> None:
        """
        Initialize Firestore connection and manager state.
        
        Args:
            namespace: Namespace prefix for collection names
            credentials_path: Path to Firebase credentials file
            credentials_dict: Dictionary containing Firebase credentials
            project_id: GCP project ID (optional)
            logger_options: Optional logger configuration
        """
        self.namespace = namespace
        self._db = None
        self._app = None
        self._connection_lock = Lock()
        self._model_collection_map = {}  # Maps model classes to collection names
        self._indexed_fields = {}  # Maps collection names to fields that should be indexed
        
        # Store GCP options for later use
        self._gcp_options = {
            'credentials_path': credentials_path,
            'project_id': project_id
        }
        
        # Initialize the logger
        self._setup_logger(logger_options or {})
        
        # Initialize Firebase connection
        self._setup_firebase(credentials_path, credentials_dict)
    
    def _setup_logger(self, logger_options: Dict[str, Any]) -> None:
        """
        Set up the logger for this FirestoreManager instance.
        
        Args:
            logger_options: Logger configuration options
        """
        if 'logger_instance' in logger_options:
            self.logger = logger_options['logger_instance']
            self.logger.info("Using provided logger instance for FirestoreManager")
        else:
            # Create a new logger
            log_level = logger_options.get('log_level', 'info')
            log_namespace = logger_options.get('namespace', f"firestore-{self.namespace}")
            
            self.logger = Logger(
                logger_type=logger_options.get('logger_type', 'local'),
                namespace=log_namespace,
                instance_id=logger_options.get('instance_id', f"firestore-manager-{self.namespace}"),
                log_level=log_level,
                **{k: v for k, v in logger_options.items() if k not in ['logger_type', 'namespace', 'instance_id', 'log_level']}
            )
            self.logger.info(f"Created new logger for FirestoreManager with namespace '{log_namespace}'")
    
    def _setup_firebase(self, credentials_path: Optional[str] = None, credentials_dict: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize Firebase connection with proper error handling.
        Uses GCPManager for authentication when possible.
        
        Args:
            credentials_path: Path to Firebase credentials file
            credentials_dict: Dictionary containing Firebase credentials
        """
        if self._db is not None:
            return
            
        with self._connection_lock:
            if self._db is not None:
                return
                
            try:
                # First, try to use GCPManager for authentication
                try:
                    self.logger.info("Attempting to initialize Firebase connection using GCPManager")
                    
                    # Get the GCP manager instance with our options
                    gcp_options = {}
                    if credentials_path:
                        gcp_options['credentials_path'] = credentials_path
                    if self._gcp_options.get('project_id'):
                        gcp_options['project_id'] = self._gcp_options['project_id']
                    
                    gcp = GCPManager.instance(gcp_options)
                    
                    # Use the firestore client from GCPManager if available
                    self._db = gcp.get_client('firestore')
                    self.logger.info(f"Firebase connection initialized using GCPManager for namespace: {self.namespace}")
                    return
                    
                except (ImportError, Exception) as e:
                    self.logger.warning(f"Could not use GCPManager, falling back to direct initialization: {e}")
                
                # Fall back to direct Firebase initialization if GCPManager failed
                self.logger.info("Initializing Firebase connection directly")
                if credentials_path:
                    self.logger.debug(f"Using credentials from path: {credentials_path}")
                    cred = credentials.Certificate(credentials_path)
                elif credentials_dict:
                    self.logger.debug("Using credentials from dictionary")
                    cred = credentials.Certificate(credentials_dict)
                else:
                    error_msg = "Either credentials_path or credentials_dict must be provided"
                    self.logger.error(error_msg)
                    raise ValueError(error_msg)
                
                # Initialize Firebase app
                self._app = firebase_admin.initialize_app(cred)
                
                # Initialize Firestore client
                self._db = firestore.client()
                
                if not self._db:
                    error_msg = "Failed to initialize Firestore client"
                    self.logger.error(error_msg)
                    raise ConnectionError(error_msg)
                    
                self.logger.info(f"Firebase connection initialized directly for namespace: {self.namespace}")
                
            except Exception as e:
                self._cleanup()
                error_msg = f"Firebase initialization failed: {e}"
                self.logger.error(error_msg)
                raise ConnectionError(error_msg) from e
    
    def _cleanup(self) -> None:
        """Clean up Firebase resources and reset connection state."""
        with self._connection_lock:
            if self._app:
                try:
                    self.logger.debug("Cleaning up Firebase resources")
                    firebase_admin.delete_app(self._app)
                    self.logger.debug("Firebase app deleted successfully")
                except Exception as e:
                    self.logger.error(f"Error during Firebase cleanup: {e}")
                finally:
                    self._app = None
                    self._db = None
                    
    def __del__(self):
        """Ensure proper cleanup on object deletion."""
        self._cleanup()
    
    @contextlib.contextmanager
    def connection(self):
        """Context manager for safe Firestore operations."""
        if not self._db:
            error_msg = "Firebase connection not initialized"
            self.logger.error(error_msg)
            raise ConnectionError(error_msg)
            
        try:
            self.logger.debug("Entering Firestore connection context")
            yield self._db
        except Exception as e:
            self.logger.error(f"Error during Firestore operation: {e}")
            raise
        finally:
            self.logger.debug("Exiting Firestore connection context")
    
    def _get_collection_name(self, model_class: Type[BaseModel]) -> str:
        """
        Get the collection name for a model class.
        
        Args:
            model_class: Pydantic model class
            
        Returns:
            Collection name in Firestore
        """
        # Check if we have a mapping already
        if model_class in self._model_collection_map:
            return self._model_collection_map[model_class]
        
        # Default to lowercase model name
        collection_name = f"{self.namespace}_{model_class.__name__.lower()}"
        return collection_name
    
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
            
        # Store indexed fields
        if indexed_fields:
            self._indexed_fields[full_collection_name] = indexed_fields
            
        self.logger.info(f"Registered model {model_class.__name__} with collection {full_collection_name}")
        if indexed_fields:
            self.logger.debug(f"Indexed fields for {full_collection_name}: {indexed_fields}")
    
    def ensure_collection_exists(self, model_class: Type[BaseModel], indexed_fields: Optional[List[str]] = None) -> None:
        """
        Ensure a collection exists for the given Pydantic model.
        
        Args:
            model_class: Pydantic model class
            indexed_fields: Optional list of fields to create indexes for
        """
        # Firestore collections are created implicitly, but we can register the model
        collection_name = self._get_collection_name(model_class)
        
        # Store indexed fields if provided
        if indexed_fields:
            self._indexed_fields[collection_name] = indexed_fields
            
        self.logger.info(f"Collection {collection_name} registered for model {model_class.__name__}")
        
        # Register the model if not already registered
        if model_class not in self._model_collection_map:
            self._model_collection_map[model_class] = collection_name
    
    def put_item(self, item: BaseModel) -> str:
        """
        Store a Pydantic model instance in Firestore.
        
        Args:
            item: Pydantic model instance to store
            
        Returns:
            Document ID of the created document
        """
        if not self._db:
            error_msg = "Firestore connection not initialized"
            self.logger.error(error_msg)
            raise ConnectionError(error_msg)
        
        # Get collection name
        collection_name = self._get_collection_name(item.__class__)
        
        self.logger.info(f"Adding document to collection {collection_name}")
        self.logger.debug(f"Model type: {item.__class__.__name__}")
        
        # Convert model to dict
        item_dict = item.model_dump()
        
        # Generate document ID if not present
        doc_id = item_dict.get('id')
        if not doc_id:
            # Create a new document reference with auto-generated ID
            doc_ref = self._db.collection(collection_name).document()
            doc_id = doc_ref.id
            
            # Add ID to item dict
            item_dict['id'] = doc_id
            self.logger.debug(f"Generated new document ID: {doc_id}")
        else:
            # Use existing ID
            doc_ref = self._db.collection(collection_name).document(doc_id)
            self.logger.debug(f"Using existing document ID: {doc_id}")
        
        # Add timestamps if not present
        if 'created_at' not in item_dict:
            item_dict['created_at'] = fs.SERVER_TIMESTAMP
        if 'updated_at' not in item_dict:
            item_dict['updated_at'] = fs.SERVER_TIMESTAMP
        
        # Handle special field types
        for key, value in item_dict.items():
            if isinstance(value, dict):
                # Ensure nested dicts are properly handled
                item_dict[key] = value
            elif isinstance(value, BaseModel):
                # Convert nested models to dicts
                item_dict[key] = value.model_dump()
        
        try:
            # Store the document
            doc_ref.set(item_dict)
            self.logger.info(f"Successfully added document with ID {doc_id} to collection {collection_name}")
        except Exception as e:
            self.logger.error(f"Error adding document to {collection_name}: {e}")
            raise
        
        return doc_id
    
    def get_item(self, model_class: Type[T], doc_id: str) -> Optional[FirestoreItem]:
        """
        Get a document from Firestore by ID and return as a FirestoreItem.
        
        Args:
            model_class: Pydantic model class
            doc_id: Document ID
            
        Returns:
            FirestoreItem instance or None if not found
        """
        if not self._db:
            error_msg = "Firestore connection not initialized"
            self.logger.error(error_msg)
            raise ConnectionError(error_msg)
        
        collection_name = self._get_collection_name(model_class)
        
        self.logger.debug(f"Getting document with ID {doc_id} from collection {collection_name}")
        
        try:
            # Get the document
            doc = self._db.collection(collection_name).document(doc_id).get()
            
            if doc.exists:
                self.logger.debug(f"Document found: {doc_id}")
                # Return as FirestoreItem for dictionary-like access
                return FirestoreItem(self, model_class, doc_id, doc.to_dict())
                
            self.logger.debug(f"Document not found: {doc_id}")
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting document {doc_id}: {e}")
            return None
    
    def get_document(self, doc_id: str, collection_name: str) -> Optional[Dict[str, Any]]:
        """
        Get a document from Firestore by ID.
        
        Args:
            doc_id: Document ID
            collection_name: Collection name
            
        Returns:
            Document data as dictionary or None if not found
        """
        if not self._db:
            error_msg = "Firestore connection not initialized"
            self.logger.error(error_msg)
            raise ConnectionError(error_msg)
        
        # Prepend namespace if not already present
        if not collection_name.startswith(f"{self.namespace}_"):
            full_collection_name = f"{self.namespace}_{collection_name}"
        else:
            full_collection_name = collection_name
        
        self.logger.debug(f"Getting document with ID {doc_id} from collection {full_collection_name}")
        
        try:
            # Get the document
            doc = self._db.collection(full_collection_name).document(doc_id).get()
            
            if doc.exists:
                self.logger.debug(f"Document found: {doc_id}")
                return doc.to_dict()
                
            self.logger.debug(f"Document not found: {doc_id}")
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting document {doc_id}: {e}")
            return None
    
    def update_document(self, doc_id: str, collection_name: str, updates: Dict[str, Any]) -> None:
        """
        Update a document in Firestore.
        
        Args:
            doc_id: Document ID
            collection_name: Collection name
            updates: Dictionary of fields to update
        """
        if not self._db:
            error_msg = "Firestore connection not initialized"
            self.logger.error(error_msg)
            raise ConnectionError(error_msg)
        
        # Prepend namespace if not already present
        if not collection_name.startswith(f"{self.namespace}_"):
            full_collection_name = f"{self.namespace}_{collection_name}"
        else:
            full_collection_name = collection_name
        
        self.logger.info(f"Updating document with ID {doc_id} in collection {full_collection_name}")
        self.logger.debug(f"Update fields: {list(updates.keys())}")
        
        # Add updated_at timestamp if not already in updates
        if 'updated_at' not in updates:
            updates['updated_at'] = fs.SERVER_TIMESTAMP
        
        # Handle special field types
        for key, value in list(updates.items()):
            if isinstance(value, dict):
                # Ensure nested dicts are properly handled
                pass
            elif isinstance(value, BaseModel):
                # Convert nested models to dicts
                updates[key] = value.model_dump()
                self.logger.debug(f"Converted nested model for field {key}")
        
        try:
            # Update the document
            self._db.collection(full_collection_name).document(doc_id).update(updates)
            self.logger.info(f"Successfully updated document with ID {doc_id} in collection {full_collection_name}")
        except Exception as e:
            self.logger.error(f"Error updating document {doc_id}: {e}")
            raise
    
    def delete_document(self, doc_id: str, collection_name: str) -> None:
        """
        Delete a document from Firestore.
        
        Args:
            doc_id: Document ID
            collection_name: Collection name
        """
        if not self._db:
            error_msg = "Firestore connection not initialized"
            self.logger.error(error_msg)
            raise ConnectionError(error_msg)
        
        # Prepend namespace if not already present
        if not collection_name.startswith(f"{self.namespace}_"):
            full_collection_name = f"{self.namespace}_{collection_name}"
        else:
            full_collection_name = collection_name
        
        self.logger.info(f"Deleting document with ID {doc_id} from collection {full_collection_name}")
        
        try:
            # Delete the document
            self._db.collection(full_collection_name).document(doc_id).delete()
            self.logger.info(f"Successfully deleted document with ID {doc_id} from collection {full_collection_name}")
        except Exception as e:
            self.logger.error(f"Error deleting document {doc_id}: {e}")
            raise
    
    def query(self, model_class: Type[BaseModel], filters: Dict[str, Any] = None) -> List[FirestoreItem]:
        """
        Query documents based on filter conditions.
        
        Args:
            model_class: Pydantic model class
            filters: Dictionary of field-value pairs to filter by
            
        Returns:
            List of FirestoreItem instances matching the query
        """
        if not self._db:
            error_msg = "Firestore connection not initialized"
            self.logger.error(error_msg)
            raise ConnectionError(error_msg)
        
        collection_name = self._get_collection_name(model_class)
        
        self.logger.info(f"Querying documents from collection {collection_name}")
        if filters:
            self.logger.debug(f"Filters: {filters}")
        
        # Start with the collection reference
        query_ref = self._db.collection(collection_name)
        
        # Add filters if provided
        if filters:
            for field, value in filters.items():
                query_ref = query_ref.where(filter=FieldFilter(field_path=field, op_string="==", value=value))
        
        try:
            # Execute the query
            docs = query_ref.stream()
            
            # Convert to FirestoreItem instances
            results = []
            for doc in docs:
                results.append(FirestoreItem(self, model_class, doc.id, doc.to_dict()))
            
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
            error_msg = "Firestore connection not initialized"
            self.logger.error(error_msg)
            raise ConnectionError(error_msg)
        
        # Prepend namespace if not already present
        if not collection_name.startswith(f"{self.namespace}_"):
            full_collection_name = f"{self.namespace}_{collection_name}"
        else:
            full_collection_name = collection_name
        
        self.logger.info(f"Querying documents from collection {full_collection_name}")
        if filters:
            self.logger.debug(f"Filters: {filters}")
        
        # Start with the collection reference
        query_ref = self._db.collection(full_collection_name)
        
        # Add filters if provided
        if filters:
            for field, value in filters.items():
                query_ref = query_ref.where(filter=FieldFilter(field_path=field, op_string="==", value=value))
        
        try:
            # Execute the query
            docs = query_ref.stream()
            
            # Convert to dictionaries with document ID
            results = []
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id  # Add document ID to the dictionary
                results.append(data)
            
            self.logger.info(f"Query returned {len(results)} documents from {full_collection_name}")
            return results
            
        except Exception as e:
            self.logger.error(f"Error querying documents from {full_collection_name}: {e}")
            raise
    
    def query_with_composite_filter(
        self, 
        model_class: Type[BaseModel], 
        filters: List[Dict[str, Any]], 
        logical_operator: str = "AND"
    ) -> List[FirestoreItem]:
        """
        Query documents using composite filters.
        
        Args:
            model_class: Pydantic model class
            filters: List of dictionaries with 'field', 'op', and 'value' keys
            logical_operator: Logical operator to join filters ('AND' or 'OR')
            
        Returns:
            List of FirestoreItem instances matching the query
        """
        if not self._db:
            error_msg = "Firestore connection not initialized"
            self.logger.error(error_msg)
            raise ConnectionError(error_msg)
        
        collection_name = self._get_collection_name(model_class)
        
        self.logger.info(f"Executing composite query on collection {collection_name}")
        self.logger.debug(f"Logical operator: {logical_operator}")
        self.logger.debug(f"Filters: {filters}")
        
        # Start with the collection reference
        query_ref = self._db.collection(collection_name)
        
        # Add filters
        for filter_dict in filters:
            field = filter_dict['field']
            op = filter_dict.get('op', '==')
            value = filter_dict['value']
            
            self.logger.debug(f"Adding filter: {field} {op} {value}")
            query_ref = query_ref.where(filter=FieldFilter(field_path=field, op_string=op, value=value))
        
        try:
            # Execute the query
            docs = query_ref.stream()
            
            # Convert to FirestoreItem instances
            results = []
            for doc in docs:
                results.append(FirestoreItem(self, model_class, doc.id, doc.to_dict()))
            
            self.logger.info(f"Composite query returned {len(results)} documents from {collection_name}")
            return results
            
        except Exception as e:
            self.logger.error(f"Error executing composite query on {collection_name}: {e}")
            raise
    
    def create_model_from_document(self, doc_id: str, collection_name: str, model_name: str = "DynamicModel") -> Optional[BaseModel]:
        """
        Create a Pydantic model instance from a Firestore document.
        
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
                
        self.logger.debug(f"Created field definitions for model {model_name}: {list(field_definitions.keys())}")
        
        try:
            # Create a dynamic Pydantic model
            DynamicModel = create_model(model_name, **field_definitions)
            
            # Create an instance of the model
            self.logger.info(f"Successfully created dynamic model {model_name} from document {doc_id}")
            return DynamicModel(**doc_data)
            
        except Exception as e:
            self.logger.error(f"Error creating dynamic model: {e}")
            return None
    
    def get_or_create(self, model_class: Type[BaseModel], doc_id: str, default_data: Dict[str, Any] = None) -> FirestoreItem:
        """
        Get a document if it exists or create it with default data.
        
        Args:
            model_class: Pydantic model class
            doc_id: Document ID
            default_data: Default data for new document
            
        Returns:
            FirestoreItem instance
        """
        if not self._db:
            error_msg = "Firestore connection not initialized"
            self.logger.error(error_msg)
            raise ConnectionError(error_msg)
        
        collection_name = self._get_collection_name(model_class)
        
        self.logger.info(f"Getting or creating document with ID {doc_id} in collection {collection_name}")
        
        # Try to get the document
        doc = self._db.collection(collection_name).document(doc_id).get()
        
        if doc.exists:
            # Return existing document
            self.logger.debug(f"Document {doc_id} already exists")
            return FirestoreItem(self, model_class, doc_id, doc.to_dict())
        else:
            # Create new document with default data
            self.logger.debug(f"Document {doc_id} does not exist, creating with default data")
            if default_data is None:
                default_data = {}
            
            # Add ID and timestamps
            default_data['id'] = doc_id
            default_data['created_at'] = fs.SERVER_TIMESTAMP
            default_data['updated_at'] = fs.SERVER_TIMESTAMP
            
            try:
                # Create the document
                self._db.collection(collection_name).document(doc_id).set(default_data)
                self.logger.info(f"Successfully created document with ID {doc_id} in collection {collection_name}")
                
                # Return the new document
                return FirestoreItem(self, model_class, doc_id, default_data)
                
            except Exception as e:
                self.logger.error(f"Error creating document {doc_id}: {e}")
                raise
    
    def batch_operation(self, operations: List[Dict[str, Any]]) -> None:
        """
        Perform batch operations on Firestore.
        
        Args:
            operations: List of operation dictionaries with 'type', 'collection', 'doc_id', and 'data' keys
        """
        if not self._db:
            raise ConnectionError("Firestore connection not initialized")
        
        # Create a batch
        batch = self._db.batch()
        
        # Add operations to the batch
        for op in operations:
            op_type = op['type']  # 'set', 'update', 'delete'
            collection = op['collection']
            doc_id = op['doc_id']
            
            # Prepend namespace if not already present
            if not collection.startswith(f"{self.namespace}_"):
                full_collection = f"{self.namespace}_{collection}"
            else:
                full_collection = collection
            
            # Get document reference
            doc_ref = self._db.collection(full_collection).document(doc_id)
            
            if op_type == 'set':
                # Set operation
                data = op['data']
                if 'updated_at' not in data:
                    data['updated_at'] = fs.SERVER_TIMESTAMP
                batch.set(doc_ref, data, merge=op.get('merge', False))
            elif op_type == 'update':
                # Update operation
                data = op['data']
                if 'updated_at' not in data:
                    data['updated_at'] = fs.SERVER_TIMESTAMP
                batch.update(doc_ref, data)
            elif op_type == 'delete':
                # Delete operation
                batch.delete(doc_ref)
        
        # Commit the batch
        batch.commit()
        self.logger.info(f"Batch operation completed with {len(operations)} operations")
    
    def model_to_firestore_item(self, item: BaseModel) -> FirestoreItem:
        """
        Convert a Pydantic model instance to a FirestoreItem.
        
        Args:
            item: Pydantic model instance
            
        Returns:
            FirestoreItem instance
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
            doc = self._db.collection(collection_name).document(doc_id).get()
            
            if not doc.exists:
                # Store the item
                self.put_item(item)
        
        # Return as FirestoreItem
        return FirestoreItem(self, item.__class__, doc_id, item_dict)


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
    
    # Initialize Firestore manager
    credentials_path = "path/to/credentials.json"
    project_id = "my-gcp-project"
    firestore_manager = FirestoreManager("myapp", credentials_path=credentials_path, project_id=project_id)


    # Register the model with indexed fields
    firestore_manager.register_model(User, "users", indexed_fields=["email", "is_active"])
    
    # Create a user
    user = User(name="Test User", email="test@example.com")
    user_id = firestore_manager.put_item(user)
    
    # Get the user as a FirestoreItem
    user_item = firestore_manager.get_item(User, user_id)
    
    # Access and update attributes
    print(user_item["name"])  # Output: Test User
    user_item["age"] = 30
    
    # Update multiple attributes
    user_item.update({
        "name": "Updated Name",
        "metadata": {"last_login": "2023-03-15"}
    })
    
    # Query users
    active_users = firestore_manager.query(User, {"is_active": True})
    
    # Delete the user
    user_item.delete()