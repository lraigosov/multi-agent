from __future__ import annotations

from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class ETLSettings(BaseSettings):
    """Centralized configuration for ETL domain."""
    
    # LLM Configuration
    llm_provider: str = Field(default="openai", description="LLM provider: openai, gemini, anthropic")
    llm_model: str = Field(default="gpt-4o-mini", description="Model name")
    llm_temperature: float = Field(default=0.1, description="Temperature for reasoning")
    
    # Source defaults
    default_source_kind: str = Field(default="file", description="Default source type")
    default_source_format: str = Field(default="csv", description="Default format")
    
    # Destination defaults
    default_dest_kind: str = Field(default="file", description="Default destination type")
    default_dest_format: str = Field(default="csv", description="Default output format")
    
    # Validation
    enable_quality_checks: bool = Field(default=True, description="Enable data quality validation")
    fail_on_validation_errors: bool = Field(default=False, description="Stop pipeline on validation errors")
    
    # Logging
    log_level: str = Field(default="INFO", description="Log level")
    log_output_dir: Path = Field(default=Path("logs"), description="Log output directory")
    
    # Outputs
    output_dir: Path = Field(default=Path("outputs"), description="Output directory for results")
    
    class Config:
        env_prefix = "ETL_"
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings() -> ETLSettings:
    return ETLSettings()
