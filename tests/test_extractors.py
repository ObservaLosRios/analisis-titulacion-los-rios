"""Tests for Excel extractor."""

import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.data_pipeline.extractors import ExcelExtractor
from src.data_pipeline.exceptions import ExtractionError


class TestExcelExtractor:
    """Test cases for ExcelExtractor class."""
    
    def test_extract_valid_file(self, temp_excel_file, sample_data):
        """Test extraction from valid Excel file."""
        extractor = ExcelExtractor(Path(temp_excel_file))
        
        result = extractor.extract()
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_data)
        assert list(result.columns) == list(sample_data.columns)
    
    def test_validate_source_valid_file(self, temp_excel_file):
        """Test source validation for valid file."""
        extractor = ExcelExtractor(Path(temp_excel_file))
        
        assert extractor.validate_source() is True
    
    def test_validate_source_nonexistent_file(self):
        """Test source validation for nonexistent file."""
        extractor = ExcelExtractor(Path("nonexistent_file.xlsx"))
        
        assert extractor.validate_source() is False
    
    def test_extract_nonexistent_file_raises_error(self):
        """Test that extracting nonexistent file raises ExtractionError."""
        extractor = ExcelExtractor(Path("nonexistent_file.xlsx"))
        
        with pytest.raises(ExtractionError):
            extractor.extract()
    
    def test_get_sheet_names(self, temp_excel_file):
        """Test getting sheet names from Excel file."""
        extractor = ExcelExtractor(Path(temp_excel_file))
        
        sheet_names = extractor.get_sheet_names()
        
        assert isinstance(sheet_names, list)
        assert len(sheet_names) > 0
    
    def test_extract_empty_dataframe_raises_error(self):
        """Test that extracting empty DataFrame raises error."""
        extractor = ExcelExtractor()
        
        with patch.object(extractor, 'validate_source', return_value=True):
            with patch('pandas.read_excel', return_value=pd.DataFrame()):
                with pytest.raises(ExtractionError):
                    extractor.extract()
    
    def test_properties(self, temp_excel_file):
        """Test extractor properties."""
        file_path = Path(temp_excel_file)
        sheet_name = "Sheet1"
        extractor = ExcelExtractor(file_path, sheet_name)
        
        assert extractor.file_path == file_path
        assert extractor.sheet_name == sheet_name
