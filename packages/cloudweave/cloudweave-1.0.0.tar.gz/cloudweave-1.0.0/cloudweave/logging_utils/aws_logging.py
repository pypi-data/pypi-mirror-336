import logging
import sys, os
import time
from typing import Dict, Any

# Import AWSManager from cloud_session_utils
from cloudweave.cloud_session_utils import AWSManager

from mypy_boto3_cloudwatch.client import CloudWatchClient
from mypy_boto3_logs.client import CloudWatchLogsClient

class AWSLogger:
    def __init__(self, name: str, config: Dict[str, Any] = None):
        """
        Simple AWS Logger for CloudWatch metrics and logs.
        
        Args:
            name: Logger name
            config: Configuration with keys:
                - namespace: CloudWatch namespace (default: 'Application')
                - dimensions: Dict of CloudWatch dimensions (default: {})
                - region: AWS region (default: 'us-east-1')
                - local_only: Skip CloudWatch integration if True (default: False)
        """
        self.name = name
        self.config = config or {}
        self.config.setdefault('namespace', 'Application')
        self.config.setdefault('dimensions', {})
        self.config.setdefault('region', 'us-east-1')
        self.config.setdefault('local_only', False)
        
        # Set up logger
        self.logger = logging.getLogger(name)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
            
        
        # Initialize AWS clients
        aws = AWSManager.instance(self.config)
        self._cloudwatch: CloudWatchClient = aws.get_client('cloudwatch')
        self._logs: CloudWatchLogsClient = aws.get_client('logs')
    
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
            formatted_message = f"{message} {extra}"
        else:
            formatted_message = message
        
        # Log locally
        self.logger.log(log_level, formatted_message)
        
        # Send to CloudWatch
        self._send_to_cloudwatch(level.upper(), message, extra)
    
    def info(self, message: str, extra: Dict[str, Any] = None):
        """Log info message and send to CloudWatch if enabled."""
        self.log('info', message, extra)
    
    def error(self, message: str, extra: Dict[str, Any] = None):
        """Log error message and send to CloudWatch if enabled."""
        self.log('error', message, extra)
    
    def debug(self, message: str, extra: Dict[str, Any] = None):
        """Log debug message and send to CloudWatch if enabled."""
        self.log('debug', message, extra)
    
    def warning(self, message: str, extra: Dict[str, Any] = None):
        """Log warning message and send to CloudWatch if enabled."""
        self.log('warning', message, extra)
    
    def critical(self, message: str, extra: Dict[str, Any] = None):
        """Log critical message and send to CloudWatch if enabled."""
        self.log('critical', message, extra)
    
    def _send_to_cloudwatch(self, level: str, message: str, extra: Dict[str, Any] = None):
        """Send log to CloudWatch Logs."""
        if self.config.get('local_only', False):
            return
            
        try:
            log_group = f"/aws/application/{self.config['namespace']}"
            log_stream = time.strftime('%Y/%m/%d')
            
            # Ensure log group exists
            try:
                self._logs.create_log_group(logGroupName=log_group)
            except:
                pass
                
            # Ensure log stream exists
            try:
                self._logs.create_log_stream(logGroupName=log_group, logStreamName=log_stream)
            except:
                pass
            
            # Prepare log message with extra data
            log_data = {
                'level': level,
                'message': message,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Add extra data if provided
            if extra:
                log_data['extra'] = extra
            
            # Convert to string for CloudWatch
            import json
            log_message = json.dumps(log_data)
            
            # Get sequence token if needed
            try:
                response = self._logs.describe_log_streams(
                    logGroupName=log_group,
                    logStreamNamePrefix=log_stream
                )
                
                sequence_token = None
                for stream in response.get('logStreams', []):
                    if stream['logStreamName'] == log_stream and 'uploadSequenceToken' in stream:
                        sequence_token = stream['uploadSequenceToken']
                        break
                
                # Put log event
                event = {
                    'timestamp': int(time.time() * 1000),
                    'message': log_message
                }
                
                if sequence_token:
                    self._logs.put_log_events(
                        logGroupName=log_group,
                        logStreamName=log_stream,
                        logEvents=[event],
                        sequenceToken=sequence_token
                    )
                else:
                    self._logs.put_log_events(
                        logGroupName=log_group,
                        logStreamName=log_stream,
                        logEvents=[event]
                    )
            except Exception as e:
                self.logger.warning(f"Error sending log to CloudWatch: {e}")
        except Exception as e:
            self.logger.warning(f"Error in CloudWatch logging: {e}")
    
    def send_metric(self, name: str, value: float, unit: str = 'Count', dimensions: Dict[str, str] = None):
        """
        Send a metric to CloudWatch.
        
        Args:
            name: Metric name
            value: Metric value
            unit: Metric unit (default: Count)
            dimensions: Additional dimensions for this metric (combined with config dimensions)
        """
        if self.config.get('local_only', False):
            return
            
        try:
            # Start with configured dimensions
            all_dimensions = self.config['dimensions'].copy()
            
            # Add additional dimensions if provided
            if dimensions:
                all_dimensions.update(dimensions)
            
            # Convert to CloudWatch dimensions format
            dimension_list = [{'Name': k, 'Value': v} for k, v in all_dimensions.items()]
            
            # Send metric
            self._cloudwatch.put_metric_data(
                Namespace=self.config['namespace'],
                MetricData=[{
                    'MetricName': name,
                    'Dimensions': dimension_list,
                    'Value': value,
                    'Unit': unit,
                    'Timestamp': time.time()
                }]
            )
            
            # Log the metric if desired
            self.debug(f"Metric sent: {name}={value} {unit}", {"dimensions": all_dimensions})
        except Exception as e:
            self.logger.warning(f"Error sending metric to CloudWatch: {e}")
    
    def time_this(self, name: str, dimensions: Dict[str, str] = None):
        """
        Decorator to time a function and send duration as metric.
        
        Args:
            name: Base name for the metric
            dimensions: Additional dimensions for this metric
            
        Example:
            @logger.time_this('data_processing', {'dataset': 'users'})
            def process_data():
                # Processing code
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                
                # Send metric
                self.send_metric(
                    f"{name}_duration", 
                    duration,
                    "Seconds",
                    dimensions
                )
                
                # Log duration
                self.info(f"{name} completed in {duration:.2f}s", {"duration": duration})
                
                return result
            return wrapper
        return decorator