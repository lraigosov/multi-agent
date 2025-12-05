from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, Any
from crewai.flow.flow import Flow, listen, start

from ..domain.entities import DataSource, DataBatch, TransformationJob, DataDestination
from ..domain.use_cases import IngestData, TransformData, LoadData, ReconcileJobResult
from ..adapters.sources import FileSourceAdapter
from ..adapters.destinations import FileDestinationAdapter
from ..adapters.transformers import PandasTransformAdapter, ValidationAdapter


@dataclass
class ETLFlowState:
    source_uri: str
    source_format: str
    dest_uri: str
    dest_format: str
    mappings: Dict[str, str]
    target_schema: Dict[str, str]
    
    batch: Optional[DataBatch] = None
    validation_report: Optional[Dict[str, Any]] = None
    load_result: Optional[Dict[str, Any]] = None
    errors: list[str] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []


class ETLPipelineFlow(Flow[ETLFlowState]):
    """Flow orchestrating ETL pipeline using use cases and adapters."""
    
    @start()
    def ingest_source(self):
        source = DataSource(
            name="user_source",
            kind="file",
            uri=self.state.source_uri,
            format=self.state.source_format,
        )
        
        use_case = IngestData(source_port=FileSourceAdapter())
        try:
            self.state.batch = use_case.execute(source)
        except Exception as e:
            self.state.errors.append(f"Ingestion failed: {e}")
    
    @listen(ingest_source)
    def transform_data(self):
        if self.state.batch is None:
            self.state.errors.append("No batch to transform")
            return
        
        job = TransformationJob(
            source_schema=self.state.batch.schema or {},
            target_schema=self.state.target_schema,
            mappings=self.state.mappings,
        )
        
        use_case = TransformData(transform_port=PandasTransformAdapter())
        try:
            self.state.batch = use_case.execute(self.state.batch, job)
        except Exception as e:
            self.state.errors.append(f"Transformation failed: {e}")
    
    @listen(transform_data)
    def validate_quality(self):
        if self.state.batch is None:
            self.state.errors.append("No batch to validate")
            return
        
        use_case = ReconcileJobResult(validation_port=ValidationAdapter())
        try:
            self.state.validation_report = use_case.execute(
                self.state.batch,
                rules={"check_nulls": True, "check_duplicates": True}
            )
        except Exception as e:
            self.state.errors.append(f"Validation failed: {e}")
    
    @listen(validate_quality)
    def load_destination(self):
        if self.state.batch is None:
            self.state.errors.append("No batch to load")
            return
        
        destination = DataDestination(
            name="user_destination",
            kind="file",
            uri=self.state.dest_uri,
            format=self.state.dest_format,
        )
        
        use_case = LoadData(destination_port=FileDestinationAdapter())
        try:
            self.state.load_result = use_case.execute(self.state.batch, destination)
        except Exception as e:
            self.state.errors.append(f"Load failed: {e}")
