"""Configuration for ETL domain."""

__all__ = ["settings", "get_settings"]

from .settings import get_settings, ETLSettings

settings = get_settings()
