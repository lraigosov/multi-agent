"""
Content Strategy Crew - Estrategia de Contenido
==============================================

Este crew se especializa en estrategia de contenido,
creación de calendarios editoriales y optimización SEO.
"""

from typing import List
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, WebsiteSearchTool, ScrapeWebsiteTool
from marketing_multiagent.tools.content_tools import (
    ContentIdeaGeneratorTool,
    SEOOptimizationTool,
    TrendingTopicsTool
)


@CrewBase
class ContentStrategyCrew:
    """Content Strategy Crew para estrategia integral de contenido"""
    
    agents_config = 'config/marketing_agents.yaml'
    tasks_config = 'config/marketing_tasks.yaml'

    @agent
    def content_creator(self) -> Agent:
        """Director creativo de contenido con herramientas especializadas"""
        return Agent(
            config=self.agents_config['content_creator'],
            verbose=True,
            tools=[
                SerperDevTool(),
                WebsiteSearchTool(),
                ContentIdeaGeneratorTool(),
                TrendingTopicsTool()
            ],
            max_iter=3,
            allow_delegation=True  # Puede delegar tareas específicas
        )

    @agent
    def seo_specialist(self) -> Agent:
        """Especialista SEO para optimización de contenido"""
        return Agent(
            config=self.agents_config['seo_specialist'],
            verbose=True,
            tools=[
                SerperDevTool(),
                WebsiteSearchTool(),
                ScrapeWebsiteTool(),
                SEOOptimizationTool()
            ],
            max_iter=3,
            allow_delegation=False
        )

    @agent
    def copywriter(self) -> Agent:
        """Copywriter especializado en conversión"""
        return Agent(
            config=self.agents_config['copywriter'],
            verbose=True,
            tools=[
                SerperDevTool(),
                WebsiteSearchTool()
            ],
            max_iter=2,
            allow_delegation=False
        )

    @task
    def content_strategy_task(self) -> Task:
        """Tarea de desarrollo de estrategia de contenido"""
        return Task(
            config=self.tasks_config['content_strategy_task'],
            agent=self.content_creator(),
            output_file='outputs/content_strategy.md'
        )

    @task
    def content_calendar_task(self) -> Task:
        """Tarea de creación de calendario editorial"""
        return Task(
            config=self.tasks_config['content_calendar_task'],
            agent=self.content_creator(),
            output_file='outputs/content_calendar.md',
            context=[self.content_strategy_task()]
        )

    @task
    def seo_strategy_task(self) -> Task:
        """Tarea de estrategia SEO integral"""
        return Task(
            config=self.tasks_config['seo_strategy_task'],
            agent=self.seo_specialist(),
            output_file='outputs/seo_strategy.md'
        )

    @task
    def keyword_research_task(self) -> Task:
        """Tarea de investigación de palabras clave"""
        return Task(
            config=self.tasks_config['keyword_research_task'],
            agent=self.seo_specialist(),
            output_file='outputs/keyword_research.md',
            context=[self.seo_strategy_task()]
        )

    @task
    def copy_strategy_task(self) -> Task:
        """Tarea de estrategia de copy y messaging"""
        return Task(
            config=self.tasks_config['copy_strategy_task'],
            agent=self.copywriter(),
            output_file='outputs/copy_strategy.md'
        )

    @task
    def conversion_copy_task(self) -> Task:
        """Tarea de creación de copy de conversión"""
        return Task(
            config=self.tasks_config['conversion_copy_task'],
            agent=self.copywriter(),
            output_file='outputs/conversion_copy.md',
            context=[self.copy_strategy_task()]
        )

    @crew
    def crew(self) -> Crew:
        """Crea el Content Strategy Crew"""
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