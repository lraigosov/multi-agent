# ETL Hexagonal (Ports & Adapters, sin LLMs)

Pipeline ETL determinista construido con **arquitectura hexagonal** (Ports & Adapters). Usa pandas para ingesta/transformación/validación/carga y puede orquestarse con el `ETLPipelineFlow` (CrewAI Flow) incluido. No requiere LLMs para ejecutarse.

## 🎯 Características

- **Arquitectura Hexagonal**: Dominio desacoplado de frameworks e infraestructura
- **Puertos y Adaptadores**: Interfaces claras para sources, transformations, validations, destinations
- **Casos de Uso Funcionales**: Ingestión, transformación, validación y carga de datos
- **Validación Integrada**: Checks de nulls y duplicados
- **Extensible**: Fácil adición de nuevos adaptadores sin modificar dominio
- **Flow incluido**: `ETLPipelineFlow` orquesta los casos de uso con los adaptadores actuales

## 📋 Casos de Uso actuales

1. **Transformación Local**: CSV → CSV/Parquet/Excel con mapeo de columnas y type casting
2. **Validación de Calidad**: Detección de nulos y duplicados

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

**Nota**: La demo usa los casos de uso directamente. El Flow `ETLPipelineFlow` está disponible si quieres orquestación declarativa.

Ver [etl_architecture.md](etl_architecture.md) para el diagrama.

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

- [etl_architecture.md](etl_architecture.md): Diagrama y principios aplicados

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
