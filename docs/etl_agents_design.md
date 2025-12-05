# Diseño Detallado de Agentes ETL (Arquitectura Propuesta)

⚠️ **Nota**: Este documento describe la arquitectura **propuesta** de agentes multi-agente con CrewAI. La implementación actual del MVP utiliza **casos de uso directos** sin orquestación de agentes LLM.

La integración con CrewAI está disponible en `src/etl_multiagent/crews/etl_orchestration_crew.py` con 5 agentes básicos y puede ampliarse con los agentes adicionales descritos aquí.

## 1. Orchestrator / Workflow Agent

**Rol**: ETL Workflow Orchestrator

**Objetivo (Goal)**:
Interpretar las instrucciones del usuario, descomponer la solicitud en sub-tareas ETL, asignar trabajo a los demás agentes y coordinar el flujo manteniendo el estado del job.

**Backstory**:
Eres un ingeniero de datos experimentado con más de 10 años orquestando pipelines ETL complejos. Tu especialidad es descomponer procesos en pasos atómicos, coordinar equipos de especialistas y mantener la trazabilidad del estado del pipeline.

**Inputs**:
- User request (texto natural): "Toma este archivo CSV de ventas y cárgalo en BigQuery con limpieza de duplicados"
- Context: archivos disponibles, credenciales, restricciones

**Outputs**:
- Execution plan JSON:
  ```json
  {
    "source": {"uri": "data/sales.csv", "format": "csv"},
    "destination": {"uri": "project.dataset.table", "format": "bigquery"},
    "transformations": ["remove_duplicates", "cast_types"],
    "validation_rules": {"check_nulls": true}
  }
  ```

**Herramientas**:
- `ParseRequestTool`: Extraer intención del usuario
- `PlanGeneratorTool`: Generar plan de ejecución
- `StateTrackerTool`: Mantener estado del job (pending, in_progress, completed, failed)

**LLM Recomendado**: GPT-4o o Gemini 2.0 Pro (razonamiento complejo y planificación)

**Configuración LLM**:
```yaml
model_provider: openai
model_name: gpt-4o
temperature: 0.2  # Baja para decisiones consistentes
max_tokens: 2000
```

---

## 2. Source Ingestion Agent

**Rol**: Source Ingestion Specialist

**Objetivo (Goal)**:
Conectarse a la fuente indicada, usar herramientas específicas (adaptadores a archivos, APIs, DBs), descargar/leer los datos brutos y pasarlos a un formato de trabajo (dataframe).

**Backstory**:
Eres un experto en ingesta de datos con experiencia en múltiples formatos (CSV, Parquet, Excel, JSON) y fuentes (archivos locales, S3, GCS, APIs REST, bases de datos). Entiendes encodings, delimitadores, compresión y esquemas.

**Inputs**:
- DataSource entity: `{name, kind, uri, format, options}`

**Outputs**:
- DataBatch entity: `{raw: DataFrame, schema: dict, stats: dict, metadata: dict}`

**Herramientas**:
- `FileReaderTool`: Lee archivos locales (CSV, Parquet, Excel)
- `S3ReaderTool`: Lee desde buckets S3/GCS
- `APIReaderTool`: Consume APIs REST
- `DatabaseReaderTool`: Query a databases
- `SchemaInferenceTool`: Infiere esquema automáticamente

**LLM Recomendado**: Gemini 2.0 Flash (rápido para tareas de extracción estructurada)

**Configuración LLM**:
```yaml
model_provider: gemini
model_name: gemini-2.0-flash
temperature: 0.1  # Muy baja, tarea determinística
max_tokens: 1000
```

---

## 3. Schema & Profiling Agent

**Rol**: Schema and Data Profiling Analyst

**Objetivo (Goal)**:
Inferir esquema, tipos, cardinalidades, estadísticas básicas. Detectar problemas de calidad evidentes (nulos, duplicados, outliers básicos). Proponer un contrato de datos intermedio.

**Backstory**:
Eres un analista de datos con experiencia en perfilado de datasets. Conoces distribuciones estadísticas, patrones de datos y mejores prácticas de calidad. Tu objetivo es revelar la "forma" de los datos antes de transformarlos.

**Inputs**:
- DataBatch con raw data

