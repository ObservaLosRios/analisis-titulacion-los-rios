"""Logging utility implementation.

This module implements structured logging using loguru,
following Clean Code principles for comprehensive logging.
"""

import sys
from pathlib import Path
from typing import Optional, Dict, Any
from loguru import logger
from datetime import datetime

from ..interfaces import Logger as LoggerInterface
from ...config import get_path_config, get_settings


class ETLLogger(LoggerInterface):
    """Structured logger for ETL pipeline operations.
    
    Implements comprehensive logging with file rotation, formatting,
    and multiple log levels. Follows Clean Code principles for
    clear and useful logging.
    """
    
    def __init__(self, logger_name: str = "ETL_Pipeline"):
        """Initialize ETL logger.
        
        Args:
            logger_name: Name identifier for this logger instance
        """
        self._logger_name = logger_name
        self._settings = get_settings()
        self._path_config = get_path_config()
        
        # Remove default handler and configure custom handlers
        logger.remove()
        self._configure_logging()
        
        # Add context
        self._logger = logger.bind(pipeline=logger_name)
    
    def _configure_logging(self) -> None:
        """Configure logging handlers and formatters."""
        
        # Console handler with color formatting
        console_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{extra[pipeline]}</cyan> | "
            "<level>{message}</level>"
        )
        
        logger.add(
            sys.stdout,
            format=console_format,
            level=self._settings.log_level,
            colorize=True,
            enqueue=True
        )
        
        # File handler with detailed formatting
        log_file_path = self._path_config.log_path / f"etl_pipeline_{datetime.now().strftime('%Y%m%d')}.log"
        
        file_format = (
            "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
            "{level: <8} | "
            "{extra[pipeline]: <15} | "
            "{name}:{function}:{line} | "
            "{message}"
        )
        
        logger.add(
            log_file_path,
            format=file_format,
            level="DEBUG",
            rotation="10 MB",
            retention="30 days",
            compression="zip",
            enqueue=True
        )
        
        # Error file handler
        error_file_path = self._path_config.log_path / f"etl_errors_{datetime.now().strftime('%Y%m%d')}.log"
        
        logger.add(
            error_file_path,
            format=file_format,
            level="ERROR",
            rotation="5 MB",
            retention="90 days",
            compression="zip",
            enqueue=True
        )
    
    def log_info(self, message: str, **kwargs) -> None:
        """Log informational message.
        
        Args:
            message: Info message to log
            **kwargs: Additional context data
        """
        self._logger.bind(**kwargs).info(message)
    
    def log_warning(self, message: str, **kwargs) -> None:
        """Log warning message.
        
        Args:
            message: Warning message to log
            **kwargs: Additional context data
        """
        self._logger.bind(**kwargs).warning(message)
    
    def log_error(self, message: str, error: Optional[Exception] = None, **kwargs) -> None:
        """Log error message.
        
        Args:
            message: Error message to log
            error: Optional exception object
            **kwargs: Additional context data
        """
        if error:
            self._logger.bind(**kwargs).error(f"{message} | Exception: {str(error)}")
            if hasattr(error, '__traceback__'):
                self._logger.bind(**kwargs).error(f"Traceback: {error.__traceback__}")
        else:
            self._logger.bind(**kwargs).error(message)
    
    def log_debug(self, message: str, **kwargs) -> None:
        """Log debug message.
        
        Args:
            message: Debug message to log
            **kwargs: Additional context data
        """
        self._logger.bind(**kwargs).debug(message)
    
    def log_operation_start(self, operation: str, **kwargs) -> None:
        """Log the start of an operation.
        
        Args:
            operation: Name of the operation starting
            **kwargs: Additional context data
        """
        self.log_info(f"Starting operation: {operation}", operation=operation, **kwargs)
    
    def log_operation_end(self, operation: str, execution_time: float, 
                         success: bool = True, **kwargs) -> None:
        """Log the end of an operation.
        
        Args:
            operation: Name of the operation ending
            execution_time: Time taken to execute operation
            success: Whether operation was successful
            **kwargs: Additional context data
        """
        status = "SUCCESS" if success else "FAILED"
        message = f"Operation {operation} completed: {status} in {execution_time:.2f}s"
        
        if success:
            self.log_info(message, operation=operation, execution_time=execution_time, **kwargs)
        else:
            self.log_error(message, operation=operation, execution_time=execution_time, **kwargs)
    
    def log_data_stats(self, operation: str, records_before: int, 
                       records_after: int, **kwargs) -> None:
        """Log data processing statistics.
        
        Args:
            operation: Name of the data operation
            records_before: Number of records before operation
            records_after: Number of records after operation
            **kwargs: Additional context data
        """
        records_changed = records_before - records_after
        change_percentage = (records_changed / records_before * 100) if records_before > 0 else 0
        
        message = (f"Data operation {operation}: "
                  f"{records_before:,} → {records_after:,} records "
                  f"({records_changed:+,} records, {change_percentage:+.1f}%)")
        
        self.log_info(
            message,
            operation=operation,
            records_before=records_before,
            records_after=records_after,
            records_changed=records_changed,
            change_percentage=change_percentage,
            **kwargs
        )
    
    def log_quality_metrics(self, quality_score: float, total_records: int,
                           valid_records: int, **kwargs) -> None:
        """Log data quality metrics.
        
        Args:
            quality_score: Data quality score (0-100)
            total_records: Total number of records
            valid_records: Number of valid records
            **kwargs: Additional context data
        """
        message = (f"Data Quality Assessment: "
                  f"Score={quality_score:.1f}%, "
                  f"Valid={valid_records:,}/{total_records:,} records")
        
        if quality_score >= 90:
            self.log_info(message, quality_score=quality_score, **kwargs)
        elif quality_score >= 70:
            self.log_warning(message, quality_score=quality_score, **kwargs)
        else:
            self.log_error(message, quality_score=quality_score, **kwargs)
    
    def log_file_operation(self, operation: str, file_path: str, 
                          file_size: int = None, **kwargs) -> None:
        """Log file operations.
        
        Args:
            operation: Type of file operation (read, write, etc.)
            file_path: Path to the file
            file_size: Optional file size in bytes
            **kwargs: Additional context data
        """
        if file_size:
            size_mb = file_size / (1024 * 1024)
            message = f"File {operation}: {file_path} ({size_mb:.2f} MB)"
        else:
            message = f"File {operation}: {file_path}"
        
        self.log_info(
            message,
            operation=operation,
            file_path=file_path,
            file_size=file_size,
            **kwargs
        )
    
    def log_performance_metrics(self, operation: str, metrics: Dict[str, Any]) -> None:
        """Log performance metrics.
        
        Args:
            operation: Name of the operation
            metrics: Dictionary of performance metrics
        """
        message = f"Performance metrics for {operation}: {metrics}"
        self.log_info(message, operation=operation, **metrics)
    
    def create_operation_logger(self, operation_name: str) -> 'OperationLogger':
        """Create a logger for a specific operation.
        
        Args:
            operation_name: Name of the operation
            
        Returns:
            OperationLogger instance
        """
        return OperationLogger(self, operation_name)
    
    @property
    def logger_name(self) -> str:
        """Get the logger name."""
        return self._logger_name


