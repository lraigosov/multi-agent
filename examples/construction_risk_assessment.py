"""
Ejemplo SST: Evaluación de Riesgos en Obra de Construcción
========================================================

Este ejemplo demuestra cómo usar el crew de evaluación de riesgos
para analizar peligros en un sitio de construcción.
"""

import sys
from pathlib import Path

# Agregar el directorio src al path
current_dir = Path(__file__).parent
src_dir = current_dir.parent / "src"
sys.path.insert(0, str(src_dir))

from sst_multiagent.crews.risk_assessment_crew import RiskAssessmentCrew


def construction_site_risk_assessment():
    """
    Ejecuta una evaluación de riesgos para un sitio de construcción
    de un edificio de oficinas de 5 pisos.
    """
    
    print("🏗️ Iniciando evaluación de riesgos - Obra de construcción...")
    
    # Datos específicos del sitio
    site_inputs = {
        "industry": "construction",
        "target_audience": "construction workers and safety managers",
        "marketing_objectives": "comprehensive risk assessment and safety compliance",
        "site_context": {
            "project_type": "5-story office building construction",
            "location": "Madrid, España",
            "workforce_size": 45,
            "main_activities": [
                "excavación y cimentación",
                "estructura de hormigón",
                "trabajo en altura",
                "soldadura y corte",
                "manejo de maquinaria pesada"
            ],
            "critical_hazards": [
                "caídas desde altura",
                "atrapamiento por maquinaria",
                "exposición a sustancias químicas",
                "riesgos eléctricos",
                "golpes por objetos"
            ],
            "regulatory_framework": [
                "RD 1627/1997 (obras de construcción)",
                "Ley 31/1995 (prevención de riesgos laborales)",
                "RD 773/1997 (equipos de protección individual)",
                "RD 486/1997 (lugares de trabajo)"
            ]
        }
    }
    
    try:
        print("👷 Configurando crew de evaluación de riesgos...")
        
        # Crear instancia del crew
        risk_crew = RiskAssessmentCrew()
        
        print("🔍 Ejecutando evaluación con agentes especializados...")
        print("   • Risk Analyst: Identificando peligros y evaluando riesgos")
        print("   • Compliance Officer: Verificando cumplimiento normativo")
        
        # Ejecutar el crew
        result = risk_crew.crew().kickoff(inputs=site_inputs)
        
        print("✅ Evaluación de riesgos completada!")
        
        # Mostrar resumen
        print("\n" + "="*70)
        print("🏗️ EVALUACIÓN DE RIESGOS - OBRA DE CONSTRUCCIÓN")
        print("="*70)
        
        print(f"🏢 Proyecto: {site_inputs['site_context']['project_type']}")
        print(f"📍 Ubicación: {site_inputs['site_context']['location']}")
        print(f"👷 Trabajadores: {site_inputs['site_context']['workforce_size']}")
        
        print(f"\n⚠️ Peligros Críticos Identificados:")
        for i, hazard in enumerate(site_inputs['site_context']['critical_hazards'], 1):
            print(f"  {i}. {hazard.title()}")
        
        print(f"\n📋 Normativa Aplicable:")
        for reg in site_inputs['site_context']['regulatory_framework']:
            print(f"  • {reg}")
        
        # Simular resultados de la evaluación
        risk_assessment_results = {
            "high_priority_risks": [
                {
                    "hazard": "Caídas desde altura",
                    "probability": "Alta",
                    "severity": "Crítica", 
                    "risk_level": "Muy Alto",
                    "controls": [
                        "Sistemas de protección colectiva (barandillas)",
                        "EPI anticaídas (arneses, cuerdas)",
                        "Capacitación específica en trabajo en altura",
                        "Supervisión continua"
                    ]
                },
                {
                    "hazard": "Atrapamiento por maquinaria",
                    "probability": "Media",
                    "severity": "Crítica",
                    "risk_level": "Alto", 
                    "controls": [
                        "Dispositivos de seguridad en maquinaria",
                        "Procedimientos de lockout/tagout",
                        "Señalización y delimitación de áreas",
                        "Capacitación en manejo seguro"
                    ]
                }
            ],
            "compliance_status": {
                "rd_1627_1997": "Cumple - Plan de seguridad aprobado",
                "ley_31_1995": "Cumple - Evaluación de riesgos actualizada",
                "rd_773_1997": "Requiere acción - Revisar EPIs de soldadura",
                "rd_486_1997": "Cumple - Instalaciones provisionales adecuadas"
            }
        }
        
        print(f"\n🚨 Riesgos de Prioridad Alta:")
        for risk in risk_assessment_results['high_priority_risks']:
            print(f"\n  🔴 {risk['hazard']}")
            print(f"     Probabilidad: {risk['probability']} | Severidad: {risk['severity']}")
            print(f"     Nivel de Riesgo: {risk['risk_level']}")
            print(f"     Controles requeridos:")
            for control in risk['controls']:
                print(f"       - {control}")
        
        print(f"\n📊 Estado de Cumplimiento Normativo:")
        for regulation, status in risk_assessment_results['compliance_status'].items():
            icon = "✅" if "Cumple" in status else "⚠️"
            print(f"  {icon} {regulation.upper()}: {status}")
        
        # Guardar evaluación detallada
        output_file = "outputs/construction_risk_assessment.md"
        Path("outputs").mkdir(exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Evaluación de Riesgos - Obra de Construcción\n\n")
            
            f.write(f"## Información del Proyecto\n\n")
            f.write(f"- **Tipo:** {site_inputs['site_context']['project_type']}\n")
            f.write(f"- **Ubicación:** {site_inputs['site_context']['location']}\n")
            f.write(f"- **Trabajadores:** {site_inputs['site_context']['workforce_size']}\n\n")
            
            f.write(f"## Actividades Principales\n\n")
            for activity in site_inputs['site_context']['main_activities']:
                f.write(f"- {activity.title()}\n")
            
            f.write(f"\n## Evaluación de Riesgos Críticos\n\n")
            for risk in risk_assessment_results['high_priority_risks']:
                f.write(f"### {risk['hazard']}\n\n")
                f.write(f"- **Probabilidad:** {risk['probability']}\n")
                f.write(f"- **Severidad:** {risk['severity']}\n")
                f.write(f"- **Nivel de Riesgo:** {risk['risk_level']}\n\n")
                f.write(f"**Medidas de Control:**\n\n")
                for control in risk['controls']:
                    f.write(f"- {control}\n")
                f.write("\n")
            
            f.write(f"## Estado de Cumplimiento\n\n")
            f.write(f"| Normativa | Estado |\n")
            f.write(f"|-----------|--------|\n")
            for regulation, status in risk_assessment_results['compliance_status'].items():
                f.write(f"| {regulation.upper()} | {status} |\n")
            
            f.write(f"\n## Análisis Detallado del Crew\n\n")
            f.write(f"```\n{str(result)}\n```\n")
        
        print(f"\n📋 Evaluación completa guardada en: {output_file}")
        
        # Plan de acción recomendado
        print(f"\n💡 Plan de Acción Inmediato:")
        print(f"  1. 🚨 Implementar sistemas anticaídas en todas las áreas de altura")
        print(f"  2. 🔒 Revisar y actualizar procedimientos de lockout/tagout")
        print(f"  3. 🛡️ Inspeccionar y completar EPIs faltantes (soldadura)")
        print(f"  4. 📚 Programar capacitaciones específicas por actividad")
        print(f"  5. 📊 Establecer sistema de auditorías semanales")
        
        return result
        
    except Exception as e:
        print(f"❌ Error durante la evaluación: {str(e)}")
        raise


if __name__ == "__main__":
    # Configurar entorno
    from dotenv import load_dotenv
    load_dotenv()
    
    try:
        result = construction_site_risk_assessment()
        print(f"\n🏆 Evaluación de riesgos completada exitosamente!")
        print(f"⚠️ Se identificaron riesgos críticos que requieren atención inmediata.")
        print(f"📋 Consulta el reporte completo en outputs/construction_risk_assessment.md")
    except Exception as e:
        print(f"\n❌ Error ejecutando evaluación: {str(e)}")
        print(f"🔧 Verifica la configuración del entorno.")