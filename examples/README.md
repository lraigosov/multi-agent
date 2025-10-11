# Ejemplos de Uso - Marketing Multi-Agent System

Esta carpeta contiene ejemplos prácticos que demuestran cómo usar el sistema de marketing multi-agente en diferentes escenarios reales.

## 📁 Ejemplos Disponibles

### 1. `fintech_startup_analysis.py`
**Caso de Uso:** Análisis completo de marketing para startup fintech
- **Industria:** Fintech / Aplicación de finanzas personales
- **Objetivo:** Lanzamiento de producto y estrategia go-to-market
- **Crews Utilizados:** Marketing Intelligence Flow completo
- **Duración:** ~15-20 minutos

```bash
python examples/fintech_startup_analysis.py
```

### 2. `ecommerce_campaign_optimization.py`
**Caso de Uso:** Optimización de campaña Google Ads para e-commerce
- **Industria:** Fashion e-commerce
- **Objetivo:** Mejorar ROAS de campaña navideña
- **Crews Utilizados:** Campaign Optimization Flow
- **Duración:** ~10-15 minutos

```bash
python examples/ecommerce_campaign_optimization.py
```

### 3. `saas_competitive_analysis.py`
**Caso de Uso:** Análisis competitivo para SaaS B2B
- **Industria:** CRM para pequeñas empresas
- **Objetivo:** Identificar oportunidades de diferenciación
- **Crews Utilizados:** Competitor Analysis Crew
- **Duración:** ~10-12 minutos

```bash
python examples/saas_competitive_analysis.py
```

### 4. `healthtech_content_strategy.py`
**Caso de Uso:** Estrategia de contenido para telemedicina
- **Industria:** Salud digital / Telemedicina
- **Objetivo:** Desarrollar estrategia de contenido completa
- **Crews Utilizados:** Content Strategy Crew
- **Duración:** ~12-15 minutos

```bash
python examples/healthtech_content_strategy.py
```

### 5. `construction_risk_assessment.py` (SST)
**Caso de Uso:** Evaluación de riesgos en obra de construcción
- **Industria:** Construcción / SST
- **Objetivo:** Identificar y evaluar riesgos laborales críticos
- **Crews Utilizados:** Risk Assessment Crew (SST)
- **Duración:** ~10-15 minutos

```bash
python examples/construction_risk_assessment.py
```

## 🚀 Cómo Ejecutar los Ejemplos

### Prerrequisitos
1. **Configurar variables de entorno:** Copia `.env.example` a `.env` y completa las API keys
2. **Instalar dependencias:** `pip install -r requirements.txt`
3. **Ubicación correcta:** Ejecutar desde el directorio raíz del proyecto

### Ejecución Individual

```bash
# Ejemplo 1: Análisis Fintech
python examples/fintech_startup_analysis.py

# Ejemplo 2: Optimización E-commerce
python examples/ecommerce_campaign_optimization.py

# Ejemplo 3: Análisis Competitivo SaaS
python examples/saas_competitive_analysis.py

# Ejemplo 4: Estrategia Contenido HealthTech
python examples/healthtech_content_strategy.py

# Ejemplo 5: Evaluación Riesgos SST
python examples/construction_risk_assessment.py
```

### Ejecución con CLI Principal

```bash
# Análisis completo usando el CLI
python -m marketing_multiagent.main analyze --industry "fintech" --audience "millennials professionals"

# Optimización de campaña
python -m marketing_multiagent.main optimize-campaign --name "Holiday Campaign" --budget 75000

# Crew específico
python -m marketing_multiagent.main run-crew --crew competitor-analysis --industry "saas" --audience "small businesses"

# CLI Global - Ejecutar crew de SST
python -m multiagent.cli run-crew --domain sst --crew RiskAssessmentCrew --inputs '{"industry":"construction","target_audience":"construction workers"}'
```

## 📊 Resultados y Outputs

Cada ejemplo genera archivos de resultado en la carpeta `outputs/`:

