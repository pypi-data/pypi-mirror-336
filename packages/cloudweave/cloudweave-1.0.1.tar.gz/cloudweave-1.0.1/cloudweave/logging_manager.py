import enum
import logging
import io
import os
import time
import json
import uuid
import functools
import threading
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
from threading import Lock

# Importing existing components - these are assumed to exist in your codebase


class LoggerType(enum.Enum):
    """Enum for supported logger types."""
    LOCAL = "local"
    AWS = "aws"
    GCP = "gcp"
    LOKI = "loki"
    STORAGE = "storage"
    
    @classmethod
    def from_string(cls, value: str) -> 'LoggerType':
        """Convert string to enum value."""
        try:
            return cls(value.lower())
        except ValueError:
            valid_values = ', '.join([e.value for e in cls])
            raise ValueError(f"Invalid logger type: {value}. Valid values are: {valid_values}")


class Logger:
    """
    Unified logger interface that can connect to multiple logging backends.
    Supports maintaining multiple connections to different logging types simultaneously.
    
    Usage:
        # Create a local logger
        local_logger = Logger(
            logger_type="local",
            namespace="myapp",
            instance_id="local-logs"
        )
        
        # Create an AWS CloudWatch logger
        aws_logger = Logger(
            logger_type="aws",
            namespace="myapp",
            instance_id="aws-logs",
            region="us-east-1"
        )
        
        # Create a Storage-based logger
        storage_logger = Logger(
            logger_type="storage",
            namespace="myapp",
            instance_id="storage-logs",
            storage_type="s3",
            bucket="my-logs-bucket"
        )
        
        # Log messages
        local_logger.info("Application started")
        aws_logger.error("Something went wrong", {"method": "GET", "path": "/api/users"})
        
        # Send metrics
        aws_logger.send_metric("api_requests", 1, {"endpoint": "/api/users"})
    """
    
    # Registry of logger instances
    _registry = {}
    _lock = Lock()
    
    def __init__(self, 
                logger_type: Union[str, LoggerType],
                namespace: str,
                instance_id: Optional[str] = None,
                **kwargs):
        """
        Initialize a logger connection.
        
        Args:
            logger_type: Type of logger to create (local, aws, gcp, loki, storage)
            namespace: Namespace prefix for logs
            instance_id: Optional unique identifier for this logger
            **kwargs: Logger-specific configuration parameters
        """
        # Convert string to enum if necessary
        if isinstance(logger_type, str):
            self.logger_type = LoggerType.from_string(logger_type)
        else:
            self.logger_type = logger_type
            
        self.namespace = namespace
        
        # Generate unique instance ID if not provided
        self.instance_id = instance_id or f"{self.logger_type.value}-{namespace}-{uuid.uuid4()}"
        
        # Common configuration with defaults
        self.config = kwargs
        self.config.setdefault('stdout', True)
        self.config.setdefault('log_level', 'info')
        self.config.setdefault('labels', {})
        
        # Backend-specific objects
        self._logger_backend = None
        self._storage = None
        self._metric_values = {}
        
        # Set up logging backend
        self._setup_logger(**kwargs)
        
        # Register this instance
        with Logger._lock:
            Logger._registry[self.instance_id] = self
    
    @classmethod
    def get_instance(cls, instance_id: str) -> Optional['Logger']:
        """
        Get a logger instance by ID.
        
        Args:
            instance_id: Logger instance ID
            
        Returns:
            Logger instance or None if not found
        """
        return cls._registry.get(instance_id)
        
    @classmethod
    def list_instances(cls) -> List[str]:
        """
        List all registered logger instance IDs.
        
        Returns:
            List of instance IDs
        """
        return list(cls._registry.keys())
    
    def _setup_logger(self, **kwargs):
        """
        Initialize the logger backend based on the logger type.
        
        Args:
            **kwargs: Logger-specific configuration parameters
        """
        if self.logger_type == LoggerType.LOCAL:
            self._setup_local_logger(**kwargs)
        elif self.logger_type == LoggerType.AWS:
            self._setup_aws_logger(**kwargs)
        elif self.logger_type == LoggerType.GCP:
            self._setup_gcp_logger(**kwargs)
        elif self.logger_type == LoggerType.LOKI:
            self._setup_loki_logger(**kwargs)
        elif self.logger_type == LoggerType.STORAGE:
            self._setup_storage_logger(**kwargs)
        else:
            raise ValueError(f"Unsupported logger type: {self.logger_type}")
    
    def _setup_local_logger(self, **kwargs):
        """Initialize local logger."""
        from cloudweave.logging_utils.string_logger import StringLogHandler

        # Set up Python logger
        self._logger = logging.getLogger(f"{self.namespace}-{self.instance_id}")
        self._logger.setLevel(self._get_log_level(self.config.get('log_level', 'info')))
        self._logger.handlers = []  # Clear existing handlers
        
        # Add stdout handler if enabled
        if self.config.get('stdout', True):
            console_handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)
            self._logger.addHandler(console_handler)
        
        # Add file handler if log_file is specified
        if 'log_file' in self.config:
            try:
                # Ensure directory exists
                log_dir = os.path.dirname(self.config['log_file'])
                if log_dir and not os.path.exists(log_dir):
                    os.makedirs(log_dir)
                    
                file_handler = logging.FileHandler(self.config['log_file'])
                formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
                file_handler.setFormatter(formatter)
                self._logger.addHandler(file_handler)
            except Exception as e:
                print(f"Error setting up file handler: {e}")
        
        # Add string handler for in-memory logs
        self._string_handler = StringLogHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self._string_handler.setFormatter(formatter)
        self._logger.addHandler(self._string_handler)
        
        print(f"Local logger initialized for namespace: {self.namespace} with ID: {self.instance_id}")
    
    def _setup_aws_logger(self, **kwargs):
        """Initialize AWS CloudWatch logger."""
        # Set up a local logger for stdout
        self._setup_local_logger(**kwargs)
        
        # Import AWS-specific logger
        from cloudweave.logging_utils import AWSLogger
        
        # Create AWS logger
        aws_config = {
            'namespace': self.namespace,
            'dimensions': self.config.get('dimensions', {'Service': self.namespace}),
            'region': self.config.get('region', 'us-east-1'),
            'local_only': False
        }
        
        # Add any additional AWS config
        for key, value in kwargs.items():
            if key not in aws_config:
                aws_config[key] = value
        
        # Create AWS logger instance
        self._aws_logger = AWSLogger(self.instance_id, aws_config)
        
        print(f"AWS logger initialized for namespace: {self.namespace} with ID: {self.instance_id}")
    
    def _setup_gcp_logger(self, **kwargs):
        """Initialize GCP Cloud Logging logger."""
        # Set up a local logger for stdout
        self._setup_local_logger(**kwargs)
        
        # Check required parameters
        if 'project_id' not in kwargs:
            raise ValueError("GCP logger requires project_id")
        
        # Import GCP-specific logger
        from cloudweave.logging_utils import GCPLogger
        
        # Create GCP logger
        gcp_config = {
            'project_id': kwargs['project_id'],
            'namespace': self.namespace,
            'labels': self.config.get('labels', {})
        }
        
        # Add any additional GCP config
        for key, value in kwargs.items():
            if key not in gcp_config:
                gcp_config[key] = value
        
        # Create GCP logger instance
        self._gcp_logger = GCPLogger(self.instance_id, gcp_config)
        
        print(f"GCP logger initialized for namespace: {self.namespace} with ID: {self.instance_id}")
    
    def _setup_loki_logger(self, **kwargs):
        """Initialize Grafana Loki logger."""
        # Set up a local logger for stdout
        self._setup_local_logger(**kwargs)
        
        # Check required parameters
        if 'loki_url' not in kwargs:
            raise ValueError("Loki logger requires loki_url")
        
        # Import Loki-specific logger
        from cloudweave.logging_utils import LokiLogger
        
        # Create Loki logger
        loki_config = {
            'loki_url': kwargs['loki_url'],
            'labels': self.config.get('labels', {'service': self.namespace}),
            'batch_size': self.config.get('batch_size', 10),
            'batch_interval': self.config.get('batch_interval', 5)
        }
        
        # Add any additional Loki config
        for key, value in kwargs.items():
            if key not in loki_config:
                loki_config[key] = value
        
        # Create Loki logger instance
        self._loki_logger = LokiLogger(self.instance_id, loki_config)
        
        print(f"Loki logger initialized for namespace: {self.namespace} with ID: {self.instance_id}")
    
    def _setup_storage_logger(self, **kwargs):
        """Initialize Storage-based logger."""
        from cloudweave.storage_manager import Storage, StorageType

        # Set up a local logger for stdout
        self._setup_local_logger(**kwargs)
        
        # Check required parameters
        required_params = ['storage_type', 'bucket']
        for param in required_params:
            if param not in kwargs:
                raise ValueError(f"Storage logger requires {param}")
        
        # Set up Storage
        storage_options = kwargs.get('storage_options', {})
        
        # Initialize Storage instance
        self._storage = Storage(
            storage_type=kwargs['storage_type'],
            namespace=self.namespace,
            instance_id=f"{self.instance_id}-storage",
            default_bucket=kwargs['bucket'],
            **storage_options
        )
        
        # Storage logger configuration
        self._storage_config = {
            'bucket': kwargs['bucket'],
            'prefix': kwargs.get('prefix', 'logs/'),
            'upload_interval': kwargs.get('upload_interval', 300)  # 5 minutes
        }
        
        # Initialize upload tracking
        self._last_upload_time = time.time()
        
        # Start background upload thread for storage logger
        self._stop_thread = False
        self._upload_thread = threading.Thread(target=self._upload_logs_periodically)
        self._upload_thread.daemon = True
        self._upload_thread.start()
        
        print(f"Storage logger initialized for namespace: {self.namespace} with ID: {self.instance_id}")
    
    def _get_log_level(self, level: str) -> int:
        """Convert log level string to logging level."""
        level_map = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'critical': logging.CRITICAL
        }
        return level_map.get(level.lower(), logging.INFO)
    
    def _format_log_message(self, message: str, extra: Dict[str, Any] = None) -> str:
        """Format log message with extra data if provided."""
        if extra and extra.get('labels'):
            return f"{message} {json.dumps(extra['labels'])}"
        return message
    
    def debug(self, message: str, extra: Dict[str, Any] = None) -> None:
        """Log a debug message."""
        self._log('debug', message, extra)
    
    def info(self, message: str, extra: Dict[str, Any] = None) -> None:
        """Log an info message."""
        self._log('info', message, extra)
    
    def warning(self, message: str, extra: Dict[str, Any] = None) -> None:
        """Log a warning message."""
        self._log('warning', message, extra)
    
    def error(self, message: str, extra: Dict[str, Any] = None) -> None:
        """Log an error message."""
        self._log('error', message, extra)
    
    def critical(self, message: str, extra: Dict[str, Any] = None) -> None:
        """Log a critical message."""
        self._log('critical', message, extra)
    
    def _log(self, level: str, message: str, extra: Dict[str, Any] = None) -> None:
        """Internal method to handle logging with the appropriate backend."""
        # Log to local logger (which may include stdout and file)
        formatted_message = self._format_log_message(message, extra)
        log_level = self._get_log_level(level)
        self._logger.log(log_level, formatted_message)
        
        # Log to specific backends
        if self.logger_type == LoggerType.AWS and hasattr(self, '_aws_logger'):
            self._aws_logger.log(level, message, extra)
        
        elif self.logger_type == LoggerType.GCP and hasattr(self, '_gcp_logger'):
            self._gcp_logger.log(level, message, extra)
        
        elif self.logger_type == LoggerType.LOKI and hasattr(self, '_loki_logger'):
            self._loki_logger.log(level, message, extra)
        
        elif self.logger_type == LoggerType.STORAGE:
            # Storage logger uses the string handler and uploads periodically
            current_time = time.time()
            if current_time - self._last_upload_time >= self._storage_config['upload_interval']:
                self._upload_logs()
                self._last_upload_time = current_time
    
    def send_metric(self, name: str, value: float, labels: Dict[str, str] = None) -> None:
        """
        Send a metric to the logging backend.
        
        Args:
            name: Metric name
            value: Metric value
            labels: Additional labels for the metric
        """
        # Store the metric value
        self._metric_values[name] = value
        
        # Create metric labels
        metric_labels = {'metric_name': name, 'metric_value': value}
        if labels:
            metric_labels.update(labels)
        
        # Log the metric message
        metric_message = f"METRIC: {name}={value}"
        
        if self.logger_type == LoggerType.AWS and hasattr(self, '_aws_logger'):
            self._aws_logger.send_metric(name, value, labels)
        
        elif self.logger_type == LoggerType.GCP and hasattr(self, '_gcp_logger'):
            self._gcp_logger.send_metric(name, value, labels)
        
        elif self.logger_type == LoggerType.LOKI and hasattr(self, '_loki_logger'):
            self._loki_logger.send_metric(name, value, labels)
        
        # Always log metric as a normal log message
        self.info(metric_message, {'labels': metric_labels})
    
    def get_metric(self, name: str, default: float = 0.0) -> float:
        """Get the latest value of a metric."""
        return self._metric_values.get(name, default)
    
    def _get_log_filename(self) -> str:
        """Generate a log filename based on current time."""
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        return f"{self.namespace}_{self.instance_id}_{timestamp}.log"
    
    def _upload_logs(self) -> None:
        """Upload collected logs to storage (for storage logger type)."""
        if self.logger_type != LoggerType.STORAGE or not self._storage:
            return
            
        logs = self._string_handler.get_logs()
        if not logs:
            return
            
        filename = self._get_log_filename()
        path = f"{self._storage_config['prefix'].rstrip('/')}/{filename}"
        
        try:
            # Use Storage class to write logs
            success = self._storage.write_text(
                content=logs,
                bucket_name=self._storage_config['bucket'],
                path=path,
                content_type="text/plain"
            )
            
            if success:
                self.info(f"Uploaded logs to storage: {path}")
                self._string_handler.clear()
            else:
                self.error(f"Failed to upload logs to storage: {path}")
        except Exception as e:
            self.error(f"Error uploading logs: {e}")
    
    def _upload_logs_periodically(self) -> None:
        """Background thread to upload logs at regular intervals."""
        while not self._stop_thread:
            time.sleep(1)  # Check every second
            
            current_time = time.time()
            if current_time - self._last_upload_time >= self._storage_config['upload_interval']:
                self._upload_logs()
                self._last_upload_time = current_time
    
    def upload_metrics_to_storage(self, path_prefix: str = "metrics/") -> bool:
        """
        Upload current metrics to storage as JSON (for storage logger type).
        
        Args:
            path_prefix: Path prefix in storage bucket
        
        Returns:
            bool: True if upload was successful, False otherwise
        """
        if self.logger_type != LoggerType.STORAGE or not self._storage:
            self.error("Cannot upload metrics: not a storage logger")
            return False
            
        if not self._metric_values:
            self.info("No metrics to upload")
            return True
            
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        path = f"{path_prefix.rstrip('/')}/metrics_{timestamp}.json"
        
        try:
            # Add timestamp to metrics
            metrics_data = {
                "timestamp": datetime.now().isoformat(),
                "metrics": self._metric_values,
                "labels": self.config.get('labels', {})
            }
            
            # Use Storage class to write metrics
            success = self._storage.write_json(
                data=metrics_data,
                bucket_name=self._storage_config['bucket'],
                path=path
            )
            
            if success:
                self.info(f"Uploaded metrics to storage: {path}")
                return True
            else:
                self.error(f"Failed to upload metrics to storage: {path}")
                return False
        except Exception as e:
            self.error(f"Error uploading metrics: {e}")
            return False
    
    def time_this(self, name: str, labels: Dict[str, str] = None):
        """
        Decorator to time a function and send duration as a metric.
        
        Args:
            name: Base name for the metric
            labels: Additional labels for the metric
            
        Example:
            @logger.time_this('data_processing')
            def process_data():
                # Processing code
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                
                # Send metric
                self.send_metric(f"{name}_duration", duration, labels)
                
                return result
            return wrapper
        return decorator
    
    def __del__(self):
        """Clean up resources when the logger is destroyed."""
        # For storage logger, ensure logs are uploaded
        if self.logger_type == LoggerType.STORAGE:
            if hasattr(self, '_upload_thread'):
                self._stop_thread = True
                
            if hasattr(self, '_string_handler') and hasattr(self, '_storage'):
                self._upload_logs()


# Example usage
if __name__ == "__main__":
    # Create a local logger
    local_logger = Logger(
        logger_type=LoggerType.LOCAL,
        namespace="myapp",
        instance_id="local-logs",
        log_file="logs/application.log",
        log_level="info"
    )
    
    # Create an AWS CloudWatch logger
    aws_logger = Logger(
        logger_type=LoggerType.AWS,
        namespace="myapp",
        instance_id="aws-logs",
        region="us-east-1",
        dimensions={
            "Service": "API",
            "Environment": "Production" 
        }
    )
    
    # Create a GCP Cloud Logging logger
    gcp_logger = Logger(
        logger_type=LoggerType.GCP,
        namespace="myapp",
        instance_id="gcp-logs",
        project_id="my-gcp-project",
        labels={
            "service": "api",
            "environment": "production"
        }
    )
    
    # Create a Loki logger
    loki_logger = Logger(
        logger_type=LoggerType.LOKI,
        namespace="myapp",
        instance_id="loki-logs",
        loki_url="http://loki:3100/loki/api/v1/push",
        labels={
            "service": "api",
            "environment": "production"
        }
    )
    
    # Create a Storage-based logger with S3
    s3_logger = Logger(
        logger_type=LoggerType.STORAGE,
        namespace="myapp",
        instance_id="s3-logs",
        storage_type="s3",
        bucket="my-logs-bucket",
        prefix="application-logs/",
        upload_interval=60,  # Upload every minute
        storage_options={
            "region": "us-east-1"
        }
    )
    
    # Create a Storage-based logger with GCS
    gcs_logger = Logger(
        logger_type=LoggerType.STORAGE,
        namespace="myapp",
        instance_id="gcs-logs",
        storage_type="gcs",
        bucket="my-gcs-logs-bucket",
        prefix="application-logs/",
        upload_interval=120,  # Upload every 2 minutes
        storage_options={
            "project_id": "my-gcp-project"
        }
    )
    
    # Log messages to different loggers
    local_logger.info("Application started (local)")
    aws_logger.info("Application started (AWS)")
    gcp_logger.info("Application started (GCP)")
    loki_logger.info("Application started (Loki)")
    s3_logger.info("Application started (S3 Storage)")
    gcs_logger.info("Application started (GCS Storage)")
    
    # Log error with additional context
    aws_logger.error("API request failed", {
        "labels": {
            "method": "GET",
            "path": "/api/users",
            "status_code": 500
        }
    })
    
    # Send metrics
    aws_logger.send_metric("api_requests", 1, {"endpoint": "/api/users"})
    gcp_logger.send_metric("api_requests", 2, {"endpoint": "/api/products"})
    
    # Use the time_this decorator
    @local_logger.time_this("data_processing")
    def process_data():
        time.sleep(0.5)  # Simulate work
        return {"status": "success"}
    
    # Process data and log timing
    result = process_data()
    
    # List all logger instances
    instances = Logger.list_instances()
    print(f"Logger instances: {instances}")
    
    # Get a specific instance
    retrieved_logger = Logger.get_instance("aws-logs")