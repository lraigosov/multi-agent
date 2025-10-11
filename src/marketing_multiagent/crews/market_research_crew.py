"""
Market Research Crew - Investigación de Mercado
===============================================

Este crew se especializa en investigación profunda de mercado,
análisis de audiencia y identificación de oportunidades de mercado.
"""

from typing import List
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, WebsiteSearchTool, ScrapeWebsiteTool
from marketing_multiagent.tools.market_research_tools import (
    TrendAnalysisTool,
    AudienceInsightsTool,
    MarketSizingTool
)


@CrewBase
class MarketResearchCrew:
    """Market Research Crew para análisis de mercado y audiencia"""
    
    agents_config = 'config/marketing_agents.yaml'
    tasks_config = 'config/marketing_tasks.yaml'

    @agent
    def market_researcher(self) -> Agent:
        """Investigador de mercado senior con herramientas especializadas"""
        return Agent(
            config=self.agents_config['market_researcher'],
            verbose=True,
            tools=[
                SerperDevTool(),
                WebsiteSearchTool(),
                TrendAnalysisTool(),
                MarketSizingTool()
            ],
            max_iter=3,
            allow_delegation=False
        )

    @agent
    def audience_analyst(self) -> Agent:
        """Analista especializado en comportamiento de audiencia"""
        return Agent(
            config=self.agents_config['market_researcher'],  # Reutiliza config base
            verbose=True,
            tools=[
                SerperDevTool(),
                AudienceInsightsTool(),
                ScrapeWebsiteTool()
            ],
            max_iter=3,
            allow_delegation=False
        )

    @task
    def market_research_task(self) -> Task:
        """Tarea principal de investigación de mercado"""
        return Task(
            config=self.tasks_config['market_research_task'],
            agent=self.market_researcher(),
            output_file='outputs/market_research_report.md'
        )

    @task
    def audience_research_task(self) -> Task:
        """Tarea de análisis profundo de audiencia"""
        return Task(
            config=self.tasks_config['audience_research_task'],
            agent=self.audience_analyst(),
            output_file='outputs/audience_analysis_report.md',
            context=[self.market_research_task()]  # Usa contexto del research previo
        )

    @crew
    def crew(self) -> Crew:
        """Crea el Market Research Crew"""
        return Crew(
            agents=self.agents,  # Auto-creado por @agent decorator
            tasks=self.tasks,    # Auto-creado por @task decorator
            process=Process.sequential,
            verbose=True,
            memory=True,  # Habilita memoria para contexto entre tareas
            embedder={
                "provider": "openai",
                "config": {
                    "model": "text-embedding-3-small"
                }
            }
        )