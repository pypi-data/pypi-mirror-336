import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cloudweave import Logger, log_event, LoggerType

# Example of using log_event function
if __name__ == "__main__":
    # Create loggers for different purposes
    error_logger = Logger(
        logger_type=LoggerType.AWS,
        namespace="myapp",
        instance_id="error-logger",
        region="us-east-1"
    )
    
    debug_logger = Logger(
        logger_type=LoggerType.LOCAL,
        namespace="myapp",
        instance_id="debug-logger",
        log_level="debug"
    )
    
    metrics_logger = Logger(
        logger_type=LoggerType.STORAGE,
        namespace="myapp",
        instance_id="metrics-logger",
        storage_type="s3",
        bucket="my-metrics-bucket"
    )
    
    # Global options
    global_opt = {
        'verbose': True,
        'add_context': True
    }
    
    # Standard logging
    log_event("Application started", opt=global_opt)
    
    # Log with specific logger
    log_event("Critical error occurred", level="critical", logger_id="error-logger", opt=global_opt)
    
    # Verbose logging (only logged when verbose=True)
    log_event("Processing item 1 of 1000", opt={**global_opt, 'is_verbose': True})
    
    # Debug logging with custom labels
    log_event(
        "Database query took 150ms",
        level="debug",
        logger_id="debug-logger",
        opt={
            **global_opt,
            'labels': {
                'database': 'postgres',
                'query_time_ms': 150,
                'query_type': 'SELECT'
            }
        }
    )
    
    # Error logging with extra data
    log_event(
        "API request failed",
        level="error",
        logger_id="error-logger",
        opt=global_opt,
        extra={
            'labels': {
                'status_code': 500,
                'endpoint': '/api/users',
                'method': 'GET'
            }
        }
    )
    
    # Using custom context in labels instead of in message
    log_event(
        "Metric recorded",
        logger_id="metrics-logger",
        opt={
            **global_opt,
            'context_in_message': False
        },
        extra={
            'labels': {
                'metric_name': 'api_requests',
                'metric_value': 42
            }
        }
    )