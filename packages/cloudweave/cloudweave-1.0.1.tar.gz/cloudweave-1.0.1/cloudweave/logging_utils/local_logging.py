import logging
import sys
import time
import json
import functools
from typing import Dict, Any, Optional
import requests
from datetime import datetime

class LokiLogger:
    def __init__(self, name: str, config: Dict[str, Any] = None):
        """
        Simple Logger with support for local stdout and Grafana Loki.
        
        Args:
            name: Logger name
            config: Configuration with keys:
                - local_only: Only log to stdout, no Loki (default: True)
                - loki_url: Loki API URL, required if local_only is False
                - labels: Dict of Loki labels (default: {})
                - batch_size: Number of logs to batch before sending (default: 10)
                - batch_interval: Max seconds between sends (default: 5)
        """
        self.name = name
        self.config = config or {}
        self.config.setdefault('local_only', True)
        self.config.setdefault('labels', {})
        self.config.setdefault('batch_size', 10)
        self.config.setdefault('batch_interval', 5)
        
        # Make sure service name is in labels
        if 'service' not in self.config['labels']:
            self.config['labels']['service'] = name
        
        # Set up standard Python logger for stdout
        self.logger = logging.getLogger(name)
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
        
        # Initialize Loki buffers if not in local-only mode
        if not self.config['local_only']:
            if 'loki_url' not in self.config:
                raise ValueError("Loki URL is required when local_only is False")
            
            # Initialize log buffer for batching
            self._log_buffer = []
            self._last_flush_time = time.time()
    
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
        
        # Extract labels if they exist in extra
        extra_labels = None
        if extra:
            if 'labels' in extra:
                extra_labels = extra['labels']
            
            # Format message with extra data for stdout
            formatted_message = f"{message} {json.dumps(extra)}"
        else:
            formatted_message = message
        
        # Log to stdout
        self.logger.log(log_level, formatted_message)
        
        # Send to Loki
        self._send_to_loki(level.upper(), message, extra_labels)
    
    def info(self, message: str, extra: Dict[str, Any] = None):
        """Log info message to stdout and Loki."""
        self.log('info', message, extra)
    
    def error(self, message: str, extra: Dict[str, Any] = None):
        """Log error message to stdout and Loki."""
        self.log('error', message, extra)
    
    def debug(self, message: str, extra: Dict[str, Any] = None):
        """Log debug message to stdout and Loki."""
        self.log('debug', message, extra)
    
    def warning(self, message: str, extra: Dict[str, Any] = None):
        """Log warning message to stdout and Loki."""
        self.log('warning', message, extra)
    
    def critical(self, message: str, extra: Dict[str, Any] = None):
        """Log critical message to stdout and Loki."""
        self.log('critical', message, extra)
    
    def _send_to_loki(self, level: str, message: str, extra_labels: Dict[str, str] = None):
        """Add log to Loki buffer and flush if needed."""
        if self.config['local_only']:
            return
            
        # Create a log entry
        timestamp_ns = int(time.time() * 1e9)
        
        # Combine configured labels with extra labels
        labels = self.config['labels'].copy()
        labels['level'] = level
        if extra_labels:
            labels.update(extra_labels)
        
        # Format labels for Loki
        labels_str = ','.join([f'{k}="{v}"' for k, v in labels.items()])
        
        # Format message for Loki
        log_message = f"{level} - {message}"
        
        # Add entry to buffer
        self._log_buffer.append({
            'stream': {
                'labels': labels_str
            },
            'values': [
                [str(timestamp_ns), log_message]
            ]
        })
        
        # Check if we should flush the buffer
        current_time = time.time()
        if (len(self._log_buffer) >= self.config['batch_size'] or
                current_time - self._last_flush_time >= self.config['batch_interval']):
            self._flush_logs()
    
    def _flush_logs(self):
        """Flush buffered logs to Loki."""
        if not self._log_buffer:
            return
            
        try:
            # Prepare the Loki payload
            payload = {
                'streams': self._log_buffer
            }
            
            # Send to Loki
            headers = {
                'Content-Type': 'application/json'
            }
            
            response = requests.post(
                self.config['loki_url'],
                headers=headers,
                data=json.dumps(payload),
                timeout=5
            )
            
            if response.status_code >= 400:
                self.logger.warning(f"Failed to send logs to Loki: {response.status_code} - {response.text}")
            
            # Clear buffer and update flush time
            self._log_buffer = []
            self._last_flush_time = time.time()
            
        except Exception as e:
            self.logger.warning(f"Error sending logs to Loki: {e}")
    
    def send_metric(self, name: str, value: float, labels: Dict[str, str] = None):
        """
        Send a metric as a special log entry to Loki.
        
        Since Loki isn't primarily a metrics system, this formats metrics
        in a way that can be queried and graphed in Grafana.
        
        Args:
            name: Metric name
            value: Metric value
            labels: Additional labels for the metric
        """
        # Prepare labels for the metric
        combined_labels = self.config['labels'].copy()
        combined_labels['metric_name'] = name
        combined_labels['metric_value'] = str(value)
        
        if labels:
            combined_labels.update(labels)
        
        # Format as a metric log line that can be extracted with LogQL
        metric_message = f"METRIC {name}={value}"
        
        # Send to Loki using the log method
        self.log('info', metric_message, {'labels': combined_labels})
    
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
                
                # Create metric labels
                metric_labels = labels or {}
                metric_labels['function'] = func.__name__
                
                # Send metric
                self.send_metric(
                    f"{name}_duration", 
                    duration,
                    metric_labels
                )
                
                # Log duration
                self.info(f"{name} completed in {duration:.2f}s", {
                    'labels': {
                        'duration': f"{duration:.2f}",
                        'function': func.__name__
                    }
                })
                
                return result
            return wrapper
        return decorator
    
    def __del__(self):
        """Ensure logs are flushed when the logger is destroyed."""
        if hasattr(self, '_log_buffer') and self._log_buffer:
            self._flush_logs()