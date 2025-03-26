"""
Logging utilities for Python applications.
"""

import os
import sys
import logging
import logging.handlers
import json
import datetime
from typing import Dict, Any, Optional, List, Union, TextIO


class JsonFormatter(logging.Formatter):
    """
    Formatter for JSON-structured log messages.
    """
    
    def __init__(self, include_timestamp: bool = True, include_level: bool = True,
                include_name: bool = True, extra_fields: Optional[Dict[str, Any]] = None):
        """
        Initialize the JSON formatter.
        
        Args:
            include_timestamp (bool): Whether to include a timestamp
            include_level (bool): Whether to include the log level
            include_name (bool): Whether to include the logger name
            extra_fields (dict, optional): Extra fields to include in every log message
        """
        super().__init__()
        self.include_timestamp = include_timestamp
        self.include_level = include_level
        self.include_name = include_name
        self.extra_fields = extra_fields or {}
    
    def format(self, record: logging.LogRecord) -> str:
        """Format the log record as a JSON string."""
        log_data = {}
        
        # Add standard fields
        if self.include_timestamp:
            log_data["timestamp"] = datetime.datetime.fromtimestamp(
                record.created
            ).isoformat()
        
        if self.include_level:
            log_data["level"] = record.levelname
        
        if self.include_name:
            log_data["logger"] = record.name
        
        # Add the message
        log_data["message"] = record.getMessage()
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields from the formatter
        log_data.update(self.extra_fields)
        
        # Add extra fields from the record
        for key, value in record.__dict__.items():
            if key not in ["args", "asctime", "created", "exc_info", "exc_text", 
                          "filename", "funcName", "id", "levelname", "levelno",
                          "lineno", "module", "msecs", "message", "msg", 
                          "name", "pathname", "process", "processName", 
                          "relativeCreated", "stack_info", "thread", "threadName"]:
                log_data[key] = value
        
        return json.dumps(log_data)


def setup_logger(name: str = None, 
                level: int = logging.INFO,
                log_file: Optional[str] = None,
                console: bool = True,
                json_format: bool = False,
                rotate: bool = True,
                max_bytes: int = 10485760,  # 10 MB
                backup_count: int = 5) -> logging.Logger:
    """
    Set up a logger with file and/or console handlers.
    
    Args:
        name (str, optional): Logger name (defaults to root logger)
        level (int): Logging level
        log_file (str, optional): Path to log file
        console (bool): Whether to log to console
        json_format (bool): Whether to use JSON formatting
        rotate (bool): Whether to use rotating file handler
        max_bytes (int): Maximum file size before rotation
        backup_count (int): Number of backup files to keep
        
    Returns:
        logging.Logger: Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create formatters
    if json_format:
        formatter = JsonFormatter()
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    
    # Add console handler if requested
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # Add file handler if requested
    if log_file:
        # Create directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
        
        if rotate:
            file_handler = logging.handlers.RotatingFileHandler(
                log_file, maxBytes=max_bytes, backupCount=backup_count
            )
        else:
            file_handler = logging.FileHandler(log_file)
        
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


class LogCapture:
    """
    Context manager for capturing logs.
    
    Example:
        >>> with LogCapture() as logs:
        >>>     logging.info("Test message")
        >>> print(logs.messages)  # ["Test message"]
    """
    
    def __init__(self, logger_name: Optional[str] = None, level: int = logging.INFO):
        """
        Initialize the log capture.
        
        Args:
            logger_name (str, optional): Name of the logger to capture
            level (int): Minimum logging level to capture
        """
        self.logger_name = logger_name
        self.level = level
        self.handler = None
        self.messages = []
    
    def __enter__(self):
        """Set up the log capture."""
        logger = logging.getLogger(self.logger_name)
        
        class ListHandler(logging.Handler):
            def __init__(self, messages_list):
                super().__init__()
                self.messages_list = messages_list
            
            def emit(self, record):
                self.messages_list.append(record.getMessage())
        
        self.handler = ListHandler(self.messages)
        self.handler.setLevel(self.level)
        logger.addHandler(self.handler)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up the log capture."""
        if self.handler:
            logging.getLogger(self.logger_name).removeHandler(self.handler)


def log_function_call(logger: Optional[logging.Logger] = None, 
                     level: int = logging.DEBUG):
    """
    Decorator to log function calls with arguments and return values.
    
    Args:
        logger (logging.Logger, optional): Logger to use
        level (int): Logging level
        
    Returns:
        Function decorator
        
    Example:
        >>> @log_function_call()
        >>> def add(a, b):
        >>>     return a + b
        >>> 
        >>> result = add(1, 2)  # Logs function call and result
    """
    def decorator(func):
        nonlocal logger
        
        # Get or create logger
        if logger is None:
            logger = logging.getLogger(func.__module__)
        
        def wrapper(*args, **kwargs):
            # Log function call
            args_str = ", ".join([repr(a) for a in args])
            kwargs_str = ", ".join([f"{k}={repr(v)}" for k, v in kwargs.items()])
            params = ", ".join(filter(None, [args_str, kwargs_str]))
            logger.log(level, f"Calling {func.__name__}({params})")
            
            try:
                # Call the function
                result = func(*args, **kwargs)
                
                # Log the result
                logger.log(level, f"{func.__name__} returned {repr(result)}")
                return result
            except Exception as e:
                # Log any exceptions
                logger.exception(f"{func.__name__} raised {type(e).__name__}: {str(e)}")
                raise
        
        return wrapper
    
    return decorator
