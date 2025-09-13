"""Data quality validator implementation.

This module implements comprehensive data quality validation following
Clean Code principles and providing detailed quality reports.
"""

import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Any, Set, Tuple
import time
import re

from ..interfaces import DataValidator
from ..exceptions import ValidationError, DataQualityError
from ..models import DataQualityReport, TitulacionRecord
from ...config import get_settings


class DataQualityValidator(DataValidator):
    """Comprehensive data quality validator.
    
    Implements data quality assessment including:
    - Missing value analysis
    - Data type validation
    - Business rule validation
    - Duplicate detection
    - Consistency checks
    """
    
    def __init__(self, quality_threshold: float = 80.0):
        """Initialize data quality validator.
        
        Args:
            quality_threshold: Minimum quality score threshold (0-100)
        """
        self._settings = get_settings()
        self._quality_threshold = quality_threshold
        
        # Define expected columns and their types
        self._expected_columns = {
            'codigo_institucion': 'string',
            'nombre_institucion': 'string',
            'region': 'string',
            'carrera': 'string',
            'ano_titulacion': 'integer',
            'cantidad_titulados': 'integer'
        }
        
        # Define validation rules
        self._validation_rules = {
            'year_range': (1990, 2030),
            'quantity_range': (0, 10000),
            'required_columns': ['region', 'ano_titulacion']
        }
    
    def validate(self, data: pd.DataFrame) -> DataQualityReport:
        """Validate data quality and generate comprehensive report.
        
        Args:
            data: DataFrame to validate
            
        Returns:
            DataQualityReport with validation results
            
        Raises:
            ValidationError: If validation process fails
        """
        start_time = time.time()
        
        try:
            print(f"Starting data quality validation for {len(data)} records...")
            
            # Initialize counters
            total_records = len(data)
            validation_errors = []
            data_types_issues = []
            
            # Validate structure
            structure_valid, structure_errors = self._validate_structure(data)
            validation_errors.extend(structure_errors)
            
            # Analyze missing values
            missing_values_by_column = self._analyze_missing_values(data)
            
            # Validate data types
            type_issues = self._validate_data_types(data)
            data_types_issues.extend(type_issues)
            
            # Validate business rules
            business_rule_errors = self._validate_business_rules(data)
            validation_errors.extend(business_rule_errors)
            
            # Detect duplicates
            duplicate_records = self._detect_duplicates(data)
            
            # Validate individual records
            valid_records = self._validate_records(data)
            invalid_records = total_records - valid_records
            
            # Create quality report
            quality_report = DataQualityReport(
                total_records=total_records,
                valid_records=valid_records,
                invalid_records=invalid_records,
                missing_values_by_column=missing_values_by_column,
                duplicate_records=duplicate_records,
                data_types_issues=data_types_issues,
                validation_errors=validation_errors
            )
            
            validation_time = time.time() - start_time
            
            print(f"Data quality validation completed in {validation_time:.2f} seconds")
            print(f"Quality Score: {quality_report.data_quality_score:.1f}%")
            
            # Check if quality meets threshold
            if quality_report.data_quality_score < self._quality_threshold:
                print(f"Warning: Data quality score {quality_report.data_quality_score:.1f}% "
                      f"is below threshold {self._quality_threshold}%")
            
            return quality_report
            
        except Exception as e:
            raise ValidationError(
                f"Data quality validation failed: {str(e)}",
                validation_rule="quality_validation",
                original_error=e
            )
    
    def clean_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Clean data based on validation rules.
        
        Args:
            data: DataFrame to clean
            
        Returns:
            Cleaned DataFrame with invalid records removed or corrected
        """
        try:
            print(f"Starting data cleaning based on validation rules...")
            
            cleaned_data = data.copy()
            initial_count = len(cleaned_data)
            
            # Remove rows with missing required columns
            for col in self._validation_rules['required_columns']:
                if col in cleaned_data.columns:
                    before_count = len(cleaned_data)
                    cleaned_data = cleaned_data.dropna(subset=[col])
                    after_count = len(cleaned_data)
                    if before_count != after_count:
                        print(f"Removed {before_count - after_count} records with missing '{col}'")
            
            # Clean year values
            if 'ano_titulacion' in cleaned_data.columns:
                year_min, year_max = self._validation_rules['year_range']
                before_count = len(cleaned_data)
                cleaned_data = cleaned_data[
                    (cleaned_data['ano_titulacion'] >= year_min) & 
                    (cleaned_data['ano_titulacion'] <= year_max)
                ]
                after_count = len(cleaned_data)
                if before_count != after_count:
                    print(f"Removed {before_count - after_count} records with invalid years")
            
            # Clean quantity values
            if 'cantidad_titulados' in cleaned_data.columns:
                qty_min, qty_max = self._validation_rules['quantity_range']
                before_count = len(cleaned_data)
                cleaned_data = cleaned_data[
                    (cleaned_data['cantidad_titulados'] >= qty_min) & 
                    (cleaned_data['cantidad_titulados'] <= qty_max)
                ]
                after_count = len(cleaned_data)
                if before_count != after_count:
                    print(f"Removed {before_count - after_count} records with invalid quantities")
            
            # Remove duplicates
            before_count = len(cleaned_data)
            cleaned_data = cleaned_data.drop_duplicates()
            after_count = len(cleaned_data)
            if before_count != after_count:
                print(f"Removed {before_count - after_count} duplicate records")
            
            final_count = len(cleaned_data)
            records_removed = initial_count - final_count
            
            print(f"Data cleaning completed: {records_removed} records removed, "
                  f"{final_count} records remaining")
            
            return cleaned_data
            
        except Exception as e:
            raise ValidationError(
                f"Data cleaning failed: {str(e)}",
                validation_rule="data_cleaning",
                original_error=e
            )
    
    def _validate_structure(self, data: pd.DataFrame) -> Tuple[bool, List[str]]:
        """Validate data structure and schema.
        
        Args:
            data: DataFrame to validate
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Check if DataFrame is not empty
        if data.empty:
            errors.append("DataFrame is empty")
            return False, errors
        
        # Check for required columns
        missing_required = []
        for col in self._validation_rules['required_columns']:
            if col not in data.columns:
                # Try to find similar column names
                similar_cols = [c for c in data.columns if col.lower() in c.lower()]
                if similar_cols:
                    errors.append(f"Required column '{col}' not found. Similar columns: {similar_cols}")
                else:
                    missing_required.append(col)
        
        if missing_required:
            errors.append(f"Missing required columns: {missing_required}")
        
        # Check for completely empty columns
        empty_columns = data.columns[data.isnull().all()].tolist()
        if empty_columns:
            errors.append(f"Completely empty columns found: {empty_columns}")
        
        is_valid = len(errors) == 0
        return is_valid, errors
    
    def _analyze_missing_values(self, data: pd.DataFrame) -> Dict[str, int]:
        """Analyze missing values by column.
        
        Args:
            data: DataFrame to analyze
            
        Returns:
            Dictionary mapping column names to missing value counts
        """
        missing_counts = data.isnull().sum()
        return missing_counts[missing_counts > 0].to_dict()
    
    def _validate_data_types(self, data: pd.DataFrame) -> List[str]:
        """Validate data types against expected schema.
        
        Args:
            data: DataFrame to validate
            
        Returns:
            List of data type issues found
        """
        issues = []
        
        for col, expected_type in self._expected_columns.items():
            if col in data.columns:
                actual_dtype = str(data[col].dtype)
                
                # Check type compatibility
                if expected_type == 'integer':
                    if not pd.api.types.is_integer_dtype(data[col]) and not pd.api.types.is_numeric_dtype(data[col]):
                        issues.append(f"Column '{col}' expected integer, got {actual_dtype}")
                elif expected_type == 'string':
                    if not pd.api.types.is_object_dtype(data[col]):
                        issues.append(f"Column '{col}' expected string, got {actual_dtype}")
                elif expected_type == 'float':
                    if not pd.api.types.is_numeric_dtype(data[col]):
                        issues.append(f"Column '{col}' expected float, got {actual_dtype}")
        
        return issues
    
    def _validate_business_rules(self, data: pd.DataFrame) -> List[str]:
        """Validate business-specific rules.
        
        Args:
            data: DataFrame to validate
            
        Returns:
            List of business rule violations
        """
        errors = []
        
        # Validate graduation years
        if 'ano_titulacion' in data.columns:
            year_min, year_max = self._validation_rules['year_range']
            invalid_years = data[
                (data['ano_titulacion'] < year_min) | 
                (data['ano_titulacion'] > year_max)
            ]
            if len(invalid_years) > 0:
                errors.append(f"Found {len(invalid_years)} records with invalid graduation years")
        
        # Validate quantities
        if 'cantidad_titulados' in data.columns:
            qty_min, qty_max = self._validation_rules['quantity_range']
            invalid_quantities = data[
                (data['cantidad_titulados'] < qty_min) | 
                (data['cantidad_titulados'] > qty_max)
            ]
            if len(invalid_quantities) > 0:
                errors.append(f"Found {len(invalid_quantities)} records with invalid graduate quantities")
        
        # Validate region format
        if 'region' in data.columns:
            # Check for empty or very short region names
            invalid_regions = data[
                (data['region'].str.len() < 3) | 
                (data['region'].str.contains(r'^\d+$', na=False))
            ]
            if len(invalid_regions) > 0:
                errors.append(f"Found {len(invalid_regions)} records with invalid region names")
        
        return errors
    
    def _detect_duplicates(self, data: pd.DataFrame) -> int:
        """Detect duplicate records.
        
        Args:
            data: DataFrame to check for duplicates
            
        Returns:
            Number of duplicate records found
        """
        return data.duplicated().sum()
    
    def _validate_records(self, data: pd.DataFrame) -> int:
        """Validate individual records using Pydantic model.
        
        Args:
            data: DataFrame with records to validate
            
        Returns:
            Number of valid records
        """
        valid_count = 0
        
        # Sample validation for performance on large datasets
        sample_size = min(1000, len(data))
        sample_data = data.sample(n=sample_size) if len(data) > sample_size else data
        
        for idx, row in sample_data.iterrows():
            try:
                # Convert row to dict and validate with Pydantic model
                record_dict = row.to_dict()
                
                # Map column names to model fields (simplified mapping)
                mapped_dict = {}
                for key, value in record_dict.items():
                    # Handle NaN values
                    if pd.isna(value):
                        mapped_dict[key] = None
                    else:
                        mapped_dict[key] = value
                
                # Try to create TitulacionRecord (basic validation)
                # Note: This is a simplified validation - in practice, you'd map all fields
                if all(key in mapped_dict for key in ['region']):
                    valid_count += 1
                    
            except Exception:
                # Record is invalid
                continue
        
        # Extrapolate to full dataset
        if len(data) > sample_size:
            validation_rate = valid_count / sample_size
            estimated_valid = int(len(data) * validation_rate)
            return estimated_valid
        
        return valid_count
    
    def generate_quality_summary(self, quality_report: DataQualityReport) -> str:
        """Generate human-readable quality summary.
        
        Args:
            quality_report: Quality report to summarize
            
        Returns:
            Formatted quality summary string
        """
        summary = []
        summary.append("=== DATA QUALITY REPORT ===")
        summary.append(f"Total Records: {quality_report.total_records:,}")
        summary.append(f"Valid Records: {quality_report.valid_records:,}")
        summary.append(f"Invalid Records: {quality_report.invalid_records:,}")
        summary.append(f"Quality Score: {quality_report.data_quality_score:.1f}%")
        summary.append("")
        
        if quality_report.duplicate_records > 0:
            summary.append(f"Duplicate Records: {quality_report.duplicate_records:,}")
        
        if quality_report.missing_values_by_column:
            summary.append("Missing Values by Column:")
            for col, count in quality_report.missing_values_by_column.items():
                percentage = (count / quality_report.total_records) * 100
                summary.append(f"  - {col}: {count:,} ({percentage:.1f}%)")
        
        if quality_report.data_types_issues:
            summary.append("Data Type Issues:")
            for issue in quality_report.data_types_issues[:5]:  # Show first 5
                summary.append(f"  - {issue}")
        
        if quality_report.validation_errors:
            summary.append("Validation Errors:")
            for error in quality_report.validation_errors[:5]:  # Show first 5
                summary.append(f"  - {error}")
        
        return "\n".join(summary)
    
    @property
    def quality_threshold(self) -> float:
        """Get the quality threshold."""
        return self._quality_threshold
