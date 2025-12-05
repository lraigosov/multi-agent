from __future__ import annotations

from crewai import Agent, Task, Crew
from typing import Dict, Any


class ETLOrchestrationCrew:
    """Crew orchestrating ETL agents using hexagonal ports."""
    
    def __init__(self):
        self.orchestrator_agent = Agent(
            role="ETL Orchestrator",
            goal="Coordinate end-to-end ETL pipeline execution",
            backstory="Expert in workflow coordination and ETL patterns",
            verbose=True,
        )
        
        self.source_agent = Agent(
            role="Source Ingestion Specialist",
            goal="Extract data from various sources reliably",
            backstory="Experienced data engineer specializing in data ingestion",
            verbose=True,
        )
        
        self.transform_agent = Agent(
            role="Data Transformation Expert",
            goal="Transform and map data to target schema",
            backstory="Senior ETL developer with expertise in data quality",
            verbose=True,
        )
        
        self.validation_agent = Agent(
            role="Data Quality Analyst",
            goal="Validate data integrity and quality",
            backstory="Data quality specialist ensuring compliance",
            verbose=True,
        )
        
        self.loader_agent = Agent(
            role="Destination Loader",
            goal="Load validated data to target systems",
            backstory="Database and storage expert with deployment experience",
            verbose=True,
        )
    
    def crew(self) -> Crew:
        tasks = [
            Task(
                description="Orchestrate ETL pipeline: parse user request, identify source/dest, coordinate agents",
                expected_output="Execution plan with source, transformations, validations, destination",
                agent=self.orchestrator_agent,
            ),
            Task(
                description="Ingest data from source using appropriate adapter",
                expected_output="DataBatch with raw data, schema, and stats",
                agent=self.source_agent,
            ),
            Task(
                description="Apply transformations and mappings to data batch",
                expected_output="Transformed DataBatch ready for validation",
                agent=self.transform_agent,
            ),
            Task(
                description="Validate data quality and flag issues",
                expected_output="Validation report with status and issues",
                agent=self.validation_agent,
            ),
            Task(
                description="Load validated data to destination",
                expected_output="Load confirmation with rows written and path",
                agent=self.loader_agent,
            ),
        ]
        
        return Crew(
            agents=[
                self.orchestrator_agent,
                self.source_agent,
                self.transform_agent,
                self.validation_agent,
                self.loader_agent,
            ],
            tasks=tasks,
            verbose=True,
        )
