import time
import uuid
import weakref
import abc
from threading import Lock
from typing import Dict, Any, Optional, Union, Type

from cloudweave.utilities import Singleton
from cloudweave.database_manager import Database, DatabaseType
from cloudweave.logging_manager import Logger, LoggerType
from cloudweave.notification_manager import NotificationManager
from cloudweave.storage_manager import Storage, StorageType

class AuthenticationError(Exception):
    """Exception raised for authentication errors."""
    pass

class CloudWeaveAuthManager(Singleton):
    """
    Central authentication manager for CloudWeave.
    Controls access to all package components through API key validation.
    """
    
    def _initialize(self, api_key: Optional[str] = None, token_validity: int = 86400):
        """
        Initialize the CloudWeaveAuthManager.
        
        Args:
            api_key: API key for authentication
            token_validity: Token validity period in seconds (default: 24 hours)
        """
        # Authentication state
        self._valid_api_key = "your-secret-api-key"  # Replace with your actual key
        self._is_authenticated = False
        self._auth_expiry = 0
        self._token_validity = token_validity
        
        # Component references
        self._database_instances = {}
        self._logger_instances = {}
        self._notification_instances = {}
        self._storage_instances = {}
        
        # Create default logger for auth manager
        self._setup_default_logger()
        
        # Authenticate if API key is provided
        if api_key:
            self.authenticate(api_key)
            
        self.logger.info("CloudWeaveAuthManager initialized")
    
    def _setup_default_logger(self) -> None:
        """Set up the default logger for the auth manager."""
        try:
            self.logger = Logger(
                logger_type=LoggerType.LOCAL,
                namespace="auth-manager",
                instance_id=f"auth-manager-{uuid.uuid4()}",
                log_level='info'
            )
            self.logger.info("Default logger initialized for CloudWeaveAuthManager")
        except Exception as e:
            # Fallback to Python's standard logging if Logger creation fails
            import logging
            self.logger = logging.getLogger("auth-manager")
            self.logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(handler)
            self.logger.warning(f"Using fallback logger due to error: {e}")
    
    def authenticate(self, api_key: str) -> bool:
        """
        Authenticate with API key.
        
        Args:
            api_key: The API key to validate
            
        Returns:
            True if authentication successful
            
        Raises:
            AuthenticationError: If API key is invalid
        """
        if api_key != self._valid_api_key:
            self.logger.warning("Authentication failed: Invalid API key")
            raise AuthenticationError("Invalid API key")
        
        # Set authentication status
        self._is_authenticated = True
        self._auth_expiry = int(time.time()) + self._token_validity
        
        self.logger.info("Authentication successful")
        return True
    
    def is_authenticated(self) -> bool:
        """Check if currently authenticated and token is valid."""
        if not self._is_authenticated:
            return False
        
        # Check if token has expired
        if int(time.time()) > self._auth_expiry:
            self._is_authenticated = False
            return False
        
        return True
    
    def check_auth(self) -> None:
        """
        Check if authenticated and token is valid.
        
        Raises:
            AuthenticationError: If not authenticated or token expired
        """
        if not self._is_authenticated:
            raise AuthenticationError("Not authenticated")
        
        if int(time.time()) > self._auth_expiry:
            self._is_authenticated = False
            raise AuthenticationError("Authentication has expired")
    
    # Database methods
    def get_database(self, 
                    db_type: Union[str, DatabaseType],
                    namespace: str,
                    instance_id: Optional[str] = None,
                    logger_options: Dict[str, Any] = None,
                    **kwargs) -> Database:
        """
        Get or create a database instance.
        
        Args:
            db_type: Type of database to connect to
            namespace: Namespace prefix for tables/collections
            instance_id: Optional unique identifier for this connection
            logger_options: Optional logger configuration
            **kwargs: Database-specific connection parameters
            
        Returns:
            Database instance
            
        Raises:
            AuthenticationError: If not authenticated
        """
        # Check authentication
        self.check_auth()
        
        # Generate instance ID if not provided
        if not instance_id:
            if isinstance(db_type, str):
                db_type_str = db_type
            else:
                db_type_str = db_type.value
            instance_id = f"{db_type_str}-{namespace}-{uuid.uuid4()}"
        
        # Check if we already have this instance
        if instance_id in self._database_instances:
            self.logger.info(f"Returning existing database instance: {instance_id}")
            return self._database_instances[instance_id]
        
        # Set up logger options
        if logger_options is None:
            logger_options = {
                'logger_instance': self.logger
            }
        
        # Create new database instance
        self.logger.info(f"Creating new database instance: {instance_id}")
        db = Database(
            db_type=db_type,
            namespace=namespace,
            instance_id=instance_id,
            logger_options=logger_options,
            **kwargs
        )
        
        # Store reference
        self._database_instances[instance_id] = db
        
        return db
    
    def list_database_instances(self) -> Dict[str, Database]:
        """
        List all database instances.
        
        Returns:
            Dictionary of instance IDs to database instances
            
        Raises:
            AuthenticationError: If not authenticated
        """
        self.check_auth()
        return self._database_instances
    
    # Logger methods
    def get_logger(self,
                  logger_type: Union[str, LoggerType],
                  namespace: str,
                  instance_id: Optional[str] = None,
                  **kwargs) -> Logger:
        """
        Get or create a logger instance.
        
        Args:
            logger_type: Type of logger to create
            namespace: Namespace prefix for logs
            instance_id: Optional unique identifier for this logger
            **kwargs: Logger-specific configuration parameters
            
        Returns:
            Logger instance
            
        Raises:
            AuthenticationError: If not authenticated
        """
        # Check authentication
        self.check_auth()
        
        # Generate instance ID if not provided
        if not instance_id:
            if isinstance(logger_type, str):
                logger_type_str = logger_type
            else:
                logger_type_str = logger_type.value
            instance_id = f"{logger_type_str}-{namespace}-{uuid.uuid4()}"
        
        # Check if we already have this instance
        if instance_id in self._logger_instances:
            self.logger.info(f"Returning existing logger instance: {instance_id}")
            return self._logger_instances[instance_id]
        
        # Create new logger instance
        self.logger.info(f"Creating new logger instance: {instance_id}")
        logger = Logger(
            logger_type=logger_type,
            namespace=namespace,
            instance_id=instance_id,
            **kwargs
        )
        
        # Store reference
        self._logger_instances[instance_id] = logger
        
        return logger
    
    def list_logger_instances(self) -> Dict[str, Logger]:
        """
        List all logger instances.
        
        Returns:
            Dictionary of instance IDs to logger instances
            
        Raises:
            AuthenticationError: If not authenticated
        """
        self.check_auth()
        return self._logger_instances
    
    def get_default_logger(self) -> Logger:
        """
        Get the default logger.
        
        Returns:
            Default logger instance
            
        Raises:
            AuthenticationError: If not authenticated
        """
        self.check_auth()
        return self.logger
    
    def get_notification_manager(self,
                            default_provider: str = 'aws',
                            instance_id: Optional[str] = None,
                            aws_options: Dict[str, Any] = None,
                            google_options: Dict[str, Any] = None,
                            storage_options: Dict[str, Any] = None,
                            **kwargs) -> NotificationManager:
        """
        Get or create a notification manager instance.
        
        Args:
            default_provider: Default email provider to use ('aws' or 'google')
            instance_id: Optional unique identifier for this notification manager
            aws_options: Configuration for AWS email service
            google_options: Configuration for Google email service
            storage_options: Storage configuration options
            **kwargs: Additional notification manager configuration
            
        Returns:
            NotificationManager instance
            
        Raises:
            AuthenticationError: If not authenticated
        """
        # Check authentication
        self.check_auth()
        
        # Generate instance ID if not provided
        if not instance_id:
            instance_id = f"notification-{default_provider}-{uuid.uuid4()}"
        
        # Check if we already have this instance
        if instance_id in self._notification_instances:
            self.logger.info(f"Returning existing notification manager instance: {instance_id}")
            return self._notification_instances[instance_id]
        
        # Create logger options
        logger_options = kwargs.get('logger_options', {})
        if 'logger_instance' not in logger_options:
            logger_options['logger_instance'] = self.logger
        
        # Create notification manager options
        options = {
            'default_provider': default_provider,
            'logger_options': logger_options
        }
        
        # Add provider options if provided
        if aws_options:
            options['aws_options'] = aws_options
        
        if google_options:
            options['google_options'] = google_options
        
        if storage_options:
            options['storage_options'] = storage_options
        
        # Add any additional options
        for key, value in kwargs.items():
            if key != 'logger_options' and key not in options:
                options[key] = value
        
        # Create new notification manager instance
        self.logger.info(f"Creating new notification manager instance: {instance_id}")
        notification_manager = NotificationManager(options)
        
        # Store reference
        self._notification_instances[instance_id] = notification_manager
        
        return notification_manager
    
    def list_notification_manager_instances(self) -> Dict[str, NotificationManager]:
        """
        List all notification manager instances.
        
        Returns:
            Dictionary of instance IDs to notification manager instances
            
        Raises:
            AuthenticationError: If not authenticated
        """
        self.check_auth()
        return self._notification_instances
    
    
    def get_storage(self,
                storage_type: Union[str, StorageType],
                namespace: str,
                instance_id: Optional[str] = None,
                default_bucket: Optional[str] = None,
                **kwargs) -> Storage:
        """
        Get or create a storage instance.
        
        Args:
            storage_type: Type of storage to connect to (s3 or gcs)
            namespace: Namespace prefix for buckets/folders
            instance_id: Optional unique identifier for this connection
            default_bucket: Optional default bucket name
            **kwargs: Storage-specific connection parameters
            
        Returns:
            Storage instance
            
        Raises:
            AuthenticationError: If not authenticated
        """
        # Check authentication
        self.check_auth()
        
        # Generate instance ID if not provided
        if not instance_id:
            if isinstance(storage_type, str):
                storage_type_str = storage_type
            else:
                storage_type_str = storage_type.value
            instance_id = f"{storage_type_str}-{namespace}-{uuid.uuid4()}"
        
        # Check if we already have this instance
        if instance_id in self._storage_instances:
            self.logger.info(f"Returning existing storage instance: {instance_id}")
            return self._storage_instances[instance_id]
        
        # Create new storage instance
        self.logger.info(f"Creating new storage instance: {instance_id}")
        
        # Set default bucket if provided
        storage_kwargs = kwargs.copy()
        if default_bucket:
            storage_kwargs['default_bucket'] = default_bucket
        
        # Use the auth manager's logger for storage
        storage = Storage(
            storage_type=storage_type,
            namespace=namespace,
            instance_id=instance_id,
            logger_instance=self.logger,
            **storage_kwargs
        )
        
        # Store reference
        self._storage_instances[instance_id] = storage
        
        return storage

    def list_storage_instances(self) -> Dict[str, Storage]:
        """
        List all storage instances.
        
        Returns:
            Dictionary of instance IDs to storage instances
            
        Raises:
            AuthenticationError: If not authenticated
        """
        self.check_auth()
        return self._storage_instances


# Create a global factory function for easier access
def get_auth_manager(api_key: Optional[str] = None) -> CloudWeaveAuthManager:
    """
    Get or initialize the CloudWeaveAuthManager.
    
    Args:
        api_key: Optional API key for authentication
        
    Returns:
        CloudWeaveAuthManager instance
    """
    return CloudWeaveAuthManager(api_key)