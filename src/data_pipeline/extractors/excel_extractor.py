"""Excel data extractor implementation.

This module implements the data extraction functionality for Excel files,
following the Single Responsibility Principle and providing robust error handling.
"""

import pandas as pd
from pathlib import Path
from typing import Optional, List, Dict, Any
import time
import os

from ..interfaces import DataExtractor
from ..exceptions import ExtractionError
from ..models import ProcessingResult
from ...config import get_path_config, get_settings


class ExcelExtractor(DataExtractor):
    """Excel file data extractor.
    
    Implements data extraction from Excel files with robust error handling
    and validation. Follows the Single Responsibility Principle by focusing
    solely on Excel data extraction.
    """
    
    def __init__(self, file_path: Optional[Path] = None, sheet_name: Optional[str] = None):
        """Initialize Excel extractor.
        
        Args:
            file_path: Path to Excel file. If None, uses default from config
            sheet_name: Name of sheet to extract. If None, uses first sheet
        """
        self._settings = get_settings()
        self._path_config = get_path_config()
        self._file_path = file_path or self._path_config.excel_file_path
        self._sheet_name = sheet_name
        self._supported_extensions = {'.xlsx', '.xls'}
    
    def extract(self) -> pd.DataFrame:
        """Extract data from Excel file.
        
        Returns:
            DataFrame containing extracted data
            
        Raises:
            ExtractionError: If extraction fails for any reason
        """
        start_time = time.time()
        
        try:
            # Validate source before extraction
            if not self.validate_source():
                raise ExtractionError(
                    f"Source validation failed for file: {self._file_path}",
                    source_path=str(self._file_path)
                )
            
            # Read Excel file
            if self._sheet_name:
                data = pd.read_excel(
                    self._file_path,
                    sheet_name=self._sheet_name,
                    engine='openpyxl'
                )
            else:
                # Read first sheet
                data = pd.read_excel(
                    self._file_path,
                    engine='openpyxl'
                )
            
            # Validate extracted data
            if data.empty:
                raise ExtractionError(
                    f"No data found in Excel file: {self._file_path}",
                    source_path=str(self._file_path)
                )
            
            extraction_time = time.time() - start_time
            
            # Log extraction success
            print(f"Successfully extracted {len(data)} records from {self._file_path} "
                  f"in {extraction_time:.2f} seconds")
            
            return data
            
        except pd.errors.EmptyDataError as e:
            raise ExtractionError(
                "Excel file is empty or has no readable data",
                source_path=str(self._file_path),
                original_error=e
            )
        except pd.errors.ParserError as e:
            raise ExtractionError(
                "Failed to parse Excel file - file may be corrupted",
                source_path=str(self._file_path),
                original_error=e
            )
        except PermissionError as e:
            raise ExtractionError(
                "Permission denied accessing Excel file",
                source_path=str(self._file_path),
                original_error=e
            )
        except Exception as e:
            raise ExtractionError(
                f"Unexpected error during Excel extraction: {str(e)}",
                source_path=str(self._file_path),
                original_error=e
            )
    
    def validate_source(self) -> bool:
        """Validate that the Excel source is accessible and valid.
        
        Returns:
            True if source is valid, False otherwise
        """
        try:
            # Check if file exists
            if not self._file_path.exists():
                print(f"Error: Excel file does not exist: {self._file_path}")
                return False
            
            # Check if it's a file (not directory)
            if not self._file_path.is_file():
                print(f"Error: Path is not a file: {self._file_path}")
                return False
            
            # Check file extension
            if self._file_path.suffix.lower() not in self._supported_extensions:
                print(f"Error: Unsupported file extension: {self._file_path.suffix}")
                return False
            
            # Check file is readable
            if not os.access(self._file_path, os.R_OK):
                print(f"Error: File is not readable: {self._file_path}")
                return False
            
            # Check file size (not empty)
            if self._file_path.stat().st_size == 0:
                print(f"Error: File is empty: {self._file_path}")
                return False
            
            return True
            
        except Exception as e:
            print(f"Error validating Excel source: {str(e)}")
            return False
    
    def get_sheet_names(self) -> List[str]:
        """Get list of sheet names in the Excel file.
        
        Returns:
            List of sheet names
            
        Raises:
            ExtractionError: If unable to read sheet names
        """
        try:
            if not self.validate_source():
                raise ExtractionError(
                    f"Cannot read sheet names - source validation failed: {self._file_path}",
                    source_path=str(self._file_path)
                )
            
            excel_file = pd.ExcelFile(self._file_path, engine='openpyxl')
            return excel_file.sheet_names
            
        except Exception as e:
            raise ExtractionError(
                f"Failed to get sheet names from Excel file: {str(e)}",
                source_path=str(self._file_path),
                original_error=e
            )
    
    def extract_multiple_sheets(self, sheet_names: Optional[List[str]] = None) -> Dict[str, pd.DataFrame]:
        """Extract data from multiple sheets.
        
        Args:
            sheet_names: List of sheet names to extract. If None, extracts all sheets
            
        Returns:
            Dictionary mapping sheet names to DataFrames
            
        Raises:
            ExtractionError: If extraction fails
        """
        try:
            if not self.validate_source():
                raise ExtractionError(
                    f"Source validation failed: {self._file_path}",
                    source_path=str(self._file_path)
                )
            
            available_sheets = self.get_sheet_names()
            
            if sheet_names is None:
                sheets_to_extract = available_sheets
            else:
                # Validate requested sheets exist
                invalid_sheets = set(sheet_names) - set(available_sheets)
                if invalid_sheets:
                    raise ExtractionError(
                        f"Requested sheets not found: {invalid_sheets}. "
                        f"Available sheets: {available_sheets}",
                        source_path=str(self._file_path)
                    )
                sheets_to_extract = sheet_names
            
            # Extract data from each sheet
            result = {}
            for sheet_name in sheets_to_extract:
                extractor = ExcelExtractor(self._file_path, sheet_name)
                result[sheet_name] = extractor.extract()
            
            return result
            
        except Exception as e:
            if isinstance(e, ExtractionError):
                raise
            raise ExtractionError(
                f"Failed to extract multiple sheets: {str(e)}",
                source_path=str(self._file_path),
                original_error=e
            )
    
    @property
    def file_path(self) -> Path:
        """Get the file path being used for extraction."""
        return self._file_path
    
    @property
    def sheet_name(self) -> Optional[str]:
        """Get the sheet name being used for extraction."""
        return self._sheet_name
