#!/usr/bin/env python3
"""
DEMO DIRECTO - Usando Google Generative AI sin CrewAI
Prueba directa de la API de Gemini para verificar conectividad
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Verificar que las rutas existan
Path("outputs").mkdir(exist_ok=True)
Path("logs").mkdir(exist_ok=True)

try:
    import google.generativeai as genai
    print("✅ Google Generative AI cargado correctamente")
except ImportError as e:
    print(f"❌ Error importando Google Generative AI: {e}")
    sys.exit(1)

def test_gemini_direct():
    """Prueba directa de Google Gemini"""
    
    api_key = os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ No se encontró GOOGLE_API_KEY en el .env")
        return False
    
    print(f"🔑 API Key encontrada: {api_key[:12]}...{api_key[-8:]}")
    
    try:
        # Configurar Gemini
        genai.configure(api_key=api_key)
        
        # Listar modelos disponibles
        print("\n📋 Modelos disponibles:")
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                print(f"  ✅ {model.name}")
        
        # Crear modelo
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Prompt de prueba
        prompt = """
        Analiza brevemente el mercado español de herramientas de productividad empresarial.
        Incluye 3 competidores principales y el tamaño estimado del mercado.
        """
        
        print("\n🚀 Generando respuesta...")
        response = model.generate_content(prompt)
        
        print("\n✅ RESPUESTA GENERADA:")
        print("=" * 50)
        print(response.text)
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Error con Gemini: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 DEMO DIRECTO - GOOGLE GEMINI")
    print("=" * 50)
    
    success = test_gemini_direct()
    
    if success:
        print("\n✅ Gemini funciona correctamente!")
        print("💡 El problema está en la integración CrewAI-LiteLLM")
    else:
        print("\n❌ Hay un problema con la configuración de Gemini")
    
    print("\n🏁 Demo completado")

if __name__ == "__main__":
    main()