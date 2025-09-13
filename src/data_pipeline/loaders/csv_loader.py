"""CSV data loader implementation.

This module implements data loading functionality for CSV files,
following the Single Responsibility Principle and providing robust error handling.
"""

import pandas as pd
from pathlib import Path
from typing import Optional, Dict, Any
import time
import os

from ..interfaces import DataLoader
from ..exceptions import LoadingError
from ..models import ProcessingResult, DataQualityReport
from ...config import get_path_config, get_settings


class CSVLoader(DataLoader):
    """CSV file data loader.
    
    Implements data loading to CSV files with validation and error handling.
    Follows the Single Responsibility Principle by focusing solely on CSV data loading.
    """
    
    def __init__(self, encoding: str = 'utf-8', separator: str = ','):
        """Initialize CSV loader.
        
        Args:
            encoding: File encoding for CSV output
            separator: Column separator character
        """
        self._settings = get_settings()
        self._path_config = get_path_config()
        self._encoding = encoding
        self._separator = separator
    
    def load(self, data: pd.DataFrame, destination: str) -> ProcessingResult:
        """Load data to CSV destination.
        
        Args:
            data: DataFrame to load
            destination: Target destination path (relative or absolute)
            
        Returns:
            ProcessingResult with operation details
            
        Raises:
            LoadingError: If loading fails
        """
        start_time = time.time()
        
        try:
            # Validate destination
            if not self.validate_destination(destination):
                raise LoadingError(
                    f"Destination validation failed: {destination}",
                    destination_path=destination
                )
            
            # Resolve full path
            destination_path = self._resolve_destination_path(destination)
            
            # Ensure directory exists
            destination_path.parent.mkdir(parents=True, exist_ok=True)
            
            print(f"Loading {len(data)} records to {destination_path}...")
            
            # Write to CSV
            data.to_csv(
                destination_path,
                index=False,
                encoding=self._encoding,
                sep=self._separator
            )
            
            # Verify file was created and has correct size
            if not destination_path.exists():
                raise LoadingError(
                    "File was not created successfully",
                    destination_path=str(destination_path)
                )
            
            file_size = destination_path.stat().st_size
            if file_size == 0:
                raise LoadingError(
                    "Created file is empty",
                    destination_path=str(destination_path)
                )
            
            loading_time = time.time() - start_time
            
            # Create result
            result = ProcessingResult(
                success=True,
                message=f"Successfully loaded {len(data)} records to CSV",
                records_processed=len(data),
                execution_time_seconds=loading_time,
                output_file_path=str(destination_path)
            )
            
            print(f"Loading completed: {len(data)} records saved to {destination_path} "
                  f"({file_size:,} bytes) in {loading_time:.2f} seconds")
            
            return result
            
        except Exception as e:
            if isinstance(e, LoadingError):
                raise
            raise LoadingError(
                f"Unexpected error during CSV loading: {str(e)}",
                destination_path=destination,
                original_error=e
            )
    
    def validate_destination(self, destination: str) -> bool:
        """Validate that the destination is accessible and valid.
        
        Args:
            destination: Target destination path
            
        Returns:
            True if destination is valid, False otherwise
        """
        try:
            # Check if destination is not empty
            if not destination or not destination.strip():
                print("Error: Destination path is empty")
                return False
            
            # Resolve full path
            destination_path = self._resolve_destination_path(destination)
            
            # Check if it's a valid file path (not directory)
            if destination_path.suffix == '':
                print(f"Error: Destination must be a file, not directory: {destination_path}")
                return False
            
            # Check if it's a CSV file
            if destination_path.suffix.lower() != '.csv':
                print(f"Error: Destination must be a CSV file: {destination_path}")
                return False
            
            # Check if parent directory exists or can be created
            parent_dir = destination_path.parent
            if not parent_dir.exists():
                try:
                    parent_dir.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    print(f"Error: Cannot create parent directory {parent_dir}: {str(e)}")
                    return False
            
            # Check write permissions
            if parent_dir.exists() and not os.access(parent_dir, os.W_OK):
                print(f"Error: No write permission for directory: {parent_dir}")
                return False
            
            # Check if file exists and is writable
            if destination_path.exists() and not os.access(destination_path, os.W_OK):
                print(f"Error: No write permission for file: {destination_path}")
                return False
            
            return True
            
        except Exception as e:
            print(f"Error validating destination: {str(e)}")
            return False
    
    def load_with_metadata(self, data: pd.DataFrame, destination: str, 
                          metadata: Optional[Dict[str, Any]] = None) -> ProcessingResult:
        """Load data with metadata header.
        
        Args:
            data: DataFrame to load
            destination: Target destination path
            metadata: Optional metadata to include in file header
            
        Returns:
            ProcessingResult with operation details
        """
        try:
            if metadata:
                # Create a temporary file with metadata header
                destination_path = self._resolve_destination_path(destination)
                
                # Write metadata as comments
                with open(destination_path, 'w', encoding=self._encoding) as f:
                    f.write("# Metadata\n")
                    for key, value in metadata.items():
                        f.write(f"# {key}: {value}\n")
                    f.write("# End Metadata\n")
                
                # Append data
                data.to_csv(
                    destination_path,
                    mode='a',
                    index=False,
                    encoding=self._encoding,
                    sep=self._separator
                )
                
                return ProcessingResult(
                    success=True,
                    message=f"Successfully loaded {len(data)} records with metadata",
                    records_processed=len(data),
                    execution_time_seconds=0,
                    output_file_path=str(destination_path)
                )
            else:
                # Load without metadata
                return self.load(data, destination)
                
        except Exception as e:
            raise LoadingError(
                f"Failed to load data with metadata: {str(e)}",
                destination_path=destination,
                original_error=e
            )
    
    def append_data(self, data: pd.DataFrame, destination: str) -> ProcessingResult:
        """Append data to existing CSV file.
        
        Args:
            data: DataFrame to append
            destination: Target destination path
            
        Returns:
            ProcessingResult with operation details
        """
        start_time = time.time()
        
        try:
            destination_path = self._resolve_destination_path(destination)
            
            # Check if file exists
            if not destination_path.exists():
                # If file doesn't exist, create it
                return self.load(data, destination)
            
            # Append to existing file
            data.to_csv(
                destination_path,
                mode='a',
                header=False,  # Don't write header when appending
                index=False,
                encoding=self._encoding,
                sep=self._separator
            )
            
            loading_time = time.time() - start_time
            
            result = ProcessingResult(
                success=True,
                message=f"Successfully appended {len(data)} records to CSV",
                records_processed=len(data),
                execution_time_seconds=loading_time,
                output_file_path=str(destination_path)
            )
            
            print(f"Append completed: {len(data)} records appended to {destination_path}")
            
            return result
            
        except Exception as e:
            raise LoadingError(
                f"Failed to append data to CSV: {str(e)}",
                destination_path=destination,
                original_error=e
            )
    
    def _resolve_destination_path(self, destination: str) -> Path:
        """Resolve destination to full path.
        
        Args:
            destination: Destination path (relative or absolute)
            
        Returns:
            Resolved Path object
        """
        destination_path = Path(destination)
        
        # If relative path, resolve against clean data directory
        if not destination_path.is_absolute():
            destination_path = self._path_config.clean_data_path / destination_path
        
        return destination_path
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """Get information about a CSV file.
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            Dictionary with file information
        """
        try:
            path = Path(file_path)
            
            if not path.exists():
                return {"error": "File does not exist"}
            
            stat = path.stat()
            
            # Try to read basic info about the CSV
            try:
                df_sample = pd.read_csv(path, nrows=5)
                columns = list(df_sample.columns)
                estimated_rows = sum(1 for line in open(path, 'r', encoding=self._encoding)) - 1  # Subtract header
            except Exception:
                columns = []
                estimated_rows = 0
            
            return {
                "file_path": str(path),
                "file_size_bytes": stat.st_size,
                "file_size_mb": round(stat.st_size / (1024 * 1024), 2),
                "modified_time": stat.st_mtime,
                "columns": columns,
                "estimated_rows": estimated_rows
            }
            
        except Exception as e:
            return {"error": f"Failed to get file info: {str(e)}"}
    
    @property
    def encoding(self) -> str:
        """Get the encoding being used for CSV files."""
        return self._encoding
    
    @property
    def separator(self) -> str:
        """Get the separator being used for CSV files."""
        return self._separator
