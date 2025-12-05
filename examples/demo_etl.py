#!/usr/bin/env python3
"""
ETL Pipeline Demo - Hexagonal Architecture

Demonstrates end-to-end ETL using use cases, ports, and adapters (no CrewAI agents).
"""
from pathlib import Path
import pandas as pd

from etl_multiagent.domain.entities import DataSource, DataBatch, TransformationJob, DataDestination
from etl_multiagent.domain.use_cases import IngestData, TransformData, LoadData, ReconcileJobResult
from etl_multiagent.adapters.sources import FileSourceAdapter
from etl_multiagent.adapters.destinations import FileDestinationAdapter
from etl_multiagent.adapters.transformers import PandasTransformAdapter, ValidationAdapter


def create_sample_data():
    """Create sample CSV for demo."""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    sample_file = data_dir / "sample_input.csv"
    
    df = pd.DataFrame({
        "id": [1, 2, 3, 4, 5],
        "name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
        "age": [25, 30, 35, 28, 32],
        "salary": [50000, 60000, 70000, 55000, 65000],
        "department": ["IT", "HR", "IT", "Finance", "HR"],
    })
    
    df.to_csv(sample_file, index=False)
    print(f"✓ Created sample data: {sample_file}")
    return sample_file


def run_etl_success_case():
    """Demo: Successful ETL pipeline execution using use cases."""
    print("\n" + "="*60)
    print("CASO DE ÉXITO: ETL Pipeline con validación OK")
    print("="*60)
    
    sample_file = create_sample_data()
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "sample_output.csv"
    
    try:
        # 1. Ingest data from source
        print("\n🔹 Step 1: Ingest data from source")
        source = DataSource(
            name="sample_input",
            kind="file",
            uri=str(sample_file),
            format="csv",
        )
        ingest_uc = IngestData(source_port=FileSourceAdapter())
        batch = ingest_uc.execute(source)
        print(f"  ✓ Ingested {batch.stats['rows']} rows, {batch.stats['cols']} columns")
        
        # 2. Transform data
        print("\n🔹 Step 2: Transform data with mappings")
        job = TransformationJob(
            source_schema=batch.schema or {},
            target_schema={
                "employee_id": "int64",
                "employee_name": "object",
                "employee_age": "int64",
            },
            mappings={
                "employee_id": "id",
                "employee_name": "name",
                "employee_age": "age",
            },
        )
        transform_uc = TransformData(transform_port=PandasTransformAdapter())
        batch = transform_uc.execute(batch, job)
        print(f"  ✓ Transformed to {len(batch.raw.columns)} columns")
        
        # 3. Validate data quality
        print("\n🔹 Step 3: Validate data quality")
        validation_uc = ReconcileJobResult(validation_port=ValidationAdapter())
        validation_report = validation_uc.execute(
            batch,
            rules={"check_nulls": True, "check_duplicates": True}
        )
        print(f"  ✓ Validation status: {validation_report['status']}")
        if validation_report.get('issues'):
            for issue in validation_report['issues']:
                print(f"    ⚠️  {issue}")
        
        # 4. Load to destination
        print("\n🔹 Step 4: Load to destination")
        destination = DataDestination(
            name="sample_output",
            kind="file",
            uri=str(output_file),
            format="csv",
        )
        load_uc = LoadData(destination_port=FileDestinationAdapter())
        load_result = load_uc.execute(batch, destination)
        print(f"  ✓ Loaded {load_result['rows_written']} rows to {load_result['path']}")
        
        print("\n✅ Pipeline completed successfully!")
            
    except Exception as e:
        print(f"\n❌ Pipeline failed: {e}")


def run_etl_failure_case():
    """Demo: ETL pipeline with controlled failure (missing file)."""
    print("\n" + "="*60)
    print("CASO DE FALLO CONTROLADO: Archivo fuente no existe")
    print("="*60)
    
    try:
        # Intentar leer archivo inexistente
        print("\n🔹 Attempting to ingest non-existent file")
        source = DataSource(
            name="nonexistent",
            kind="file",
            uri="data/nonexistent_file.csv",
            format="csv",
        )
        ingest_uc = IngestData(source_port=FileSourceAdapter())
        batch = ingest_uc.execute(source)
        
        print("\n❌ Se esperaba un error pero no se capturó")
            
    except FileNotFoundError as e:
        print(f"  ✅ FileNotFoundError capturado correctamente:")
        print(f"     {e}")
        print("\n✅ Error handling funcionó como esperado")
    except Exception as e:
        print(f"\n✅ Excepción capturada correctamente: {e}")


if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════╗
║  ETL Multi-Agent System - Hexagonal Architecture Demo     ║
║  Arquitectura: Ports & Adapters (Use Cases + Adapters)    ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    # Caso 1: Éxito
    run_etl_success_case()
    
    # Caso 2: Fallo controlado
    run_etl_failure_case()
    
    print("\n" + "="*60)
    print("Demo completado. Revisa outputs/ para los resultados.")
    print("="*60)
