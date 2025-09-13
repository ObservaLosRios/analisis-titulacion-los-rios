"""Data pipeline package initialization."""

from .extractors import ExcelExtractor
from .transformers import DataCleaner, RegionalFilter
from .validators import DataQualityValidator
from .loaders import CSVLoader
from .utils import ETLLogger, OperationLogger
from .models import TitulacionRecord, DataQualityReport, ProcessingResult
from .exceptions import (
    ETLError, ExtractionError, TransformationError, 
    LoadingError, ValidationError, ConfigurationError, DataQualityError
)

__all__ = [
    # Extractors
    "ExcelExtractor",
    
    # Transformers
    "DataCleaner",
    "RegionalFilter",
    
    # Validators
    "DataQualityValidator",
    
    # Loaders
    "CSVLoader",
    
    # Utils
    "ETLLogger",
    "OperationLogger",
    
    # Models
    "TitulacionRecord",
    "DataQualityReport", 
    "ProcessingResult",
    
    # Exceptions
    "ETLError",
    "ExtractionError",
    "TransformationError",
    "LoadingError",
    "ValidationError",
    "ConfigurationError",
    "DataQualityError"
]