class OperationLogger:
    """Context manager for logging specific operations.
    
    Provides automatic start/end logging with timing and error handling.
    """
    
    def __init__(self, etl_logger: ETLLogger, operation_name: str):
        """Initialize operation logger.
        
        Args:
            etl_logger: Parent ETL logger instance
            operation_name: Name of the operation
        """
        self._etl_logger = etl_logger
        self._operation_name = operation_name
        self._start_time = None
        self._success = True
        self._context = {}
    
    def __enter__(self) -> 'OperationLogger':
        """Enter context manager."""
        import time
        self._start_time = time.time()
        self._etl_logger.log_operation_start(self._operation_name, **self._context)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit context manager."""
        import time
        execution_time = time.time() - self._start_time
        
        # Determine if operation was successful
        self._success = exc_type is None
        
        if not self._success:
            self._etl_logger.log_error(
                f"Operation {self._operation_name} failed",
                error=exc_val,
                **self._context
            )
        
        self._etl_logger.log_operation_end(
            self._operation_name,
            execution_time,
            self._success,
            **self._context
        )
    
    def add_context(self, **kwargs) -> 'OperationLogger':
        """Add context data to operation logging.
        
        Args:
            **kwargs: Context data to add
            
        Returns:
            Self for method chaining
        """
        self._context.update(kwargs)
        return self
    
    def log_info(self, message: str, **kwargs) -> None:
        """Log info message within operation context."""
        context = {**self._context, **kwargs}
        self._etl_logger.log_info(f"[{self._operation_name}] {message}", **context)
    
    def log_warning(self, message: str, **kwargs) -> None:
        """Log warning message within operation context."""
        context = {**self._context, **kwargs}
        self._etl_logger.log_warning(f"[{self._operation_name}] {message}", **context)
    
    def log_error(self, message: str, error: Optional[Exception] = None, **kwargs) -> None:
        """Log error message within operation context."""
        context = {**self._context, **kwargs}
        self._etl_logger.log_error(f"[{self._operation_name}] {message}", error, **context)
