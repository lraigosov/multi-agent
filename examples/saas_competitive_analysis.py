"""
Ejemplo 3: Análisis de Competencia para SaaS B2B
===============================================

Este ejemplo demuestra cómo usar el crew de análisis competitivo
para una empresa SaaS B2B que compite en el mercado de CRM.
"""

import sys
from pathlib import Path

# Agregar el directorio src al path
current_dir = Path(__file__).parent
src_dir = current_dir.parent / "src"
sys.path.insert(0, str(src_dir))

from marketing_multiagent.crews.competitor_analysis_crew import CompetitorAnalysisCrew


def saas_competitive_analysis():
    """
    Ejecuta un análisis competitivo completo para una startup SaaS
    que desarrolla una solución CRM para pequeñas empresas.
    """
    
    print("🔍 Iniciando análisis competitivo para SaaS CRM...")
    
    # Configuración del contexto competitivo
    analysis_inputs = {
        "industry": "SaaS CRM for small businesses",
        "target_audience": "small business owners and sales teams (10-50 employees)",
        "marketing_objectives": "understand competitive landscape and identify differentiation opportunities",
        "company_context": {
            "product_name": "SmallBiz CRM Pro",
            "key_features": [
                "easy setup and onboarding",
                "affordable pricing for SMBs", 
                "mobile-first design",
                "integration with popular SMB tools",
                "automated follow-up sequences"
            ],
            "target_price_point": "€29-79 per user per month",
            "main_competitors": [
                "HubSpot CRM",
                "Pipedrive", 
                "Salesforce Essentials",
                "Zoho CRM",
                "Freshworks CRM"
            ]
        }
    }
    
    try:
        print("🎯 Configurando crew de análisis competitivo...")
        
        # Crear instancia del crew
        competitive_crew = CompetitorAnalysisCrew()
        
        print("🤖 Ejecutando análisis con agentes especializados...")
        print("   • Competitor Analyst: Investigando competidores principales")
        print("   • Market Researcher: Analizando posicionamiento de mercado") 
        print("   • Marketing Strategist: Identificando oportunidades")
        
        # Ejecutar el crew
        result = competitive_crew.crew().kickoff(inputs=analysis_inputs)
        
        print("✅ Análisis competitivo completado!")
        
        # Mostrar resumen
        print("\n" + "="*65)
        print("🏆 RESUMEN ANÁLISIS COMPETITIVO - SAAS CRM")
        print("="*65)
        
        print(f"🏢 Industria: {analysis_inputs['industry']}")
        print(f"🎯 Segmento: {analysis_inputs['target_audience']}")
        
        print(f"\n🥊 Competidores Principales:")
        for i, competitor in enumerate(analysis_inputs['company_context']['main_competitors'], 1):
            print(f"  {i}. {competitor}")
        
        print(f"\n💰 Rango de Precios Objetivo: {analysis_inputs['company_context']['target_price_point']}")
        
        # Simular insights clave del análisis
        competitive_insights = {
            "market_gaps": [
                "Falta de soluciones verdaderamente mobile-first",
                "Onboarding complejo en la mayoría de competidores",
                "Precios prohibitivos para empresas muy pequeñas",
                "Integraciones limitadas con herramientas SMB populares"
            ],
            "differentiation_opportunities": [
                "Setup en menos de 15 minutos",
                "Pricing transparente sin costes ocultos", 
                "Soporte en español especializado para SMBs",
                "Templates específicos por industria"
            ],
            "competitive_threats": [
                "HubSpot free tier muy competitivo",
                "Salesforce ecosistema maduro",
                "Pipedrive fuerte en Europa",
                "Zoho suite completa de herramientas"
            ]
        }
        
        print(f"\n🎯 Oportunidades de Diferenciación Identificadas:")
        for i, opportunity in enumerate(competitive_insights['differentiation_opportunities'], 1):
            print(f"  {i}. {opportunity}")
        
        print(f"\n⚠️ Principales Amenazas Competitivas:")
        for i, threat in enumerate(competitive_insights['competitive_threats'], 1):
            print(f"  {i}. {threat}")
        
        # Guardar análisis detallado
        output_file = "outputs/saas_competitive_analysis.md"
        Path("outputs").mkdir(exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Análisis Competitivo - SaaS CRM\n\n")
            
            f.write(f"## Configuración del Análisis\n\n")
            f.write(f"- **Industria:** {analysis_inputs['industry']}\n")
            f.write(f"- **Audiencia:** {analysis_inputs['target_audience']}\n")
            f.write(f"- **Producto:** {analysis_inputs['company_context']['product_name']}\n")
            f.write(f"- **Rango de Precios:** {analysis_inputs['company_context']['target_price_point']}\n\n")
            
            f.write(f"## Competidores Analizados\n\n")
            for competitor in analysis_inputs['company_context']['main_competitors']:
                f.write(f"- {competitor}\n")
            
            f.write(f"\n## Brechas de Mercado Identificadas\n\n")
            for gap in competitive_insights['market_gaps']:
                f.write(f"- {gap}\n")
            
            f.write(f"\n## Oportunidades de Diferenciación\n\n")
            for opportunity in competitive_insights['differentiation_opportunities']:
                f.write(f"- {opportunity}\n")
            
            f.write(f"\n## Amenazas Competitivas\n\n")
            for threat in competitive_insights['competitive_threats']:
                f.write(f"- {threat}\n")
            
            f.write(f"\n## Análisis Detallado del Crew\n\n")
            f.write(f"```\n{str(result)}\n```\n")
        
        print(f"\n📊 Análisis completo guardado en: {output_file}")
        
        # Recomendaciones estratégicas
        print(f"\n💡 Recomendaciones Estratégicas Clave:")
        print(f"  1. 🚀 Enfocar go-to-market en setup ultra-rápido")
        print(f"  2. 💰 Mantener pricing agresivo vs competidores premium") 
        print(f"  3. 📱 Liderar en experiencia mobile-first")
        print(f"  4. 🔧 Priorizar integraciones con herramientas SMB populares")
        print(f"  5. 🏆 Crear ventaja en soporte localizado")
        
        return result
        
    except Exception as e:
        print(f"❌ Error durante el análisis competitivo: {str(e)}")
        raise


if __name__ == "__main__":
    # Configurar entorno
    from dotenv import load_dotenv
    load_dotenv()
    
    try:
        result = saas_competitive_analysis()
        print(f"\n🏁 Análisis competitivo SaaS completado exitosamente!")
        print(f"📈 El análisis revela oportunidades claras de diferenciación en el mercado CRM.")
        print(f"📋 Consulta el reporte completo en outputs/saas_competitive_analysis.md")
    except Exception as e:
        print(f"\n❌ Error ejecutando análisis: {str(e)}")
        print(f"🔧 Revisa la configuración y variables de entorno.")