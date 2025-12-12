"""
Ejemplo 4: Estrategia de Contenido para Empresa de Salud Digital
==============================================================

Este ejemplo muestra cómo desarrollar una estrategia de contenido completa
para una empresa de telemedicina usando el crew especializado.
"""

import sys
from pathlib import Path

# Agregar el directorio src al path
current_dir = Path(__file__).parent
src_dir = current_dir.parent / "src"
sys.path.insert(0, str(src_dir))

from marketing_multiagent.crews.content_strategy_crew import ContentStrategyCrew


def healthtech_content_strategy():
    """
    Desarrolla una estrategia de contenido integral para una plataforma
    de telemedicina que busca educar y generar confianza en su audiencia.
    """
    
    print("📝 Iniciando desarrollo de estrategia de contenido para HealthTech...")
    
    # Configuración del contexto de contenido
    content_inputs = {
        "industry": "digital health and telemedicine",
        "target_audience": "patients seeking convenient healthcare access and healthcare providers looking for digital solutions",
        "marketing_objectives": "build trust, educate market, generate qualified leads, establish thought leadership",
        "content_context": {
            "company_name": "TeleMed Connect",
            "services": [
                "virtual consultations with doctors",
                "mental health therapy sessions",
                "chronic disease management",
                "prescription management",
                "health monitoring integration"
            ],
            "target_demographics": {
                "primary": "working professionals aged 25-45",
                "secondary": "elderly patients with mobility issues",
                "tertiary": "healthcare providers seeking efficiency"
            },
            "content_goals": [
                "educate about telemedicine benefits",
                "address privacy and security concerns", 
                "showcase success stories",
                "provide health tips and insights",
                "build medical credibility"
            ],
            "compliance_requirements": [
                "HIPAA compliance",
                "medical accuracy verification",
                "patient privacy protection",
                "regulatory advertising guidelines"
            ]
        }
    }
    
    try:
        print("👥 Configurando crew de estrategia de contenido...")
        
        # Crear instancia del crew
        content_crew = ContentStrategyCrew()
        
        print("🎬 Ejecutando desarrollo de estrategia con agentes especializados...")
        print("   • Content Strategist: Planificando arquitectura de contenido")
        print("   • SEO Specialist: Optimizando para búsqueda médica")
        print("   • Copywriter: Desarrollando messaging clave")
        print("   • Social Media Specialist: Creando estrategia multi-canal")
        
        # Ejecutar el crew
        result = content_crew.crew().kickoff(inputs=content_inputs)
        
        print("✅ Estrategia de contenido completada!")
        
        # Mostrar resumen estratégico
        print("\n" + "="*70)
        print("🏥 ESTRATEGIA DE CONTENIDO - TELEMEDICINA")
        print("="*70)
        
        print(f"🏢 Empresa: {content_inputs['content_context']['company_name']}")
        print(f"🎯 Industria: {content_inputs['industry']}")
        print(f"👥 Audiencias: {len(content_inputs['content_context']['target_demographics'])} segmentos")
        
        # Simular estrategia de contenido desarrollada
        content_strategy = {
            "content_pillars": [
                {
                    "name": "Educación en Telemedicina",
                    "description": "Contenido educativo sobre beneficios y uso de telemedicina",
                    "percentage": 30,
                    "formats": ["blog posts", "infografías", "videos explicativos"]
                },
                {
                    "name": "Historias de Éxito de Pacientes",
                    "description": "Testimonios y casos de uso reales (con privacidad)",
                    "percentage": 25,
                    "formats": ["case studies", "video testimoniales", "posts en redes"]
                },
                {
                    "name": "Insights Médicos y Wellness",
                    "description": "Consejos de salud y información médica confiable",
                    "percentage": 25,
                    "formats": ["artículos médicos", "webinars", "newsletters"]
                },
                {
                    "name": "Innovación en Salud Digital", 
                    "description": "Tendencias y avances en tecnología médica",
                    "percentage": 20,
                    "formats": ["whitepapers", "podcasts", "eventos virtuales"]
                }
            ],
            "content_calendar": {
                "weekly_frequency": {
                    "blog_posts": 2,
                    "social_media_posts": 5,
                    "newsletter": 1,
                    "video_content": 1
                },
                "monthly_special": [
                    "webinar educativo",
                    "whitepaper sobre tendencias",
                    "case study detallado"
                ]
            },
            "seo_strategy": {
                "primary_keywords": [
                    "telemedicina españa",
                    "consulta médica online",
                    "médico virtual",
                    "teleconsulta segura"
                ],
                "content_clusters": [
                    "beneficios telemedicina",
                    "seguridad datos médicos", 
                    "consultas virtuales efectivas",
                    "salud digital tendencias"
                ]
            }
        }
        
        print(f"\n📊 Pilares de Contenido Desarrollados:")
        for i, pillar in enumerate(content_strategy['content_pillars'], 1):
            print(f"  {i}. {pillar['name']} ({pillar['percentage']}%)")
            print(f"     └ {pillar['description']}")
        
        print(f"\n📅 Frecuencia de Publicación Recomendada:")
        for content_type, frequency in content_strategy['content_calendar']['weekly_frequency'].items():
            print(f"  • {content_type.replace('_', ' ').title()}: {frequency}x por semana")
        
        print(f"\n🔍 Palabras Clave SEO Principales:")
        for keyword in content_strategy['seo_strategy']['primary_keywords']:
            print(f"  • {keyword}")
        
        # Guardar estrategia completa
        output_file = "outputs/healthtech_content_strategy.md"
        Path("outputs").mkdir(exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Estrategia de Contenido - {content_inputs['content_context']['company_name']}\n\n")
            
            f.write(f"## Resumen Ejecutivo\n\n")
            f.write(f"Estrategia de contenido integral para posicionar a {content_inputs['content_context']['company_name']} ")
            f.write(f"como líder confiable en el sector de telemedicina.\n\n")
            
            f.write(f"## Audiencias Objetivo\n\n")
            for segment, description in content_inputs['content_context']['target_demographics'].items():
                f.write(f"**{segment.title()}:** {description}\n\n")
            
            f.write(f"## Pilares de Contenido\n\n")
            for pillar in content_strategy['content_pillars']:
                f.write(f"### {pillar['name']} ({pillar['percentage']}%)\n\n")
                f.write(f"{pillar['description']}\n\n")
                f.write(f"**Formatos:** {', '.join(pillar['formats'])}\n\n")
            
            f.write(f"## Calendario Editorial\n\n")
            f.write(f"### Frecuencia Semanal\n\n")
            for content_type, frequency in content_strategy['content_calendar']['weekly_frequency'].items():
                f.write(f"- **{content_type.replace('_', ' ').title()}:** {frequency} publicaciones\n")
            
            f.write(f"\n### Contenido Especial Mensual\n\n")
            for special in content_strategy['content_calendar']['monthly_special']:
                f.write(f"- {special.title()}\n")
            
            f.write(f"\n## Estrategia SEO\n\n")
            f.write(f"### Palabras Clave Principales\n\n")
            for keyword in content_strategy['seo_strategy']['primary_keywords']:
                f.write(f"- {keyword}\n")
            
            f.write(f"\n### Clusters de Contenido\n\n")
            for cluster in content_strategy['seo_strategy']['content_clusters']:
                f.write(f"- {cluster}\n")
            
            f.write(f"\n## Consideraciones de Compliance\n\n")
            for requirement in content_inputs['content_context']['compliance_requirements']:
                f.write(f"- {requirement}\n")
            
            f.write(f"\n## Análisis Detallado del Crew\n\n")
            f.write(f"```\n{str(result)}\n```\n")
        
        print(f"\n📋 Estrategia completa guardada en: {output_file}")
        
        # Métricas de éxito sugeridas
        print(f"\n📈 KPIs Recomendados para Seguimiento:")
        print(f"  📊 Métricas de Contenido:")
        print(f"    • Tiempo de permanencia en blog: >2 min")
        print(f"    • Tasa de engagement en redes: >4%") 
        print(f"    • Downloads de whitepapers: >100/mes")
        print(f"  🔍 Métricas SEO:")
        print(f"    • Ranking top 10 para keywords principales")
        print(f"    • Tráfico orgánico: +25% en 6 meses")
        print(f"  💼 Métricas de Negocio:")
        print(f"    • Leads calificados desde contenido: +40%")
        print(f"    • Conversión contenido → demo: >8%")
        
        return result
        
    except Exception as e:
        print(f"❌ Error durante desarrollo de estrategia: {str(e)}")
        raise


if __name__ == "__main__":
    # Configurar entorno
    from dotenv import load_dotenv
    load_dotenv()
    
    try:
        result = healthtech_content_strategy()
        print(f"\n🎯 Estrategia de contenido HealthTech completada!")
        print(f"📚 Se ha desarrollado una estrategia integral con 4 pilares de contenido.")
        print(f"📋 La estrategia incluye compliance médico y optimización SEO especializada.")
        print(f"📊 Consulta el plan detallado en outputs/healthtech_content_strategy.md")
    except Exception as e:
        print(f"\n❌ Error ejecutando estrategia: {str(e)}")
        print(f"🔧 Verifica la configuración del entorno.")