**Outputs**:
- Data profiling report JSON:
  ```json
  {
    "schema": {"col1": "int64", "col2": "object"},
    "stats": {
      "rows": 10000,
      "cols": 5,
      "nulls_per_col": {"col1": 0, "col2": 150},
      "duplicates": 23,
      "outliers": {"col3": [1, 5, 99]}
    },
    "recommendations": ["Remove duplicates", "Impute nulls in col2"]
  }
  ```

**Herramientas**:
- `DataProfilingTool`: Genera estadísticas descriptivas
- `OutlierDetectorTool`: Detecta anomalías
- `PatternRecognitionTool`: Identifica patrones (emails, fechas, etc.)

**LLM Recomendado**: Claude 3.5 Sonnet (excelente para análisis y contexto largo)

**Configuración LLM**:
```yaml
model_provider: anthropic
model_name: claude-3-5-sonnet
temperature: 0.3
max_tokens: 3000
```

---

## 4. Transformation & Mapping Agent

**Rol**: Transformation and Mapping Engineer

**Objetivo (Goal)**:
Definir el plan de transformación entre esquema origen y esquema destino. Aplicar reglas de negocio (limpieza, normalización, agregaciones, enrichment). Generar o actualizar código/plantillas de transformación.

**Backstory**:
Eres un ingeniero ETL senior con experiencia en SQL, Python y frameworks de transformación (dbt, Spark). Tu especialidad es diseñar mappings eficientes y aplicar reglas de negocio complejas manteniendo integridad de datos.

**Inputs**:
- DataBatch (raw)
- TransformationJob: `{source_schema, target_schema, mappings, rules}`

**Outputs**:
- Transformed DataBatch
- Transformation code (SQL o Python) generado

**Herramientas**:
- `TransformationEngineTool`: Aplica mappings y reglas
- `TypeCasterTool`: Convierte tipos de datos
- `CleansingTool`: Limpia strings, normaliza fechas
- `EnrichmentTool`: Agrega columnas calculadas

**LLM Recomendado**: GPT-4o (balance calidad/costo para generación de código)

**Configuración LLM**:
```yaml
model_provider: openai
model_name: gpt-4o
temperature: 0.15
max_tokens: 2500
```

---

## 5. Validation & QA Agent

**Rol**: Data Quality and Validation Specialist

**Objetivo (Goal)**:
Ejecutar reglas de validación de calidad de datos. Comparar resultados contra umbrales o expectativas definidas. Decidir si el lote es apto para carga o requiere correcciones.

**Backstory**:
Eres un especialista en calidad de datos con experiencia en frameworks de testing (Great Expectations, dbt tests). Tu misión es garantizar que solo datos válidos y confiables lleguen a producción.

**Inputs**:
- DataBatch (transformed)
- Validation rules: `{check_nulls, check_duplicates, check_types, check_ranges}`

**Outputs**:
- Validation report JSON:
  ```json
  {
    "status": "pass" | "warning" | "fail",
    "issues": ["col2 has 150 nulls", "23 duplicate rows"],
    "rows_validated": 10000,
    "fitness_for_load": true
  }
  ```

**Herramientas**:
- `ValidationEngineTool`: Ejecuta checks configurables
- `ThresholdComparatorTool`: Compara métricas vs umbrales
- `ReferentialIntegrityTool`: Valida foreign keys

**LLM Recomendado**: Gemini 2.0 Flash (rápido, tarea bien definida)

**Configuración LLM**:
```yaml
model_provider: gemini
model_name: gemini-2.0-flash
temperature: 0.05  # Muy baja, decisiones críticas
max_tokens: 1500
```

---

## 6. Destination Loader Agent

**Rol**: Destination Loader and Writer

**Objetivo (Goal)**:
Escribir los datos transformados en el destino elegido. Gestionar creación/actualización de tablas o archivos. Devolver identificadores de carga, paths y metadatos.

**Backstory**:
Eres un ingeniero de data warehousing con experiencia en Postgres, BigQuery, Snowflake, y sistemas de archivos distribuidos. Conoces estrategias de carga (replace, append, upsert), particionamiento y optimización de escritura.

**Inputs**:
- DataBatch (validated)
- DataDestination: `{name, kind, uri, format, options}`

**Outputs**:
- Load result JSON:
  ```json
  {
    "status": "success",
    "path": "outputs/sales_clean.csv",
    "rows_written": 9977,
    "warnings": []
  }
  ```

