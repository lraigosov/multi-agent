"""
Analytics Tools - Herramientas de Análisis y Medición
=====================================================

Herramientas especializadas para tracking de performance,
cálculo de ROI y análisis de métricas de marketing.
"""

from typing import Any, Type, Dict, List, Optional
from pydantic import BaseModel, Field
from crewai_tools import BaseTool
import json
from datetime import datetime, timedelta


class PerformanceTrackerInput(BaseModel):
    """Input schema para tracking de performance"""
    campaign_name: str = Field(..., description="Nombre de la campaña a trackear")
    metrics: List[str] = Field(..., description="Métricas a analizar")
    time_period: str = Field(default="last_30_days", description="Período de análisis")


class PerformanceTrackerTool(BaseTool):
    """Herramienta para tracking y análisis de performance de campañas"""
    name: str = "performance_tracker"
    description: str = (
        "Trackea y analiza el rendimiento de campañas de marketing, "
        "proporcionando insights y recomendaciones de optimización."
    )
    args_schema: Type[BaseModel] = PerformanceTrackerInput

    def _run(self, campaign_name: str, metrics: List[str], time_period: str = "last_30_days") -> str:
        """Analiza el performance de campañas"""
        try:
            # Simulación de datos de performance
            performance_data = {
                "campaign_name": campaign_name,
                "analysis_period": time_period,
                "report_date": datetime.now().isoformat(),
                "metrics_analyzed": metrics,
                "overall_performance": {
                    "status": "Bueno",
                    "score": 78,
                    "trend": "Mejorando",
                    "vs_previous_period": "+15%"
                },
                "key_metrics": {
                    "reach": {
                        "value": "125,340",
                        "change": "+22%",
                        "target": "100,000",
                        "status": "Superando objetivo"
                    },
                    "engagement_rate": {
                        "value": "4.2%",
                        "change": "+0.8%",
                        "target": "3.5%",
                        "status": "Superando objetivo"
                    },
                    "click_through_rate": {
                        "value": "2.1%",
                        "change": "+0.3%",
                        "target": "2.0%",
                        "status": "En objetivo"
                    },
                    "conversion_rate": {
                        "value": "3.8%",
                        "change": "-0.2%",
                        "target": "4.0%",
                        "status": "Bajo objetivo"
                    },
                    "cost_per_acquisition": {
                        "value": "€45",
                        "change": "+€5",
                        "target": "€40",
                        "status": "Necesita optimización"
                    },
                    "return_on_ad_spend": {
                        "value": "3.2x",
                        "change": "-0.1x",
                        "target": "3.5x",
                        "status": "Bajo objetivo"
                    }
                },
                "channel_breakdown": {
                    "google_ads": {
                        "spend": "€15,000",
                        "conversions": 387,
                        "cpa": "€38.76",
                        "roas": "4.1x",
                        "performance": "Excelente"
                    },
                    "facebook_ads": {
                        "spend": "€12,000",
                        "conversions": 278,
                        "cpa": "€43.17",
                        "roas": "3.8x",
                        "performance": "Bueno"
                    },
                    "linkedin_ads": {
                        "spend": "€8,000",
                        "conversions": 156,
                        "cpa": "€51.28",
                        "roas": "2.9x",
                        "performance": "Necesita mejora"
                    },
                    "email_marketing": {
                        "spend": "€2,000",
                        "conversions": 234,
                        "cpa": "€8.55",
                        "roas": "8.2x",
                        "performance": "Excelente"
                    }
                },
                "audience_insights": {
                    "top_performing_segments": [
                        "Profesionales 30-45 años",
                        "Gerentes en tecnología",
                        "Usuarios mobile-first"
                    ],
                    "underperforming_segments": [
                        "Audiencia +55 años",
                        "Usuarios desktop-only",
                        "Mercados internacionales"
                    ],
                    "demographic_breakdown": {
                        "age_25_34": "28% de conversiones",
                        "age_35_44": "35% de conversiones", 
                        "age_45_54": "22% de conversiones",
                        "age_55_plus": "15% de conversiones"
                    }
                },
                "temporal_analysis": {
                    "best_performing_days": ["Martes", "Miércoles", "Jueves"],
                    "best_performing_hours": "9-11 AM, 2-4 PM",
                    "seasonal_patterns": "Mayor actividad a mitad de semana",
                    "peak_conversion_times": "Martes 10 AM, Jueves 3 PM"
                },
                "optimization_opportunities": [
                    {
                        "area": "LinkedIn Ads",
                        "issue": "CPA alto vs otras plataformas",
                        "recommendation": "Ajustar targeting, probar nuevos creativos",
                        "potential_impact": "15-20% reducción en CPA"
                    },
                    {
                        "area": "Conversion Rate",
                        "issue": "Bajo performance vs objetivo",
                        "recommendation": "A/B test landing pages, optimizar funnel",
                        "potential_impact": "0.5-1% mejora en CVR"
                    },
                    {
                        "area": "Audiencia +55",
                        "issue": "Baja conversión",
                        "recommendation": "Crear messaging específico, ajustar canales",
                        "potential_impact": "25% mejora en segment performance"
                    }
                ],
                "competitive_benchmarking": {
                    "industry_average_ctr": "1.8%",
                    "our_performance": "2.1% - Sobre promedio",
                    "industry_average_cvr": "3.2%",
                    "our_performance_cvr": "3.8% - Sobre promedio",
                    "industry_average_cpa": "€52",
                    "our_performance_cpa": "€45 - Mejor que promedio"
                },
                "forecasting": {
                    "next_30_days_projection": {
                        "estimated_reach": "140,000",
                        "estimated_conversions": "1,200",
                        "estimated_revenue": "€180,000",
                        "confidence_level": "85%"
                    },
                    "quarter_projection": {
                        "estimated_growth": "18%",
                        "budget_recommendation": "€120,000",
                        "roi_projection": "3.8x"
                    }
                }
            }
            
            return json.dumps(performance_data, indent=2, ensure_ascii=False)
            
        except Exception as e:
            return f"Error en tracking de performance: {str(e)}"


