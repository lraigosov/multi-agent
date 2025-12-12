#!/usr/bin/env python3
"""
Marketing Multi-Agent System - Punto de Entrada Principal
========================================================

Sistema completo de marketing digital multi-agente usando CrewAI.
Proporciona análisis integral, estrategia de contenido y optimización de campañas.

Usage:
    python -m marketing_multiagent.main --help
    python -m marketing_multiagent.main analyze --industry "technology" --audience "business professionals"
    python -m marketing_multiagent.main optimize-campaign --name "Q4 Campaign" --budget 50000
"""

import sys
import os
import click
import json
from pathlib import Path
from typing import Dict, List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

# Agregar el directorio src al path
current_dir = Path(__file__).parent
src_dir = current_dir.parent
sys.path.insert(0, str(src_dir))

from marketing_multiagent.flows.marketing_intelligence_flow import (
    MarketingIntelligenceFlow,
    MarketingFlowState
)
from marketing_multiagent.flows.campaign_optimization_flow import (
    CampaignOptimizationFlow,
    CampaignOptimizationState
)
from marketing_multiagent.crews.market_research_crew import MarketResearchCrew
from marketing_multiagent.crews.competitor_analysis_crew import CompetitorAnalysisCrew
from marketing_multiagent.crews.content_strategy_crew import ContentStrategyCrew

console = Console()

