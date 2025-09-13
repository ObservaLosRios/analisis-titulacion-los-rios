"""Data cleaning transformer implementation.

This module implements data cleaning operations following Clean Code principles
and the Single Responsibility Principle.
"""

import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Any, Set
import re
import time

from ..interfaces import DataTransformer
from ..exceptions import TransformationError
from ..models import ProcessingResult
from ...config import get_settings


class DataCleaner(DataTransformer):
    """Data cleaning transformer.
    
    Implements comprehensive data cleaning operations including:
    - Missing value handling
    - Data type standardization
    - Text normalization
    - Duplicate removal
    - Outlier detection
    """
    
    def __init__(self):
        """Initialize data cleaner with default settings."""
        self._settings = get_settings()
        self._text_columns_pattern = r'.*(?:nombre|titulo|carrera|institucion|region|provincia|comuna|area|modalidad|sede).*'
        self._numeric_columns_pattern = r'.*(?:codigo|cantidad|ano|mes|edad).*'
    
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """Transform data by applying comprehensive cleaning operations.
        
        Args:
            data: Input DataFrame to clean
            
        Returns:
            Cleaned DataFrame
            
        Raises:
            TransformationError: If transformation fails
        """
        start_time = time.time()
        
        try:
            if not self.validate_input(data):
                raise TransformationError(
                    "Input validation failed for data cleaning",
                    transformation_step="input_validation"
                )
            
            # Create a copy to avoid modifying original data
            cleaned_data = data.copy()
            
            print(f"Starting data cleaning for {len(cleaned_data)} records...")
            
            # Apply cleaning steps
            cleaned_data = self._standardize_column_names(cleaned_data)
            cleaned_data = self._clean_text_columns(cleaned_data)
            cleaned_data = self._handle_missing_values(cleaned_data)
            cleaned_data = self._standardize_data_types(cleaned_data)
            cleaned_data = self._remove_duplicates(cleaned_data)
            cleaned_data = self._handle_outliers(cleaned_data)
            
            cleaning_time = time.time() - start_time
            records_processed = len(cleaned_data)
            
            print(f"Data cleaning completed: {records_processed} records processed "
                  f"in {cleaning_time:.2f} seconds")
            
            return cleaned_data
            
        except Exception as e:
            if isinstance(e, TransformationError):
                raise
            raise TransformationError(
                f"Unexpected error during data cleaning: {str(e)}",
                transformation_step="data_cleaning",
                original_error=e
            )
    
    def validate_input(self, data: pd.DataFrame) -> bool:
        """Validate input data before cleaning.
        
        Args:
            data: DataFrame to validate
            
        Returns:
            True if data is valid for cleaning, False otherwise
        """
        try:
            # Check if DataFrame is not None
            if data is None:
                print("Error: Input data is None")
                return False
            
            # Check if DataFrame is not empty
            if data.empty:
                print("Error: Input DataFrame is empty")
                return False
            
            # Check if DataFrame has columns
            if len(data.columns) == 0:
                print("Error: DataFrame has no columns")
                return False
            
            # Check if DataFrame has at least some data
            if len(data) == 0:
                print("Error: DataFrame has no rows")
                return False
            
            return True
            
        except Exception as e:
            print(f"Error validating input data: {str(e)}")
            return False
    
    def _standardize_column_names(self, data: pd.DataFrame) -> pd.DataFrame:
        """Standardize column names to snake_case and lowercase.
        
        Args:
            data: DataFrame with columns to standardize
            
        Returns:
            DataFrame with standardized column names
        """
        try:
            standardized_data = data.copy()
            
            # Convert to lowercase and replace spaces/special chars with underscores
            new_columns = []
            for col in standardized_data.columns:
                # Convert to string and lowercase
                new_col = str(col).lower()
                # Replace spaces and special characters with underscores
                new_col = re.sub(r'[^\w\s]', '_', new_col)
                new_col = re.sub(r'\s+', '_', new_col)
                # Remove multiple underscores
                new_col = re.sub(r'_+', '_', new_col)
                # Remove leading/trailing underscores
                new_col = new_col.strip('_')
                new_columns.append(new_col)
            
            standardized_data.columns = new_columns
            
            print(f"Standardized {len(new_columns)} column names")
            return standardized_data
            
        except Exception as e:
            raise TransformationError(
                f"Failed to standardize column names: {str(e)}",
                transformation_step="column_standardization",
                original_error=e
            )
    
    def _clean_text_columns(self, data: pd.DataFrame) -> pd.DataFrame:
        """Clean text columns by normalizing whitespace and format.
        
        Args:
            data: DataFrame with text columns to clean
            
        Returns:
            DataFrame with cleaned text columns
        """
        try:
            cleaned_data = data.copy()
            
            # Identify text columns
            text_columns = self._identify_text_columns(cleaned_data)
            
            for col in text_columns:
                if col in cleaned_data.columns:
                    # Convert to string and handle NaN
                    cleaned_data[col] = cleaned_data[col].astype(str)
                    
                    # Replace 'nan', 'None', 'null' strings with actual NaN
                    cleaned_data[col] = cleaned_data[col].replace(
                        ['nan', 'None', 'null', 'NULL', 'NaN'], np.nan
                    )
                    
                    # Clean valid text values
                    mask = cleaned_data[col].notna()
                    if mask.any():
                        # Strip whitespace
                        cleaned_data.loc[mask, col] = cleaned_data.loc[mask, col].str.strip()
                        
                        # Replace multiple spaces with single space
                        cleaned_data.loc[mask, col] = cleaned_data.loc[mask, col].str.replace(
                            r'\s+', ' ', regex=True
                        )
                        
                        # Convert to proper case for names and titles
                        if any(keyword in col.lower() for keyword in ['nombre', 'titulo', 'carrera']):
                            cleaned_data.loc[mask, col] = cleaned_data.loc[mask, col].str.title()
            
            print(f"Cleaned {len(text_columns)} text columns")
            return cleaned_data
            
        except Exception as e:
            raise TransformationError(
                f"Failed to clean text columns: {str(e)}",
                transformation_step="text_cleaning",
                original_error=e
            )
    
    def _handle_missing_values(self, data: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values using appropriate strategies.
        
        Args:
            data: DataFrame with missing values
            
        Returns:
            DataFrame with handled missing values
        """
        try:
            handled_data = data.copy()
            
            # Calculate missing value statistics
            missing_stats = handled_data.isnull().sum()
            total_missing = missing_stats.sum()
            
            if total_missing > 0:
                print(f"Handling {total_missing} missing values across {len(missing_stats[missing_stats > 0])} columns")
                
                for col in handled_data.columns:
                    missing_count = missing_stats[col]
                    if missing_count > 0:
                        missing_percentage = (missing_count / len(handled_data)) * 100
                        
                        # Strategy based on column type and missing percentage
                        if missing_percentage > 90:
                            # Drop columns with >90% missing
                            print(f"Dropping column '{col}' with {missing_percentage:.1f}% missing values")
                            handled_data.drop(columns=[col], inplace=True)
                        elif col in self._identify_numeric_columns(handled_data):
                            # Fill numeric columns with median or 0
                            if 'cantidad' in col.lower():
                                handled_data[col].fillna(0, inplace=True)
                            else:
                                handled_data[col].fillna(handled_data[col].median(), inplace=True)
                        else:
                            # Fill text columns with 'Unknown' or mode
                            if handled_data[col].dtype == 'object':
                                mode_value = handled_data[col].mode()
                                fill_value = mode_value[0] if len(mode_value) > 0 else 'Unknown'
                                handled_data[col].fillna(fill_value, inplace=True)
            
            return handled_data
            
        except Exception as e:
            raise TransformationError(
                f"Failed to handle missing values: {str(e)}",
                transformation_step="missing_values",
                original_error=e
            )
    
    def _standardize_data_types(self, data: pd.DataFrame) -> pd.DataFrame:
        """Standardize data types for consistent processing.
        
        Args:
            data: DataFrame with inconsistent data types
            
        Returns:
            DataFrame with standardized data types
        """
        try:
            standardized_data = data.copy()
            
            # Identify numeric columns
            numeric_columns = self._identify_numeric_columns(standardized_data)
            
            for col in numeric_columns:
                if col in standardized_data.columns:
                    try:
                        # Convert to numeric, handling errors
                        standardized_data[col] = pd.to_numeric(
                            standardized_data[col], 
                            errors='coerce'
                        )
                        
                        # Convert specific integer columns
                        if any(keyword in col.lower() for keyword in ['ano', 'mes', 'cantidad', 'codigo']):
                            standardized_data[col] = standardized_data[col].fillna(0).astype('Int64')
                        
                    except Exception as e:
                        print(f"Warning: Could not convert column '{col}' to numeric: {str(e)}")
            
            # Ensure text columns are strings
            text_columns = self._identify_text_columns(standardized_data)
            for col in text_columns:
                if col in standardized_data.columns:
                    standardized_data[col] = standardized_data[col].astype(str)
                    standardized_data[col] = standardized_data[col].replace('nan', np.nan)
            
            print(f"Standardized data types for {len(standardized_data.columns)} columns")
            return standardized_data
            
        except Exception as e:
            raise TransformationError(
                f"Failed to standardize data types: {str(e)}",
                transformation_step="data_type_standardization",
                original_error=e
            )
    
    def _remove_duplicates(self, data: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicate records.
        
        Args:
            data: DataFrame potentially containing duplicates
            
        Returns:
            DataFrame without duplicates
        """
        try:
            initial_count = len(data)
            deduplicated_data = data.drop_duplicates()
            final_count = len(deduplicated_data)
            
            duplicates_removed = initial_count - final_count
            if duplicates_removed > 0:
                print(f"Removed {duplicates_removed} duplicate records")
            
            return deduplicated_data
            
        except Exception as e:
            raise TransformationError(
                f"Failed to remove duplicates: {str(e)}",
                transformation_step="duplicate_removal",
                original_error=e
            )
    
    def _handle_outliers(self, data: pd.DataFrame) -> pd.DataFrame:
        """Handle outliers in numeric columns.
        
        Args:
            data: DataFrame potentially containing outliers
            
        Returns:
            DataFrame with handled outliers
        """
        try:
            handled_data = data.copy()
            numeric_columns = self._identify_numeric_columns(handled_data)
            
            for col in numeric_columns:
                if col in handled_data.columns and col not in ['codigo', 'ano']:
                    # Use IQR method for outlier detection
                    Q1 = handled_data[col].quantile(0.25)
                    Q3 = handled_data[col].quantile(0.75)
                    IQR = Q3 - Q1
                    
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    
                    # Count outliers
                    outliers = handled_data[
                        (handled_data[col] < lower_bound) | (handled_data[col] > upper_bound)
                    ]
                    
                    if len(outliers) > 0:
                        print(f"Found {len(outliers)} outliers in column '{col}'")
                        
                        # Cap outliers instead of removing
                        handled_data[col] = np.where(
                            handled_data[col] < lower_bound, lower_bound, handled_data[col]
                        )
                        handled_data[col] = np.where(
                            handled_data[col] > upper_bound, upper_bound, handled_data[col]
                        )
            
            return handled_data
            
        except Exception as e:
            raise TransformationError(
                f"Failed to handle outliers: {str(e)}",
                transformation_step="outlier_handling",
                original_error=e
            )
    
    def _identify_text_columns(self, data: pd.DataFrame) -> List[str]:
        """Identify text columns based on name patterns and data types.
        
        Args:
            data: DataFrame to analyze
            
        Returns:
            List of text column names
        """
        text_columns = []
        
        for col in data.columns:
            # Check by name pattern
            if re.search(self._text_columns_pattern, col.lower()):
                text_columns.append(col)
            # Check by data type
            elif data[col].dtype == 'object':
                text_columns.append(col)
        
        return text_columns
    
    def _identify_numeric_columns(self, data: pd.DataFrame) -> List[str]:
        """Identify numeric columns based on name patterns.
        
        Args:
            data: DataFrame to analyze
            
        Returns:
            List of numeric column names
        """
        numeric_columns = []
        
        for col in data.columns:
            # Check by name pattern
            if re.search(self._numeric_columns_pattern, col.lower()):
                numeric_columns.append(col)
            # Check by data type
            elif pd.api.types.is_numeric_dtype(data[col]):
                numeric_columns.append(col)
        
        return numeric_columns
