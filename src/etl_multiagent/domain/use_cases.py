from __future__ import annotations

from ..domain.entities import DataSource, DataBatch, TransformationJob, DataDestination
from ..ports import SourcePort, TransformPort, ValidationPort, DestinationPort


class IngestData:
    def __init__(self, source_port: SourcePort):
        self.source_port = source_port

    def execute(self, source: DataSource) -> DataBatch:
        return self.source_port.read(source)


class TransformData:
    def __init__(self, transform_port: TransformPort):
        self.transform_port = transform_port

    def execute(self, batch: DataBatch, job: TransformationJob) -> DataBatch:
        return self.transform_port.apply(batch, job)


class LoadData:
    def __init__(self, destination_port: DestinationPort):
        self.destination_port = destination_port

    def execute(self, batch: DataBatch, destination: DataDestination) -> dict:
        return self.destination_port.write(batch, destination)


class ReconcileJobResult:
    def __init__(self, validation_port: ValidationPort):
        self.validation_port = validation_port

    def execute(self, batch: DataBatch, rules: dict) -> dict:
        return self.validation_port.validate(batch, rules)
