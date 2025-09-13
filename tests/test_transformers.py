"""Tests for data transformers."""

import pytest
import pandas as pd
import numpy as np

from src.data_pipeline.transformers import DataCleaner, RegionalFilter
from src.data_pipeline.exceptions import TransformationError


class TestDataCleaner:
    """Test cases for DataCleaner class."""
    
    def test_transform_valid_data(self, sample_data):
        """Test transformation of valid data."""
        cleaner = DataCleaner()
        
        result = cleaner.transform(sample_data)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) <= len(sample_data)  # May remove some records
    
    def test_validate_input_valid_data(self, sample_data):
        """Test input validation for valid data."""
        cleaner = DataCleaner()
        
        assert cleaner.validate_input(sample_data) is True
    
    def test_validate_input_empty_dataframe(self):
        """Test input validation for empty DataFrame."""
        cleaner = DataCleaner()
        empty_df = pd.DataFrame()
        
        assert cleaner.validate_input(empty_df) is False
    
    def test_validate_input_none(self):
        """Test input validation for None input."""
        cleaner = DataCleaner()
        
        assert cleaner.validate_input(None) is False
    
    def test_standardize_column_names(self, sample_data):
        """Test column name standardization."""
        # Create data with messy column names
        messy_data = sample_data.copy()
        messy_data.columns = ['Código Institución!', 'Nombre de la Institución', 
                             'REGIÓN', 'provincia__test', 'carrera'][:len(messy_data.columns)]
        
        cleaner = DataCleaner()
        result = cleaner._standardize_column_names(messy_data)
        
        # Check that column names are cleaned
        for col in result.columns:
            assert col.islower()
            assert ' ' not in col
            assert '!' not in col
    
    def test_clean_text_columns(self, sample_data):
        """Test text column cleaning."""
        # Add some messy text data
        dirty_data = sample_data.copy()
        dirty_data.loc[0, 'nombre_institucion'] = '  Universidad  A  '
        dirty_data.loc[1, 'nombre_institucion'] = 'nan'
        
        cleaner = DataCleaner()
        result = cleaner._clean_text_columns(dirty_data)
        
        # Check that text is cleaned
        assert result.loc[0, 'nombre_institucion'].strip() == 'Universidad A'
        assert pd.isna(result.loc[1, 'nombre_institucion'])


class TestRegionalFilter:
    """Test cases for RegionalFilter class."""
    
    def test_transform_filters_correctly(self, sample_data):
        """Test that regional filter correctly filters data."""
        filter_instance = RegionalFilter('Los Ríos')
        
        result = filter_instance.transform(sample_data)
        
        # Should only have Los Ríos records
        assert len(result) == 3  # 3 Los Ríos records in sample data
        assert all(result['region'].str.contains('Los Ríos', na=False))
    
    def test_validate_input_valid_data(self, sample_data):
        """Test input validation for valid data."""
        filter_instance = RegionalFilter('Los Ríos')
        
        assert filter_instance.validate_input(sample_data) is True
    
    def test_validate_input_no_region_column(self):
        """Test input validation when no region column exists."""
        data_no_region = pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})
        filter_instance = RegionalFilter('Los Ríos')
        
        assert filter_instance.validate_input(data_no_region) is False
    
    def test_filter_with_criteria(self, sample_data):
        """Test filtering with specific criteria."""
        filter_instance = RegionalFilter('Los Ríos')
        criteria = {'region': 'Los Ríos'}
        
        result = filter_instance.filter(sample_data, criteria)
        
        assert len(result) == 3
        assert all(result['region'].str.contains('Los Ríos', na=False))
    
    def test_validate_criteria_valid(self):
        """Test criteria validation for valid criteria."""
        filter_instance = RegionalFilter('Los Ríos')
        criteria = {'region': 'Los Ríos'}
        
        assert filter_instance.validate_criteria(criteria) is True
    
    def test_validate_criteria_empty(self):
        """Test criteria validation for empty criteria."""
        filter_instance = RegionalFilter('Los Ríos')
        criteria = {}
        
        assert filter_instance.validate_criteria(criteria) is False
    
    def test_get_regional_summary(self, sample_data):
        """Test regional summary generation."""
        filter_instance = RegionalFilter('Los Ríos')
        
        summary = filter_instance.get_regional_summary(sample_data)
        
        assert 'total_records' in summary
        assert 'target_region_records' in summary
        assert 'counts_by_region' in summary
        assert summary['total_records'] == len(sample_data)
        assert summary['target_region'] == 'Los Ríos'
    
    def test_target_region_property(self):
        """Test target_region property."""
        target = 'Test Region'
        filter_instance = RegionalFilter(target)
        
        assert filter_instance.target_region == target
