"""
Ejemplo 2: Optimización de Campaña E-commerce
============================================

Este ejemplo muestra cómo optimizar una campaña de marketing digital
para una tienda de e-commerce con problemas de conversión.
"""

import sys
from pathlib import Path

# Agregar el directorio src al path
current_dir = Path(__file__).parent
src_dir = current_dir.parent / "src"
sys.path.insert(0, str(src_dir))

from marketing_multiagent.flows.campaign_optimization_flow import (
    CampaignOptimizationFlow,
    CampaignOptimizationState
)


def ecommerce_campaign_optimization():
    """
    Optimiza una campaña de Google Ads para e-commerce con bajo ROI.
    """
    
    print("🎯 Iniciando optimización de campaña e-commerce...")
    
    # Datos de la campaña actual
    campaign_data = {
        "name": "Holiday Season 2024 - Fashion Collection",
        "type": "google_ads_shopping",
        "budget": 75000,  # €75,000 mensuales
        "current_metrics": {
            "impressions": 850000,
            "clicks": 12750,
            "conversions": 382,
            "revenue": 28650,
            "ctr": 1.5,  # Click Through Rate
            "cvr": 3.0,  # Conversion Rate  
            "roas": 0.38,  # Return on Ad Spend
            "cpa": 196.34  # Cost Per Acquisition
        },
        "target_metrics": {
            "ctr": 2.5,
            "cvr": 5.0,
            "roas": 3.0,
            "cpa": 50.0
        }
    }
    
    # Configurar estado de optimización
    optimization_state = CampaignOptimizationState(
        campaign_name=campaign_data["name"],
        campaign_type=campaign_data["type"],
        current_budget=campaign_data["budget"],
        target_metrics=campaign_data["target_metrics"]
    )
    
    # Añadir contexto específico
    optimization_state.current_performance = campaign_data["current_metrics"]
    optimization_state.industry_context = {
        "industry": "fashion e-commerce",
        "peak_season": "holiday season",
        "main_products": [
            "winter coats and jackets",
            "holiday party dresses", 
            "winter accessories",
            "gift items under €100"
        ],
        "main_challenges": [
            "high competition during holidays",
            "price-sensitive customers",
            "seasonal inventory management",
            "mobile optimization issues"
        ]
    }
    
    try:
        # Ejecutar flow de optimización
        flow = CampaignOptimizationFlow()
        flow.state = optimization_state
        
        print("🔄 Analizando performance actual...")
        print(f"📊 ROAS actual: {campaign_data['current_metrics']['roas']:.2f}")
        print(f"🎯 ROAS objetivo: {campaign_data['target_metrics']['roas']:.2f}")
        
        result = flow.kickoff()
        
        print("✅ Optimización completada!")
        
        # Mostrar resumen de optimización
        print("\n" + "="*70)
        print("📈 RESUMEN DE OPTIMIZACIÓN - CAMPAÑA E-COMMERCE")
        print("="*70)
        
        print(f"🛍️ Campaña: {optimization_state.campaign_name}")
        print(f"💰 Presupuesto: €{optimization_state.current_budget:,.2f}")
        print(f"📈 Score de Performance: {optimization_state.performance_score:.1f}/100")
        print(f"🚨 Prioridad de Implementación: {optimization_state.implementation_priority.upper()}")
        
        print(f"\n🔧 Ajustes Recomendados:")
        print(f"  • Ajuste de Presupuesto: {'✅ Necesario' if optimization_state.budget_adjustment_needed else '❌ No requerido'}")
        print(f"  • Refresh Creativo: {'✅ Necesario' if optimization_state.creative_refresh_needed else '❌ No requerido'}")
        
        # Calcular mejoras proyectadas
        current_roas = campaign_data['current_metrics']['roas']
        target_roas = campaign_data['target_metrics']['roas']
        improvement_potential = ((target_roas - current_roas) / current_roas) * 100
        
        print(f"\n💡 Impacto Proyectado:")
        print(f"  • Mejora en ROAS: +{improvement_potential:.1f}%")
        print(f"  • Revenue Adicional Estimado: €{(target_roas - current_roas) * optimization_state.current_budget:,.2f}")
        
        # Guardar plan de optimización detallado
        output_file = "outputs/ecommerce_campaign_optimization.md"
        Path("outputs").mkdir(exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Plan de Optimización - Campaña E-commerce\n\n")
            f.write(f"## Información de la Campaña\n\n")
            f.write(f"- **Nombre:** {optimization_state.campaign_name}\n")
            f.write(f"- **Tipo:** {optimization_state.campaign_type}\n")
            f.write(f"- **Presupuesto:** €{optimization_state.current_budget:,.2f}\n\n")
            
            f.write(f"## Métricas Actuales vs Objetivos\n\n")
            f.write(f"| Métrica | Actual | Objetivo | Gap |\n")
            f.write(f"|---------|--------|----------|-----|\n")
            for metric, target in campaign_data['target_metrics'].items():
                current = campaign_data['current_metrics'].get(metric, 0)
                gap = ((target - current) / current * 100) if current > 0 else 0
                f.write(f"| {metric.upper()} | {current:.2f} | {target:.2f} | {gap:+.1f}% |\n")
            
            f.write(f"\n## Análisis de Performance\n\n")
            f.write(f"**Score General:** {optimization_state.performance_score:.1f}/100\n\n")
            f.write(f"**Prioridad:** {optimization_state.implementation_priority}\n\n")
            
            f.write(f"## Recomendaciones Detalladas\n\n")
            f.write(f"{str(result)}\n")
        
        print(f"\n📋 Plan de optimización guardado en: {output_file}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error durante la optimización: {str(e)}")
        raise


if __name__ == "__main__":
    # Configurar entorno
    from dotenv import load_dotenv
    load_dotenv()
    
    try:
        result = ecommerce_campaign_optimization()
        print(f"\n🎊 Ejemplo de optimización completado!")
        print(f"📊 La campaña tiene potencial para mejorar significativamente su ROAS.")
        print(f"💼 Consulta el plan detallado en outputs/ecommerce_campaign_optimization.md")
    except Exception as e:
        print(f"\n❌ Error ejecutando optimización: {str(e)}")
        print(f"💡 Verifica la configuración de las variables de entorno.")