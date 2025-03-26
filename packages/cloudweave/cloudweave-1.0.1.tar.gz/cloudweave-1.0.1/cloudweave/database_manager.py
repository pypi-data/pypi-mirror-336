import abc
import enum
import uuid
from typing import Dict, Any, Optional, List, Union, Type, TypeVar
from threading import Lock

from pydantic import BaseModel

# Import the database managers
from cloudweave.database_utils import DynamoManager, DynamoItem
from cloudweave.database_utils import FirestoreManager, FirestoreItem
from cloudweave.database_utils import MongoDBManager, MongoDBDoc

# Import Logger for proper logging
from cloudweave.logging_manager import Logger, LoggerType

T = TypeVar('T', bound=BaseModel)

class DatabaseType(enum.Enum):
    """Enum for supported database types."""
    DYNAMODB = "dynamodb"
    FIRESTORE = "firestore"
    MONGODB = "mongodb"
    
    @classmethod
    def from_string(cls, value: str) -> 'DatabaseType':
        """Convert string to enum value."""
        try:
            return cls(value.lower())
        except ValueError:
            valid_values = ', '.join([e.value for e in cls])
            raise ValueError(f"Invalid database type: {value}. Valid values are: {valid_values}")


class DatabaseItem:
    """
    Unified wrapper for database items that provides dictionary-like access.
    """
    
    def __init__(self, db_item):
        """
        Initialize with a specific database item.
        
        Args:
            db_item: A database item (DynamoItem, FirestoreItem, or MongoDBDoc)
        """
        self._db_item = db_item
        
    def __getitem__(self, key: str) -> Any:
        """Get an attribute value."""
        return self._db_item[key]
        
    def __setitem__(self, key: str, value: Any) -> None:
        """Set an attribute value and update in the database."""
        # Update the dictionary first
        self._db_item[key] = value
        
        # Explicitly update the database as well
        if hasattr(self._db_item, 'update'):
            self._db_item.update({key: value})
        
    def get(self, key: str, default: Any = None) -> Any:
        """Get an attribute value with a default."""
        return self._db_item.get(key, default)
    
    def save(self) -> None:
        """Save any local changes back to the database."""
        self._db_item.update(self._db_item.to_dict())
            
    def update(self, updates: Dict[str, Any]) -> None:
        """Update multiple attributes at once."""
        self._db_item.update(updates)
        
    def refresh(self) -> None:
        """Refresh data from the database."""
        self._db_item.refresh()
        
    def delete(self) -> None:
        """Delete this item from the database."""
        self._db_item.delete()
        
    def to_dict(self) -> Dict[str, Any]:
        """Get a dictionary representation of the item."""
        return self._db_item.to_dict()


