"""ETL Pipeline Orchestrator.

This module implements the main ETL pipeline orchestrator following
the Dependency Inversion Principle and providing a clean interface
for pipeline execution.
"""

import time
from typing import Optional, Dict, Any, List
from pathlib import Path
import pandas as pd

from .data_pipeline import (
    ExcelExtractor, DataCleaner, RegionalFilter, DataQualityValidator,
    CSVLoader, ETLLogger, ProcessingResult, DataQualityReport,
    ETLError, ExtractionError, TransformationError, LoadingError, ValidationError
)
from .config import get_settings, get_path_config


class ETLPipeline:
    """Main ETL Pipeline orchestrator.
    
    Coordinates the entire ETL process following the Single Responsibility
    Principle and Dependency Inversion. Provides comprehensive error handling,
    logging, and monitoring.
    """
    
    def __init__(self, quality_threshold: float = 75.0):
        """Initialize ETL pipeline.
        
        Args:
            quality_threshold: Minimum data quality threshold (0-100)
        """
        self._settings = get_settings()
        self._path_config = get_path_config()
        self._quality_threshold = quality_threshold
        
        # Initialize components
        self._logger = ETLLogger("ETL_PIPELINE")
        self._extractor = ExcelExtractor()
        self._cleaner = DataCleaner()
        self._regional_filter = RegionalFilter()
        self._validator = DataQualityValidator(quality_threshold)
        self._loader = CSVLoader()
        
        # Pipeline state
        self._pipeline_results = {}
        self._execution_start_time = None
    
    def run_full_pipeline(self, output_filename: Optional[str] = None) -> ProcessingResult:
        """Execute the complete ETL pipeline.
        
        Args:
            output_filename: Optional custom output filename
            
        Returns:
            ProcessingResult with pipeline execution details
            
        Raises:
            ETLError: If pipeline execution fails
        """
        self._execution_start_time = time.time()
        
        with self._logger.create_operation_logger("FULL_ETL_PIPELINE") as op_logger:
            try:
                op_logger.log_info("Starting complete ETL pipeline execution")
                
                # Step 1: Extract data
                raw_data = self._extract_data(op_logger)
                
                # Step 2: Clean data
                cleaned_data = self._clean_data(raw_data, op_logger)
                
                # Step 3: Filter for Los Ríos region
                filtered_data = self._filter_regional_data(cleaned_data, op_logger)
                
                # Step 4: Validate data quality
                quality_report = self._validate_data_quality(filtered_data, op_logger)
                
                # Step 5: Load clean data
                output_filename = output_filename or f"titulacion_los_rios_clean_{int(time.time())}.csv"
                load_result = self._load_data(filtered_data, output_filename, op_logger)
                
                # Generate final result
                total_execution_time = time.time() - self._execution_start_time
                
                final_result = ProcessingResult(
                    success=True,
                    message="ETL Pipeline completed successfully",
                    records_processed=len(filtered_data),
                    execution_time_seconds=total_execution_time,
                    output_file_path=load_result.output_file_path,
                    quality_report=quality_report
                )
                
                # Log pipeline summary
                self._log_pipeline_summary(final_result, op_logger)
                
                return final_result
                
            except Exception as e:
                total_execution_time = time.time() - self._execution_start_time
                
                error_result = ProcessingResult(
                    success=False,
                    message=f"ETL Pipeline failed: {str(e)}",
                    records_processed=0,
                    execution_time_seconds=total_execution_time
                )
                
                op_logger.log_error("ETL Pipeline execution failed", error=e)
                
                if isinstance(e, ETLError):
                    raise
                else:
                    raise ETLError(f"Pipeline execution failed: {str(e)}", original_error=e)
    
    def run_extraction_only(self) -> ProcessingResult:
        """Run only the data extraction step.
        
        Returns:
            ProcessingResult with extraction details
        """
        with self._logger.create_operation_logger("EXTRACTION_ONLY") as op_logger:
            try:
                raw_data = self._extract_data(op_logger)
                
                return ProcessingResult(
                    success=True,
                    message=f"Data extraction completed successfully",
                    records_processed=len(raw_data),
                    execution_time_seconds=0
                )
                
            except Exception as e:
                op_logger.log_error("Extraction failed", error=e)
                raise
    
    def run_validation_only(self, data_source: Optional[str] = None) -> DataQualityReport:
        """Run only data validation.
        
        Args:
            data_source: Optional path to data file. If None, extracts from default source
            
        Returns:
            DataQualityReport with validation results
        """
        with self._logger.create_operation_logger("VALIDATION_ONLY") as op_logger:
            try:
                if data_source:
                    # Load data from specified source
                    if data_source.endswith('.csv'):
                        import pandas as pd
                        data = pd.read_csv(data_source)
                    else:
                        data = self._extract_data(op_logger)
                else:
                    data = self._extract_data(op_logger)
                
                return self._validate_data_quality(data, op_logger)
                
            except Exception as e:
                op_logger.log_error("Validation failed", error=e)
                raise
    
    def get_regional_summary(self) -> Dict[str, Any]:
        """Get summary of available regional data.
        
        Returns:
            Dictionary with regional data summary
        """
        try:
            with self._logger.create_operation_logger("REGIONAL_SUMMARY") as op_logger:
                raw_data = self._extract_data(op_logger)
                return self._regional_filter.get_regional_summary(raw_data)
                
        except Exception as e:
            self._logger.log_error("Failed to generate regional summary", error=e)
            return {"error": str(e)}
    
    def _extract_data(self, op_logger) -> 'pd.DataFrame':
        """Extract data from Excel source.
        
        Args:
            op_logger: Operation logger instance
            
        Returns:
            Extracted DataFrame
        """
        try:
            op_logger.log_info("Starting data extraction")
            
            # Validate source exists
            if not self._extractor.validate_source():
                raise ExtractionError(
                    f"Source validation failed: {self._extractor.file_path}",
                    source_path=str(self._extractor.file_path)
                )
            
            # Extract data
            data = self._extractor.extract()
            
            op_logger.log_info(
                f"Data extraction completed: {len(data)} records, {len(data.columns)} columns",
                records_extracted=len(data),
                columns_count=len(data.columns)
            )
            
            # Log basic statistics
            self._logger.log_data_stats("EXTRACTION", 0, len(data))
            
            return data
            
        except Exception as e:
            op_logger.log_error("Data extraction failed", error=e)
            raise
    
    def _clean_data(self, data, op_logger) -> 'pd.DataFrame':
        """Clean the extracted data.
        
        Args:
            data: Raw DataFrame to clean
            op_logger: Operation logger instance
            
        Returns:
            Cleaned DataFrame
        """
        try:
            op_logger.log_info("Starting data cleaning")
            
            initial_records = len(data)
            cleaned_data = self._cleaner.transform(data)
            final_records = len(cleaned_data)
            
            op_logger.log_info(
                f"Data cleaning completed: {initial_records} → {final_records} records",
                records_before=initial_records,
                records_after=final_records
            )
            
            self._logger.log_data_stats("CLEANING", initial_records, final_records)
            
            return cleaned_data
            
        except Exception as e:
            op_logger.log_error("Data cleaning failed", error=e)
            raise
    
    def _filter_regional_data(self, data, op_logger) -> 'pd.DataFrame':
        """Filter data for target region.
        
        Args:
            data: DataFrame to filter
            op_logger: Operation logger instance
            
        Returns:
            Filtered DataFrame
        """
        try:
            op_logger.log_info(f"Starting regional filtering for '{self._settings.target_region}'")
            
            initial_records = len(data)
            filtered_data = self._regional_filter.transform(data)
            final_records = len(filtered_data)
            
            if final_records == 0:
                # Get available regions for troubleshooting
                available_regions = self._regional_filter._get_available_regions(data)
                op_logger.log_warning(
                    f"No records found for region '{self._settings.target_region}'. "
                    f"Available regions: {available_regions[:10]}"  # Show first 10
                )
            
            op_logger.log_info(
                f"Regional filtering completed: {initial_records} → {final_records} records",
                target_region=self._settings.target_region,
                records_before=initial_records,
                records_after=final_records
            )
            
            self._logger.log_data_stats("REGIONAL_FILTERING", initial_records, final_records)
            
            return filtered_data
            
        except Exception as e:
            op_logger.log_error("Regional filtering failed", error=e)
            raise
    
    def _validate_data_quality(self, data, op_logger) -> DataQualityReport:
        """Validate data quality.
        
        Args:
            data: DataFrame to validate
            op_logger: Operation logger instance
            
        Returns:
            DataQualityReport
        """
        try:
            op_logger.log_info("Starting data quality validation")
            
            quality_report = self._validator.validate(data)
            
            # Log quality metrics
            self._logger.log_quality_metrics(
                quality_report.data_quality_score,
                quality_report.total_records,
                quality_report.valid_records
            )
            
            # Check quality threshold
            if quality_report.data_quality_score < self._quality_threshold:
                op_logger.log_warning(
                    f"Data quality score {quality_report.data_quality_score:.1f}% "
                    f"is below threshold {self._quality_threshold}%"
                )
            
            op_logger.log_info(
                f"Data quality validation completed: {quality_report.data_quality_score:.1f}% quality score",
                quality_score=quality_report.data_quality_score,
                valid_records=quality_report.valid_records,
                total_records=quality_report.total_records
            )
            
            return quality_report
            
        except Exception as e:
            op_logger.log_error("Data quality validation failed", error=e)
            raise
    
    def _load_data(self, data, filename: str, op_logger) -> ProcessingResult:
        """Load cleaned data to destination.
        
        Args:
            data: DataFrame to load
            filename: Output filename
            op_logger: Operation logger instance
            
        Returns:
            ProcessingResult from loading operation
        """
        try:
            op_logger.log_info(f"Starting data loading to '{filename}'")
            
            # Create metadata
            metadata = {
                "pipeline_execution_time": time.strftime("%Y-%m-%d %H:%M:%S"),
                "target_region": self._settings.target_region,
                "records_count": len(data),
                "pipeline_version": "1.0",
                "data_source": str(self._extractor.file_path)
            }
            
            # Load with metadata
            load_result = self._loader.load_with_metadata(data, filename, metadata)
            
            # Log file operation
            if load_result.output_file_path:
                file_path = Path(load_result.output_file_path)
                if file_path.exists():
                    file_size = file_path.stat().st_size
                    self._logger.log_file_operation("WRITE", str(file_path), file_size)
            
            op_logger.log_info(
                f"Data loading completed: {len(data)} records saved to '{load_result.output_file_path}'",
                output_file=load_result.output_file_path,
                records_saved=len(data)
            )
            
            return load_result
            
        except Exception as e:
            op_logger.log_error("Data loading failed", error=e)
            raise
    
    def _log_pipeline_summary(self, result: ProcessingResult, op_logger) -> None:
        """Log pipeline execution summary.
        
        Args:
            result: ProcessingResult with pipeline results
            op_logger: Operation logger instance
        """
        summary_lines = [
            "=== ETL PIPELINE EXECUTION SUMMARY ===",
            f"Status: {'SUCCESS' if result.success else 'FAILED'}",
            f"Records Processed: {result.records_processed:,}",
            f"Execution Time: {result.execution_time_seconds:.2f} seconds",
            f"Output File: {result.output_file_path or 'None'}",
            f"Target Region: {self._settings.target_region}"
        ]
        
        if result.quality_report:
            summary_lines.extend([
                f"Data Quality Score: {result.quality_report.data_quality_score:.1f}%",
                f"Valid Records: {result.quality_report.valid_records:,}",
                f"Invalid Records: {result.quality_report.invalid_records:,}"
            ])
        
        summary = "\n".join(summary_lines)
        op_logger.log_info(f"Pipeline Summary:\n{summary}")
    
    @property
    def target_region(self) -> str:
        """Get the target region for filtering."""
        return self._settings.target_region
    
    @property
    def quality_threshold(self) -> float:
        """Get the data quality threshold."""
        return self._quality_threshold