class ROICalculatorInput(BaseModel):
    """Input schema para cálculo de ROI"""
    campaign_investment: float = Field(..., description="Inversión total en la campaña")
    revenue_generated: float = Field(..., description="Revenue generado")
    additional_costs: float = Field(default=0, description="Costos adicionales")
    time_period: str = Field(..., description="Período de análisis")


class ROICalculatorTool(BaseTool):
    """Herramienta para cálculo detallado de ROI y métricas financieras"""
    name: str = "roi_calculator"
    description: str = (
        "Calcula ROI, ROAS y otras métricas financieras de campañas de marketing, "
        "incluyendo análisis de rentabilidad y proyecciones."
    )
    args_schema: Type[BaseModel] = ROICalculatorInput

    def _run(self, campaign_investment: float, revenue_generated: float, additional_costs: float = 0, time_period: str = "") -> str:
        """Calcula métricas de ROI detalladas"""
        try:
            total_costs = campaign_investment + additional_costs
            net_profit = revenue_generated - total_costs
            roi_percentage = (net_profit / total_costs) * 100 if total_costs > 0 else 0
            roas = revenue_generated / campaign_investment if campaign_investment > 0 else 0
            
            roi_analysis = {
                "calculation_date": datetime.now().isoformat(),
                "time_period": time_period,
                "investment_breakdown": {
                    "campaign_investment": f"€{campaign_investment:,.2f}",
                    "additional_costs": f"€{additional_costs:,.2f}",
                    "total_investment": f"€{total_costs:,.2f}"
                },
                "revenue_analysis": {
                    "total_revenue": f"€{revenue_generated:,.2f}",
                    "net_profit": f"€{net_profit:,.2f}",
                    "profit_margin": f"{(net_profit/revenue_generated*100):.1f}%" if revenue_generated > 0 else "N/A"
                },
                "key_metrics": {
                    "roi_percentage": f"{roi_percentage:.1f}%",
                    "roi_ratio": f"{roi_percentage/100 + 1:.2f}:1",
                    "roas": f"{roas:.2f}x",
                    "cost_per_euro_revenue": f"€{campaign_investment/revenue_generated:.3f}" if revenue_generated > 0 else "N/A",
                    "payback_period": "Inmediato" if roi_percentage > 0 else "No alcanzado"
                },
                "performance_rating": {
                    "rating": self._get_roi_rating(roi_percentage),
                    "description": self._get_roi_description(roi_percentage),
                    "industry_benchmark": "ROI promedio industria: 300-500%",
                    "vs_benchmark": "Sobre promedio" if roi_percentage > 300 else "Bajo promedio" if roi_percentage < 300 else "En promedio"
                },
                "detailed_breakdown": {
                    "customer_acquisition": {
                        "estimated_new_customers": int(revenue_generated / 150),  # Asumiendo AOV de €150
                        "customer_acquisition_cost": f"€{total_costs / (revenue_generated / 150):.2f}" if revenue_generated > 0 else "N/A",
                        "lifetime_value_ratio": "3.2:1"  # Típico LTV:CAC ratio
                    },
                    "channel_efficiency": {
                        "cost_efficiency_score": min(100, (roas - 1) * 25) if roas >= 1 else 0,
                        "revenue_efficiency": "Alta" if roas > 4 else "Media" if roas > 2 else "Baja",
                        "scalability_potential": "Alta" if roi_percentage > 200 else "Media" if roi_percentage > 100 else "Baja"
                    }
                },
                "optimization_insights": {
                    "break_even_point": f"€{total_costs:,.2f} en revenue",
                    "target_roi_achievement": f"€{total_costs * 4:,.2f} revenue para 300% ROI",
                    "efficiency_improvements": [
                        "Optimizar targeting para reducir CAC",
                        "Mejorar landing pages para aumentar CVR",
                        "Implementar remarketing para maximizar LTV",
                        "A/B test creativos para mejorar CTR"
                    ]
                },
                "forecasting": {
                    "if_doubled_investment": {
                        "investment": f"€{total_costs * 2:,.2f}",
                        "projected_revenue": f"€{revenue_generated * 1.8:,.2f}",  # Assuming diminishing returns
                        "projected_roi": f"{((revenue_generated * 1.8 - total_costs * 2) / (total_costs * 2) * 100):.1f}%"
                    },
                    "optimal_budget_recommendation": {
                        "recommended_budget": f"€{total_costs * 1.5:,.2f}",
                        "reasoning": "Balance entre eficiencia y escala",
                        "expected_roi": f"{roi_percentage * 0.85:.1f}%"  # Slight decrease due to scaling
                    }
                },
                "risk_analysis": {
                    "risk_level": "Bajo" if roi_percentage > 200 else "Medio" if roi_percentage > 50 else "Alto",
                    "risk_factors": [
                        "Variabilidad estacional" if roi_percentage < 100 else None,
                        "Dependencia de canales específicos" if roas < 2 else None,
                        "Competencia intensificada" if roi_percentage < 150 else None
                    ],
                    "mitigation_strategies": [
                        "Diversificar canales de adquisición",
                        "Implementar testing continuo",
                        "Monitorear métricas leading indicators",
                        "Establecer alertas de performance"
                    ]
                },
                "recommendations": [
                    "Continuar inversión" if roi_percentage > 100 else "Revisar estrategia",
                    "Escalar campañas exitosas" if roas > 3 else "Optimizar antes de escalar",
                    "Implementar attribution modeling" if revenue_generated > 50000 else "Mejorar tracking básico",
                    "Desarrollar testing roadmap" if roi_percentage > 50 else "Revisar fundamentals"
                ]
            }
            
            # Limpiar None values
            roi_analysis["risk_analysis"]["risk_factors"] = [
                factor for factor in roi_analysis["risk_analysis"]["risk_factors"] if factor is not None
            ]
            
            return json.dumps(roi_analysis, indent=2, ensure_ascii=False)
            
        except Exception as e:
            return f"Error calculando ROI: {str(e)}"
    
    def _get_roi_rating(self, roi_percentage: float) -> str:
        """Determina el rating basado en ROI"""
        if roi_percentage >= 500:
            return "Excelente"
        elif roi_percentage >= 300:
            return "Muy Bueno"
        elif roi_percentage >= 150:
            return "Bueno"
        elif roi_percentage >= 50:
            return "Aceptable"
        elif roi_percentage >= 0:
            return "Necesita Mejora"
        else:
            return "Deficiente"
    
    def _get_roi_description(self, roi_percentage: float) -> str:
        """Proporciona descripción del performance"""
        if roi_percentage >= 500:
            return "Performance excepcional, continuar e incrementar inversión"
        elif roi_percentage >= 300:
            return "Excelente retorno, considerar scaling cuidadoso"
        elif roi_percentage >= 150:
            return "Buen retorno, buscar oportunidades de optimización"
        elif roi_percentage >= 50:
            return "Retorno moderado, revisar targeting y creativos"
        elif roi_percentage >= 0:
            return "Cerca del break-even, optimización urgente requerida"
        else:
            return "Pérdidas, revisión completa de estrategia necesaria"