class Database:
    """
    Unified database interface that can connect to multiple database backends.
    Supports maintaining multiple connections to different database types simultaneously.
    """
    
    # Registry of database instances
    _registry = {}
    _lock = Lock()
    
    def __init__(self, 
               db_type: Union[str, DatabaseType],
               namespace: str,
               instance_id: Optional[str] = None,
               logger_options: Dict[str, Any] = None,
               **kwargs):
        """
        Initialize a database connection.
        
        Args:
            db_type: Type of database to connect to
            namespace: Namespace prefix for tables/collections
            instance_id: Optional unique identifier for this connection
            logger_options: Optional logger configuration
            **kwargs: Database-specific connection parameters
        """
        # Convert string to enum if necessary
        if isinstance(db_type, str):
            self.db_type = DatabaseType.from_string(db_type)
        else:
            self.db_type = db_type
            
        self.namespace = namespace
        
        # Generate unique instance ID if not provided
        self.instance_id = instance_id or f"{self.db_type.value}-{namespace}-{uuid.uuid4()}"
        
        # Initialize the logger
        self._setup_logger(logger_options or {})
        
        self._db_manager = None
        self._model_mappings = {}  # Maps model classes to collection/table names
        self._indexed_fields = {}  # Maps collection/table names to fields that should be indexed
        
        # Set up database connection
        self._setup_database(**kwargs)
        
        # Register this instance
        with Database._lock:
            Database._registry[self.instance_id] = self
    
    def _setup_logger(self, logger_options: Dict[str, Any]) -> None:
        """
        Set up the logger for this Database instance.
        
        Args:
            logger_options: Logger configuration options
        """
        if 'logger_instance' in logger_options:
            self.logger = logger_options['logger_instance']
            self.logger.info("Using provided logger instance for Database")
        else:
            # Create a new logger
            log_level = logger_options.get('log_level', 'info')
            log_namespace = logger_options.get('namespace', f"database-{self.namespace}")
            
            self.logger = Logger(
                logger_type=logger_options.get('logger_type', 'local'),
                namespace=log_namespace,
                instance_id=logger_options.get('instance_id', f"database-{self.db_type.value}-{self.instance_id}"),
                log_level=log_level,
                **{k: v for k, v in logger_options.items() if k not in ['logger_type', 'namespace', 'instance_id', 'log_level']}
            )
            self.logger.info(f"Created new logger for Database with namespace '{log_namespace}'")
    
    @classmethod
    def get_instance(cls, instance_id: str) -> Optional['Database']:
        """
        Get a database instance by ID.
        
        Args:
            instance_id: Database instance ID
            
        Returns:
            Database instance or None if not found
        """
        return cls._registry.get(instance_id)
        
    @classmethod
    def list_instances(cls) -> List[str]:
        """
        List all registered database instance IDs.
        
        Returns:
            List of instance IDs
        """
        return list(cls._registry.keys())
    
    def _setup_database(self, **kwargs):
        """
        Initialize the database connection based on the database type.
        
        Args:
            **kwargs: Database-specific connection parameters
        """
        self.logger.info(f"Setting up {self.db_type.value} database connection")
        
        if self.db_type == DatabaseType.DYNAMODB:
            self._setup_dynamodb(**kwargs)
        elif self.db_type == DatabaseType.FIRESTORE:
            self._setup_firestore(**kwargs)
        elif self.db_type == DatabaseType.MONGODB:
            self._setup_mongodb(**kwargs)
        else:
            error_msg = f"Unsupported database type: {self.db_type}"
            self.logger.error(error_msg)
            raise ValueError(error_msg)
    
    def _setup_dynamodb(self, **kwargs):
        """
        Initialize DynamoDB connection.
        
        Args:
            session: boto3 session
            **kwargs: Additional DynamoDB-specific parameters
        """
        try:
            # Set up logger options to pass to the DynamoDB manager
            session_params = kwargs.get("opt")
            logger_options = {
                'logger_instance': self.logger
            }
                
            self._db_manager = DynamoManager(
                self.namespace,
                session_params.get("region", "us-east-2"),
                logger_options=logger_options
            )
            self.logger.info(f"DynamoDB connection initialized for namespace: {self.namespace} with ID: {self.instance_id}")
        except Exception as e:
            self.logger.error(f"Failed to initialize DynamoDB connection: {e}")
            raise
    
    def _setup_firestore(self, credentials_path=None, credentials_dict=None, **kwargs):
        """
        Initialize Firestore connection.
        
        Args:
            credentials_path: Path to Firebase credentials file
            credentials_dict: Dictionary containing Firebase credentials
            **kwargs: Additional Firestore-specific parameters
        """
        try:
            # Set up logger options to pass to the Firestore manager
            logger_options = {
                'logger_instance': self.logger
            }
            
            self._db_manager = FirestoreManager(
                namespace=self.namespace,
                credentials_path=credentials_path,
                credentials_dict=credentials_dict,
                logger_options=logger_options,
                **kwargs
            )
            self.logger.info(f"Firestore connection initialized for namespace: {self.namespace} with ID: {self.instance_id}")
        except Exception as e:
            self.logger.error(f"Failed to initialize Firestore connection: {e}")
            raise
    
    def _setup_mongodb(self, connection_string=None, database_name=None, **kwargs):
        """
        Initialize MongoDB connection.
        
        Args:
            connection_string: MongoDB connection string
            database_name: Database name
            **kwargs: Additional MongoDB-specific parameters
        """
        try:
            # Set up logger options to pass to the MongoDB manager
            logger_options = {
                'logger_instance': self.logger
            }
            
            if not connection_string:
                connection_string = kwargs.get('connection_string', 'mongodb://localhost:27017/')
                self.logger.debug(f"Using connection string: {connection_string}")
                
            if not database_name:
                database_name = kwargs.get('database_name', self.namespace)
                self.logger.debug(f"Using database name: {database_name}")
                
            self._db_manager = MongoDBManager(
                connection_string=connection_string,
                database_name=database_name,
                namespace=self.namespace,
                logger_options=logger_options
            )
            self.logger.info(f"MongoDB connection initialized for namespace: {self.namespace} with ID: {self.instance_id}")
        except Exception as e:
            self.logger.error(f"Failed to initialize MongoDB connection: {e}")
            raise
    
    def register_model(self, model_class: Type[BaseModel], 
                    collection_name: Optional[str] = None, 
                    indexed_fields: Optional[List[str]] = None) -> None:
        """
        Register a model class with a specific collection/table name.
        
        Args:
            model_class: Pydantic model class to register
            collection_name: Optional custom collection/table name
            indexed_fields: Optional list of fields to be indexed
        """
        self.logger.info(f"Registering model {model_class.__name__} with database")
        
        if self.db_type == DatabaseType.DYNAMODB:
            # For DynamoDB, we need to create indexes differently
            self.logger.debug(f"Creating DynamoDB indexes for {model_class.__name__}")
            indexes = {}
            if indexed_fields:
                # Get field types to ensure consistent type conversion
                model_fields = getattr(model_class, 'model_fields', None)
                
                for field in indexed_fields:
                    indexes[f"{field}-index"] = {
                        'hash_key': field
                    }
                    self.logger.debug(f"Added index for field: {field}")
                    
            self._db_manager.ensure_table_exists(model_class, indexes)
            
        elif self.db_type == DatabaseType.FIRESTORE:
            # For Firestore, use the register_model method
            self.logger.debug(f"Registering Firestore model: {model_class.__name__}")
            self._db_manager.register_model(model_class, collection_name, indexed_fields)
            
        elif self.db_type == DatabaseType.MONGODB:
            # For MongoDB, use the register_model method
            self.logger.debug(f"Registering MongoDB model: {model_class.__name__}")
            self._db_manager.register_model(model_class, collection_name, indexed_fields)
        
        # Store model mapping
        if collection_name:
            self._model_mappings[model_class] = collection_name
            self.logger.debug(f"Mapped {model_class.__name__} to collection/table: {collection_name}")
        else:
            # Use default naming convention
            self._model_mappings[model_class] = model_class.__name__.lower()
            self.logger.debug(f"Using default collection/table name: {model_class.__name__.lower()}")
        
        # Store indexed fields
        if indexed_fields:
            self._indexed_fields[self._model_mappings[model_class]] = indexed_fields
            self.logger.debug(f"Indexed fields for {model_class.__name__}: {indexed_fields}")
    
    def get_collection_name(self, model_class: Type[BaseModel]) -> str:
        """
        Get the collection/table name for a model class.
        
        Args:
            model_class: Pydantic model class
            
        Returns:
            Collection/table name
        """
        collection_name = self._model_mappings.get(model_class, model_class.__name__.lower())
        self.logger.debug(f"Retrieved collection name for {model_class.__name__}: {collection_name}")
        return collection_name
    
    def ensure_collection_exists(self, model_class: Type[BaseModel], indexed_fields: Optional[List[str]] = None) -> None:
        """
        Ensure a collection/table exists for the given Pydantic model.
        
        Args:
            model_class: Pydantic model class
            indexed_fields: Optional list of fields to create indexes for
        """
        self.logger.info(f"Ensuring collection/table exists for {model_class.__name__}")
        
        if self.db_type == DatabaseType.DYNAMODB:
            # For DynamoDB, convert indexed_fields to GSIs
            self.logger.debug(f"Creating DynamoDB table for {model_class.__name__}")
            indexes = {}
            if indexed_fields:
                for field in indexed_fields:
                    indexes[f"{field}-index"] = {
                        'hash_key': field
                    }
                    self.logger.debug(f"Added index for field: {field}")
                    
            self._db_manager.ensure_table_exists(model_class, indexes)
            
        elif self.db_type == DatabaseType.FIRESTORE:
            # For Firestore, use the ensure_collection_exists method
            self.logger.debug(f"Ensuring Firestore collection exists for {model_class.__name__}")
            self._db_manager.ensure_collection_exists(model_class, indexed_fields)
            
        elif self.db_type == DatabaseType.MONGODB:
            # For MongoDB, use the ensure_collection_exists method
            self.logger.debug(f"Ensuring MongoDB collection exists for {model_class.__name__}")
            self._db_manager.ensure_collection_exists(model_class, indexed_fields)
        
        # Store indexed fields
        collection_name = self.get_collection_name(model_class)
        if indexed_fields:
            self._indexed_fields[collection_name] = indexed_fields
            self.logger.debug(f"Stored indexed fields for {collection_name}: {indexed_fields}")
    
    def put_item(self, item: BaseModel) -> str:
        """
        Store a Pydantic model instance in the database.
        
        Args:
            item: Pydantic model instance to store
            
        Returns:
            Document/item ID
        """
        self.logger.info(f"Storing {item.__class__.__name__} in database")
        
        try:
            # Generate UUID if not present
            item_dict = item.model_dump()
            if 'id' not in item_dict or item_dict['id'] is None:
                # Add UUID to the model
                item_id = str(uuid.uuid4())
                setattr(item, 'id', item_id)
            
            # Store the item
            result_id = self._db_manager.put_item(item)
            
            # Log and return
            self.logger.info(f"Successfully stored item with ID: {result_id}")
            return result_id
        except Exception as e:
            self.logger.error(f"Failed to store item: {e}")
            raise
    
    def get_item(self, model_class: Type[T], item_id: str) -> Optional[DatabaseItem]:
        """
        Get an item from the database by ID.
        
        Args:
            model_class: Pydantic model class
            item_id: Item ID
            
        Returns:
            DatabaseItem instance or None if not found
        """
        self.logger.debug(f"Getting {model_class.__name__} with ID: {item_id}")
        
        try:
            if self.db_type == DatabaseType.DYNAMODB:
                # For DynamoDB, we need to pass the ID as a key dictionary
                db_item = self._db_manager.get_item(model_class, {'id': item_id})
                
                # If the item exists and we have indexed fields, convert string booleans back to proper booleans
                if db_item and hasattr(self, '_indexed_fields'):
                    collection_name = self.get_collection_name(model_class)
                    indexed_fields = self._indexed_fields.get(collection_name, [])
                    
                    # Convert string booleans back to proper booleans
                    for field in indexed_fields:
                        if field in db_item and isinstance(db_item[field], str):
                            if db_item[field].lower() == 'true':
                                db_item[field] = True
                            elif db_item[field].lower() == 'false':
                                db_item[field] = False
            else:
                # For Firestore and MongoDB
                db_item = self._db_manager.get_item(model_class, item_id)
                    
            if db_item:
                self.logger.debug(f"Found item with ID: {item_id}")
                return DatabaseItem(db_item)
                    
            self.logger.debug(f"Item not found with ID: {item_id}")
            return None
        except Exception as e:
            self.logger.error(f"Error getting item {item_id}: {e}")
            return None
    
    def get_document(self, doc_id: str, collection_name: str) -> Optional[Dict[str, Any]]:
        """
        Get a document from the database by ID.
        
        Args:
            doc_id: Document ID
            collection_name: Collection/table name
            
        Returns:
            Document data as dictionary or None if not found
        """
        self.logger.debug(f"Getting document with ID: {doc_id} from collection: {collection_name}")
        
        try:
            # Handle DynamoDB differently
            if self.db_type == DatabaseType.DYNAMODB:
                # Find the model class associated with this collection name
                model_class = None
                for model, coll_name in self._model_mappings.items():
                    if coll_name == collection_name:
                        model_class = model
                        break
                
                if model_class is None:
                    raise ValueError(f"No model class found for collection {collection_name}")
                
                # Use get_item with key as a dictionary
                result = self._db_manager.get_item(model_class, {'id': doc_id})
                
                # Convert string booleans back to proper booleans
                if result and hasattr(self, '_indexed_fields'):
                    indexed_fields = self._indexed_fields.get(collection_name, [])
                    
                    for field in indexed_fields:
                        if field in result and isinstance(result[field], str):
                            if result[field].lower() == 'true':
                                result[field] = True
                            elif result[field].lower() == 'false':
                                result[field] = False
            else:
                # For Firestore and MongoDB
                result = self._db_manager.get_document(doc_id, collection_name)
                
            if result:
                self.logger.debug(f"Found document with ID: {doc_id}")
            else:
                self.logger.debug(f"Document not found with ID: {doc_id}")
                
            return result
        except Exception as e:
            self.logger.error(f"Error getting document {doc_id}: {e}")
            return None
    
    def update_document(self, doc_id: str, collection_name: str, updates: Dict[str, Any]) -> None:
        """
        Update a document in the database.
        
        Args:
            doc_id: Document ID
            collection_name: Collection/table name
            updates: Dictionary of fields to update
        """
        self.logger.info(f"Updating document with ID: {doc_id} in collection: {collection_name}")
        
        try:
            # For DynamoDB, handle differently
            if self.db_type == DatabaseType.DYNAMODB:
                # Find the model class
                model_class = None
                for model, coll in self._model_mappings.items():
                    if coll == collection_name:
                        model_class = model
                        break
                        
                if model_class is None:
                    raise ValueError(f"No model found for collection {collection_name}")
                    
                # Check if we have indexed fields for this collection
                indexed_fields = self._indexed_fields.get(collection_name, [])
                
                # Create a deep copy of updates to avoid modifying the original
                modified_updates = {}
                for k, v in updates.items():
                    if k in indexed_fields and isinstance(v, bool):
                        # Convert boolean to string for indexed fields
                        modified_updates[k] = str(v).lower()
                    else:
                        modified_updates[k] = v
                        
                # Now use the DynamoDB manager's method
                self._db_manager.update_item(model_class, {'id': doc_id}, modified_updates)
            else:
                # For non-DynamoDB databases
                self._db_manager.update_document(doc_id, collection_name, updates)
                
            self.logger.info(f"Successfully updated document with ID: {doc_id}")
        except Exception as e:
            self.logger.error(f"Error updating document {doc_id}: {e}")
            raise
    
    def delete_document(self, doc_id: str, collection_name: str) -> None:
        """
        Delete a document from the database.
        
        Args:
            doc_id: Document ID
            collection_name: Collection/table name
        """
        self.logger.info(f"Deleting document with ID: {doc_id} from collection: {collection_name}")
        
        try:
            # Handle DynamoDB differently
            if self.db_type == DatabaseType.DYNAMODB:
                # Find the model class associated with this collection name
                model_class = None
                for model, coll_name in self._model_mappings.items():
                    if coll_name == collection_name:
                        model_class = model
                        break
                
                if model_class is None:
                    raise ValueError(f"No model class found for collection {collection_name}")
                
                # Use delete_item with key as a dictionary
                self._db_manager.delete_item(model_class, {'id': doc_id})
            else:
                # For Firestore and MongoDB
                self._db_manager.delete_document(doc_id, collection_name)
                
            self.logger.info(f"Successfully deleted document with ID: {doc_id}")
        except Exception as e:
            self.logger.error(f"Error deleting document {doc_id}: {e}")
            raise
    
    def query(self, model_class: Type[BaseModel], filters: Dict[str, Any] = None) -> List[DatabaseItem]:
        """
        Query items based on filter conditions.
        
        Args:
            model_class: Pydantic model class
            filters: Dictionary of field-value pairs to filter by
            
        Returns:
            List of DatabaseItem instances matching the query
        """
        self.logger.info(f"Querying {model_class.__name__} with filters")
        if filters:
            self.logger.debug(f"Filters: {filters}")
        
        try:
            # Handle different query interfaces for each database type
            if self.db_type == DatabaseType.DYNAMODB:
                self.logger.debug("Adapting query for DynamoDB")
                results = []
                if not filters:
                    self.logger.warning("Empty filters for DynamoDB query, returning empty result")
                    return []
                    
                # Get collection name to look up indexed fields
                collection_name = self.get_collection_name(model_class)
                indexed_fields = self._indexed_fields.get(collection_name, [])
                
                # Find a field to use as the partition key from the filters
                # Prioritize fields that are indexed
                partition_key = None
                for field in filters:
                    if field in indexed_fields:
                        partition_key = field
                        break
                        
                if not partition_key:
                    self.logger.warning(f"No suitable indexed field found in filters: {list(filters.keys())}")
                    return []
                    
                # Get the partition value and handle type conversion if needed
                partition_value = filters[partition_key]
                
                # Convert boolean values to strings for indexed fields
                if isinstance(partition_value, bool):
                    partition_value = str(partition_value).lower()
                    
                self.logger.debug(f"Using partition key: {partition_key}={partition_value}")
                
                # Remove the partition key from filters
                remaining_filters = {k: v for k, v in filters.items() if k != partition_key}
                
                # Convert any boolean values in remaining filters
                for k, v in remaining_filters.items():
                    if isinstance(v, bool) and k in indexed_fields:
                        remaining_filters[k] = str(v).lower()
                        
                # Execute the query
                index_name = f"{partition_key}-index"
                self.logger.debug(f"Using GSI: {index_name}")
                
                filter_expression = None
                if remaining_filters:
                    filter_expression = " AND ".join([f"#{k} = :{k}" for k in remaining_filters])
                    self.logger.debug(f"Filter expression: {filter_expression}")
                
                items = self._db_manager.query(
                    model_class=model_class,
                    partition_key=partition_key,
                    partition_value=partition_value,
                    filter_expression=filter_expression,
                    expression_values=remaining_filters,
                    index_name=index_name
                )
                
                # Convert to DatabaseItem instances and handle type conversions
                for item in items:
                    # Convert string booleans back to actual booleans
                    for field in indexed_fields:
                        if field in item and isinstance(item[field], str):
                            if item[field].lower() == 'true':
                                item[field] = True
                            elif item[field].lower() == 'false':
                                item[field] = False
                                
                    results.append(DatabaseItem(item))
                    
                self.logger.info(f"Query returned {len(results)} items")
                return results
                    
            else:
                # For Firestore and MongoDB, the query interface is similar
                self.logger.debug(f"Executing standard query for {self.db_type.value}")
                items = self._db_manager.query(model_class, filters)
                
                # Convert to DatabaseItem instances
                results = [DatabaseItem(item) for item in items]
                self.logger.info(f"Query returned {len(results)} items")
                return results
                    
        except Exception as e:
            self.logger.error(f"Error executing query: {e}")
            return []
    
    def query_documents(self, collection_name: str, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Query documents based on filter conditions and return raw dictionaries.
        
        Args:
            collection_name: Collection/table name
            filters: Dictionary of field-value pairs to filter by
            
        Returns:
            List of document dictionaries matching the query
        """
        self.logger.info(f"Querying documents from collection: {collection_name}")
        if filters:
            self.logger.debug(f"Filters: {filters}")
        
        try:
            # DynamoDB doesn't have a direct equivalent to this method
            if self.db_type == DatabaseType.DYNAMODB:
                # For DynamoDB, we need to adapt the query
                self.logger.warning("query_documents not fully supported for DynamoDB")
                if not filters:
                    # For empty filters, we need a scan operation
                    self.logger.warning("Empty filters for DynamoDB query, returning empty result")
                    return []
                
                # This is a simplification - in a real implementation, you'd need proper scan/query
                self.logger.debug("Returning empty result for DynamoDB query_documents")
                return []
                
            else:
                # For Firestore and MongoDB, the query_documents interface is similar
                self.logger.debug(f"Executing standard query_documents for {self.db_type.value}")
                results = self._db_manager.query_documents(collection_name, filters)
                self.logger.info(f"Query returned {len(results)} documents")
                return results
                
        except Exception as e:
            self.logger.error(f"Error executing query_documents: {e}")
            return []
    
    def batch_operation(self, operations: List[Dict[str, Any]]) -> None:
        """
        Perform batch operations on the database.
        
        Args:
            operations: List of operation dictionaries with 'type', 'collection', 'doc_id', and 'data' keys
        """
        self.logger.info(f"Performing batch operation with {len(operations)} operations")
        
        try:
            # Each database has a different batch operation interface
            if self.db_type == DatabaseType.DYNAMODB:
                # Not directly supported in our simplified DynamoManager
                self.logger.debug("Using individual operations for DynamoDB batch operation")
                for i, op in enumerate(operations):
                    op_type = op['type']
                    collection = op['collection']
                    doc_id = op['doc_id']
                    data = op.get('data', {})
                    
                    self.logger.debug(f"Operation {i+1}: {op_type} on {collection}/{doc_id}")
                    
                    # Find the model class for this collection
                    model_class = None
                    for model, coll_name in self._model_mappings.items():
                        if coll_name == collection:
                            model_class = model
                            break
                    
                    if model_class is None:
                        raise ValueError(f"No model class found for collection {collection}")
                    
                    if op_type == 'set' or op_type == 'update':
                        # Handle boolean fields in indexed fields
                        if hasattr(self, '_indexed_fields'):
                            indexed_fields = self._indexed_fields.get(collection, [])
                            for field in indexed_fields:
                                if field in data and isinstance(data[field], bool):
                                    data[field] = str(data[field]).lower()
                        
                        self._db_manager.update_item(model_class, {'id': doc_id}, data)
                    elif op_type == 'delete':
                        self._db_manager.delete_item(model_class, {'id': doc_id})
                    else:
                        self.logger.warning(f"Unsupported operation type: {op_type}")
                        
            elif self.db_type == DatabaseType.FIRESTORE:
                # Use the batch_operation method
                self.logger.debug("Using native batch_operation for Firestore")
                self._db_manager.batch_operation(operations)
                    
            elif self.db_type == DatabaseType.MONGODB:
                # Use the batch_write method
                self.logger.debug("Using native batch_write for MongoDB")
                self._db_manager.batch_write(operations)
                    
            self.logger.info(f"Successfully completed batch operation")
                    
        except Exception as e:
            self.logger.error(f"Error performing batch operation: {e}")
            raise
    
    def get_or_create(self, model_class: Type[BaseModel], doc_id: str, default_data: Dict[str, Any] = None) -> DatabaseItem:
        """
        Get an item if it exists or create it with default data.
        
        Args:
            model_class: Pydantic model class
            doc_id: Document ID
            default_data: Default data for new document
            
        Returns:
            DatabaseItem instance
        """
        self.logger.info(f"Getting or creating {model_class.__name__} with ID: {doc_id}")
        
        try:
            # Each database has a different get_or_create interface
            if self.db_type == DatabaseType.DYNAMODB:
                # Not directly supported in our simplified DynamoManager
                self.logger.debug("Implementing get_or_create for DynamoDB")
                try:
                    item = self._db_manager.get_item(model_class, {'id': doc_id})
                    if item:
                        self.logger.debug(f"Found existing item with ID: {doc_id}")
                        return DatabaseItem(item)
                except KeyError:
                    self.logger.debug(f"Item not found, creating new item with ID: {doc_id}")
                    pass
                    
                # Create new item with default data
                if default_data is None:
                    default_data = {}
                    
                # Add ID
                default_data['id'] = doc_id
                
                # Create model instance
                model_instance = model_class(**default_data)
                
                # Store in DynamoDB
                self._db_manager.put_item(model_instance)
                self.logger.info(f"Created new item with ID: {doc_id}")
                
                # Return as DatabaseItem
                return DatabaseItem(self._db_manager.get_item(model_class, {'id': doc_id}))
                
            elif self.db_type == DatabaseType.FIRESTORE:
                # Use the get_or_create method
                self.logger.debug("Using native get_or_create for Firestore")
                item = self._db_manager.get_or_create(model_class, doc_id, default_data)
                return DatabaseItem(item)
                
            elif self.db_type == DatabaseType.MONGODB:
                # Use the get_or_create method
                self.logger.debug("Using native get_or_create for MongoDB")
                item = self._db_manager.get_or_create(model_class, doc_id, default_data)
                return DatabaseItem(item)
                
        except Exception as e:
            self.logger.error(f"Error in get_or_create for {doc_id}: {e}")
            raise
    
    def model_to_db_item(self, item: BaseModel) -> DatabaseItem:
        """
        Convert a Pydantic model instance to a DatabaseItem.
        
        Args:
            item: Pydantic model instance
            
        Returns:
            DatabaseItem instance
        """
        self.logger.info(f"Converting {item.__class__.__name__} to database item")
        
        try:
            if self.db_type == DatabaseType.DYNAMODB:
                # For DynamoDB, we need to store the item first
                self.logger.debug("Storing model in DynamoDB before conversion")
                item_dict = item.model_dump()
                doc_id = item_dict.get('id')
                
                doc_id = self.put_item(item)
                    
                # Get the item and return as DatabaseItem
                db_item = self._db_manager.get_item(item.__class__, {'id': doc_id})
                
                if db_item is None:
                    self.logger.error(f"Failed to retrieve item with ID {doc_id} after storing")
                    raise ValueError(f"Item with ID {doc_id} not found after storing")
                    
                self.logger.debug(f"Created DatabaseItem for ID: {doc_id}")
                return DatabaseItem(db_item)
                    
            elif self.db_type == DatabaseType.FIRESTORE:
                # Use the model_to_firestore_item method
                self.logger.debug("Using native model_to_firestore_item for Firestore")
                item = self._db_manager.model_to_firestore_item(item)
                if item is None:
                    raise ValueError("Failed to convert model to Firestore item")
                return DatabaseItem(item)
                    
            elif self.db_type == DatabaseType.MONGODB:
                # Use the model_to_mongo_doc method
                self.logger.debug("Using native model_to_mongo_doc for MongoDB")
                item = self._db_manager.model_to_mongo_doc(item)
                if item is None:
                    raise ValueError("Failed to convert model to MongoDB doc")
                return DatabaseItem(item)
            
            else:
                raise ValueError(f"Unsupported database type: {self.db_type}")
                    
        except Exception as e:
            self.logger.error(f"Error converting model to database item: {e}")
            raise
    
    def get_native_manager(self):
        """
        Get the native database manager instance.
        
        Returns:
            The underlying database manager (DynamoManager, FirestoreManager, or MongoDBManager)
        """
        return self._db_manager


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
    
    # Create instances of different database types
    dynamo_db = Database(
        db_type=DatabaseType.DYNAMODB,
        namespace="myapp_dynamo",
        instance_id="dynamo-users"
    )
    
    firestore_db = Database(
        db_type=DatabaseType.FIRESTORE,
        namespace="myapp_firestore",
        instance_id="firestore-users",
        credentials_path="path/to/credentials.json",
        project_id = "my-gcp-project"
    )
    
    mongodb_db = Database(
        db_type=DatabaseType.MONGODB,
        namespace="myapp_mongo",
        instance_id="mongo-users",
        connection_string="mongodb://localhost:27017/",
        database_name="myapp"
    )
    
    # Register the model with indexed fields in all databases
    dynamo_db.register_model(User, "users", indexed_fields=["email", "is_active"])
    firestore_db.register_model(User, "users", indexed_fields=["email", "is_active"])
    mongodb_db.register_model(User, "users", indexed_fields=["email", "is_active"])
    
    # Create a user in DynamoDB
    user = User(name="DynamoDB User", email="dynamo@example.com")
    dynamo_user_id = dynamo_db.put_item(user)
    
    # Create a user in Firestore
    user = User(name="Firestore User", email="firestore@example.com")
    firestore_user_id = firestore_db.put_item(user)
    
    # Create a user in MongoDB
    user = User(name="MongoDB User", email="mongo@example.com")
    mongodb_user_id = mongodb_db.put_item(user)
    
    # List all database instances
    instances = Database.list_instances()
    print(f"Database instances: {instances}")
    
    # Get a specific instance
    retrieved_db = Database.get_instance("firestore-users")
    
    # Retrieve and update users from each database
    dynamo_user = dynamo_db.get_item(User, dynamo_user_id)
    dynamo_user["age"] = 30
    
    firestore_user = firestore_db.get_item(User, firestore_user_id)
    firestore_user["age"] = 35
    
    mongodb_user = mongodb_db.get_item(User, mongodb_user_id)
    mongodb_user["age"] = 40