"""
Competitor Analysis Crew - Análisis de Competencia
=================================================

Este crew se especializa en análisis competitivo, benchmarking
y identificación de oportunidades de diferenciación.
"""

from typing import List
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, WebsiteSearchTool, ScrapeWebsiteTool
from marketing_multiagent.tools.competitor_analysis_tools import (
    CompetitorScannerTool,
    PricingAnalysisTool,
    ContentAuditTool
)


@CrewBase
class CompetitorAnalysisCrew:
    """Competitor Analysis Crew para análisis competitivo integral"""
    
    agents_config = 'config/marketing_agents.yaml'
    tasks_config = 'config/marketing_tasks.yaml'

    @agent
    def competitor_analyst(self) -> Agent:
        """Analista especialista en competencia con herramientas avanzadas"""
        return Agent(
            config=self.agents_config['competitor_analyst'],
            verbose=True,
            tools=[
                SerperDevTool(),
                WebsiteSearchTool(),
                ScrapeWebsiteTool(),
                CompetitorScannerTool(),
                PricingAnalysisTool()
            ],
            max_iter=4,
            allow_delegation=False
        )

    @agent
    def content_analyst(self) -> Agent:
        """Analista especializado en contenido y estrategias de comunicación"""
        return Agent(
            config=self.agents_config['competitor_analyst'],  # Reutiliza config
            verbose=True,
            tools=[
                SerperDevTool(),
                WebsiteSearchTool(),
                ScrapeWebsiteTool(),
                ContentAuditTool()
            ],
            max_iter=3,
            allow_delegation=False
        )

    @task
    def competitive_analysis_task(self) -> Task:
        """Tarea principal de análisis competitivo"""
        return Task(
            config=self.tasks_config['competitive_analysis_task'],
            agent=self.competitor_analyst(),
            output_file='outputs/competitive_analysis_report.md'
        )

    @task
    def competitor_content_analysis_task(self) -> Task:
        """Tarea de análisis de contenido de competidores"""
        return Task(
            config=self.tasks_config['competitor_content_analysis_task'],
            agent=self.content_analyst(),
            output_file='outputs/competitor_content_analysis.md',
            context=[self.competitive_analysis_task()]
        )

    @crew
    def crew(self) -> Crew:
        """Crea el Competitor Analysis Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=True,
            embedder={
                "provider": "openai",
                "config": {
                    "model": "text-embedding-3-small"
                }
            }
        )