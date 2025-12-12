from __future__ import annotations

from typing import Any
import pandas as pd

from ..domain.entities import DataBatch, TransformationJob


class PandasTransformAdapter:
    def apply(self, batch: DataBatch, job: TransformationJob) -> DataBatch:
        df = batch.raw
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Batch raw data must be pandas DataFrame")
        
        # Apply column mappings
        df_transformed = df.copy()
        for target_col, source_col in job.mappings.items():
            if source_col in df_transformed.columns:
                df_transformed[target_col] = df_transformed[source_col]
        
        # Apply transformation rules (simple example: type casting)
        for col, dtype in job.target_schema.items():
            if col in df_transformed.columns:
                try:
                    df_transformed[col] = df_transformed[col].astype(dtype)
                except Exception:
                    pass  # Skip errors for now
        
        return DataBatch(
            raw=df_transformed,
            schema={"columns": df_transformed.dtypes.to_dict()},
            stats={"rows": len(df_transformed), "cols": len(df_transformed.columns)},
            metadata={**batch.metadata, "transformed": True}
        )


class ValidationAdapter:
    def validate(self, batch: DataBatch, rules: dict[str, Any]) -> dict[str, Any]:
        df = batch.raw
        if not isinstance(df, pd.DataFrame):
            return {"status": "error", "message": "Batch is not DataFrame"}
        
        issues = []
        
        # Check for nulls
        if rules.get("check_nulls"):
            null_counts = df.isnull().sum()
            for col, count in null_counts.items():
                if count > 0:
                    issues.append(f"{col}: {count} null values")
        
        # Check for duplicates
        if rules.get("check_duplicates"):
            dup_count = df.duplicated().sum()
            if dup_count > 0:
                issues.append(f"{dup_count} duplicate rows found")
        
        return {
            "status": "pass" if not issues else "warning",
            "issues": issues,
            "rows_validated": len(df),
        }
