#!/usr/bin/env python3
"""
🚀 Demo del Sistema Multi-Agente con Google Gemini
=================================================

Demuestra el funcionamiento del sistema multi-agente usando Gemini
para análisis completo de marketing digital.
"""

import os
from dotenv import load_dotenv
from pathlib import Path
import sys

# Configurar el entorno
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
    """Configura Google Gemini como LLM"""
    
    # Buscar la API key (soporta ambos nombres)
    api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        print("❌ No se encontró GEMINI_API_KEY o GOOGLE_API_KEY en el .env")
        return None, None
    
    try:
        # Crear LLM con Gemini
        llm = LLM(
            model="gemini/gemini-2.5-flash",
            api_key=api_key
        )
        
        print(f"✅ Google Gemini configurado")
        print(f"🔑 API Key: {api_key[:12]}...{api_key[-8:]}")
        print(f"🧠 Modelo: Gemini 1.5 Flash")
        return llm, "Google Gemini 1.5 Flash"
        
    except Exception as e:
        print(f"❌ Error configurando Gemini: {e}")
        return None, None

def create_marketing_crew(llm):
    """Crea un crew especializado en análisis de marketing digital"""
    
    print("🤖 Creando agentes especializados...")
    
    # 🔍 Agente 1: Investigador de Mercado
    researcher = Agent(
        role="🔍 Senior Market Research Analyst",
        goal="Realizar investigación profunda del mercado de SaaS B2B en España",
        backstory="""Eres un analista senior especializado en mercados tecnológicos españoles.
        Con 8 años de experiencia, dominas técnicas avanzadas de investigación cuantitativa 
        y cualitativa. Tu expertise incluye análisis competitivos, sizing de mercados y 
        identificación de oportunidades en el sector SaaS B2B.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    # 📈 Agente 2: Estratega Digital
    strategist = Agent(
        role="📈 Digital Marketing Strategist",
        goal="Desarrollar estrategias de marketing digital data-driven y escalables",
        backstory="""Eres un estratega de marketing digital con un historial comprobado 
        en el crecimiento de startups SaaS. Especializado en growth hacking, marketing 
        automation y optimización de funnels de conversión. Has liderado el crecimiento 
        de 3 startups de €0 a €1M ARR.""",
        verbose=True,
        allow_delegation=True,
        llm=llm
    )
    
    # ✍️ Agente 3: Content Marketing Expert
    content_expert = Agent(
        role="✍️ Content Marketing Specialist",
        goal="Crear estrategias de contenido que generen leads cualificados",
        backstory="""Eres un experto en content marketing B2B con 6 años creando contenido 
        que convierte. Tu enfoque combina SEO técnico, storytelling persuasivo y 
        lead generation. Has generado más de 10,000 MQLs para empresas SaaS mediante 
        estrategias de contenido innovadoras.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    print("📋 Definiendo tareas del análisis...")
    
    # 📊 Tarea 1: Investigación de Mercado
    research_task = Task(
        description="""Realiza un análisis exhaustivo del mercado SaaS B2B en España 2024-2025.
        
        🎯 **SCOPE**: Herramientas de productividad y automatización empresarial
        
        **DELIVERABLES ESPECÍFICOS:**
        1. **Market Sizing**: TAM, SAM, SOM con cifras actualizadas
        2. **Competitive Landscape**: Top 10 players, pricing, positioning
        3. **Customer Segments**: Empresas 50-500 empleados por sector
        4. **Growth Drivers**: Factores de crecimiento del mercado
        5. **Market Gaps**: Oportunidades no cubiertas
        6. **Pricing Analysis**: Rangos típicos por funcionalidad
        7. **Customer Pain Points**: Top 5 problemas identificados
        
        **FUENTES A CONSIDERAR**: 
        - Reports de IDC/Gartner sobre España
        - Análisis de startups locales exitosas  
        - Datos de inversión en SaaS español
        - Encuestas a directivos empresariales""",
        agent=researcher,
        expected_output="""**INFORME DE INVESTIGACIÓN DE MERCADO** (1000-1200 palabras)
        
        Estructura requerida:
        - 📊 Executive Summary (3 puntos clave)
        - 🎯 Market Size & Growth (TAM: €X, CAGR: X%)
        - 🏢 Competitive Analysis (tabla comparativa)
        - 👥 Customer Segmentation (3 segmentos prioritarios)
        - 🔍 Opportunities & Gaps (5 oportunidades específicas)
        - 💡 Strategic Recommendations (3 recomendaciones)"""
    )
    
    # 🚀 Tarea 2: Estrategia de Growth
    strategy_task = Task(
        description="""Desarrolla una estrategia de go-to-market completa para una startup 
        SaaS B2B que va a lanzar una herramienta de automatización de workflows.
        
        **CONTEXTO DEL PRODUCTO:**
        - Target: Empresas 50-500 empleados
        - Pricing: Freemium + €29/usuario/mes
        - Funcionalidad: Automatización de procesos internos
        - Competencia: Monday.com, Asana, Notion
        
        **PRESUPUESTO DISPONIBLE:** €80,000 para 6 meses
        **OBJETIVO:** 500 clientes de pago en 6 meses
        
        **DELIVERABLES:**
        1. **Positioning Statement** único y diferenciado
        2. **Go-to-Market Strategy** por fases
        3. **Channel Mix** con asignación de presupuesto
        4. **Customer Acquisition Strategy** específica
        5. **Pricing Strategy** optimizada
        6. **Launch Timeline** detallado
        7. **Success Metrics** y KPIs
        8. **Risk Mitigation** plan""",
        agent=strategist,
        expected_output="""**ESTRATEGIA GO-TO-MARKET COMPLETA** (1200-1500 palabras)
        
        Incluye:
        - 🎯 Positioning & Value Prop (elevator pitch)
        - 📈 GTM Roadmap (6 meses en fases)
        - 💰 Budget Allocation (€80K distribuidos)
        - 🔄 Customer Acquisition Funnel
        - 📊 KPI Dashboard (15 métricas clave)
        - ⚠️ Risk Assessment & Contingency Plan
        - 🏆 Success Criteria & Milestones""",
        context=[research_task]
    )
    
    # 📝 Tarea 3: Estrategia de Contenido
    content_task = Task(
        description="""Crea una estrategia de content marketing integral para apoyar 
        la estrategia go-to-market, enfocada en generar leads B2B cualificados.
        
        **AUDIENCIA OBJETIVO:**
        - CTOs y Heads of Operations
        - Empresas 50-500 empleados  
        - Sectores: Tech, Consulting, Agencies
        
        **CANALES PRIORITARIOS:**
        - Blog corporativo (SEO-focused)
        - LinkedIn (thought leadership)
        - Email marketing (nurturing)
        - Webinars (lead generation)
        
        **OBJETIVOS ESPECÍFICOS:**
        - 50,000 visits/mes al blog en 6 meses
        - 200 MQLs/mes vía contenido
        - 15% conversion rate blog→trial
        
        **DELIVERABLES:**
        1. **Content Pillars** estratégicos (4 pilares)
        2. **Editorial Calendar** primer trimestre
        3. **SEO Strategy** con keywords objetivo
        4. **Lead Magnets** design y strategy
        5. **Content Distribution** plan multi-canal
        6. **Influencer Outreach** strategy
        7. **Content Performance** metrics""",
        agent=content_expert,
        expected_output="""**PLAN DE CONTENT MARKETING** (1000-1200 palabras)
        
        Componentes:
        - 🎯 Content Strategy Framework
        - 📅 Editorial Calendar Q1 (36 contenidos)
        - 🔍 SEO Keyword Strategy (50+ keywords)
        - 🧲 Lead Generation Assets (5 lead magnets)
        - 📈 Distribution & Amplification Plan
        - 🤝 Influencer Partnership Strategy
        - 📊 Content Analytics Dashboard""",
        context=[research_task, strategy_task]
    )
    
    # Crear el crew
    crew = Crew(
        agents=[researcher, strategist, content_expert],
        tasks=[research_task, strategy_task, content_task],
        process=Process.sequential,
        verbose=True,
        memory=True,
        planning=True
    )
    
    return crew

def run_gemini_demo():
    """Ejecuta la demostración completa con Gemini"""
    
    print("🚀 SISTEMA MULTI-AGENTE - DEMO CON GOOGLE GEMINI")
    print("=" * 70)
    
    # Configurar Gemini
    llm, model_name = setup_gemini()
    if not llm:
        print("\n💡 Para configurar Gemini:")
        print("   1. Ve a https://aistudio.google.com/app/apikey")
        print("   2. Crea una API key gratuita") 
        print("   3. Añádela a tu .env como GEMINI_API_KEY=tu-key")
        return
    
    print(f"\n🎯 CASO DE USO: Análisis completo SaaS B2B España")
    print(f"⚡ MODELO: {model_name} (GRATIS)")
    print(f"👥 AGENTES: 3 especializados")
    print(f"📋 TAREAS: Research → Strategy → Content")
    
    # Crear crew
    crew = create_marketing_crew(llm)
    
    print(f"\n🚀 Iniciando análisis...")
    print(f"⏱️ Tiempo estimado: 4-6 minutos")
    print("=" * 70)
    
    try:
        # Ejecutar el análisis
        result = crew.kickoff()
        
        # Generar archivo de salida
        timestamp = Path().absolute().name
        output_file = Path("outputs") / f"gemini_saas_analysis_{timestamp}.md"
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("# 🚀 Análisis SaaS B2B España - Sistema Multi-Agente\n\n")
            f.write(f"**🤖 Modelo:** {model_name}\n")
            f.write(f"**📅 Fecha:** 11 de octubre de 2025\n")
            f.write(f"**🎯 Caso:** Startup SaaS automatización workflows\n")
            f.write(f"**💰 Presupuesto:** €80,000 / 6 meses\n\n")
            f.write("---\n\n")
            f.write("## 📊 RESULTADO DEL ANÁLISIS\n\n")
            f.write(str(result))
            f.write("\n\n---\n")
            f.write("\n*🤖 Generado por CrewAI + Google Gemini*")
            f.write("\n*📈 Sistema Multi-Agente lraigosov/multi-agent*")
        
        # Mostrar resultados
        print("\n" + "🎉" * 20)
        print("¡ANÁLISIS COMPLETADO EXITOSAMENTE!")
        print("🎉" * 20)
        
        print(f"\n📄 **ARCHIVO GENERADO:** {output_file}")
        print(f"📏 **TAMAÑO:** {len(str(result)):,} caracteres")
        print(f"🧠 **MODELO:** {model_name}")
        print(f"⚡ **COSTO:** ¡GRATIS! (Gemini)")
        
        # Preview del contenido
        result_str = str(result)
        lines = result_str.split('\n')
        preview_lines = [line for line in lines[:20] if line.strip()]
        
        print(f"\n📖 **PREVIEW DEL ANÁLISIS:**")
        print("-" * 60)
        for line in preview_lines[:15]:
            print(line[:80] + "..." if len(line) > 80 else line)
        if len(lines) > 20:
            print(f"... (+{len(lines)-20} líneas adicionales)")
        print("-" * 60)
        
        print(f"\n🎯 **PRÓXIMOS PASOS:**")
        print(f"   1. ✅ Revisar análisis completo: {output_file}")
        print(f"   2. 🚀 Implementar recomendaciones estratégicas")
        print(f"   3. 📊 Ejecutar más análisis con diferentes casos")
        print(f"   4. 🔄 Iterar y refinar el approach")
        
        print(f"\n💡 **EXPERIMENTOS SUGERIDOS:**")
        print(f"   • Cambiar el sector target (fintech, healthtech)")
        print(f"   • Variar el presupuesto (€20K vs €200K)")
        print(f"   • Probar diferentes modelos de pricing")
        print(f"   • Analizar mercados internacionales")
        
    except Exception as e:
        print(f"\n❌ ERROR DURANTE LA EJECUCIÓN:")
        print(f"   Tipo: {type(e).__name__}")
        print(f"   Mensaje: {str(e)}")
        
        print(f"\n🔧 DIAGNÓSTICO:")
        print(f"   • Modelo: {model_name}")  
        print(f"   • API Key: Configurada ✅")
        
        print(f"\n💡 POSIBLES SOLUCIONES:")
        print(f"   1. Verificar conexión a internet")
        print(f"   2. Confirmar que Gemini API esté activa")
        print(f"   3. Revisar límites de rate limiting")
        print(f"   4. Intentar con un prompt más simple")

if __name__ == "__main__":
    run_gemini_demo()