from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class DataSource:
    name: str
    kind: str  # e.g., "file", "bucket", "api", "db"
    uri: str
    format: str  # e.g., csv, parquet, xlsx
    options: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DataBatch:
    raw: Any
    schema: Optional[Dict[str, Any]] = None
    stats: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TransformationJob:
    source_schema: Dict[str, Any]
    target_schema: Dict[str, Any]
    mappings: Dict[str, str]
    rules: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class DataDestination:
    name: str
    kind: str  # e.g., "file", "db", "warehouse"
    uri: str
    format: str  # csv, parquet, table
    options: Dict[str, Any] = field(default_factory=dict)
