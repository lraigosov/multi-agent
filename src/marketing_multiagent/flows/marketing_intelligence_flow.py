"""
Marketing Intelligence Flow - Flujo Principal de Marketing Digital
================================================================

Este flow coordina múltiples crews para crear una estrategia 
integral de marketing digital con análisis completo.
"""

from typing import Dict, List, Any
from pydantic import BaseModel, Field
from crewai.flow.flow import Flow, listen, start, router, or_, and_
from crewai import LLM
from marketing_multiagent.crews.market_research_crew import MarketResearchCrew
from marketing_multiagent.crews.competitor_analysis_crew import CompetitorAnalysisCrew
from marketing_multiagent.crews.content_strategy_crew import ContentStrategyCrew
from marketing_multiagent.crews.digital_marketing_crew import DigitalMarketingCrew
import json
from datetime import datetime


class MarketingFlowState(BaseModel):
    """Estado estructurado para el flujo de marketing"""
    # Inputs iniciales
    industry: str = ""
    target_audience: str = ""
    marketing_objectives: List[str] = []
    budget_range: str = ""
    timeline: str = ""
    
    # Resultados de investigación
    market_research_completed: bool = False
    market_insights: Dict[str, Any] = {}
    audience_analysis: Dict[str, Any] = {}
    
    # Análisis competitivo
    competitive_analysis_completed: bool = False
    competitor_insights: Dict[str, Any] = {}
    positioning_opportunities: List[str] = []
    
    # Estrategia de contenido
    content_strategy_completed: bool = False
    content_plan: Dict[str, Any] = {}
    seo_strategy: Dict[str, Any] = {}
    
    # Estrategia final
    final_strategy_completed: bool = False
    marketing_strategy: Dict[str, Any] = {}
    implementation_plan: Dict[str, Any] = {}
    
    # Control de flujo
    analysis_quality_score: float = 0.0
    requires_deep_analysis: bool = False
    ready_for_implementation: bool = False


