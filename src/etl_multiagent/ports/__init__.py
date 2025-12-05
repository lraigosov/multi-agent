from __future__ import annotations

from typing import Protocol, Any

from ..domain.entities import DataSource, DataBatch, TransformationJob, DataDestination


class SourcePort(Protocol):
    def read(self, source: DataSource) -> DataBatch:
        ...


class TransformPort(Protocol):
    def apply(self, batch: DataBatch, job: TransformationJob) -> DataBatch:
        ...


class ValidationPort(Protocol):
    def validate(self, batch: DataBatch, rules: dict[str, Any]) -> dict[str, Any]:
        ...


class DestinationPort(Protocol):
    def write(self, batch: DataBatch, destination: DataDestination) -> dict[str, Any]:
        ...


class OrchestrationPort(Protocol):
    def coordinate(self, workflow: dict[str, Any]) -> dict[str, Any]:
        ...
