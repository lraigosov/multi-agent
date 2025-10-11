"""
Digital Marketing Orchestrator Crew - Coordinación General
=========================================================

Este crew coordina todas las actividades de marketing digital,
integrando insights de otros crews y gestionando la implementación.
"""

from typing import List
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, WebsiteSearchTool
from marketing_multiagent.tools.analytics_tools import (
    PerformanceTrackerTool,
    ROICalculatorTool
)


@CrewBase
class DigitalMarketingCrew:
    """Crew principal para coordinación de marketing digital"""
    
    agents_config = 'config/marketing_agents.yaml'
    tasks_config = 'config/marketing_tasks.yaml'

    @agent
    def marketing_strategist(self) -> Agent:
        """Estratega senior de marketing digital"""
        return Agent(
            config=self.agents_config['marketing_strategist'],
            verbose=True,
            tools=[
                SerperDevTool(),
                WebsiteSearchTool()
            ],
            max_iter=4,
            allow_delegation=True  # Puede coordinar con otros agentes
        )

    @agent
    def campaign_manager(self) -> Agent:
        """Gestor de campañas y coordinación"""
        return Agent(
            config=self.agents_config['campaign_manager'],
            verbose=True,
            tools=[
                SerperDevTool(),
                PerformanceTrackerTool(),
                ROICalculatorTool()
            ],
            max_iter=3,
            allow_delegation=True
        )

    @agent
    def data_analyst(self) -> Agent:
        """Analista de datos y performance"""
        return Agent(
            config=self.agents_config['data_analyst'],
            verbose=True,
            tools=[
                PerformanceTrackerTool(),
                ROICalculatorTool()
            ],
            max_iter=3,
            allow_delegation=False
        )

    @task
    def marketing_strategy_task(self) -> Task:
        """Tarea de desarrollo de estrategia integral"""
        return Task(
            config=self.tasks_config['marketing_strategy_task'],
            agent=self.marketing_strategist(),
            output_file='outputs/marketing_strategy.md'
        )

    @task
    def brand_positioning_task(self) -> Task:
        """Tarea de posicionamiento de marca"""
        return Task(
            config=self.tasks_config['brand_positioning_task'],
            agent=self.marketing_strategist(),
            output_file='outputs/brand_positioning.md',
            context=[self.marketing_strategy_task()]
        )

    @task
    def campaign_planning_task(self) -> Task:
        """Tarea de planificación de campañas"""
        return Task(
            config=self.tasks_config['campaign_planning_task'],
            agent=self.campaign_manager(),
            output_file='outputs/campaign_plan.md'
        )

    @task
    def campaign_coordination_task(self) -> Task:
        """Tarea de coordinación de implementación"""
        return Task(
            config=self.tasks_config['campaign_coordination_task'],
            agent=self.campaign_manager(),
            output_file='outputs/implementation_guide.md',
            context=[self.campaign_planning_task()]
        )

    @task
    def analytics_setup_task(self) -> Task:
        """Tarea de configuración de analytics"""
        return Task(
            config=self.tasks_config['analytics_setup_task'],
            agent=self.data_analyst(),
            output_file='outputs/analytics_setup.md'
        )

    @task
    def performance_analysis_task(self) -> Task:
        """Tarea de análisis de performance"""
        return Task(
            config=self.tasks_config['performance_analysis_task'],
            agent=self.data_analyst(),
            output_file='outputs/performance_framework.md',
            context=[self.analytics_setup_task()]
        )

    @crew
    def crew(self) -> Crew:
        """Crea el Digital Marketing Crew principal"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,  # Proceso jerárquico para coordinación
            manager_llm="gpt-4",  # LLM específico para el manager
            verbose=True,
            memory=True,
            embedder={
                "provider": "openai",
                "config": {
                    "model": "text-embedding-3-small"
                }
            }
        )