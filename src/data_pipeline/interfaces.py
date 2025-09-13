"""Abstract base classes for the ETL pipeline.

This module defines the abstract interfaces following the Interface Segregation
and Dependency Inversion principles from SOLID.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import pandas as pd
from ..data_pipeline.models import ProcessingResult, DataQualityReport


class DataExtractor(ABC):
    """Abstract base class for data extractors.
    
    Defines the interface for all data extraction operations,
    following the Interface Segregation Principle.
    """
    
    @abstractmethod
    def extract(self) -> pd.DataFrame:
        """Extract data from source.
        
        Returns:
            DataFrame containing extracted data
            
        Raises:
            ExtractionError: If extraction fails
        """
        pass
    
    @abstractmethod
    def validate_source(self) -> bool:
        """Validate that the data source is accessible and valid.
        
        Returns:
            True if source is valid, False otherwise
        """
        pass


class DataTransformer(ABC):
    """Abstract base class for data transformers.
    
    Defines the interface for all data transformation operations.
    """
    
    @abstractmethod
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """Transform the provided data.
        
        Args:
            data: Input DataFrame to transform
            
        Returns:
            Transformed DataFrame
            
        Raises:
            TransformationError: If transformation fails
        """
        pass
    
    @abstractmethod
    def validate_input(self, data: pd.DataFrame) -> bool:
        """Validate input data before transformation.
        
        Args:
            data: DataFrame to validate
            
        Returns:
            True if data is valid for transformation, False otherwise
        """
        pass


class DataLoader(ABC):
    """Abstract base class for data loaders.
    
    Defines the interface for all data loading operations.
    """
    
    @abstractmethod
    def load(self, data: pd.DataFrame, destination: str) -> ProcessingResult:
        """Load data to destination.
        
        Args:
            data: DataFrame to load
            destination: Target destination path
            
        Returns:
            ProcessingResult with operation details
            
        Raises:
            LoadingError: If loading fails
        """
        pass
    
    @abstractmethod
    def validate_destination(self, destination: str) -> bool:
        """Validate that the destination is accessible and valid.
        
        Args:
            destination: Target destination path
            
        Returns:
            True if destination is valid, False otherwise
        """
        pass


class DataValidator(ABC):
    """Abstract base class for data validators.
    
    Defines the interface for all data validation operations.
    """
    
    @abstractmethod
    def validate(self, data: pd.DataFrame) -> DataQualityReport:
        """Validate data quality and generate report.
        
        Args:
            data: DataFrame to validate
            
        Returns:
            DataQualityReport with validation results
        """
        pass
    
    @abstractmethod
    def clean_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Clean data based on validation rules.
        
        Args:
            data: DataFrame to clean
            
        Returns:
            Cleaned DataFrame
        """
        pass


class DataFilter(ABC):
    """Abstract base class for data filters.
    
    Defines the interface for filtering operations.
    """
    
    @abstractmethod
    def filter(self, data: pd.DataFrame, criteria: Dict[str, Any]) -> pd.DataFrame:
        """Filter data based on provided criteria.
        
        Args:
            data: DataFrame to filter
            criteria: Filtering criteria
            
        Returns:
            Filtered DataFrame
        """
        pass
    
    @abstractmethod
    def validate_criteria(self, criteria: Dict[str, Any]) -> bool:
        """Validate filtering criteria.
        
        Args:
            criteria: Criteria to validate
            
        Returns:
            True if criteria are valid, False otherwise
        """
        pass


class Logger(ABC):
    """Abstract base class for logging operations.
    
    Defines the interface for all logging operations.
    """
    
    @abstractmethod
    def log_info(self, message: str, **kwargs) -> None:
        """Log informational message."""
        pass
    
    @abstractmethod
    def log_warning(self, message: str, **kwargs) -> None:
        """Log warning message."""
        pass
    
    @abstractmethod
    def log_error(self, message: str, error: Optional[Exception] = None, **kwargs) -> None:
        """Log error message."""
        pass
    
    @abstractmethod
    def log_debug(self, message: str, **kwargs) -> None:
        """Log debug message."""
        pass