def setup_environment():
    """Configura el entorno y carga variables de configuración"""
    from dotenv import load_dotenv
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Crear directorios necesarios
    directories = ["outputs", "outputs/reports", "logs", "temp"]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    console.print("✅ Entorno configurado correctamente", style="green")


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Sistema de Marketing Digital Multi-Agente con CrewAI"""
    setup_environment()


@cli.command()
@click.option("--industry", required=True, help="Industria objetivo (ej: 'technology', 'healthcare')")
@click.option("--audience", required=True, help="Audiencia objetivo (ej: 'business professionals')")
@click.option("--objectives", multiple=True, help="Objetivos de marketing (puede especificar múltiples)")
@click.option("--budget", help="Rango de presupuesto (ej: '10000-50000')")
@click.option("--timeline", help="Timeline del proyecto (ej: '3 months')")
@click.option("--output-format", default="markdown", help="Formato de output: markdown, json, pdf")
def analyze(industry: str, audience: str, objectives: tuple, budget: Optional[str], 
           timeline: Optional[str], output_format: str):
    """Ejecuta análisis completo de marketing digital"""
    
    console.print(Panel.fit(
        f"🚀 Iniciando Análisis de Marketing Digital\n\n"
        f"🏢 Industria: {industry}\n"
        f"🎯 Audiencia: {audience}\n" +
        (f"💰 Presupuesto: {budget}\n" if budget else "") +
        (f"⏰ Timeline: {timeline}\n" if timeline else ""),
        title="Marketing Intelligence Flow"
    ))
    
    try:
        # Configurar estado del flow
        flow_state = MarketingFlowState(
            industry=industry,
            target_audience=audience,
            marketing_objectives=list(objectives) if objectives else [
                "increase brand awareness", 
                "generate qualified leads", 
                "improve conversion rate"
            ],
            budget_range=budget or "25000-75000",
            timeline=timeline or "6 months"
        )
        
        # Ejecutar el flow de marketing intelligence
        flow = MarketingIntelligenceFlow()
        flow.state = flow_state
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Ejecutando análisis completo...", total=None)
            
            try:
                # Iniciar el flow
                result = flow.kickoff()
                progress.update(task, completed=True)
                
                # Mostrar resultados
                console.print("\n🎉 Análisis completado exitosamente!", style="bold green")
                
                # Crear tabla de resumen
                summary_table = Table(title="Resumen de Análisis")
                summary_table.add_column("Componente", style="cyan")
                summary_table.add_column("Estado", style="green")
                summary_table.add_column("Score", style="yellow")
                
                summary_table.add_row(
                    "Investigación de Mercado", 
                    "✅ Completado" if flow_state.market_research_completed else "❌ Error",
                    f"{flow_state.analysis_quality_score:.1f}/100"
                )
                summary_table.add_row(
                    "Análisis Competitivo",
                    "✅ Completado" if flow_state.competitive_analysis_completed else "❌ Error",
                    f"{flow_state.analysis_quality_score:.1f}/100"
                )
                summary_table.add_row(
                    "Estrategia de Contenido",
                    "✅ Completado" if flow_state.content_strategy_completed else "❌ Error",
                    f"{flow_state.analysis_quality_score:.1f}/100"
                )
                summary_table.add_row(
                    "Estrategia Final",
                    "✅ Completado" if flow_state.final_strategy_completed else "❌ Error",
                    f"{flow_state.analysis_quality_score:.1f}/100"
                )
                
                console.print(summary_table)
                
                # Guardar resultados
                output_file = f"outputs/marketing_analysis_{industry.replace(' ', '_')}.{output_format}"
                save_results(result, output_file, output_format)
                
                console.print(f"\n📄 Resultados guardados en: {output_file}")
                
            except Exception as e:
                progress.update(task, completed=True)
                console.print(f"❌ Error durante la ejecución: {str(e)}", style="bold red")
                raise
                
    except Exception as e:
        console.print(f"❌ Error configurando análisis: {str(e)}", style="bold red")
        sys.exit(1)


@cli.command()
@click.option("--name", required=True, help="Nombre de la campaña")
@click.option("--budget", type=float, required=True, help="Presupuesto de la campaña")
@click.option("--type", "campaign_type", default="digital_ads", help="Tipo de campaña")
@click.option("--metrics", multiple=True, help="Métricas a optimizar")
def optimize_campaign(name: str, budget: float, campaign_type: str, metrics: tuple):
    """Optimiza una campaña de marketing existente"""
    
    console.print(Panel.fit(
        f"🎯 Optimizando Campaña de Marketing\n\n"
        f"📊 Campaña: {name}\n"
        f"💰 Presupuesto: €{budget:,.2f}\n"
        f"📈 Tipo: {campaign_type}\n",
        title="Campaign Optimization Flow"
    ))
    
    try:
        # Configurar estado de optimización
        optimization_state = CampaignOptimizationState(
            campaign_name=name,
            campaign_type=campaign_type,
            current_budget=budget,
            target_metrics={metric: 0.0 for metric in metrics} if metrics else {
                "ctr": 2.0,
                "cvr": 3.5,
                "roas": 3.0,
                "cpa": 50.0
            }
        )
        
        # Ejecutar flow de optimización
        flow = CampaignOptimizationFlow()
        flow.state = optimization_state
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Optimizando campaña...", total=None)
            
            try:
                result = flow.kickoff()
                progress.update(task, completed=True)
                
                console.print("\n🎯 Optimización completada!", style="bold green")
                
                # Mostrar recomendaciones
                optimization_table = Table(title="Recomendaciones de Optimización")
                optimization_table.add_column("Área", style="cyan")
                optimization_table.add_column("Prioridad", style="yellow")
                optimization_table.add_column("Impacto Proyectado", style="green")
                
                optimization_table.add_row(
                    "Performance General",
                    optimization_state.implementation_priority.upper(),
                    f"Score: {optimization_state.performance_score:.1f}/100"
                )
                
                if optimization_state.budget_adjustment_needed:
                    optimization_table.add_row(
                        "Ajuste de Presupuesto",
                        "ALTA",
                        "15-25% mejora en eficiencia"
                    )
                
                if optimization_state.creative_refresh_needed:
                    optimization_table.add_row(
                        "Refresh Creativo",
                        "ALTA",
                        "10-20% mejora en engagement"
                    )
                
                console.print(optimization_table)
                
                # Guardar plan de optimización
                output_file = f"outputs/campaign_optimization_{name.replace(' ', '_')}.json"
                save_results(result, output_file, "json")
                
                console.print(f"\n📋 Plan de optimización guardado en: {output_file}")
                
            except Exception as e:
                progress.update(task, completed=True)
                console.print(f"❌ Error durante optimización: {str(e)}", style="bold red")
                raise
                
    except Exception as e:
        console.print(f"❌ Error configurando optimización: {str(e)}", style="bold red")
        sys.exit(1)


@cli.command()
@click.option("--crew", required=True, 
              type=click.Choice(['market-research', 'competitor-analysis', 'content-strategy']),
              help="Tipo de crew a ejecutar")
@click.option("--industry", required=True, help="Industria objetivo")
@click.option("--audience", required=True, help="Audiencia objetivo")
@click.option("--objectives", help="Objetivos específicos")
def run_crew(crew: str, industry: str, audience: str, objectives: Optional[str]):
    """Ejecuta un crew específico de forma independiente"""
    
    console.print(Panel.fit(
        f"🤖 Ejecutando Crew Especializado\n\n"
        f"👥 Crew: {crew}\n"
        f"🏢 Industria: {industry}\n"
        f"🎯 Audiencia: {audience}\n",
        title="Individual Crew Execution"
    ))
    
    # Preparar inputs
    inputs = {
        "industry": industry,
        "target_audience": audience,
        "marketing_objectives": objectives or "general analysis"
    }
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(f"Ejecutando {crew}...", total=None)
            
            # Seleccionar y ejecutar crew
            if crew == "market-research":
                crew_instance = MarketResearchCrew()
                result = crew_instance.crew().kickoff(inputs=inputs)
            elif crew == "competitor-analysis":
                crew_instance = CompetitorAnalysisCrew()
                result = crew_instance.crew().kickoff(inputs=inputs)
            elif crew == "content-strategy":
                crew_instance = ContentStrategyCrew()
                result = crew_instance.crew().kickoff(inputs=inputs)
            
            progress.update(task, completed=True)
            
            console.print(f"\n✅ {crew} ejecutado exitosamente!", style="bold green")
            
            # Guardar resultado
            output_file = f"outputs/{crew}_{industry.replace(' ', '_')}.md"
            save_results(str(result), output_file, "markdown")
            
            console.print(f"📄 Resultado guardado en: {output_file}")
            
    except Exception as e:
        console.print(f"❌ Error ejecutando crew: {str(e)}", style="bold red")
        sys.exit(1)


@cli.command()
def list_examples():
    """Muestra ejemplos de uso del sistema"""
    
    console.print(Panel.fit(
        "📚 Ejemplos de Uso del Sistema\n\n"
        "1. Análisis Completo de Marketing:\n"
        "   marketing-multiagent analyze --industry 'technology' --audience 'business professionals'\n\n"
        "2. Optimización de Campaña:\n"
        "   marketing-multiagent optimize-campaign --name 'Q4 Campaign' --budget 50000\n\n"
        "3. Ejecutar Crew Específico:\n"
        "   marketing-multiagent run-crew --crew market-research --industry 'fintech' --audience 'startups'\n\n"
        "4. Análisis con Objetivos Específicos:\n"
        "   marketing-multiagent analyze --industry 'healthcare' --audience 'medical professionals' \\\n"
        "                                --objectives 'lead generation' --objectives 'brand awareness'\n\n"
        "5. Ver Estado del Sistema:\n"
        "   marketing-multiagent status\n",
        title="Guía de Uso"
    ))


@cli.command()
def status():
    """Muestra el estado del sistema y configuración"""
    
    console.print(Panel.fit("🔍 Verificando Estado del Sistema...", title="System Status"))
    
    status_table = Table(title="Estado de Configuración")
    status_table.add_column("Componente", style="cyan")
    status_table.add_column("Estado", style="green")
    status_table.add_column("Detalles")
    
    # Verificar variables de entorno
    env_vars = ["OPENAI_API_KEY", "SERPER_API_KEY"]
    for var in env_vars:
        value = os.getenv(var)
        if value:
            status_table.add_row(var, "✅ Configurado", "(hidden)")
        else:
            status_table.add_row(var, "❌ Faltante", "No configurado")
    
    # Verificar directorios
    directories = ["outputs", "logs", "temp"]
    for directory in directories:
        if Path(directory).exists():
            status_table.add_row(f"Directorio {directory}", "✅ Existe", str(Path(directory).absolute()))
        else:
            status_table.add_row(f"Directorio {directory}", "❌ Faltante", "Necesita crearse")
    
    console.print(status_table)


def save_results(data, output_file: str, format_type: str):
    """Guarda los resultados en el formato especificado"""
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        if format_type == "json":
            if isinstance(data, str):
                # Intentar parsear como JSON si es string
                try:
                    data = json.loads(data)
                except json.JSONDecodeError:
                    data = {"result": data}
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        elif format_type == "markdown":
            with open(output_path, 'w', encoding='utf-8') as f:
                if isinstance(data, dict):
                    f.write(f"# Resultado de Análisis\n\n")
                    f.write(f"**Fecha:** {json.dumps(data, ensure_ascii=False, indent=2)}\n\n")
                else:
                    f.write(str(data))
                    
        else:  # default to text
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(str(data))
                
    except Exception as e:
        console.print(f"❌ Error guardando archivo: {str(e)}", style="red")


def main():
    """Punto de entrada principal"""
    try:
        cli()
    except KeyboardInterrupt:
        console.print("\n👋 Operación cancelada por el usuario", style="yellow")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n❌ Error inesperado: {str(e)}", style="bold red")
        sys.exit(1)


if __name__ == "__main__":
    main()