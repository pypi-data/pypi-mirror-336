import json
import time
from typing import Dict, Any, Optional, List, Union, Type, TypeVar, get_type_hints
from threading import Lock
import uuid

# Import AWSManager from cloud_session_utils
from cloudweave.cloud_session_utils import AWSManager
from cloudweave.utilities import Singleton
from cloudweave.logging_manager import Logger, LoggerType

from botocore.exceptions import ClientError
from pydantic import BaseModel


T = TypeVar('T', bound=BaseModel)

class DynamoItem:
    """
    Dictionary-like wrapper for interacting with DynamoDB items.
    Provides a seamless interface similar to dictionary access.
    """
    
    def __init__(self, manager: 'DynamoManager', model_class: Type[BaseModel], key: Dict[str, Any], data: Dict[str, Any] = None):
        """
        Initialize a new DynamoDB item wrapper.
        
        Args:
            manager: DynamoManager instance
            model_class: Pydantic model class
            key: Primary key of the item
            data: Optional data to initialize with
        """
        self.manager = manager
        self.model_class = model_class
        self.key = key
        self._data = data or self._load_data()
        
    def _load_data(self) -> Dict[str, Any]:
        """Load item data from DynamoDB."""
        data = self.manager.get_item(self.model_class, self.key)
        if data is None:
            self.manager.logger.error(f"Item with key {self.key} not found in table {self.manager._get_table_name(self.model_class)}")
            raise KeyError(f"Item with key {self.key} not found")
        return data
        
    def __getitem__(self, key: str) -> Any:
        """Get an attribute value."""
        if key not in self._data:
            self._data = self._load_data()  # Refresh data
        return self._data.get(key)
        
    def __setitem__(self, key: str, value: Any) -> None:
        """Set an attribute value and update in DynamoDB."""
        self._data[key] = value
        # Explicitly call update to persist the change
        self.manager.update_item(self.model_class, self.key, {key: value})
        
    def get(self, key: str, default: Any = None) -> Any:
        """Get an attribute value with a default."""
        try:
            return self[key]
        except (KeyError, AttributeError):
            return default
            
    def update(self, updates: Dict[str, Any]) -> None:
        """Update multiple attributes at once."""
        self._data.update(updates)
        self.manager.update_item(self.model_class, self.key, updates)
        
    def refresh(self) -> None:
        """Refresh data from DynamoDB."""
        self._data = self._load_data()
        
    def delete(self) -> None:
        """Delete this item from DynamoDB."""
        self.manager.delete_item(self.model_class, self.key)
        self._data = {}
        
    def to_dict(self) -> Dict[str, Any]:
        """Get a dictionary representation of the item."""
        return self._data.copy()


