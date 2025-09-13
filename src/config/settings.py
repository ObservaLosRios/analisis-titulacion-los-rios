"""Configuration module for the ETL pipeline.

This module contains all configuration settings and constants used throughout
the ETL pipeline, following the Single Responsibility Principle.
"""

import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables.
    
    Uses Pydantic for validation and type safety, ensuring configuration
    integrity following Clean Code principles.
    """
    
    # Paths
    data_raw_path: str = Field(default="data/raw", description="Raw data directory")
    data_processed_path: str = Field(default="data/processed", description="Processed data directory")
    data_clean_path: str = Field(default="data/clean", description="Clean data directory")
    log_path: str = Field(default="logs", description="Log files directory")
    
    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    
    # Regional filter
    target_region: str = Field(default="Los Ríos", description="Target region for analysis")
    
    # File configuration
    excel_file_name: str = Field(default="Informe_Titulacion_2024_SIES_.xlsx", description="Excel file name")
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        case_sensitive = False


class PathConfig:
    """Path configuration manager.
    
    Centralizes path management following the Single Responsibility Principle.
    Ensures all paths are properly resolved and accessible.
    """
    
    def __init__(self, settings: Settings):
        """Initialize path configuration with settings.
        
        Args:
            settings: Application settings instance
        """
        self.settings = settings
        self._base_path = Path.cwd()
        self._ensure_directories_exist()
    
    @property
    def raw_data_path(self) -> Path:
        """Get raw data directory path."""
        return self._base_path / self.settings.data_raw_path
    
    @property
    def processed_data_path(self) -> Path:
        """Get processed data directory path."""
        return self._base_path / self.settings.data_processed_path
    
    @property
    def clean_data_path(self) -> Path:
        """Get clean data directory path."""
        return self._base_path / self.settings.data_clean_path
    
    @property
    def log_path(self) -> Path:
        """Get log directory path."""
        return self._base_path / self.settings.log_path
    
    @property
    def excel_file_path(self) -> Path:
        """Get full path to Excel file."""
        return self.raw_data_path / self.settings.excel_file_name
    
    def _ensure_directories_exist(self) -> None:
        """Ensure all required directories exist."""
        directories = [
            self.raw_data_path,
            self.processed_data_path,
            self.clean_data_path,
            self.log_path
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)


def get_settings() -> Settings:
    """Get application settings.
    
    Factory function that loads environment variables and returns
    configured settings instance.
    
    Returns:
        Settings instance with loaded configuration
    """
    load_dotenv()
    return Settings()


def get_path_config() -> PathConfig:
    """Get path configuration.
    
    Factory function that returns path configuration instance.
    
    Returns:
        PathConfig instance with resolved paths
    """
    settings = get_settings()
    return PathConfig(settings)