**Herramientas**:
- `FileWriterTool`: Escribe CSV, Parquet, Excel
- `DatabaseWriterTool`: Carga a Postgres, MySQL
- `BigQueryWriterTool`: Carga a BigQuery
- `S3WriterTool`: Escribe a buckets S3/GCS

**LLM Recomendado**: GPT-3.5 Turbo (tarea operativa, menor costo)

**Configuración LLM**:
```yaml
model_provider: openai
model_name: gpt-3.5-turbo
temperature: 0.1
max_tokens: 1000
```

---

## 7. Observer / Logging & Autocorrection Agent (Opcional en MVP)

**Rol**: Pipeline Observer and Autocorrection Specialist

**Objetivo (Goal)**:
Recibir los logs de todos los agentes. Analizar errores recurrentes y patrones de fallo. Sugerir ajustes en prompts, reglas y mappings para futuras ejecuciones.

**Backstory**:
Eres un SRE y MLOps engineer especializado en observabilidad y reliability de pipelines. Tu expertise incluye análisis de logs, detección de anomalías y autocorrección basada en patrones históricos.

**Inputs**:
- Pipeline execution logs
- Error messages y stack traces
- Historical run data

**Outputs**:
- Autocorrection suggestions JSON:
  ```json
  {
    "patterns_detected": ["FileNotFoundError en 3 de últimas 5 runs"],
    "suggestions": [
      "Verificar permisos de lectura en source",
      "Agregar retry con backoff exponencial",
      "Validar existencia de archivo antes de lectura"
    ],
    "learned_rules": {"always_check_file_exists": true}
  }
  ```

**Herramientas**:
- `LogAnalyzerTool`: Parsea y analiza logs estructurados
- `PatternDetectorTool`: Detecta errores recurrentes
- `KnowledgeBaseTool`: Almacena/recupera aprendizajes

**LLM Recomendado**: Claude 3.5 Sonnet (análisis profundo, contexto largo)

**Configuración LLM**:
```yaml
model_provider: anthropic
model_name: claude-3-5-sonnet
temperature: 0.4  # Mayor creatividad para sugerencias
max_tokens: 4000
```

---

## Flujo de Mensajes Entre Agentes

```
User Request
     │
     ▼
[Orchestrator Agent] ──── Parse & Plan ───┐
     │                                      │
     ├─► [Source Agent] ─── Ingest ───────►│
     │        │                              │
     │        ▼                              │
     ├─► [Profiling Agent] ─ Analyze ─────►│
     │        │                              │
     │        ▼                              │
     ├─► [Transform Agent] ─ Transform ───►│
     │        │                              │
     │        ▼                              │
     ├─► [Validation Agent] ─ Validate ───►│
     │        │                              │
     │        ▼                              │
     ├─► [Loader Agent] ──── Load ────────►│
     │                                      │
     ▼                                      ▼
[Observer Agent] ◄───── Logs & Feedback ◄──┘
     │
     ▼
Knowledge Base (for future runs)
```

## Autocorrección y Bucle de Mejora

### Mecanismos de Autocorrección

1. **Retry con Backoff**: Si un agente falla (ej. timeout de API), el orchestrator reintenta con delay incremental.

2. **Crítica y Revisión**: El Validation Agent revisa las decisiones del Transform Agent. Si detecta inconsistencias graves:
   - Retorna feedback al Transform Agent
   - Transform Agent ajusta mappings/reglas
   - Re-ejecuta transformación

3. **Aprendizaje de Patrones**: El Observer Agent registra:
   - Mappings exitosos por tipo de fuente/destino
   - Reglas de validación efectivas
   - Errores comunes y sus soluciones

4. **Almacenamiento de Conocimiento**:
   - Base de datos de "plantillas" de transformación reutilizables
   - Reglas de validación derivadas de ejecuciones previas
   - Configuraciones óptimas de LLM por tipo de tarea

### Ejemplo de Flujo de Autocorrección

```
1. Transform Agent aplica mapping inicial
2. Validation Agent detecta: "50% de valores nulos en columna crítica"
3. Validation Agent envía feedback: "Mapping incorrecto, revisar col_name"
4. Transform Agent recibe feedback, ajusta mapping
5. Re-ejecuta transformación
6. Validation Agent valida nuevamente → OK
7. Observer Agent registra: "Mapping correcto para este tipo de fuente"
```
