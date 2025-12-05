# ETL Multi-Agent System - Hexagonal Architecture

Sistema ETL multi-agente construido con **arquitectura hexagonal** (Ports & Adapters) y orquestado con **CrewAI**. Permite procesar datos desde múltiples fuentes (archivos, APIs, bases de datos) y cargarlos en diversos destinos (archivos, data warehouses) con transformaciones, validaciones y autocorrección.

## 🎯 Características

- **Arquitectura Hexagonal**: Dominio desacoplado de frameworks e infraestructura
- **Puertos y Adaptadores**: Interfaces claras para sources, transformations, validations, destinations
- **Casos de Uso Funcionales**: Ingestión, transformación, validación y carga de datos
- **Validación Integrada**: Checks de nulls, duplicados y tipos de datos
- **Extensible**: Fácil adición de nuevos adaptadores sin modificar dominio
- **Preparado para CrewAI** (v0.2+): Arquitectura lista para integración con agentes multi-LLM

## 📋 Casos de Uso (Actuales)

1. **Transformación Local**: CSV → CSV con mapeo de columnas y type casting
2. **Validación de Calidad**: Detección de nulos y duplicados

## 🔮 Casos de Uso (Futuros - v0.2+)

1. **Migración de Datos**: CSV → Parquet con limpieza y normalización
2. **Data Warehousing**: Archivos locales → BigQuery con validación de calidad
3. **Integración de APIs**: REST API → Base de datos relacional
4. **Data Lakes**: Múltiples fuentes → S3/GCS con particionamiento

## 🏗️ Arquitectura

```
CLI/Scripts (Driving Adapters)
         │
         ▼
   Use Cases + Adapters (Application Layer)
         │
         ▼
Domain (Entities + Use Cases + Ports)
         │
         ▼
Adapters (Files, DBs, Cloud, Driven)
```

**Nota**: La implementación actual utiliza casos de uso directamente. CrewAI Crew y Flow están definidos pero son opcionales para futuras extensiones.

Ver [Diagrama Detallado](../docs/etl_architecture.md)

## 🚀 Instalación

```bash
# Clonar repositorio
git clone https://github.com/lraigosov/multi-agent.git
cd multi-agent

# Activar entorno virtual
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
# o con Poetry
poetry install
```

## ⚙️ Configuración

Copia `.env.example` y configura:

```env
# LLM Provider (openai, gemini, anthropic)
ETL_LLM_PROVIDER=gemini
ETL_LLM_MODEL=gemini-2.0-flash
ETL_LLM_TEMPERATURE=0.1

# Google Gemini (gratuito)
GOOGLE_API_KEY=your_key_here

# OpenAI (alternativo)
OPENAI_API_KEY=sk-your_key_here

# Configuración ETL
ETL_ENABLE_QUALITY_CHECKS=true
ETL_FAIL_ON_VALIDATION_ERRORS=false
ETL_LOG_LEVEL=INFO
```

## 🎮 Uso

### Demo Funcional

```bash
# Demo con caso de éxito y manejo de errores
python examples/demo_etl.py
```

**Salida esperada:**
- Ingesta de datos desde CSV
- Transformación de columnas (mapeo y type casting)
- Validación de calidad de datos
- Carga a archivo CSV destino en `outputs/`

**Nota**: La demo ejecuta el pipeline ETL completo sin dependencias de LLMs ni CrewAI Crew/Flow.
```

### Uso Programático

```python
from etl_multiagent.flows.etl_pipeline_flow import ETLPipelineFlow, ETLFlowState

# Configurar estado del flow
state = ETLFlowState(
    source_uri="data/sales.csv",
    source_format="csv",
    dest_uri="outputs/sales_clean.parquet",
    dest_format="parquet",
    mappings={
        "sale_id": "id",
        "customer_name": "name",
        "amount": "sale_amount",
    },
    target_schema={
        "sale_id": "int64",
        "customer_name": "object",
        "sale_amount": "float64",
    },
)

# Ejecutar pipeline
flow = ETLPipelineFlow()
flow.state = state
result = flow.kickoff()

# Revisar resultados
print(f"Status: {state.validation_report['status']}")
print(f"Output: {state.load_result['path']}")
```

## 📚 Documentación

- [Arquitectura Hexagonal](../docs/etl_architecture.md): Diagrama y principios
- [Diseño de Agentes](../docs/etl_agents_design.md): Roles, goals, herramientas, LLMs
- [Riesgos y Mitigaciones](../docs/etl_risks_mitigations.md): Limitaciones y planes futuros
- [Checklist Producción](../docs/etl_production_checklist.md): Pasos para hardening

## 🧪 Testing

```bash
# Tests unitarios
pytest tests/test_etl_domain.py

# Tests de integración
pytest tests/test_etl_adapters.py

# Demo completo
python examples/demo_etl.py
```

## 📦 Estructura del Proyecto

```
src/etl_multiagent/
├── domain/
│   ├── entities.py         # DataSource, DataBatch, TransformationJob, DataDestination
│   └── use_cases.py        # IngestData, TransformData, LoadData, ReconcileJobResult
├── ports/
│   └── __init__.py         # SourcePort, TransformPort, ValidationPort, DestinationPort
├── adapters/
│   ├── sources.py          # FileSourceAdapter, S3SourceAdapter (stub)
│   ├── destinations.py     # FileDestinationAdapter, BigQueryDestinationAdapter (stub)
│   └── transformers.py     # PandasTransformAdapter, ValidationAdapter
├── crews/
│   └── etl_orchestration_crew.py  # 5 agentes especializados
├── flows/
│   └── etl_pipeline_flow.py       # Flow con listen-based orchestration
└── config/
    └── settings.py         # ETLSettings (pydantic)

config/
├── etl_agents.yaml         # Configuración de agentes
├── etl_tasks.yaml          # Configuración de tareas
└── etl_config.yaml         # Configuración de herramientas
```

## 🔧 Extensibilidad

### Agregar Nueva Fuente

1. Implementar adaptador:
```python
class BigQuerySourceAdapter:
    def read(self, source: DataSource) -> DataBatch:
        # Implementar query a BigQuery
        ...
```

2. Registrar en use case:
```python
if source.kind == "bigquery":
    adapter = BigQuerySourceAdapter()
```

### Agregar Nuevo Destino

1. Implementar adaptador:
```python
class SnowflakeDestinationAdapter:
    def write(self, batch: DataBatch, dest: DataDestination) -> dict:
        # Implementar carga a Snowflake
        ...
```

2. Usar en flow o crew sin modificar dominio.

## 🤝 Contribución

1. Fork el repositorio
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -m "Add nueva funcionalidad"`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

## 📄 Licencia

MIT License - ver [LICENSE](../LICENSE) para detalles.

## 🙏 Agradecimientos

- [CrewAI](https://github.com/crewAIInc/crewAI) por el framework multi-agente
- [Alistair Cockburn](https://alistair.cockburn.us/hexagonal-architecture/) por Hexagonal Architecture
- Comunidad open source por herramientas y feedback
