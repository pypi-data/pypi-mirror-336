import logging
import sys, os
import time
import functools
import json
from typing import Dict, Any, Optional

# Import GCP libraries
from google.cloud.monitoring import MetricServiceClient
from google.cloud import monitoring_v3
from google.cloud import logging as cloud_logging
from google.api import metric_pb2
from google.api import label_pb2
from google.protobuf import timestamp_pb2

# Import GCPManager from cloud_session_utils
from cloudweave.cloud_session_utils import GCPManager

class GCPLogger:
    def __init__(self, name: str, config: Dict[str, Any] = None):
        """
        Simple GCP Logger for Cloud Monitoring metrics and Cloud Logging.
        
        Args:
            name: Logger name
            config: Configuration with keys:
                - project_id: GCP project ID (required)
                - namespace: Metric namespace prefix (default: 'custom.googleapis.com')
                - labels: Dict of metric labels (default: {})
                - local_only: Skip GCP integration if True (default: False)
        """
        self.name = name
        self.config = config or {}
        
        if 'project_id' not in self.config:
            raise ValueError("GCP project_id is required in config")
            
        self.config.setdefault('namespace', 'custom.googleapis.com')
        self.config.setdefault('labels', {})
        self.config.setdefault('local_only', False)
        
        # Set up standard Python logger
        self.logger = logging.getLogger(name)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
        
        # Initialize GCP clients if not in local-only mode
        if not self.config['local_only']:
            # Get GCP clients
            gcp = GCPManager.instance(self.config)
            self._project_path = f"projects/{self.config['project_id']}"
            
            # Set up Cloud Monitoring client
            self._metric_client: MetricServiceClient = gcp.get_client("monitoring")
            
            # Set up Cloud Logging client
            self._logging_client: cloud_logging.Client = gcp.get_client("logging")
            self._cloud_logger = self._logging_client.logger(self.name)
    
    def log(self, level: str, message: str, extra: Dict[str, Any] = None):
        """
        Log a message with the specified level and optional extra data.
        
        Args:
            level: Log level (debug, info, warning, error, critical)
            message: Log message
            extra: Additional data to include with the log
        """
        # Convert level string to logging level
        level_map = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'critical': logging.CRITICAL
        }
        log_level = level_map.get(level.lower(), logging.INFO)
        
        # Format message with extra data if needed
        if extra:
            formatted_message = f"{message} {json.dumps(extra)}"
        else:
            formatted_message = message
        
        # Log locally
        self.logger.log(log_level, formatted_message)
        
        # Send to Cloud Logging
        self._send_to_cloud_logging(level.upper(), message, extra)
    
    def info(self, message: str, extra: Dict[str, Any] = None):
        """Log info message and send to Cloud Logging."""
        self.log('info', message, extra)
    
    def error(self, message: str, extra: Dict[str, Any] = None):
        """Log error message and send to Cloud Logging."""
        self.log('error', message, extra)
    
    def debug(self, message: str, extra: Dict[str, Any] = None):
        """Log debug message and send to Cloud Logging."""
        self.log('debug', message, extra)
    
    def warning(self, message: str, extra: Dict[str, Any] = None):
        """Log warning message and send to Cloud Logging."""
        self.log('warning', message, extra)
    
    def critical(self, message: str, extra: Dict[str, Any] = None):
        """Log critical message and send to Cloud Logging."""
        self.log('critical', message, extra)
    
    def _send_to_cloud_logging(self, level: str, message: str, extra: Dict[str, Any] = None):
        """Send log to Google Cloud Logging."""
        if self.config['local_only']:
            return
            
        try:
            # Map level string to severity
            severity_map = {
                'DEBUG': 'DEBUG',
                'INFO': 'INFO',
                'WARNING': 'WARNING',
                'ERROR': 'ERROR',
                'CRITICAL': 'CRITICAL'
            }
            severity = severity_map.get(level.upper(), 'DEFAULT')
            
            # Start with labels from config
            labels = self.config['labels'].copy()
            
            # Add extra data as structured information
            if extra:
                # If 'labels' key exists in extra, merge with our labels
                if 'labels' in extra:
                    labels.update(extra['labels'])
                    
                # Remove 'labels' from extra to avoid duplication
                extra_data = extra.copy()
                if 'labels' in extra_data:
                    del extra_data['labels']
            else:
                extra_data = None
            
            # Use structured logging if extra data exists
            if extra_data:
                # Create structured payload
                payload = {
                    'message': message,
                    'data': extra_data
                }
                
                # Log structured entry
                self._cloud_logger.log_struct(
                    payload,
                    severity=severity,
                    labels=labels
                )
            else:
                # Simple text logging
                self._cloud_logger.log_text(
                    message,
                    severity=severity,
                    labels=labels
                )
        except Exception as e:
            self.logger.warning(f"Error sending log to Cloud Logging: {e}")
    
    def send_metric(self, name: str, value: float, unit: str = 'count', labels: Dict[str, str] = None):
        """
        Send a metric to Cloud Monitoring.
        
        Args:
            name: Metric name (will be prefixed with namespace)
            value: Metric value
            unit: Metric unit (default: 'count')
            labels: Additional labels for this metric (merged with config labels)
        """
        if self.config['local_only']:
            return
            
        try:
            # Construct the full metric type
            metric_type = f"{self.config['namespace']}/{name}"
            
            # Create metric descriptor if it doesn't exist
            self._ensure_metric_descriptor_exists(metric_type, unit)
            
            # Create timeseries data
            series = monitoring_v3.TimeSeries()
            series.metric.type = metric_type
            
            # Combine base labels with additional labels
            all_labels = self.config['labels'].copy()
            if labels:
                all_labels.update(labels)
            
            # Add labels to metric
            for key, val in all_labels.items():
                series.metric.labels[key] = str(val)
            
            # Add resource
            series.resource.type = 'global'
            
            # Add datapoint with current timestamp
            now = time.time()
            timestamp = timestamp_pb2.Timestamp()
            timestamp.seconds = int(now)
            timestamp.nanos = int((now - int(now)) * 10**9)
            
            point = monitoring_v3.Point()
            point.interval.end_time.seconds = timestamp.seconds
            point.interval.end_time.nanos = timestamp.nanos
            point.value.double_value = value
            series.points.append(point)
            
            # Write the timeseries
            self._metric_client.create_time_series(
                name=self._project_path,
                time_series=[series]
            )
            
            # Log the metric if desired
            self.debug(f"Metric sent: {name}={value} {unit}", {"labels": all_labels})
        except Exception as e:
            self.logger.warning(f"Error sending metric to Cloud Monitoring: {e}")
    
    def _ensure_metric_descriptor_exists(self, metric_type: str, unit: str):
        """Ensure the metric descriptor exists in Cloud Monitoring."""
        try:
            try:
                self._metric_client.get_metric_descriptor(name=f"{self._project_path}/metricDescriptors/{metric_type}")
            except Exception:
                # Create the metric descriptor
                descriptor = metric_pb2.MetricDescriptor()
                descriptor.name = f"{self._project_path}/metricDescriptors/{metric_type}"
                descriptor.type = metric_type
                descriptor.metric_kind = metric_pb2.MetricDescriptor.MetricKind.GAUGE
                descriptor.value_type = metric_pb2.MetricDescriptor.ValueType.DOUBLE
                descriptor.description = f"Custom metric: {metric_type}"
                
                # Set unit based on common unit types
                unit_map = {
                    'count': '{count}',
                    'seconds': 's',
                    'milliseconds': 'ms',
                    'bytes': 'By',
                    'kilobytes': 'kBy',
                    'megabytes': 'MBy',
                    'gigabytes': 'GBy'
                }
                descriptor.unit = unit_map.get(unit.lower(), unit)
                
                # Add all labels defined in config
                for key, _ in self.config['labels'].items():
                    label = label_pb2.LabelDescriptor()
                    label.key = key
                    label.value_type = label_pb2.LabelDescriptor.ValueType.STRING
                    descriptor.labels.append(label)
                
                # Create the descriptor
                self._metric_client.create_metric_descriptor(
                    name=self._project_path,
                    metric_descriptor=descriptor
                )
        except Exception as e:
            self.logger.warning(f"Error creating metric descriptor: {e}")
    
    def time_this(self, name: str, labels: Dict[str, str] = None):
        """
        Decorator to time a function and send duration as metric.
        
        Args:
            name: Base name for the metric
            labels: Additional labels for this metric
            
        Example:
            @logger.time_this('data_processing', {'dataset': 'users'})
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
                self.send_metric(
                    f"{name}_duration", 
                    duration,
                    "seconds",
                    labels
                )
                
                # Log duration
                self.info(f"{name} completed in {duration:.2f}s", {"duration": duration})
                
                return result
            return wrapper
        return decorator