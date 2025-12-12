#!/usr/bin/env python3
"""
DEMO SST - Sistema Multi-Agente para Seguridad y Salud en el Trabajo
Análisis de riesgos laborales y cumplimiento normativo usando Google Gemini 2.5 Flash
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# Cargar variables de entorno
load_dotenv()

# Verificar que las rutas existan
Path("outputs").mkdir(exist_ok=True)
Path("logs").mkdir(exist_ok=True)

# Importar las dependencias necesarias
try:
    from crewai import Agent, Task, Crew, Process
    from crewai.llm import LLM
    print("✅ CrewAI cargado correctamente")
except ImportError as e:
    print(f"❌ Error importando CrewAI: {e}")
    sys.exit(1)

def setup_gemini():
    """Configura Google Gemini como LLM para SST"""
    
    # Buscar la API key
    api_key = os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ No se encontró GOOGLE_API_KEY en el .env")
        return None, None
    
    try:
        # Crear LLM con Gemini - usar modelo disponible
        llm = LLM(
            model="gemini/gemini-2.5-flash",
            api_key=api_key
        )
        
        print(f"✅ Google Gemini configurado para SST")
        print(f"🔑 API Key: {api_key[:12]}...{api_key[-8:]}")
        return llm, "Google Gemini 2.5 Flash"
        
    except Exception as e:
        print(f"❌ Error configurando Gemini: {e}")
        return None, None

def create_sst_crew(llm):
    """Crea un crew especializado en SST"""
    
    print("🦺 Creando agentes especialistas en SST...")
    
    # 🔍 Agente 1: Analista de Riesgos Laborales
    risk_analyst = Agent(
        role="🔍 Analista Senior de Riesgos Laborales",
        goal="Identificar, evaluar y clasificar riesgos de seguridad y salud en el trabajo",
        backstory="""Eres un especialista en prevención de riesgos laborales con 10 años de experiencia 
        en empresas industriales españolas. Tienes certificación en normas OHSAS 18001/ISO 45001 y 
        profundo conocimiento de la Ley 31/1995 de Prevención de Riesgos Laborales española. 
        Tu expertise incluye evaluación de riesgos, análisis de incidentes y desarrollo de medidas preventivas.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    # 📋 Agente 2: Especialista en Cumplimiento Normativo
    compliance_officer = Agent(
        role="📋 Especialista en Cumplimiento Normativo SST",
        goal="Asegurar el cumplimiento de la normativa española e internacional de SST",
        backstory="""Eres un experto en legislación de prevención de riesgos laborales con especialización 
        en normativa española y europea. Conoces en detalle la Ley 31/1995, RD 39/1997, directivas europeas 
        de SST, y normas ISO 45001. Tu experiencia incluye auditorías de cumplimiento, elaboración de 
        procedimientos de seguridad y formación en normativa para empresas medianas.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    # 📊 Agente 3: Planificador de Medidas Preventivas
    prevention_planner = Agent(
        role="📊 Planificador Estratégico de Medidas Preventivas",
        goal="Desarrollar planes integrales de prevención y mejora continua en SST",
        backstory="""Eres un consultor especializado en sistemas de gestión de SST con experiencia en 
        implementación de medidas preventivas cost-effective para empresas de 50-200 empleados. 
        Tu expertise incluye desarrollo de planes de formación, diseño de procedimientos operativos 
        seguros, y establecimiento de indicadores KPI para monitoreo de seguridad laboral.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    return [risk_analyst, compliance_officer, prevention_planner]

def create_sst_tasks(agents):
    """Crea las tareas específicas para el análisis SST"""
    
    print("📋 Definiendo tareas de análisis SST...")
    
    risk_analyst, compliance_officer, prevention_planner = agents
    
    # Tarea 1: Evaluación de Riesgos
    risk_assessment_task = Task(
        description="""Realiza una evaluación integral de riesgos laborales para una empresa manufacturera española 
        de 120 empleados dedicada a fabricación de componentes metálicos.
        
        Analiza:
        1. Riesgos físicos (ruido, vibraciones, temperatura, iluminación)
        2. Riesgos químicos (sustancias peligrosas, vapores, polvo metálico)
        3. Riesgos ergonómicos (posturas forzadas, manipulación manual, movimientos repetitivos)
        4. Riesgos psicosociales (estrés laboral, carga de trabajo, organización)
        5. Riesgos de seguridad (máquinas, herramientas, caídas, cortes)
        
        Para cada riesgo identifica:
        - Probabilidad de ocurrencia (Baja/Media/Alta)
        - Severidad del daño (Leve/Grave/Muy Grave)
        - Nivel de riesgo resultante
        - Trabajadores expuestos
        - Medidas preventivas recomendadas
        
        Base tu análisis en la matriz de riesgos española y mejores prácticas del sector metal.""",
        expected_output="""Informe detallado de evaluación de riesgos con:
        - Matriz de riesgos clasificados por nivel de prioridad
        - Identificación específica de puestos de trabajo críticos
        - Recomendaciones de medidas preventivas por riesgo
        - Cronograma de implementación sugerido""",
        agent=risk_analyst
    )
    
    # Tarea 2: Análisis de Cumplimiento Normativo
    compliance_task = Task(
        description="""Basándote en la evaluación de riesgos, analiza el cumplimiento normativo requerido 
        para la empresa manufacturera.
        
        Evalúa cumplimiento de:
        1. Ley 31/1995 de Prevención de Riesgos Laborales
        2. RD 39/1997 Reglamento de los Servicios de Prevención
        3. RD 485/1997 sobre señalización de seguridad
        4. RD 486/1997 sobre lugares de trabajo
        5. RD 487/1997 sobre manipulación manual de cargas
        6. RD 1215/1997 sobre equipos de trabajo
        7. Norma ISO 45001:2018 (opcional pero recomendada)
        
        Para cada normativa identifica:
        - Requisitos específicos aplicables
        - Nivel de cumplimiento actual estimado
        - Gaps de cumplimiento críticos
        - Documentación requerida
        - Formación obligatoria necesaria
        - Plazos legales de implementación""",
        expected_output="""Análisis de cumplimiento normativo con:
        - Gap analysis detallado por normativa
        - Priorización de acciones de cumplimiento
        - Calendario de implementación normativa
        - Lista de documentación requerida""",
        agent=compliance_officer
    )
    
    # Tarea 3: Plan Integral de Prevención
    prevention_plan_task = Task(
        description="""Desarrolla un plan integral de prevención de riesgos laborales para los próximos 12 meses.
        
        El plan debe incluir:
        1. Medidas técnicas (equipos de protección, mejoras en instalaciones)
        2. Medidas organizativas (procedimientos, instrucciones de trabajo)
        3. Medidas formativas (capacitación por puesto, sensibilización)
        4. Medidas de control (inspecciones, auditorías, indicadores)
        5. Plan de emergencias y primeros auxilios
        6. Sistema de gestión de SST
        
        Considera:
        - Presupuesto estimado: €75,000 anuales
        - Priorización por nivel de riesgo identificado
        - ROI en reducción de siniestralidad
        - Cronograma de implementación realista
        - KPIs de seguimiento y control
        - Asignación de responsabilidades
        - Sistema de mejora continua""",
        expected_output="""Plan integral de prevención que incluya:
        - Programa anual de actividades preventivas
        - Presupuesto detallado por medida
        - Cronograma de implementación mensual
        - KPIs y métricas de seguimiento
        - Matriz de responsabilidades
        - Procedimientos de control y mejora continua""",
        agent=prevention_planner
    )
    
    return [risk_assessment_task, compliance_task, prevention_plan_task]

def run_sst_demo():
    """Ejecuta el demo de SST"""
    
    print("🦺 DEMO SST - SISTEMA MULTI-AGENTE")
    print("=" * 60)
    
    # Configurar Gemini
    llm, model_name = setup_gemini()
    if not llm:
        print("❌ No se pudo configurar el modelo de IA")
        return
    
    print(f"\n🎯 CASO DE USO: Evaluación SST empresa manufacturera")
    print(f"⚡ MODELO: {model_name}")
    print(f"👥 AGENTES: 3 especialistas SST")
    print(f"📋 TAREAS: Riesgos → Normativa → Plan Prevención")
    
    # Crear agentes y tareas
    agents = create_sst_crew(llm)
    tasks = create_sst_tasks(agents)
    
    # Crear y configurar el crew
    print("🤖 Creando crew SST...")
    crew = Crew(
        agents=agents,
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )
    
    print("\n🚀 Iniciando análisis SST...")
    print("⏱️ Tiempo estimado: 5-8 minutos")
    print("=" * 60)
    
    try:
        # Ejecutar el análisis
        result = crew.kickoff()
        
        # Guardar resultado
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"outputs/sst_analysis_{timestamp}.md"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(str(result))
        
        print("\n" + "🎉" * 15)
        print("¡ANÁLISIS SST COMPLETADO!")
        print("🎉" * 15)
        
        print(f"\n📄 **ARCHIVO:** {output_file}")
        print(f"📏 **TAMAÑO:** {len(str(result)):,} caracteres")
        print(f"🧠 **MODELO:** {model_name}")
        print(f"💰 **COSTO:** ¡GRATIS!")
        
        # Mostrar preview del resultado
        preview = str(result)[:500] + "..." if len(str(result)) > 500 else str(result)
        print(f"\n📖 **PREVIEW:**")
        print("-" * 45)
        print(preview)
        print("-" * 45)
        
        print(f"\n✅ **ÉXITO:** Análisis SST completado")
        print(f"🔄 **PRÓXIMO:** Revisar archivo completo en {output_file}")
        
    except Exception as e:
        print(f"\n❌ ERROR DURANTE LA EJECUCIÓN:")
        print(f"   Tipo: {type(e).__name__}")
        print(f"   Mensaje: {e}")
        print(f"\n🔧 DIAGNÓSTICO:")
        print(f"   • Modelo: {model_name}")
        print(f"   • API Key: {'Configurada ✅' if os.getenv('GOOGLE_API_KEY') else 'No encontrada ❌'}")
        
        print(f"\n💡 POSIBLES SOLUCIONES:")
        print(f"   1. Verificar conexión a internet")
        print(f"   2. Confirmar que Gemini API esté activa")
        print(f"   3. Revisar límites de rate limiting")
        print(f"   4. Intentar con un prompt más simple")

if __name__ == "__main__":
    run_sst_demo()