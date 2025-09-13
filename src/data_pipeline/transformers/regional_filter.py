"""Regional filter transformer implementation.

This module implements filtering operations to focus on Los Ríos region data,
following the Single Responsibility Principle.
"""

import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Any
import time
import re

from ..interfaces import DataTransformer, DataFilter
from ..exceptions import TransformationError
from ..models import ProcessingResult
from ...config import get_settings


class RegionalFilter(DataTransformer, DataFilter):
    """Regional data filter.
    
    Implements filtering operations to extract data specific to Los Ríos region,
    including validation and flexible criteria matching.
    """
    
    def __init__(self, target_region: Optional[str] = None):
        """Initialize regional filter.
        
        Args:
            target_region: Target region name. If None, uses config default
        """
        self._settings = get_settings()
        self._target_region = target_region or self._settings.target_region
        
        # Regional variations and synonyms
        self._regional_variations = {
            'los rios': ['los ríos', 'los rios', 'de los ríos', 'de los rios', 'región de los ríos'],
            'los ríos': ['los ríos', 'los rios', 'de los ríos', 'de los rios', 'región de los ríos']
        }
    
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """Transform data by filtering for target region.
        
        Args:
            data: Input DataFrame to filter
            
        Returns:
            Filtered DataFrame containing only target region data
            
        Raises:
            TransformationError: If transformation fails
        """
        start_time = time.time()
        
        try:
            if not self.validate_input(data):
                raise TransformationError(
                    "Input validation failed for regional filtering",
                    transformation_step="input_validation"
                )
            
            print(f"Starting regional filtering for '{self._target_region}' from {len(data)} records...")
            
            # Apply regional filter
            criteria = {'region': self._target_region}
            filtered_data = self.filter(data, criteria)
            
            filtering_time = time.time() - start_time
            records_kept = len(filtered_data)
            records_filtered = len(data) - records_kept
            
            print(f"Regional filtering completed: {records_kept} records kept, "
                  f"{records_filtered} records filtered out in {filtering_time:.2f} seconds")
            
            if records_kept == 0:
                print(f"Warning: No records found for region '{self._target_region}'. "
                      f"Available regions: {self._get_available_regions(data)}")
            
            return filtered_data
            
        except Exception as e:
            if isinstance(e, TransformationError):
                raise
            raise TransformationError(
                f"Unexpected error during regional filtering: {str(e)}",
                transformation_step="regional_filtering",
                original_error=e
            )
    
    def validate_input(self, data: pd.DataFrame) -> bool:
        """Validate input data before filtering.
        
        Args:
            data: DataFrame to validate
            
        Returns:
            True if data is valid for filtering, False otherwise
        """
        try:
            # Check basic DataFrame validity
            if data is None or data.empty:
                print("Error: Input data is None or empty")
                return False
            
            # Check if region column exists
            region_column = self._find_region_column(data)
            if region_column is None:
                print(f"Error: No region column found in data. Available columns: {list(data.columns)}")
                return False
            
            # Check if region column has data
            if data[region_column].isna().all():
                print(f"Error: Region column '{region_column}' contains only null values")
                return False
            
            return True
            
        except Exception as e:
            print(f"Error validating input data for regional filtering: {str(e)}")
            return False
    
    def filter(self, data: pd.DataFrame, criteria: Dict[str, Any]) -> pd.DataFrame:
        """Filter data based on provided criteria.
        
        Args:
            data: DataFrame to filter
            criteria: Filtering criteria dictionary
            
        Returns:
            Filtered DataFrame
            
        Raises:
            TransformationError: If filtering fails
        """
        try:
            if not self.validate_criteria(criteria):
                raise TransformationError(
                    f"Invalid filtering criteria: {criteria}",
                    transformation_step="criteria_validation"
                )
            
            filtered_data = data.copy()
            
            # Apply region filter if specified
            if 'region' in criteria:
                target_region = criteria['region']
                filtered_data = self._filter_by_region(filtered_data, target_region)
            
            # Apply additional filters if specified
            for key, value in criteria.items():
                if key != 'region' and key in filtered_data.columns:
                    filtered_data = filtered_data[filtered_data[key] == value]
            
            return filtered_data
            
        except Exception as e:
            if isinstance(e, TransformationError):
                raise
            raise TransformationError(
                f"Failed to apply filter criteria: {str(e)}",
                transformation_step="filter_application",
                original_error=e
            )
    
    def validate_criteria(self, criteria: Dict[str, Any]) -> bool:
        """Validate filtering criteria.
        
        Args:
            criteria: Criteria to validate
            
        Returns:
            True if criteria are valid, False otherwise
        """
        try:
            # Check if criteria is not empty
            if not criteria:
                print("Error: Empty filtering criteria")
                return False
            
            # Check if criteria contains valid keys
            valid_keys = {'region', 'provincia', 'comuna', 'institucion', 'carrera'}
            invalid_keys = set(criteria.keys()) - valid_keys
            if invalid_keys:
                print(f"Warning: Unknown criteria keys: {invalid_keys}")
            
            # Check if region criteria is valid
            if 'region' in criteria:
                if not isinstance(criteria['region'], str) or not criteria['region'].strip():
                    print("Error: Region criteria must be a non-empty string")
                    return False
            
            return True
            
        except Exception as e:
            print(f"Error validating criteria: {str(e)}")
            return False
    
    def _filter_by_region(self, data: pd.DataFrame, target_region: str) -> pd.DataFrame:
        """Filter data by region using flexible matching.
        
        Args:
            data: DataFrame to filter
            target_region: Target region name
            
        Returns:
            Filtered DataFrame
        """
        region_column = self._find_region_column(data)
        if region_column is None:
            raise TransformationError(
                "No region column found for filtering",
                transformation_step="region_column_detection"
            )
        
        # Create case-insensitive filter with variations
        target_lower = target_region.lower().strip()
        variations = self._regional_variations.get(target_lower, [target_region])
        variations.append(target_region)  # Add original
        
        # Create boolean mask for matching
        mask = pd.Series([False] * len(data))
        
        for variation in variations:
            variation_mask = data[region_column].str.lower().str.strip().str.contains(
                variation.lower(), na=False, regex=False
            )
            mask = mask | variation_mask
        
        return data[mask]
    
    def _find_region_column(self, data: pd.DataFrame) -> Optional[str]:
        """Find the region column in the DataFrame.
        
        Args:
            data: DataFrame to search
            
        Returns:
            Region column name if found, None otherwise
        """
        region_patterns = [
            r'.*region.*',
            r'.*reg.*',
            r'.*administrativa.*'
        ]
        
        for col in data.columns:
            col_lower = col.lower()
            for pattern in region_patterns:
                if re.match(pattern, col_lower):
                    return col
        
        return None
    
    def _get_available_regions(self, data: pd.DataFrame) -> List[str]:
        """Get list of available regions in the data.
        
        Args:
            data: DataFrame to analyze
            
        Returns:
            List of unique region names
        """
        region_column = self._find_region_column(data)
        if region_column is None:
            return []
        
        unique_regions = data[region_column].dropna().unique().tolist()
        return sorted(unique_regions)
    
    def get_regional_summary(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Get summary statistics by region.
        
        Args:
            data: DataFrame to analyze
            
        Returns:
            Dictionary with regional summary statistics
        """
        try:
            region_column = self._find_region_column(data)
            if region_column is None:
                return {"error": "No region column found"}
            
            summary = {}
            
            # Count by region
            region_counts = data[region_column].value_counts()
            summary['counts_by_region'] = region_counts.to_dict()
            
            # Total records
            summary['total_records'] = len(data)
            
            # Target region statistics
            target_data = self._filter_by_region(data, self._target_region)
            summary['target_region'] = self._target_region
            summary['target_region_records'] = len(target_data)
            summary['target_region_percentage'] = (len(target_data) / len(data)) * 100 if len(data) > 0 else 0
            
            return summary
            
        except Exception as e:
            return {"error": f"Failed to generate regional summary: {str(e)}"}
    
    @property
    def target_region(self) -> str:
        """Get the target region being used for filtering."""
        return self._target_region
