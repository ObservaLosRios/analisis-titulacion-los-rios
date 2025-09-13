"""Data models for the ETL pipeline.

This module defines Pydantic models for data validation and type safety,
ensuring data integrity throughout the pipeline.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator


class TitulacionRecord(BaseModel):
    """Model representing a graduation record.
    
    Defines the structure and validation rules for graduation data,
    ensuring data quality and type safety.
    """
    
    # Institution information
    codigo_institucion: Optional[str] = Field(None, description="Institution code")
    nombre_institucion: Optional[str] = Field(None, description="Institution name")
    tipo_institucion: Optional[str] = Field(None, description="Institution type")
    
    # Regional information
    region: Optional[str] = Field(None, description="Region name")
    provincia: Optional[str] = Field(None, description="Province name")
    comuna: Optional[str] = Field(None, description="Comuna name")
    
    # Academic information
    area_conocimiento: Optional[str] = Field(None, description="Knowledge area")
    carrera: Optional[str] = Field(None, description="Career name")
    codigo_carrera: Optional[str] = Field(None, description="Career code")
    modalidad: Optional[str] = Field(None, description="Study modality")
    jornada: Optional[str] = Field(None, description="Study schedule")
    sede: Optional[str] = Field(None, description="Campus location")
    
    # Academic level
    nivel_academico: Optional[str] = Field(None, description="Academic level")
    titulo_profesional: Optional[str] = Field(None, description="Professional title")
    grado_academico: Optional[str] = Field(None, description="Academic degree")
    
    # Graduation data
    ano_titulacion: Optional[int] = Field(None, description="Graduation year")
    mes_titulacion: Optional[int] = Field(None, description="Graduation month")
    cantidad_titulados: Optional[int] = Field(None, description="Number of graduates")
    
    # Demographics
    genero: Optional[str] = Field(None, description="Gender")
    edad_promedio: Optional[float] = Field(None, description="Average age")
    
    @validator('ano_titulacion')
    def validate_year(cls, v):
        """Validate graduation year."""
        if v is not None and (v < 1990 or v > datetime.now().year):
            raise ValueError('Invalid graduation year')
        return v
    
    @validator('mes_titulacion')
    def validate_month(cls, v):
        """Validate graduation month."""
        if v is not None and (v < 1 or v > 12):
            raise ValueError('Invalid graduation month')
        return v
    
    @validator('cantidad_titulados')
    def validate_graduates_count(cls, v):
        """Validate graduates count."""
        if v is not None and v < 0:
            raise ValueError('Graduates count cannot be negative')
        return v


class DataQualityReport(BaseModel):
    """Model representing data quality assessment results.
    
    Tracks data quality metrics and issues found during validation.
    """
    
    total_records: int = Field(description="Total number of records")
    valid_records: int = Field(description="Number of valid records")
    invalid_records: int = Field(description="Number of invalid records")
    missing_values_by_column: Dict[str, int] = Field(description="Missing values per column")
    duplicate_records: int = Field(description="Number of duplicate records")
    data_types_issues: List[str] = Field(description="Data type issues found")
    validation_errors: List[str] = Field(description="Validation errors")
    
    @property
    def data_quality_score(self) -> float:
        """Calculate data quality score as percentage of valid records."""
        if self.total_records == 0:
            return 0.0
        return (self.valid_records / self.total_records) * 100


class ProcessingResult(BaseModel):
    """Model representing the result of a processing operation.
    
    Standardizes the response format for all processing operations.
    """
    
    success: bool = Field(description="Whether the operation was successful")
    message: str = Field(description="Result message")
    records_processed: int = Field(description="Number of records processed")
    execution_time_seconds: float = Field(description="Execution time in seconds")
    output_file_path: Optional[str] = Field(None, description="Path to output file")
    quality_report: Optional[DataQualityReport] = Field(None, description="Data quality report")
    
    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Data processed successfully",
                "records_processed": 1000,
                "execution_time_seconds": 45.2,
                "output_file_path": "data/clean/titulacion_los_rios_clean.csv",
                "quality_report": None
            }
        }
