# 🛠️ Guía de Configuración de APIs

Esta guía te ayudará a configurar las APIs necesarias para el sistema multi-agente.

## ⚠️ APIs Obligatorias

### 1. 🤖 API de IA Generativa (OBLIGATORIA)

Necesitas **al menos una** de estas opciones:

#### Opción A: OpenAI (Recomendado)
1. Ve a [OpenAI Platform](https://platform.openai.com/)
2. Crea una cuenta o inicia sesión
3. Ve a **API Keys** → **Create new secret key**
4. Copia la key que comienza con `sk-`
5. Añade a `.env`: `OPENAI_API_KEY=sk-tu-key-aqui`

**💰 Costo**: Consulta precios oficiales: https://openai.com/api/pricing

#### Opción B: Google Gemini (Gratis)
1. Ve a [AI Studio](https://aistudio.google.com/app/apikey)
2. Inicia sesión con tu cuenta Google
3. Haz clic en **Create API Key**
4. Copia la key generada
5. Añade a `.env`: `GOOGLE_API_KEY=tu-key-aqui`

**💰 Costo**: Consulta límites y precios: https://ai.google.dev/pricing (AI Studio)

#### Opción C: Anthropic Claude
1. Ve a [Anthropic Console](https://console.anthropic.com/)
2. Crea una cuenta
3. Ve a **API Keys** → **Create Key**
4. Copia la key que comienza con `sk-ant-`
5. Añade a `.env`: `ANTHROPIC_API_KEY=sk-ant-tu-key-aqui`

### 2. 🔍 API de Búsqueda (OBLIGATORIA)

#### Serper (Google Search)
1. Ve a [Serper.dev](https://serper.dev/)
2. Regístrate con tu email
3. Verifica tu email
4. Copia tu API key del dashboard
5. Añade a `.env`: `SERPER_API_KEY=tu-key-aqui`

**💰 Costo**: Revisa planes vigentes en el dashboard de Serper

---

## 🚀 Configuración Rápida (5 minutos)

### Para Desarrollo (Gratis)
```bash
# 1. Copia el archivo de ejemplo
cp .env.example .env

# 2. Configura Gemini (gratis)
GOOGLE_API_KEY=tu-google-key-aqui

# 3. Configura Serper (gratis)
SERPER_API_KEY=tu-serper-key-aqui
```

### Para Producción (Pago)
```bash
# 1. Copia el archivo de ejemplo
cp .env.example .env

# 2. Configura OpenAI (mejor calidad)
OPENAI_API_KEY=sk-tu-openai-key-aqui

# 3. Configura Serper 
SERPER_API_KEY=tu-serper-key-aqui
```

---

## 🧪 Verificar Configuración

```bash
# Verificar que las APIs funcionan
python -c "
import os
from dotenv import load_dotenv
load_dotenv()

# Verificar OpenAI
if os.getenv('OPENAI_API_KEY'):
    print('✅ OpenAI configurado')
else:
    print('❌ OpenAI no configurado')

# Verificar Google
if os.getenv('GOOGLE_API_KEY'):
    print('✅ Google Gemini configurado')
else:
    print('❌ Google Gemini no configurado')

# Verificar Serper
if os.getenv('SERPER_API_KEY'):
    print('✅ Serper configurado')
else:
    print('❌ Serper no configurado')
"

# Probar el sistema
python -m src.multiagent.cli domains
```

---

## 💡 Recomendaciones por Usuario

### 👨‍💻 Desarrolladores
- **Opción**: Google Gemini (gratis)
- **Backup**: OpenAI con límite de $5
- **Ventaja**: Sin costo para experimentar

### 🏢 Empresas/Producción
- **Opción**: OpenAI GPT-4o (mejor calidad)  
- **Backup**: Anthropic Claude (análisis complejos)
- **Ventaja**: Mejor resultado, soporte empresarial

### 🎓 Estudiantes/Académicos
- **Opción**: Hugging Face (open source)
- **Backup**: Google Gemini (gratis)
- **Ventaja**: Aprender sobre diferentes modelos

---

## 🔧 Configuración Avanzada

### Múltiples LLMs por Dominio
```env
# Marketing usa OpenAI (creatividad)
MARKETING_DEFAULT_LLM=openai/gpt-4o

# SST usa Claude (análisis detallado)
SST_DEFAULT_LLM=anthropic/claude-3-5-sonnet
```

### Configuración de Costos
```env
# Límites de gasto por mes
OPENAI_MONTHLY_LIMIT=50.00
MAX_TOKENS_PER_TASK=4000
TEMPERATURE=0.7
```

---

## ❓ Troubleshooting

### Error: "No module named 'openai'"
```bash
pip install openai anthropic google-generativeai
```

### Error: "Invalid API key"
1. Verifica que la API key esté correcta en `.env`
2. Asegúrate de que el archivo `.env` esté en la raíz del proyecto
3. Reinicia tu terminal/IDE

### Error: "Rate limit exceeded"
- Usa un modelo más económico (ej: GPT-3.5 en vez de GPT-4)
- Reduce `MAX_TOKENS_PER_TASK`
- Agrega delays entre requests

### APIs no funcionan
```bash
# Verifica conectividad
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
  "https://api.openai.com/v1/models"
```

---

## 📊 Comparación de Costos

Consulta siempre las páginas oficiales porque los precios cambian:
- Gemini: https://ai.google.dev/pricing
- OpenAI: https://openai.com/api/pricing
- Anthropic: https://www.anthropic.com/pricing

Consejo: empieza con Gemini (tier gratuito de AI Studio) y migra a otros modelos si necesitas mejor calidad o features específicas.