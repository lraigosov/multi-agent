"""
Ejemplo 1: Análisis Completo de Marketing para Startup Fintech
============================================================

Este ejemplo demuestra cómo usar el sistema multi-agente para realizar
un análisis completo de marketing para una startup fintech.
"""

import sys
from pathlib import Path

# Agregar el directorio src al path
current_dir = Path(__file__).parent
src_dir = current_dir.parent / "src"
sys.path.insert(0, str(src_dir))

from marketing_multiagent.flows.marketing_intelligence_flow import (
    MarketingIntelligenceFlow,
    MarketingFlowState
)


def fintech_startup_analysis():
    """
    Ejecuta un análisis completo de marketing para una startup fintech
    que quiere lanzar una aplicación de gestión financiera personal.
    """
    
    print("🚀 Iniciando análisis de marketing para startup fintech...")
    
    # Configurar el estado del flow con datos específicos de fintech
    flow_state = MarketingFlowState(
        industry="fintech",
        target_audience="millennials and gen-z professionals aged 25-40",
        marketing_objectives=[
            "increase brand awareness in personal finance space",
            "generate qualified app downloads",
            "build trust and credibility",
            "educate market about financial literacy"
        ],
        budget_range="50000-150000",
        timeline="12 months"
    )
    
    # Datos adicionales específicos del contexto
    flow_state.company_context = {
        "product_type": "personal finance mobile app",
        "key_features": [
            "automated budgeting",
            "investment tracking", 
            "bill management",
            "financial goal setting"
        ],
        "competitive_advantages": [
            "AI-powered insights",
            "user-friendly interface",
            "bank-level security",
            "personalized recommendations"
        ],
        "current_challenges": [
            "low brand recognition",
            "high customer acquisition cost",
            "regulatory compliance complexity",
            "user trust in new financial apps"
        ]
    }
    
    try:
        # Ejecutar el flow de marketing intelligence
        flow = MarketingIntelligenceFlow()
        flow.state = flow_state
        
        print("📊 Ejecutando análisis de mercado...")
        result = flow.kickoff()
        
        print("✅ Análisis completado exitosamente!")
        
        # Mostrar resumen de resultados
        print("\n" + "="*60)
        print("📋 RESUMEN DE ANÁLISIS - STARTUP FINTECH")
        print("="*60)
        
        print(f"🏢 Industria: {flow_state.industry}")
        print(f"🎯 Audiencia: {flow_state.target_audience}")
        print(f"💰 Presupuesto: €{flow_state.budget_range}")
        print(f"⏰ Timeline: {flow_state.timeline}")
        
        print(f"\n📈 Score de Calidad: {flow_state.analysis_quality_score:.1f}/100")
        
        print(f"\n✅ Estados de Completitud:")
        print(f"  • Investigación de Mercado: {'✅' if flow_state.market_research_completed else '❌'}")
        print(f"  • Análisis Competitivo: {'✅' if flow_state.competitive_analysis_completed else '❌'}")
        print(f"  • Estrategia de Contenido: {'✅' if flow_state.content_strategy_completed else '❌'}")
        print(f"  • Estrategia Final: {'✅' if flow_state.final_strategy_completed else '❌'}")
        
        # Guardar resultados detallados
        output_file = "outputs/fintech_startup_analysis.md"
        Path("outputs").mkdir(exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Análisis de Marketing - Startup Fintech\n\n")
            f.write(f"**Fecha de Análisis:** {flow_state.created_at}\n\n")
            f.write(f"## Configuración del Proyecto\n\n")
            f.write(f"- **Industria:** {flow_state.industry}\n")
            f.write(f"- **Audiencia Objetivo:** {flow_state.target_audience}\n")
            f.write(f"- **Presupuesto:** €{flow_state.budget_range}\n")
            f.write(f"- **Timeline:** {flow_state.timeline}\n\n")
            f.write(f"## Resultados del Análisis\n\n")
            f.write(f"**Score de Calidad:** {flow_state.analysis_quality_score:.1f}/100\n\n")
            f.write(f"### Estados de Completitud\n\n")
            f.write(f"- Investigación de Mercado: {'Completado' if flow_state.market_research_completed else 'Pendiente'}\n")
            f.write(f"- Análisis Competitivo: {'Completado' if flow_state.competitive_analysis_completed else 'Pendiente'}\n")
            f.write(f"- Estrategia de Contenido: {'Completado' if flow_state.content_strategy_completed else 'Pendiente'}\n")
            f.write(f"- Estrategia Final: {'Completado' if flow_state.final_strategy_completed else 'Pendiente'}\n\n")
            f.write(f"### Resultado Completo\n\n")
            f.write(f"```\n{str(result)}\n```\n")
        
        print(f"\n📄 Resultados detallados guardados en: {output_file}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error durante el análisis: {str(e)}")
        raise


if __name__ == "__main__":
    # Configurar entorno
    from dotenv import load_dotenv
    load_dotenv()
    
    # Ejecutar análisis
    try:
        result = fintech_startup_analysis()
        print(f"\n🎉 Ejemplo completado exitosamente!")
        print(f"💡 Consulta el archivo outputs/fintech_startup_analysis.md para ver los resultados detallados.")
    except Exception as e:
        print(f"\n❌ Error ejecutando ejemplo: {str(e)}")
        print(f"💡 Asegúrate de que las variables de entorno estén configuradas correctamente.")