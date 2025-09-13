"""Custom exceptions for the ETL pipeline.

This module defines specific exceptions for different types of errors
that can occur during the ETL process, following Clean Code principles
for proper error handling.
"""


class ETLError(Exception):
    """Base exception for all ETL pipeline errors.
    
    Provides a common base for all pipeline-specific exceptions,
    allowing for more granular error handling.
    """
    
    def __init__(self, message: str, original_error: Exception = None):
        """Initialize ETL error.
        
        Args:
            message: Human-readable error message
            original_error: Original exception that caused this error
        """
        super().__init__(message)
        self.message = message
        self.original_error = original_error
    
    def __str__(self) -> str:
        """Return string representation of error."""
        if self.original_error:
            return f"{self.message}. Original error: {str(self.original_error)}"
        return self.message


class ExtractionError(ETLError):
    """Exception raised when data extraction fails.
    
    Specific to data extraction operations, providing clear context
    about extraction failures.
    """
    
    def __init__(self, message: str, source_path: str = None, original_error: Exception = None):
        """Initialize extraction error.
        
        Args:
            message: Error description
            source_path: Path to the data source that failed
            original_error: Original exception
        """
        super().__init__(message, original_error)
        self.source_path = source_path


class TransformationError(ETLError):
    """Exception raised when data transformation fails.
    
    Specific to data transformation operations.
    """
    
    def __init__(self, message: str, transformation_step: str = None, original_error: Exception = None):
        """Initialize transformation error.
        
        Args:
            message: Error description
            transformation_step: Name of the transformation step that failed
            original_error: Original exception
        """
        super().__init__(message, original_error)
        self.transformation_step = transformation_step


class LoadingError(ETLError):
    """Exception raised when data loading fails.
    
    Specific to data loading operations.
    """
    
    def __init__(self, message: str, destination_path: str = None, original_error: Exception = None):
        """Initialize loading error.
        
        Args:
            message: Error description
            destination_path: Path to the destination that failed
            original_error: Original exception
        """
        super().__init__(message, original_error)
        self.destination_path = destination_path


class ValidationError(ETLError):
    """Exception raised when data validation fails.
    
    Specific to data validation operations.
    """
    
    def __init__(self, message: str, validation_rule: str = None, original_error: Exception = None):
        """Initialize validation error.
        
        Args:
            message: Error description
            validation_rule: Name of the validation rule that failed
            original_error: Original exception
        """
        super().__init__(message, original_error)
        self.validation_rule = validation_rule


class ConfigurationError(ETLError):
    """Exception raised when configuration is invalid or missing.
    
    Specific to configuration-related errors.
    """
    
    def __init__(self, message: str, config_key: str = None, original_error: Exception = None):
        """Initialize configuration error.
        
        Args:
            message: Error description
            config_key: Configuration key that caused the error
            original_error: Original exception
        """
        super().__init__(message, original_error)
        self.config_key = config_key


class DataQualityError(ETLError):
    """Exception raised when data quality is below acceptable threshold.
    
    Specific to data quality issues that prevent processing.
    """
    
    def __init__(self, message: str, quality_score: float = None, original_error: Exception = None):
        """Initialize data quality error.
        
        Args:
            message: Error description
            quality_score: Data quality score that triggered the error
            original_error: Original exception
        """
        super().__init__(message, original_error)
        self.quality_score = quality_score
