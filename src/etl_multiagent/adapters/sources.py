from __future__ import annotations

from pathlib import Path
from typing import Any
import pandas as pd

from ..domain.entities import DataSource, DataBatch


class FileSourceAdapter:
    def read(self, source: DataSource) -> DataBatch:
        path = Path(source.uri)
        if not path.exists():
            raise FileNotFoundError(f"Source not found: {source.uri}")
        
        if source.format == "csv":
            df = pd.read_csv(path, **source.options)
        elif source.format == "parquet":
            df = pd.read_parquet(path, **source.options)
        elif source.format in ("xlsx", "xls"):
            df = pd.read_excel(path, **source.options)
        else:
            raise ValueError(f"Unsupported format: {source.format}")
        
        return DataBatch(
            raw=df,
            schema={"columns": df.dtypes.to_dict()},
            stats={"rows": len(df), "cols": len(df.columns)},
            metadata={"source": source.uri}
        )


class S3SourceAdapter:
    """Stub for S3/GCS bucket sources."""
    def read(self, source: DataSource) -> DataBatch:
        raise NotImplementedError("S3/GCS sources require boto3/gcsfs integration")


class DatabaseSourceAdapter:
    """Stub for database sources."""
    def read(self, source: DataSource) -> DataBatch:
        raise NotImplementedError("Database sources require sqlalchemy connection")
