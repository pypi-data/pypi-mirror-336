from typing import Dict, Any, Optional, List, Union
import os

from cloudweave.logging_manager import Logger, LoggerType

def log_event(message: str, level: str = 'info', opt: Dict[str, Any] = None, **kwargs) -> None:
    """
    Universal logging function that can use different loggers and handle verbose logs.
    
    Args:
        message: The message to log
        level: Log level (debug, info, warning, error, critical)
        opt: Options dictionary which may contain:
            - verbose: Whether verbose logging is enabled
            - is_verbose: Whether this specific log is verbose
            - logger_id: ID of logger to use (overrides logger_id parameter)
            - labels: Additional labels to attach to log entry
        extra: Additional data to include with the log
        logger_id: ID of logger instance to use (default: first available)
        **kwargs: Additional keyword arguments, including:
            - is_verbose: Whether this specific log is verbose (alternative to opt['is_verbose'])
            - logger_id: ID of logger to use (overrides logger_id parameter)
            - labels: Additional labels to attach to log entry
            
    
    Returns:
        None
    """
    # Initialize options
    opt = opt or {}
    
    # Skip verbose logs if verbose mode is disabled
    is_verbose_log = kwargs.get('is_verbose', opt.get('is_verbose', False))
    verbose_enabled = opt.get('verbose', False)
    
    if is_verbose_log and not verbose_enabled:
        return
    
    # Get logger instance
    use_logger_id = kwargs.get('logger_id', opt.get('logger_id', None))
    logger = None
    
    if use_logger_id:
        # Get specific logger by ID
        logger = Logger.get_instance(use_logger_id)
    else:
        # Get first available logger or create a default one
        instances = Logger.list_instances()
        if instances:
            logger = Logger.get_instance(instances[0])
        else:
            # Create a default local logger
            logger = Logger(
                logger_type=LoggerType.LOCAL,
                namespace="default",
                instance_id="default-logger"
            )
    
    # Prepare extra data
    log_extra = kwargs.get('extra', {})
    
    # Add labels from options if present
    if 'labels' in opt:
        if 'labels' not in log_extra:
            log_extra['labels'] = {}
        log_extra['labels'].update(opt.get('labels', {}))
    
    # Add context information if available
    if opt.get('add_context', True):
        import inspect
        frame = inspect.currentframe().f_back
        file_name = frame.f_code.co_filename
        function_name = frame.f_code.co_name
        line_number = frame.f_lineno
        
        context = {
            'file': os.path.basename(file_name),
            'function': function_name,
            'line': line_number
        }
        
        # Add context to the message or to labels
        if opt.get('context_in_message', True):
            message = f"{context['file']} - {context['function']}:{context['line']} - {message}"
        else:
            if 'labels' not in log_extra:
                log_extra['labels'] = {}
            log_extra['labels'].update(context)
    
    # Log with appropriate level
    if level.lower() == 'debug':
        logger.debug(message, log_extra)
    elif level.lower() == 'warning':
        logger.warning(message, log_extra)
    elif level.lower() == 'error':
        logger.error(message, log_extra)
    elif level.lower() == 'critical':
        logger.critical(message, log_extra)
    else:
        # Default to info level
        logger.info(message, log_extra)


# Example of using log_event function
if __name__ == "__main__":
    # Create loggers for different purposes
    # Example global default logger
    default_logger = Logger(
        logger_type=LoggerType.LOCAL,
        namespace="myapp",
        instance_id="default-logger",
        log_file="logs/application.log"
    )
    
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