from __future__ import annotations

from pathlib import Path
from typing import Any
import pandas as pd

from ..domain.entities import DataBatch, DataDestination


class FileDestinationAdapter:
    def write(self, batch: DataBatch, destination: DataDestination) -> dict[str, Any]:
        path = Path(destination.uri)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        df = batch.raw
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Batch raw data must be pandas DataFrame")
        
        if destination.format == "csv":
            df.to_csv(path, index=False, **destination.options)
        elif destination.format == "parquet":
            df.to_parquet(path, index=False, **destination.options)
        elif destination.format in ("xlsx", "xls"):
            df.to_excel(path, index=False, **destination.options)
        else:
            raise ValueError(f"Unsupported format: {destination.format}")
        
        return {
            "status": "success",
            "path": str(path),
            "rows_written": len(df),
        }


class PostgresDestinationAdapter:
    """Stub for Postgres destination."""
    def write(self, batch: DataBatch, destination: DataDestination) -> dict[str, Any]:
        raise NotImplementedError("Postgres destination requires sqlalchemy + psycopg2")


class BigQueryDestinationAdapter:
    """Stub for BigQuery destination."""
    def write(self, batch: DataBatch, destination: DataDestination) -> dict[str, Any]:
        raise NotImplementedError("BigQuery destination requires google-cloud-bigquery")
