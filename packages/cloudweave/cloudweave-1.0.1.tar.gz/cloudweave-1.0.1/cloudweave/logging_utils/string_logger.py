import logging
import io
import os, sys
import time
import json
import functools
import threading
from typing import Dict, Any, Optional, List, Union
from datetime import datetime

# Import the Storage class
from cloudweave.storage_manager import Storage, StorageType

class StringLogHandler(logging.Handler):
    """
    Custom logging handler that writes log records to an in-memory string buffer.
    Useful for collecting logs to upload to cloud storage.
    """
    def __init__(self, level=logging.NOTSET):
        super().__init__(level)
        self.log_stream = io.StringIO()
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    def emit(self, record):
        """Write formatted log record to string buffer."""
        try:
            msg = self.formatter.format(record)
            self.log_stream.write(f"{msg}\n")
        except Exception:
            self.handleError(record)
    
    def get_logs(self) -> str:
        """Return current logs as a string."""
        return self.log_stream.getvalue()
    
    def clear(self):
        """Clear the log buffer."""
        self.log_stream = io.StringIO()


class StringLogger:
    """
    Unified logger that can send logs to stdout, local files, and cloud storage.
    Integrates with the Storage class for cloud storage operations.
    """
    def __init__(self, name: str, config: Dict[str, Any] = None):
        """
        Initialize the unified logger.
        
        Args:
            name: Logger name
            config: Configuration dictionary containing:
                - local_file: Path to local log file (optional)
                - stdout: Whether to log to stdout (default: True)
                - log_level: Logging level (default: INFO)
                - storage: Storage configuration:
                    - enabled: Whether to use cloud storage (default: False)
                    - storage_type: Storage type: 's3' or 'gcs' (required if enabled)
                    - bucket: Storage bucket name (required if enabled)
                    - prefix: Path prefix in bucket (default: 'logs/')
                    - upload_interval: Seconds between uploads (default: 300)
                    - namespace: Storage namespace (default: 'logs')
                    - storage_options: Additional options for Storage class
                - labels: Labels to add to log entries (default: {})
        """
        self.name = name
        self.config = config or {}
        
        # Set default configuration
        self.config.setdefault('stdout', True)
        self.config.setdefault('log_level', logging.INFO)
        self.config.setdefault('labels', {})
        
        # Initialize the Python logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.config['log_level'])
        self.logger.handlers = []  # Remove any existing handlers
        
        # Add stdout handler if enabled
        if self.config['stdout']:
            console_handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        
        # Add file handler if local file is specified
        if 'local_file' in self.config:
            try:
                file_handler = logging.FileHandler(self.config['local_file'])
                formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
            except Exception as e:
                print(f"Error setting up file handler: {e}")
        
        # Initialize string handler for collecting logs
        self.string_handler = StringLogHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.string_handler.setFormatter(formatter)
        self.logger.addHandler(self.string_handler)
        
        # Initialize storage if enabled
        self.storage = None
        if self.config.get('storage', {}).get('enabled', False):
            self._initialize_storage()
        
        # Initialize metric tracking
        self._metric_values = {}
    
    def _initialize_storage(self):
        """Initialize cloud storage connection using the Storage class."""
        storage_config = self.config.get('storage', {})
        
        # Check required fields
        required_fields = ['storage_type', 'bucket']
        for field in required_fields:
            if field not in storage_config:
                self.logger.error(f"Missing required storage config field: {field}")
                return
        
        # Set default values
        storage_config.setdefault('prefix', 'logs/')
        storage_config.setdefault('upload_interval', 300)  # 5 minutes
        storage_config.setdefault('namespace', 'logs')
        storage_config.setdefault('storage_options', {})
        
        # Store bucket info
        self._bucket = storage_config['bucket']
        self._prefix = storage_config['prefix']
        self._upload_interval = storage_config['upload_interval']
        
        try:
            # Create storage instance
            storage_options = storage_config['storage_options']
            storage_options['default_bucket'] = self._bucket
            
            self.storage = Storage(
                storage_type=storage_config['storage_type'],
                namespace=storage_config['namespace'],
                instance_id=f"{self.name}-logger",
                **storage_options
            )
            
            # Initialize upload tracking
            self._last_upload_time = time.time()
            
            # Start background upload thread
            self._stop_thread = False
            self._upload_thread = threading.Thread(target=self._upload_logs_periodically)
            self._upload_thread.daemon = True
            self._upload_thread.start()
            
            self.logger.info(f"Initialized {storage_config['storage_type']} storage for logging")
        except Exception as e:
            self.logger.error(f"Failed to initialize storage: {e}")
    
    def info(self, message: str, extra: Dict[str, Any] = None):
        """Log an info message."""
        self._log('INFO', message, extra)
    
    def error(self, message: str, extra: Dict[str, Any] = None):
        """Log an error message."""
        self._log('ERROR', message, extra)
    
    def debug(self, message: str, extra: Dict[str, Any] = None):
        """Log a debug message."""
        self._log('DEBUG', message, extra)
    
    def warning(self, message: str, extra: Dict[str, Any] = None):
        """Log a warning message."""
        self._log('WARNING', message, extra)
    
    def _log(self, level: str, message: str, extra: Dict[str, Any] = None):
        """Internal method to handle logging with proper level."""
        # Add default labels
        log_extra = {'labels': self.config['labels'].copy()}
        
        # Add extra fields if provided
        if extra:
            log_extra['labels'].update(extra)
        
        # Convert log level string to logging level
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        log_level = level_map.get(level, logging.INFO)
        
        # Format the message with extra data for structured logging
        if log_extra['labels']:
            labeled_message = f"{message} {json.dumps(log_extra['labels'])}"
        else:
            labeled_message = message
        
        # Log the message
        self.logger.log(log_level, labeled_message)
        
        # Check if we should upload logs (for cloud storage)
        if self.storage and hasattr(self, '_last_upload_time'):
            current_time = time.time()
            if current_time - self._last_upload_time >= self._upload_interval:
                self._upload_logs()
                self._last_upload_time = current_time
    
    def send_metric(self, name: str, value: float, labels: Dict[str, str] = None):
        """
        Record a metric value.
        
        Args:
            name: Metric name
            value: Metric value
            labels: Additional labels for the metric
        """
        # Store the metric value
        self._metric_values[name] = value
        
        # Log the metric
        metric_labels = {'metric_name': name, 'metric_value': value}
        if labels:
            metric_labels.update(labels)
        
        self.info(f"METRIC: {name}={value}", metric_labels)
    
    def get_metric(self, name: str, default: float = 0.0) -> float:
        """Get the latest value of a metric."""
        return self._metric_values.get(name, default)
    
    def time_this(self, name: str, labels: Dict[str, str] = None):
        """
        Decorator to time a function and record its duration.
        
        Args:
            name: Base name for the metric
            labels: Additional labels for the metric
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                
                # Record the metric
                self.send_metric(f"{name}_duration", duration, labels)
                
                return result
            return wrapper
        return decorator
    
    def get_logs(self) -> str:
        """Get all logs collected in the string handler."""
        return self.string_handler.get_logs()
    
    def clear_string_logs(self):
        """Clear the string log buffer."""
        self.string_handler.clear()
    
    def _get_log_filename(self) -> str:
        """Generate a log filename based on current time."""
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        return f"{self.name}_{timestamp}.log"
    
    def _upload_logs(self):
        """Upload collected logs to the configured storage."""
        if not self.storage:
            return
            
        logs = self.get_logs()
        if not logs:
            return
        
        filename = self._get_log_filename()
        path = f"{self._prefix.rstrip('/')}/{filename}"
        
        try:
            # Use Storage class to write logs
            success = self.storage.write_text(
                content=logs,
                bucket_name=self._bucket,
                path=path,
                content_type="text/plain"
            )
            
            if success:
                self.info(f"Uploaded logs to storage: {path}")
                self.clear_string_logs()
            else:
                self.error(f"Failed to upload logs to storage: {path}")
        except Exception as e:
            self.error(f"Error uploading logs: {e}")
    
    def _upload_logs_periodically(self):
        """Background thread to upload logs at regular intervals."""
        while not self._stop_thread:
            time.sleep(1)  # Check every second
            
            current_time = time.time()
            if current_time - self._last_upload_time >= self._upload_interval:
                self._upload_logs()
                self._last_upload_time = current_time
    
    def upload_metrics_to_storage(self, path_prefix: str = "metrics/"):
        """
        Upload current metrics to storage as JSON.
        
        Args:
            path_prefix: Path prefix in storage bucket
        
        Returns:
            bool: True if upload was successful, False otherwise
        """
        if not self.storage:
            self.error("Cannot upload metrics: storage not initialized")
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
            success = self.storage.write_json(
                data=metrics_data,
                bucket_name=self._bucket,
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
    
    def __del__(self):
        """Clean up resources and ensure logs are uploaded before destruction."""
        if hasattr(self, '_upload_thread'):
            self._stop_thread = True
            if self._upload_thread.is_alive():
                self._upload_logs()  # Final upload of pending logs


# Example usage
if __name__ == "__main__":
    # Create logger with S3 storage
    s3_logger = StringLogger(
        name="s3-app",
        config={
            'stdout': True,
            'local_file': 'app.log',
            'storage': {
                'enabled': True,
                'storage_type': 's3',
                'bucket': 'my-logs-bucket',
                'prefix': 'application-logs/',
                'upload_interval': 60,  # Upload every minute
                'namespace': 'my-application',
                'storage_options': {
                    'region': 'us-east-1'
                }
            },
            'labels': {
                'environment': 'production',
                'version': '1.0.0'
            }
        }
    )
    
    # Create logger with GCS storage
    gcs_logger = StringLogger(
        name="gcs-app",
        config={
            'stdout': True,
            'storage': {
                'enabled': True,
                'storage_type': 'gcs',
                'bucket': 'my-gcs-logs-bucket',
                'prefix': 'application-logs/',
                'upload_interval': 120,  # Upload every 2 minutes
                'namespace': 'my-application',
                'storage_options': {
                    'project_id': 'my-gcp-project'
                }
            },
            'labels': {
                'environment': 'staging',
                'version': '1.0.0'
            }
        }
    )
    
    # Basic logging
    s3_logger.info("Application started")
    s3_logger.error("Something went wrong", {"method": "GET", "path": "/api/users"})
    
    # Record a metric
    s3_logger.send_metric("api_requests", 1, {"endpoint": "/api/users"})
    
    # Time a function
    @s3_logger.time_this('data_processing', {"dataset": "users"})
    def process_data():
        time.sleep(0.5)  # Simulate work
        return {"status": "success"}
    
    # Use the timed function
    result = process_data()
    
    # Manually upload metrics (in addition to logs)
    s3_logger.upload_metrics_to_storage()