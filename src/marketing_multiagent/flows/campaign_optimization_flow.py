"""
Campaign Optimization Flow - Flujo para Optimización de Campañas
===============================================================

Este flow se enfoca en la optimización continua de campañas
activas usando análisis de performance en tiempo real.
"""

from typing import Dict, List, Any
from pydantic import BaseModel, Field
from crewai.flow.flow import Flow, listen, start, router, or_
from crewai import LLM
from marketing_multiagent.tools.analytics_tools import PerformanceTrackerTool, ROICalculatorTool
import json
from datetime import datetime


class CampaignOptimizationState(BaseModel):
    """Estado para optimización de campañas"""
    # Campaign info
    campaign_name: str = ""
    campaign_type: str = ""
    current_budget: float = 0.0
    target_metrics: Dict[str, float] = {}
    
    # Performance data
    current_performance: Dict[str, Any] = {}
    performance_score: float = 0.0
    optimization_opportunities: List[str] = []
    
    # Optimization results
    recommended_changes: Dict[str, Any] = {}
    projected_improvements: Dict[str, Any] = {}
    implementation_priority: str = "medium"
    
    # Control flags
    requires_immediate_action: bool = False
    budget_adjustment_needed: bool = False
    creative_refresh_needed: bool = False


class CampaignOptimizationFlow(Flow[CampaignOptimizationState]):
    """Flow para optimización continua de campañas"""

    @start()
    def analyze_current_performance(self) -> Dict[str, Any]:
        """Analiza el performance actual de la campaña"""
        print(f"📊 Analizando performance de: {self.state.campaign_name}")
        
        try:
            # Simular análisis de performance
            performance_tracker = PerformanceTrackerTool()
            performance_data = performance_tracker._run(
                campaign_name=self.state.campaign_name,
                metrics=["reach", "ctr", "cvr", "cpa", "roas"],
                time_period="last_7_days"
            )
            
            self.state.current_performance = json.loads(performance_data)
            
            # Calcular score de performance
            metrics = self.state.current_performance.get("key_metrics", {})
            score = 0
            
            # Evaluar métricas clave (0-100 scale)
            if "click_through_rate" in metrics:
                ctr_value = float(metrics["click_through_rate"]["value"].rstrip('%'))
                score += min(25, ctr_value * 12.5)  # 2% CTR = 25 points
                
            if "conversion_rate" in metrics:
                cvr_value = float(metrics["conversion_rate"]["value"].rstrip('%'))
                score += min(25, cvr_value * 6.25)  # 4% CVR = 25 points
                
            if "return_on_ad_spend" in metrics:
                roas_value = float(metrics["return_on_ad_spend"]["value"].rstrip('x'))
                score += min(25, roas_value * 7.14)  # 3.5x ROAS = 25 points
                
            # Budget efficiency
            cpa_status = metrics.get("cost_per_acquisition", {}).get("status", "")
            if "objetivo" in cpa_status.lower():
                score += 25
            elif "superando" in cpa_status.lower():
                score += 15
            else:
                score += 10
                
            self.state.performance_score = score
            
            print(f"📈 Score de performance: {score}/100")
            return self.state.current_performance
            
        except Exception as e:
            print(f"❌ Error analizando performance: {str(e)}")
            return {"error": str(e)}

    @router(analyze_current_performance)
    def determine_optimization_urgency(self) -> str:
        """Determina la urgencia de optimización"""
        print("🚨 Evaluando urgencia de optimización...")
        
        # Evaluar múltiples factores de urgencia
        urgency_factors = []
        
        if self.state.performance_score < 40:
            urgency_factors.append("performance_crítico")
            self.state.requires_immediate_action = True
            
        if self.state.performance_score < 60:
            urgency_factors.append("performance_bajo")
            
        # Revisar métricas específicas
        metrics = self.state.current_performance.get("key_metrics", {})
        
        for metric_name, metric_data in metrics.items():
            status = metric_data.get("status", "")
            if "bajo objetivo" in status.lower():
                urgency_factors.append(f"{metric_name}_underperforming")
                
        # Determinar ruta de optimización
        if len(urgency_factors) >= 3 or "performance_crítico" in urgency_factors:
            self.state.implementation_priority = "high"
            print("🔴 Optimización urgente requerida")
            return "urgent_optimization"
        elif len(urgency_factors) >= 1:
            self.state.implementation_priority = "medium"
            print("🟡 Optimización estándar")
            return "standard_optimization"
        else:
            self.state.implementation_priority = "low"
            print("🟢 Optimización preventiva")
            return "preventive_optimization"

    @listen("urgent_optimization")
    def urgent_campaign_fixes(self) -> Dict[str, Any]:
        """Implementa fixes urgentes para campañas críticas"""
        print("🚨 Implementando fixes urgentes...")
        
        urgent_actions = {
            "immediate_actions": [],
            "budget_adjustments": [],
            "creative_changes": [],
            "targeting_modifications": []
        }
        
        metrics = self.state.current_performance.get("key_metrics", {})
        
        # Analizar cada métrica para acciones urgentes
        if metrics.get("cost_per_acquisition", {}).get("status") == "Necesita optimización":
            urgent_actions["immediate_actions"].append("Pausar audiences con CPA >€60")
            urgent_actions["targeting_modifications"].append("Refinar targeting a top performers")
            self.state.budget_adjustment_needed = True
            
        if float(metrics.get("conversion_rate", {}).get("value", "0").rstrip('%')) < 2.0:
            urgent_actions["creative_changes"].append("Implementar nuevos creativos urgente")
            urgent_actions["immediate_actions"].append("A/B test landing pages")
            self.state.creative_refresh_needed = True
            
        if metrics.get("reach", {}).get("status") == "Bajo objetivo":
            urgent_actions["budget_adjustments"].append("Incrementar budget en 20%")
            urgent_actions["targeting_modifications"].append("Expandir audiencias similares")
            
        self.state.recommended_changes = urgent_actions
        
        print("✅ Plan de acción urgente creado")
        return urgent_actions

    @listen("standard_optimization") 
    def standard_campaign_optimization(self) -> Dict[str, Any]:
        """Optimización estándar basada en oportunidades identificadas"""
        print("🔧 Ejecutando optimización estándar...")
        
        optimization_plan = {
            "performance_improvements": [],
            "testing_recommendations": [],
            "budget_reallocation": [],
            "audience_optimization": []
        }
        
        # Analizar oportunidades del performance data
        opportunities = self.state.current_performance.get("optimization_opportunities", [])
        
        for opportunity in opportunities:
            area = opportunity.get("area", "")
            recommendation = opportunity.get("recommendation", "")
            impact = opportunity.get("potential_impact", "")
            
            if "LinkedIn" in area:
                optimization_plan["audience_optimization"].append({
                    "action": recommendation,
                    "expected_impact": impact,
                    "priority": "medium"
                })
            elif "Conversion Rate" in area:
                optimization_plan["testing_recommendations"].append({
                    "action": recommendation,
                    "expected_impact": impact,
                    "priority": "high"
                })
            elif "Audiencia" in area:
                optimization_plan["audience_optimization"].append({
                    "action": recommendation,
                    "expected_impact": impact,
                    "priority": "medium"
                })
        
        # Agregar optimizaciones basadas en benchmarking
        benchmark_data = self.state.current_performance.get("competitive_benchmarking", {})
        if benchmark_data:
            if "Sobre promedio" in benchmark_data.get("our_performance", ""):
                optimization_plan["performance_improvements"].append({
                    "action": "Mantener estrategia actual, escalar investment",
                    "rationale": "Performance sobre promedio de industria"
                })
        
        self.state.recommended_changes = optimization_plan
        
        print("✅ Plan de optimización estándar creado")
        return optimization_plan

    @listen("preventive_optimization")
    def preventive_campaign_enhancement(self) -> Dict[str, Any]:
        """Mejoras preventivas para campañas que funcionan bien"""
        print("🚀 Implementando mejoras preventivas...")
        
        enhancement_plan = {
            "scaling_opportunities": [],
            "innovation_tests": [],
            "efficiency_improvements": [],
            "future_proofing": []
        }
        
        # Oportunidades de scaling para campañas exitosas
        if self.state.performance_score > 75:
            enhancement_plan["scaling_opportunities"].extend([
                {
                    "action": "Incrementar presupuesto gradualmente (+25%)",
                    "rationale": "Alto performance justifica escalado",
                    "monitoring": "Observar ROAS durante scaling"
                },
                {
                    "action": "Expandir a audiencias similares",
                    "rationale": "Encontrar nuevos segmentos rentables",
                    "risk_level": "Bajo"
                }
            ])
            
        # Tests de innovación
        enhancement_plan["innovation_tests"].extend([
            {
                "test": "Nuevos formatos de creative (video, carousel)",
                "goal": "Mejorar engagement y freshness",
                "timeline": "2 semanas"
            },
            {
                "test": "Personalization en ad copy",
                "goal": "Incrementar relevancia y CTR",
                "timeline": "3 semanas"
            }
        ])
        
        # Eficiencias
        enhancement_plan["efficiency_improvements"].extend([
            {
                "area": "Automation",
                "action": "Implementar bidding rules avanzadas",
                "benefit": "Optimización 24/7 automática"
            },
            {
                "area": "Reporting",
                "action": "Dashboard automático de performance",
                "benefit": "Insights más rápidos"
            }
        ])
        
        self.state.recommended_changes = enhancement_plan
        
        print("✅ Plan de mejoras preventivas creado")
        return enhancement_plan

    @listen(or_("urgent_optimization", "standard_optimization", "preventive_optimization"))
    def calculate_projected_impact(self, optimization_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula el impacto proyectado de las optimizaciones"""
        print("📊 Calculando impacto proyectado...")
        
        try:
            # Obtener métricas actuales
            current_metrics = self.state.current_performance.get("key_metrics", {})
            current_cpa = 45.0  # Ejemplo
            current_roas = 3.2  # Ejemplo
            current_cvr = 3.8   # Ejemplo
            
            # Calcular mejoras proyectadas basadas en el tipo de optimización
            if self.state.implementation_priority == "high":
                # Mejoras agresivas para casos urgentes
                projected_improvements = {
                    "cpa_improvement": "15-25%",
                    "roas_improvement": "20-35%", 
                    "cvr_improvement": "10-20%",
                    "confidence_level": "Medium (60-75%)"
                }
            elif self.state.implementation_priority == "medium":
                # Mejoras moderadas para optimización estándar
                projected_improvements = {
                    "cpa_improvement": "8-15%",
                    "roas_improvement": "10-20%",
                    "cvr_improvement": "5-12%",
                    "confidence_level": "High (75-85%)"
                }
            else:
                # Mejoras incrementales para optimización preventiva
                projected_improvements = {
                    "cpa_improvement": "3-8%",
                    "roas_improvement": "5-12%",
                    "cvr_improvement": "2-8%",
                    "confidence_level": "Very High (85-95%)"
                }
            
            # Calcular ROI de la optimización
            roi_calculator = ROICalculatorTool()
            current_investment = self.state.current_budget
            
            # Proyectar revenue con mejoras
            current_revenue = current_investment * current_roas
            improved_roas = current_roas * 1.15  # 15% mejora promedio
            projected_revenue = current_investment * improved_roas
            
            roi_data = roi_calculator._run(
                campaign_investment=current_investment,
                revenue_generated=projected_revenue,
                additional_costs=0,
                time_period="projected_30_days"
            )
            
            projected_improvements["roi_analysis"] = json.loads(roi_data)
            projected_improvements["implementation_timeline"] = self._get_implementation_timeline()
            
            self.state.projected_improvements = projected_improvements
            
            print("✅ Impacto proyectado calculado")
            return projected_improvements
            
        except Exception as e:
            print(f"❌ Error calculando impacto: {str(e)}")
            return {"error": str(e)}

    @listen(calculate_projected_impact)
    def create_implementation_roadmap(self, projected_impact: Dict[str, Any]) -> Dict[str, Any]:
        """Crea roadmap detallado de implementación"""
        print("🗓️ Creando roadmap de implementación...")
        
        implementation_roadmap = {
            "campaign_name": self.state.campaign_name,
            "optimization_summary": {
                "priority_level": self.state.implementation_priority,
                "projected_improvements": projected_impact,
                "implementation_complexity": self._assess_complexity(),
                "resource_requirements": self._assess_resources()
            },
            "phase_1_immediate": {
                "timeline": "0-3 días",
                "actions": self._get_immediate_actions(),
                "success_metrics": ["CPA reduction", "CTR improvement"],
                "risk_level": "Low"
            },
            "phase_2_optimization": {
                "timeline": "1-2 semanas", 
                "actions": self._get_optimization_actions(),
                "success_metrics": ["ROAS improvement", "Conversion rate"],
                "risk_level": "Medium"
            },
            "phase_3_scaling": {
                "timeline": "2-4 semanas",
                "actions": self._get_scaling_actions(),
                "success_metrics": ["Volume growth", "Efficiency maintenance"],
                "risk_level": "Medium-High"
            },
            "monitoring_plan": {
                "daily_checks": ["Budget utilization", "CPA trends"],
                "weekly_reviews": ["Performance vs targets", "Optimization opportunities"],
                "monthly_analysis": ["ROI analysis", "Strategic adjustments"]
            },
            "rollback_plan": {
                "trigger_conditions": ["CPA increase >20%", "ROAS drop >15%"],
                "rollback_actions": ["Revert to previous settings", "Re-evaluate strategy"],
                "recovery_timeline": "24-48 hours"
            }
        }
        
        print("✅ Roadmap de implementación creado")
        print(f"🎯 Prioridad: {self.state.implementation_priority}")
        print(f"📈 Mejora proyectada ROAS: {projected_impact.get('roas_improvement', 'N/A')}")
        
        return implementation_roadmap

    def _get_implementation_timeline(self) -> Dict[str, str]:
        """Determina timeline de implementación basado en prioridad"""
        if self.state.implementation_priority == "high":
            return {
                "immediate_actions": "0-24 horas",
                "full_implementation": "3-5 días",
                "results_visible": "5-7 días"
            }
        elif self.state.implementation_priority == "medium":
            return {
                "immediate_actions": "1-3 días",
                "full_implementation": "1-2 semanas", 
                "results_visible": "2-3 semanas"
            }
        else:
            return {
                "immediate_actions": "3-7 días",
                "full_implementation": "2-4 semanas",
                "results_visible": "4-6 semanas"
            }

    def _assess_complexity(self) -> str:
        """Evalúa complejidad de implementación"""
        factors = 0
        if self.state.budget_adjustment_needed:
            factors += 1
        if self.state.creative_refresh_needed:
            factors += 2
        if len(self.state.optimization_opportunities) > 3:
            factors += 1
            
        if factors >= 3:
            return "High"
        elif factors >= 2:
            return "Medium"
        else:
            return "Low"

    def _assess_resources(self) -> Dict[str, str]:
        """Evalúa recursos necesarios"""
        return {
            "creative_team": "High" if self.state.creative_refresh_needed else "Low",
            "data_analyst": "Medium",
            "campaign_manager": "High",
            "developer": "Low" if not self.state.budget_adjustment_needed else "Medium"
        }

    def _get_immediate_actions(self) -> List[str]:
        """Obtiene acciones inmediatas basadas en análisis"""
        actions = ["Review campaign settings", "Pause underperforming ad sets"]
        
        if self.state.requires_immediate_action:
            actions.extend([
                "Emergency budget reallocation",
                "Pause worst performing creatives",
                "Implement emergency bid adjustments"
            ])
            
        return actions

    def _get_optimization_actions(self) -> List[str]:
        """Obtiene acciones de optimización"""
        return [
            "A/B test new creatives",
            "Refine audience targeting",
            "Optimize bidding strategy",
            "Improve landing page experience"
        ]

    def _get_scaling_actions(self) -> List[str]:
        """Obtiene acciones de escalado"""
        if self.state.performance_score > 70:
            return [
                "Increase budget by 25%",
                "Expand to lookalike audiences",
                "Launch in additional placements",
                "Scale successful creative formats"
            ]
        else:
            return [
                "Conservative budget increase (10%)",
                "Test expansion audiences",
                "Monitor scaling impact closely"
            ]