```
outputs/
├── fintech_startup_analysis.md
├── ecommerce_campaign_optimization.md
├── saas_competitive_analysis.md
├── healthtech_content_strategy.md
├── construction_risk_assessment.md    # SST
└── reports/
    ├── detailed_analysis_*.json
    └── performance_metrics_*.csv
```

## 🎯 Casos de Uso por Industria

### Tecnología y SaaS
- **Ejemplos:** `saas_competitive_analysis.py`
- **Enfoque:** Diferenciación competitiva, pricing strategy, feature positioning
- **Métricas:** MRR, churn rate, customer acquisition cost

### E-commerce y Retail
- **Ejemplos:** `ecommerce_campaign_optimization.py`
- **Enfoque:** Conversion optimization, seasonal campaigns, ROAS improvement
- **Métricas:** ROAS, conversion rate, cart abandonment, customer lifetime value

### Fintech y Servicios Financieros
- **Ejemplos:** `fintech_startup_analysis.py`
- **Enfoque:** Trust building, regulatory compliance, user education
- **Métricas:** User acquisition, app downloads, transaction volume

### Salud y Bienestar
- **Ejemplos:** `healthtech_content_strategy.py`
- **Enfoque:** Content authority, compliance, patient education
- **Métricas:** Content engagement, lead quality, brand trust scores

### Seguridad y Salud en el Trabajo (SST)
- **Ejemplos:** `construction_risk_assessment.py`
- **Enfoque:** Risk assessment, regulatory compliance, incident prevention
- **Métricas:** Risk levels, compliance status, safety KPIs

## 🛠️ Personalización

### Modificar Parámetros
Cada ejemplo incluye variables configurables al inicio del archivo:

```python
# Modifica estos valores para tu caso específico
analysis_inputs = {
    "industry": "tu_industria",
    "target_audience": "tu_audiencia", 
    "marketing_objectives": "tus_objetivos",
    # ... más configuraciones
}
```

### Añadir Nuevos Ejemplos
1. Crea un nuevo archivo Python en `/examples/`
2. Importa los crews o flows necesarios
3. Define el contexto específico de tu industria
4. Ejecuta y guarda resultados
5. Añade documentación en este README

### Integrar con Tu Sistema
Los ejemplos pueden servir como base para integración:

```python
from marketing_multiagent.flows.marketing_intelligence_flow import MarketingIntelligenceFlow

# Tu implementación personalizada
def mi_caso_uso_especifico():
    flow = MarketingIntelligenceFlow()
    # ... configuración específica
    result = flow.kickoff()
    return result
```

## 📋 Checklist de Validación

Antes de ejecutar ejemplos, verifica:

- [ ] Variables de entorno configuradas (`.env`)
- [ ] Dependencias instaladas (`requirements.txt`)
- [ ] API keys válidas (OpenAI, Serper, etc.)
- [ ] Carpeta `outputs/` tiene permisos de escritura
- [ ] Conexión a internet activa para APIs externas

## 🔧 Troubleshooting

### Errores Comunes

**Error: "No API key found"**
```bash
# Solución: Configurar variables de entorno
cp .env.example .env
# Editar .env con tus API keys
```

**Error: "Module not found"**
```bash
# Solución: Instalar dependencias
pip install -r requirements.txt
```

**Error: "Permission denied"**
```bash
# Solución: Crear directorio outputs
mkdir outputs
chmod 755 outputs
```

### Logs y Debugging

Cada ejemplo incluye logging detallado:
- Mensajes de progreso en consola
- Archivos de log en `logs/`
- Estados intermedios guardados para debugging

## 📞 Soporte

Si encuentras problemas:
1. Revisa este README y la documentación principal
2. Verifica la configuración siguiendo el checklist
3. Consulta los logs de error para detalles específicos
4. Abre un issue con el contexto completo del error

## 🎓 Próximos Pasos

Después de ejecutar estos ejemplos:
1. **Experimenta** con diferentes parámetros
2. **Personaliza** para tu industria específica
3. **Integra** en tu workflow de marketing
4. **Escala** usando los flows para casos complejos
5. **Contribuye** con nuevos ejemplos para la comunidad