class DynamoManager(Singleton):
    """
    Thread-safe singleton manager for DynamoDB operations.
    Uses AWSManager for authentication and session management.
    Provides seamless integration with Pydantic models.
    
    Usage:
        # Initialize the manager
        dynamo = DynamoManager.instance('myapp')
        
        # Register a model and ensure table exists
        dynamo.ensure_table_exists(User, indexes={'email-index': {'hash_key': 'email'}})
        
        # Store an item
        user = User(user_id='123', name='Test User')
        dynamo.put_item(user)
        
        # Get and work with an item
        user_item = dynamo.get_model_item(User, {'user_id': '123'})
        user_item['age'] = 30  # Updates the item in DynamoDB
    """
    
    def _initialize(self, namespace: str, region: Optional[str] = None, profile: Optional[str] = None, logger_options: Dict[str, Any] = None):
        """
        Initialize DynamoDB manager with AWSManager integration.
        
        Args:
            namespace: Namespace prefix for table names
            region: Optional AWS region
            profile: Optional AWS profile name
            logger_options: Optional logger configuration
        """
        self.namespace = namespace
        self._connection_lock = Lock()
        self._model_table_map = {}  # Maps model classes to table names
        
        # Store AWS options for manager
        self._aws_options = {
            'region': region,
            'profile': profile
        }
        
        # Initialize the logger
        self._setup_logger(logger_options or {})
        
        # Initialize AWS session (will be done lazily when needed)
        self._dynamodb = None
        
        self.logger.info(f"DynamoManager initialized with namespace '{namespace}', region '{region or 'default'}'")
    
    def _setup_logger(self, logger_options: Dict[str, Any]) -> None:
        """
        Set up the logger for this DynamoManager instance.
        
        Args:
            logger_options: Logger configuration options
        """
        if 'logger_instance' in logger_options:
            self.logger = logger_options['logger_instance']
            self.logger.info("Using provided logger instance for DynamoManager")
        else:
            # Create a new logger
            log_level = logger_options.get('log_level', 'info')
            log_namespace = logger_options.get('namespace', f"dynamo-{self.namespace}")
            
            self.logger = Logger(
                logger_type=logger_options.get('logger_type', 'local'),
                namespace=log_namespace,
                instance_id=logger_options.get('instance_id', f"dynamo-manager-{self.namespace}"),
                log_level=log_level,
                **{k: v for k, v in logger_options.items() if k not in ['logger_type', 'namespace', 'instance_id', 'log_level']}
            )
            self.logger.info(f"Created new logger for DynamoManager with namespace '{log_namespace}'")
    
    @classmethod
    def instance(cls, namespace: str = None, region: Optional[str] = None, profile: Optional[str] = None, logger_options: Dict[str, Any] = None):
        """
        Get or create the singleton instance.
        
        Args:
            namespace: Namespace prefix for table names
            region: Optional AWS region
            profile: Optional AWS profile name
            logger_options: Optional logger configuration
            
        Returns:
            DynamoManager instance
        """
        # If we already have an instance but namespace is None, return existing instance
        if cls in cls._instances and namespace is None:
            return cls._instances[cls]
        
        # Otherwise create/update instance with provided parameters
        return cls(namespace, region, profile, logger_options)
    
    def _get_dynamodb(self):
        """
        Get or create DynamoDB client using AWSManager.
        
        Returns:
            DynamoDB client
        """
        if self._dynamodb is None:
            with self._connection_lock:
                if self._dynamodb is None:
                    # Get AWSManager instance with our options
                    self.logger.debug("Initializing DynamoDB client")
                    
                    try:
                        # Get AWSManager instance with our options
                        aws = AWSManager.instance(self._aws_options)
                        
                        # Get DynamoDB client
                        self._dynamodb = aws.dynamodb
                        self.logger.info("DynamoDB client initialized successfully")
                    except Exception as e:
                        self.logger.error(f"Failed to initialize DynamoDB client: {e}")
                        raise
        
        return self._dynamodb
    
    def _get_table_name(self, model_class: Type[BaseModel]) -> str:
        """
        Get the table name for a model class.
        
        Args:
            model_class: Pydantic model class
            
        Returns:
            Table name in DynamoDB
        """
        # Check if we have a mapping already
        if model_class in self._model_table_map:
            return self._model_table_map[model_class]
        
        # Default to lowercase model name with namespace
        table_name = f"{self.namespace}_{model_class.__name__.lower()}"
        return table_name
    
    def register_model(self, model_class: Type[BaseModel], table_name: Optional[str] = None) -> None:
        """
        Register a model class with a specific table name.
        
        Args:
            model_class: Pydantic model class
            table_name: Optional custom table name
        """
        if table_name:
            full_table_name = f"{self.namespace}_{table_name}"
            self._model_table_map[model_class] = full_table_name
        else:
            self._model_table_map[model_class] = self._get_table_name(model_class)
            
        self.logger.info(f"Registered model {model_class.__name__} with table {self._model_table_map[model_class]}")
    
    def ensure_table_exists(self, model_class: Type[BaseModel], indexes: Optional[Dict[str, Dict[str, Any]]] = None) -> bool:
        """
        Ensure a table exists for the given Pydantic model.
        
        Args:
            model_class: Pydantic model class
            indexes: Optional dictionary defining GSIs
            
        Returns:
            True if table already existed, False if it was created
        """
        table_name = self._get_table_name(model_class)
        dynamodb = self._get_dynamodb()
        
        self.logger.info(f"Checking if table {table_name} exists")
        
        try:
            dynamodb.describe_table(TableName=table_name)
            self.logger.info(f"Table {table_name} already exists")
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                self.logger.info(f"Table {table_name} does not exist, creating it")
                self._create_table_from_model(model_class, indexes)
                return False
            else:
                self.logger.error(f"Error checking table existence: {e}")
                raise
    
    def _create_table_from_model(self, model_class: Type[BaseModel], indexes: Optional[Dict[str, Dict[str, Any]]] = None) -> None:
        """
        Create a DynamoDB table based on a Pydantic model.
        
        Args:
            model_class: Pydantic model class
            indexes: Optional dictionary defining GSIs
        """
        table_name = self._get_table_name(model_class)
        dynamodb = self._get_dynamodb()
        
        self.logger.info(f"Creating table {table_name} from model {model_class.__name__}")
        
        # Extract field types from model for attribute definitions
        type_hints = get_type_hints(model_class)
                
        # Always use 'id' as the partition key for consistency
        partition_key = 'id'
        
        # Create attribute definitions
        attribute_definitions = [
            {'AttributeName': partition_key, 'AttributeType': 'S'}  # Always use string type for IDs
        ]
        
        # Create key schema
        key_schema = [
            {'AttributeName': partition_key, 'KeyType': 'HASH'}
        ]         
        
        # Prepare GSI configuration
        gsi_config = []
        if indexes:
            for index_name, index_def in indexes.items():
                self.logger.debug(f"Adding GSI {index_name} with hash key {index_def['hash_key']}")
                
                # Add GSI key attributes to attribute definitions if not already there
                for key in [index_def['hash_key'], index_def.get('range_key')]:
                    if key and not any(ad['AttributeName'] == key for ad in attribute_definitions):
                        attribute_definitions.append(
                            {'AttributeName': key, 'AttributeType': self._pydantic_type_to_dynamodb_type(type_hints[key])}
                        )
                
                # Create GSI key schema
                gsi_key_schema = [
                    {'AttributeName': index_def['hash_key'], 'KeyType': 'HASH'}
                ]
                
                if 'range_key' in index_def:
                    self.logger.debug(f"Adding range key {index_def['range_key']} to GSI {index_name}")
                    gsi_key_schema.append(
                        {'AttributeName': index_def['range_key'], 'KeyType': 'RANGE'}
                    )
                
                gsi_config.append({
                    'IndexName': index_name,
                    'KeySchema': gsi_key_schema,
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                })
        
        # Create the table
        try:
            create_params = {
                'TableName': table_name,
                'KeySchema': key_schema,
                'AttributeDefinitions': attribute_definitions,
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            }
            
            if gsi_config:
                create_params['GlobalSecondaryIndexes'] = gsi_config
            
            self.logger.debug(f"Calling DynamoDB create_table with params: {json.dumps(create_params, default=str)}")
            dynamodb.create_table(**create_params)
            
            # Wait for table to be created
            self.logger.info(f"Waiting for table {table_name} to be created")
            waiter = dynamodb.get_waiter('table_exists')
            waiter.wait(TableName=table_name)
            
            self.logger.info(f"Table {table_name} created successfully")
            
        except ClientError as e:
            self.logger.error(f"Error creating table {table_name}: {e}")
            raise
    
    def _pydantic_type_to_dynamodb_type(self, field_type) -> str:
        """
        Convert a Pydantic field type to a DynamoDB attribute type.
        Ensure boolean fields are stored as strings when used as index keys.
        
        Args:
            field_type: Pydantic field type
            
        Returns:
            DynamoDB attribute type (S, N, B)
        """
        field_type_str = str(field_type)
        
        if 'str' in field_type_str:
            return 'S'
        elif any(t in field_type_str for t in ['int', 'float', 'decimal']):
            return 'N'
        elif 'bool' in field_type_str:
            return 'S'
        elif 'bytes' in field_type_str:
            return 'B'
        else:
            return 'S'  # Default to string
    
    def put_item(self, item: BaseModel) -> str:
        """
        Store a Pydantic model instance in DynamoDB.
        
        Args:
            item: Pydantic model instance to store
            
        Returns:
            Document ID of the created document
        """
        table_name = self._get_table_name(item.__class__)
        
        # Convert model to dict
        item_dict = item.model_dump()
        
        # Generate a UUID if id is not provided
        if 'id' not in item_dict or item_dict['id'] is None:
            item_dict['id'] = str(uuid.uuid4())
            
        # Store ID for return
        doc_id = item_dict['id']
        
        # Convert to DynamoDB format and store
        dynamodb_item = self._dict_to_dynamodb(item_dict)
        
        try:
            self._dynamodb.put_item(
                TableName=table_name,
                Item=dynamodb_item
            )
            self.logger.info(f"Successfully added item to {table_name}")
            return doc_id  # Return the ID here
        except Exception as e:
            self.logger.error(f"Error adding item to {table_name}: {e}")
            raise
    
    def get_item(self, model_class: Type[BaseModel], key: Union[str, Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Get an item from DynamoDB by primary key.
        
        Args:
            model_class: Pydantic model class
            key: Either a string ID or dictionary containing primary key values
                
        Returns:
            Dictionary representation of the item, or None if not found
        """
        table_name = self._get_table_name(model_class)
        dynamodb = self._get_dynamodb()
        
        # Handle string IDs by converting to a dictionary
        if isinstance(key, str):
            key = {'id': key}
        
        self.logger.debug(f"Getting item from {table_name} with key {key}")
        
        # Convert key to DynamoDB format
        dynamodb_key = self._dict_to_dynamodb(key)
        
        try:
            response = dynamodb.get_item(
                TableName=table_name,
                Key=dynamodb_key
            )
            
            if 'Item' in response:
                self.logger.debug(f"Item found in {table_name}")
                # Convert DynamoDB format back to Python dict
                return self._dynamodb_to_dict(response['Item'])
                
            self.logger.debug(f"Item not found in {table_name}")
            return None
            
        except ClientError as e:
            self.logger.error(f"Error getting item from {table_name}: {e}")
            raise
    
    def get_model_item(self, model_class: Type[BaseModel], key: Dict[str, Any]) -> Optional[DynamoItem]:
        """
        Get an item from DynamoDB by primary key and return as a DynamoItem.
        
        Args:
            model_class: Pydantic model class
            key: Dictionary containing primary key values
            
        Returns:
            DynamoItem wrapper or None if not found
        """
        data = self.get_item(model_class, key)
        if data is None:
            return None
        
        return DynamoItem(self, model_class, key, data)
    
    def update_document(self, doc_id: str, collection_name: str, updates: Dict[str, Any]) -> None:
        """
        Update a document in DynamoDB.
        
        Args:
            doc_id: Document ID
            collection_name: Collection/table name
            updates: Dictionary of fields to update
        """
        # For DynamoDB, we need to translate this to update_item
        # with the proper key format
        self.update_item(
            None,  # We don't have the model class here
            {'id': doc_id},
            updates
        )
    
    def update_item(self, model_class: Type[BaseModel], key: Dict[str, Any], updates: Dict[str, Any]) -> None:
        """
        Update an item in DynamoDB.
        
        Args:
            model_class: Pydantic model class
            key: Dictionary containing primary key values
            updates: Dictionary of attributes to update
        """
        table_name = self._get_table_name(model_class)
        dynamodb = self._get_dynamodb()
        
        self.logger.info(f"Updating item in {table_name}")
        self.logger.debug(f"Key: {key}")
        self.logger.debug(f"Updates: {json.dumps(updates, default=str)}")
        
        # Convert key to DynamoDB format
        dynamodb_key = self._dict_to_dynamodb(key)
        
        # Prepare update expression and attribute values
        update_parts = []
        expr_attr_values = {}
        expr_attr_names = {}
        
        for k, v in updates.items():
            # Use expression attribute names for reserved keywords
            attr_name = f"#{k.replace('-', '_')}"
            expr_attr_names[attr_name] = k
            update_parts.append(f"{attr_name} = :{k.replace('-', '_')}")
            
            # Convert the value to DynamoDB format
            if isinstance(v, str):
                expr_attr_values[f":{k.replace('-', '_')}"] = {'S': v}
            elif isinstance(v, bool):
                # Special handling for boolean values that might be indexed
                # Check if this is an indexed field
                if model_class and hasattr(model_class, '__indexed_fields__') and k in getattr(model_class, '__indexed_fields__', []):
                    expr_attr_values[f":{k.replace('-', '_')}"] = {'S': str(v).lower()}
                else:
                    expr_attr_values[f":{k.replace('-', '_')}"] = {'BOOL': v}
            elif isinstance(v, (int, float)):
                expr_attr_values[f":{k.replace('-', '_')}"] = {'N': str(v)}
            elif isinstance(v, dict):
                expr_attr_values[f":{k.replace('-', '_')}"] = {'M': self._dict_to_dynamodb(v)}
            elif v is None:
                update_parts[-1] = f"remove {attr_name}"
                del expr_attr_values[f":{k.replace('-', '_')}"]
            else:
                expr_attr_values[f":{k.replace('-', '_')}"] = {'S': json.dumps(v)}
        
        # Build the update expression
        update_expression = "SET " + ", ".join(update_parts)
        
        try:
            dynamodb.update_item(
                TableName=table_name,
                Key=dynamodb_key,
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expr_attr_values,
                ExpressionAttributeNames=expr_attr_names
            )
            self.logger.info(f"Successfully updated item in {table_name}")
        except ClientError as e:
            self.logger.error(f"Error updating item in {table_name}: {e}")
            raise
    
    def query(self, model_class: Type[BaseModel], partition_key: str, partition_value: Any,
             sort_condition: Optional[str] = None, index_name: Optional[str] = None,
             filter_expression: Optional[str] = None, 
             expression_values: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Query items from DynamoDB.
        
        Args:
            model_class: Pydantic model class
            partition_key: Name of the partition key
            partition_value: Value of the partition key
            sort_condition: Optional sort key condition
            index_name: Optional name of GSI to use
            filter_expression: Optional filter expression
            expression_values: Optional values for the filter expression
            
        Returns:
            List of items matching the query
        """
        table_name = self._get_table_name(model_class)
        dynamodb = self._get_dynamodb()
        
        self.logger.info(f"Querying items from {table_name}")
        self.logger.debug(f"Partition key: {partition_key}={partition_value}")
        if sort_condition:
            self.logger.debug(f"Sort condition: {sort_condition}")
        if index_name:
            self.logger.debug(f"Using index: {index_name}")
        if filter_expression:
            self.logger.debug(f"Filter expression: {filter_expression}")
        
        # Prepare key condition expression
        key_condition = f"#{partition_key} = :{partition_key}"
        expr_attr_names = {f"#{partition_key}": partition_key}
        expr_attr_values = {f":{partition_key}": self._python_to_dynamodb_value(partition_value)}
        
        # Add sort key condition if provided
        if sort_condition:
            key_condition += f" AND {sort_condition}"
        
        # Add filter expression values if provided
        if expression_values:
            for k, v in expression_values.items():
                if not k.startswith(':'):
                    k = f":{k}"
                expr_attr_values[k] = self._python_to_dynamodb_value(v)
                
                # Add attribute name if it's in the expression values
                attr_name = k[1:]  # Remove the leading colon
                if attr_name not in expr_attr_names:
                    expr_attr_names[f"#{attr_name}"] = attr_name
        
        # Prepare query parameters
        query_params = {
            'TableName': table_name,
            'KeyConditionExpression': key_condition,
            'ExpressionAttributeNames': expr_attr_names,
            'ExpressionAttributeValues': expr_attr_values
        }
        
        # Add optional parameters
        if index_name:
            query_params['IndexName'] = index_name
        
        if filter_expression:
            query_params['FilterExpression'] = filter_expression
            
        try:
            response = dynamodb.query(**query_params)
            
            # Convert DynamoDB items to Python dictionaries
            results = []
            for item in response.get('Items', []):
                results.append(self._dynamodb_to_dict(item))
            
            self.logger.info(f"Query returned {len(results)} items from {table_name}")
            return results
            
        except ClientError as e:
            self.logger.error(f"Error querying items from {table_name}: {e}")
            raise
    
    def query_items(self, model_class: Type[BaseModel], partition_key: str, partition_value: Any,
                   sort_condition: Optional[str] = None, index_name: Optional[str] = None,
                   filter_expression: Optional[str] = None, 
                   expression_values: Optional[Dict[str, Any]] = None) -> List[DynamoItem]:
        """
        Query items from DynamoDB and return as DynamoItem instances.
        
        Args:
            model_class: Pydantic model class
            partition_key: Name of the partition key
            partition_value: Value of the partition key
            sort_condition: Optional sort key condition
            index_name: Optional name of GSI to use
            filter_expression: Optional filter expression
            expression_values: Optional values for the filter expression
            
        Returns:
            List of DynamoItem instances matching the query
        """
        # Get the raw query results
        results = self.query(
            model_class, 
            partition_key, 
            partition_value, 
            sort_condition, 
            index_name, 
            filter_expression, 
            expression_values
        )
        
        # Convert to DynamoItem instances
        items = []
        schema = model_class.model_schema()
        required_fields = schema.get('required', [])
        
        for result in results:
            # Build the key from required fields
            key = {field: result[field] for field in required_fields if field in result}
            items.append(DynamoItem(self, model_class, key, result))
        
        self.logger.debug(f"Converted {len(results)} query results to DynamoItem instances")
        return items
    
    def delete_item(self, model_class: Type[BaseModel], key: Dict[str, Any]) -> None:
        """
        Delete an item from DynamoDB.
        
        Args:
            model_class: Pydantic model class
            key: Dictionary containing primary key values
        """
        table_name = self._get_table_name(model_class)
        dynamodb = self._get_dynamodb()
        
        self.logger.info(f"Deleting item from {table_name}")
        self.logger.debug(f"Key: {key}")
        
        # Convert key to DynamoDB format
        dynamodb_key = self._dict_to_dynamodb(key)
        
        try:
            dynamodb.delete_item(
                TableName=table_name,
                Key=dynamodb_key
            )
            self.logger.info(f"Successfully deleted item from {table_name}")
        except ClientError as e:
            self.logger.error(f"Error deleting item from {table_name}: {e}")
            raise
    
    def _dict_to_dynamodb(self, d: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert a Python dictionary to a DynamoDB item format.
        
        Args:
            d: Python dictionary to convert
            
        Returns:
            Dictionary in DynamoDB format
        """
        result = {}
        for k, v in d.items():
            if v is not None:  # Skip None values
                result[k] = self._python_to_dynamodb_value(v)
        return result
    
    def _python_to_dynamodb_value(self, value: Any) -> Dict[str, Any]:
        """
        Convert a Python value to DynamoDB attribute value format.
        
        Args:
            value: Python value to convert
            
        Returns:
            Value in DynamoDB format
        """
        if isinstance(value, str):
            return {'S': value}
        elif isinstance(value, bool):
            # Store booleans as strings for GSI keys
            return {'S': str(value).lower()}
        elif isinstance(value, (int, float)):
            return {'N': str(value)}
        elif isinstance(value, dict):
            return {'M': self._dict_to_dynamodb(value)}
        elif isinstance(value, list):
            return {'L': [self._python_to_dynamodb_value(item) for item in value]}
        elif value is None:
            return {'NULL': True}
        else:
            # Convert other types to JSON string
            return {'S': json.dumps(value)}
    
    def _dynamodb_to_dict(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert a DynamoDB item to a Python dictionary.
        
        Args:
            item: DynamoDB item to convert
            
        Returns:
            Python dictionary equivalent
        """
        result = {}
        
        for k, v in item.items():
            result[k] = self._dynamodb_value_to_python(v)
            
        return result
    
    def _dynamodb_value_to_python(self, value: Dict[str, Any]) -> Any:
        """
        Convert a DynamoDB attribute value to its Python equivalent.
        
        Args:
            value: DynamoDB attribute value to convert
            
        Returns:
            Python equivalent
        """
        if 'S' in value:
            return value['S']
        elif 'N' in value:
            # Try converting to int first, then float
            try:
                return int(value['N'])
            except ValueError:
                return float(value['N'])
        elif 'BOOL' in value:
            return value['BOOL']
        elif 'M' in value:
            return self._dynamodb_to_dict(value['M'])
        elif 'L' in value:
            return [self._dynamodb_value_to_python(item) for item in value['L']]
        elif 'NULL' in value:
            return None
        else:
            # Default case
            return str(value)
    
    def get_or_create(self, model_class: Type[BaseModel], key: Dict[str, Any], default_data: Dict[str, Any] = None) -> DynamoItem:
        """
        Get an item if it exists or create it with default data.
        
        Args:
            model_class: Pydantic model class
            key: Primary key of the item
            default_data: Default data for new item
            
        Returns:
            DynamoItem instance
        """
        # Try to get the item
        item = self.get_model_item(model_class, key)
        
        if item is not None:
            return item
        
        # Item doesn't exist, create it
        if default_data is None:
            default_data = {}
            
        # Add key to default data
        default_data.update(key)
        
        # Create model instance
        model_instance = model_class(**default_data)
        
        # Store in DynamoDB
        self.put_item(model_instance)
        
        # Return as DynamoItem
        return DynamoItem(self, model_class, key, default_data)
    
    def batch_write(self, items: List[BaseModel]) -> None:
        """
        Write multiple items in a batch operation.
        
        Args:
            items: List of model instances to write
            
        Note:
            All items must be of the same model class
        """
        if not items:
            return
            
        # Get the model class from the first item
        model_class = items[0].__class__
        table_name = self._get_table_name(model_class)
        dynamodb = self._get_dynamodb()
        
        # Prepare batch request
        request_items = []
        for item in items:
            # Convert to DynamoDB format
            item_dict = item.model_dump()
            dynamodb_item = self._dict_to_dynamodb(item_dict)
            
            # Add to request
            request_items.append({
                'PutRequest': {
                    'Item': dynamodb_item
                }
            })
            
            # DynamoDB has a limit of 25 items per batch
            if len(request_items) == 25:
                dynamodb.batch_write_item(
                    RequestItems={
                        table_name: request_items
                    }
                )
                request_items = []
        
        # Write any remaining items
        if request_items:
            dynamodb.batch_write_item(
                RequestItems={
                    table_name: request_items
                }
            )
            
        self.logger.info(f"Batch wrote {len(items)} items to {table_name}")