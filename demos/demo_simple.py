#!/usr/bin/env python3
"""
🚀 Demo Simplificado del Sistema Multi-Agente con Gemini
======================================================

Demostración básica pero funcional del sistema multi-agente.
"""

import os
from dotenv import load_dotenv
from pathlib import Path
import sys

# Configurar el entorno
load_dotenv()

# Añadir dummy OpenAI key si no existe (CrewAI la requiere internamente)
if not os.getenv('OPENAI_API_KEY'):
    os.environ['OPENAI_API_KEY'] = 'dummy-key-not-used'

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
    """Configura Google Gemini como LLM"""
    
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
        
        print(f"✅ Google Gemini configurado")
        print(f"🔑 API Key: {api_key[:12]}...{api_key[-8:]}")
        return llm, "Google Gemini 2.5 Flash"
        
    except Exception as e:
        print(f"❌ Error configurando Gemini: {e}")
        return None, None

def create_simple_crew(llm):
    """Crea un crew simple de 2 agentes"""
    
    print("🤖 Creando crew simplificado...")
    
    # Agente 1: Investigador
    researcher = Agent(
        role="Market Research Analyst",
        goal="Analizar tendencias del mercado español de software empresarial",
        backstory="""Eres un analista de mercado especializado en el sector tecnológico español.
        Tu expertise te permite identificar oportunidades de negocio y analizar competidores.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    # Agente 2: Estratega
    strategist = Agent(
        role="Business Strategist", 
        goal="Desarrollar recomendaciones estratégicas basadas en research",
        backstory="""Eres un estratega de negocios con experiencia en startups tecnológicas.
        Te especializas en convertir insights en planes de acción ejecutables.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    # Tarea 1: Research
    research_task = Task(
        description="""Analiza el mercado español de herramientas de productividad empresarial.
        
        Incluye:
        1. Tamaño del mercado y crecimiento
        2. Principales competidores (3-5)
        3. Segmentos de clientes más atractivos
        4. Tendencias tecnológicas relevantes
        5. Oportunidades identificadas
        
        Enfócate en empresas de 50-200 empleados.""",
        agent=researcher,
        expected_output="""Informe de mercado estructurado con:
        - Resumen ejecutivo de 2 párrafos
        - Análisis de competidores con fortalezas/debilidades
        - Segmentación de clientes objetivo
        - 3-5 oportunidades de negocio específicas
        - Recomendaciones de próximos pasos"""
    )
    
    # Tarea 2: Strategy
    strategy_task = Task(
        description="""Basándote en el research, desarrolla una estrategia para lanzar 
        una herramienta de gestión de proyectos en el mercado español.
        
        Considera:
        - Presupuesto inicial: €50,000
        - Timeline: 6 meses
        - Target: empresas medianas
        
        Desarrolla:
        1. Propuesta de valor única
        2. Estrategia de precios
        3. Canales de distribución
        4. Plan de marketing
        5. Métricas de éxito""",
        agent=strategist,
        expected_output="""Plan estratégico que incluya:
        - Posicionamiento diferenciado
        - Modelo de precios justificado
        - Mix de canales recomendado
        - Presupuesto de marketing distribuido
        - KPIs y timeline de 6 meses""",
        context=[research_task]
    )
    
    # Crear crew simplificado (sin planning ni memory para evitar errores)
    crew = Crew(
        agents=[researcher, strategist],
        tasks=[research_task, strategy_task],
        process=Process.sequential,
        verbose=True
    )
    
    return crew

def run_simple_demo():
    """Ejecuta la demostración simplificada"""
    
    print("🚀 DEMO SIMPLIFICADO - SISTEMA MULTI-AGENTE")
    print("=" * 55)
    
    # Configurar Gemini
    llm, model_name = setup_gemini()
    if not llm:
        return
    
    print(f"\n🎯 CASO: Herramientas de productividad en España")
    print(f"⚡ MODELO: {model_name}")
    print(f"👥 AGENTES: 2 (Research + Strategy)")
    
    # Crear crew
    crew = create_simple_crew(llm)
    
    print(f"\n🚀 Ejecutando análisis...")
    print(f"⏱️ Tiempo estimado: 2-3 minutos")
    print("=" * 55)
    
    try:
        # Ejecutar el análisis
        result = crew.kickoff()
        
        # Guardar resultado
        output_file = Path("outputs") / "gemini_simple_demo.md"
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("# 🚀 Análisis Mercado España - Demo Gemini\n\n")
            f.write(f"**🤖 Modelo:** {model_name}\n")
            f.write(f"**📅 Fecha:** 11 octubre 2025\n")
            f.write(f"**🎯 Target:** Herramientas productividad empresarial\n\n")
            f.write("---\n\n")
            f.write("## 📊 ANÁLISIS GENERADO\n\n")
            f.write(str(result))
            f.write("\n\n---\n")
            f.write("*🤖 Generado por CrewAI + Google Gemini*")
        
        # Mostrar resultados
        print("\n" + "🎉" * 15)
        print("¡DEMO COMPLETADA!")
        print("🎉" * 15)
        
        print(f"\n📄 **ARCHIVO:** {output_file}")
        print(f"📏 **TAMAÑO:** {len(str(result)):,} caracteres")
        print(f"🧠 **MODELO:** {model_name}")
        print(f"💰 **COSTO:** ¡GRATIS!")
        
        # Preview
        result_str = str(result)
        lines = result_str.split('\n')[:15]
        
        print(f"\n📖 **PREVIEW:**")
        print("-" * 45)
        for line in lines:
            if line.strip():
                print(line[:75] + "..." if len(line) > 75 else line)
        print("-" * 45)
        
        print(f"\n✅ **ÉXITO:** Sistema multi-agente funcionando")
        print(f"🔄 **PRÓXIMO:** Revisar archivo completo")
        
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}")
        print(f"📝 Mensaje: {str(e)}")
        print(f"\n🔧 Soluciones:")
        print(f"   1. Verificar conexión a internet")
        print(f"   2. Confirmar API key de Gemini válida")

if __name__ == "__main__":
    run_simple_demo()