class MarketingIntelligenceFlow(Flow[MarketingFlowState]):
    """Flow principal para estrategia de marketing digital"""

    @start()
    def initialize_analysis(self) -> Dict[str, str]:
        """Inicializa el análisis con parámetros del usuario"""
        print("🚀 Iniciando Marketing Intelligence Flow")
        print(f"📊 Analizando industria: {self.state.industry}")
        print(f"🎯 Audiencia objetivo: {self.state.target_audience}")
        
        # Validar inputs críticos
        if not self.state.industry or not self.state.target_audience:
            raise ValueError("Industria y audiencia objetivo son requeridos")
        
        # Preparar contexto para crews
        analysis_context = {
            "industry": self.state.industry,
            "target_audience": self.state.target_audience,
            "marketing_objectives": ", ".join(self.state.marketing_objectives),
            "analysis_start_time": datetime.now().isoformat()
        }
        
        self.state.analysis_quality_score = 0.0
        print("✅ Inicialización completada")
        return analysis_context

    @listen(initialize_analysis)
    def run_market_research(self, analysis_context: Dict[str, str]) -> Dict[str, Any]:
        """Ejecuta investigación de mercado y análisis de audiencia"""
        print("🔍 Iniciando investigación de mercado...")
        
        try:
            # Crear y ejecutar Market Research Crew
            market_crew = MarketResearchCrew()
            research_results = market_crew.crew().kickoff(inputs=analysis_context)
            
            # Procesar resultados
            self.state.market_insights = {
                "research_summary": str(research_results),
                "completion_time": datetime.now().isoformat(),
                "confidence_level": "high"
            }
            
            self.state.market_research_completed = True
            self.state.analysis_quality_score += 25.0
            
            print("✅ Investigación de mercado completada")
            return self.state.market_insights
            
        except Exception as e:
            print(f"❌ Error en investigación de mercado: {str(e)}")
            self.state.market_insights = {"error": str(e)}
            return self.state.market_insights

    @listen(run_market_research)
    def run_competitive_analysis(self, market_insights: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecuta análisis competitivo basado en insights de mercado"""
        print("🏆 Iniciando análisis competitivo...")
        
        try:
            # Preparar contexto enriquecido
            competitive_context = {
                "industry": self.state.industry,
                "target_audience": self.state.target_audience,
                "marketing_objectives": ", ".join(self.state.marketing_objectives),
                "market_context": json.dumps(market_insights) if not isinstance(market_insights, str) else market_insights
            }
            
            # Ejecutar Competitive Analysis Crew
            competitor_crew = CompetitorAnalysisCrew()
            competitive_results = competitor_crew.crew().kickoff(inputs=competitive_context)
            
            self.state.competitor_insights = {
                "analysis_summary": str(competitive_results),
                "completion_time": datetime.now().isoformat(),
                "confidence_level": "high"
            }
            
            self.state.competitive_analysis_completed = True
            self.state.analysis_quality_score += 25.0
            
            print("✅ Análisis competitivo completado")
            return self.state.competitor_insights
            
        except Exception as e:
            print(f"❌ Error en análisis competitivo: {str(e)}")
            self.state.competitor_insights = {"error": str(e)}
            return self.state.competitor_insights

    @router(run_competitive_analysis)
    def evaluate_analysis_depth(self) -> str:
        """Determina si se requiere análisis más profundo"""
        print("🤔 Evaluando calidad del análisis...")
        
        # Evaluar calidad basada en múltiples factores
        has_errors = (
            "error" in self.state.market_insights or 
            "error" in self.state.competitor_insights
        )
        
        quality_threshold = 70.0
        complex_industry = self.state.industry.lower() in [
            "tecnología", "fintech", "healthcare", "artificial intelligence"
        ]
        
        if has_errors or self.state.analysis_quality_score < quality_threshold or complex_industry:
            self.state.requires_deep_analysis = True
            print("📊 Requiere análisis profundo")
            return "deep_analysis"
        else:
            print("✅ Análisis suficiente, procediendo con estrategia")
            return "standard_strategy"

    @listen("deep_analysis")
    def run_deep_market_analysis(self) -> Dict[str, Any]:
        """Ejecuta análisis de mercado más profundo si es necesario"""
        print("🔬 Ejecutando análisis profundo...")
        
        try:
            # Contexto enriquecido para análisis profundo
            deep_context = {
                "industry": self.state.industry,
                "target_audience": self.state.target_audience,
                "marketing_objectives": ", ".join(self.state.marketing_objectives),
                "analysis_type": "deep",
                "previous_insights": json.dumps({
                    "market": self.state.market_insights,
                    "competitive": self.state.competitor_insights
                })
            }
            
            # Re-ejecutar con mayor profundidad
            market_crew = MarketResearchCrew()
            deep_results = market_crew.crew().kickoff(inputs=deep_context)
            
            # Actualizar insights con análisis más profundo
            self.state.market_insights.update({
                "deep_analysis": str(deep_results),
                "analysis_depth": "comprehensive"
            })
            
            self.state.analysis_quality_score = 85.0
            print("✅ Análisis profundo completado")
            return self.state.market_insights
            
        except Exception as e:
            print(f"❌ Error en análisis profundo: {str(e)}")
            return {"error": str(e)}

    @listen(or_("standard_strategy", "deep_analysis"))
    def develop_content_strategy(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Desarrolla estrategia de contenido basada en investigación"""
        print("📝 Desarrollando estrategia de contenido...")
        
        try:
            # Preparar contexto completo
            content_context = {
                "industry": self.state.industry,
                "target_audience": self.state.target_audience,
                "marketing_objectives": ", ".join(self.state.marketing_objectives),
                "market_insights": json.dumps(self.state.market_insights),
                "competitor_insights": json.dumps(self.state.competitor_insights)
            }
            
            # Ejecutar Content Strategy Crew
            content_crew = ContentStrategyCrew()
            content_results = content_crew.crew().kickoff(inputs=content_context)
            
            self.state.content_plan = {
                "strategy_summary": str(content_results),
                "completion_time": datetime.now().isoformat(),
                "integration_level": "full"
            }
            
            self.state.content_strategy_completed = True
            self.state.analysis_quality_score += 25.0
            
            print("✅ Estrategia de contenido completada")
            return self.state.content_plan
            
        except Exception as e:
            print(f"❌ Error en estrategia de contenido: {str(e)}")
            self.state.content_plan = {"error": str(e)}
            return self.state.content_plan

    @listen(develop_content_strategy)
    def create_integrated_strategy(self, content_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Crea la estrategia integrada final y plan de implementación"""
        print("🎯 Creando estrategia integrada...")
        
        try:
            # Contexto completo con todos los insights
            integrated_context = {
                "industry": self.state.industry,
                "target_audience": self.state.target_audience,
                "marketing_objectives": ", ".join(self.state.marketing_objectives),
                "budget_range": self.state.budget_range,
                "timeline": self.state.timeline,
                "market_research": json.dumps(self.state.market_insights),
                "competitive_analysis": json.dumps(self.state.competitor_insights),
                "content_strategy": json.dumps(self.state.content_plan)
            }
            
            # Ejecutar Digital Marketing Crew para estrategia final
            strategy_crew = DigitalMarketingCrew()
            final_strategy = strategy_crew.crew().kickoff(inputs=integrated_context)
            
            self.state.marketing_strategy = {
                "integrated_strategy": str(final_strategy),
                "completion_time": datetime.now().isoformat(),
                "readiness_score": self.state.analysis_quality_score + 25.0
            }
            
            self.state.final_strategy_completed = True
            self.state.ready_for_implementation = True
            
            print("✅ Estrategia integrada completada")
            return self.state.marketing_strategy
            
        except Exception as e:
            print(f"❌ Error en estrategia integrada: {str(e)}")
            self.state.marketing_strategy = {"error": str(e)}
            return self.state.marketing_strategy

    @listen(create_integrated_strategy)
    def finalize_deliverables(self, final_strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Finaliza y organiza todos los entregables"""
        print("📋 Finalizando entregables...")
        
        # Compilar reporte ejecutivo
        executive_summary = {
            "project_overview": {
                "industry": self.state.industry,
                "target_audience": self.state.target_audience,
                "objectives": self.state.marketing_objectives,
                "completion_date": datetime.now().isoformat(),
                "quality_score": self.state.analysis_quality_score
            },
            "key_findings": {
                "market_opportunities": "Extraer de market_insights",
                "competitive_advantages": "Extraer de competitor_insights", 
                "content_recommendations": "Extraer de content_plan",
                "strategic_priorities": "Extraer de marketing_strategy"
            },
            "deliverables": {
                "market_research_report": "outputs/market_research_report.md",
                "competitive_analysis": "outputs/competitive_analysis_report.md",
                "content_strategy": "outputs/content_strategy.md",
                "seo_strategy": "outputs/seo_strategy.md",
                "marketing_strategy": "outputs/marketing_strategy.md",
                "implementation_guide": "outputs/implementation_guide.md"
            },
            "next_steps": [
                "Revisar y aprobar estrategia propuesta",
                "Definir presupuestos específicos por canal",
                "Implementar tracking y measurement framework",
                "Iniciar ejecución por fases según timeline",
                "Establecer reviews regulares de performance"
            ],
            "success_metrics": {
                "awareness": "Reach, brand mentions, share of voice",
                "engagement": "Interacciones, time on site, email engagement",
                "conversion": "Lead generation, sales, ROI",
                "retention": "Customer satisfaction, repeat business, LTV"
            }
        }
        
        self.state.implementation_plan = executive_summary
        
        print("🎉 Flow completado exitosamente!")
        print(f"📊 Score de calidad final: {self.state.analysis_quality_score}")
        
        return {
            "status": "completed",
            "executive_summary": executive_summary,
            "total_analysis_time": "Calculado desde inicio",
            "readiness_for_implementation": self.state.ready_for_implementation
        }