#!/usr/bin/env python3
"""
ETL Pipeline Demo - Hexagonal Architecture with CrewAI

Demonstrates end-to-end ETL flow using use cases, ports, and adapters.
"""
from pathlib import Path
import pandas as pd

from etl_multiagent.flows.etl_pipeline_flow import ETLPipelineFlow, ETLFlowState


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
    """Demo: Successful ETL pipeline execution."""
    print("\n" + "="*60)
    print("CASO DE ÉXITO: ETL Pipeline con validación OK")
    print("="*60)
    
    sample_file = create_sample_data()
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "sample_output.csv"
    
    state = ETLFlowState(
        source_uri=str(sample_file),
        source_format="csv",
        dest_uri=str(output_file),
        dest_format="csv",
        mappings={
            "employee_id": "id",
            "employee_name": "name",
            "employee_age": "age",
        },
        target_schema={
            "employee_id": "int64",
            "employee_name": "object",
            "employee_age": "int64",
        },
    )
    
    flow = ETLPipelineFlow()
    flow.state = state
    
    try:
        result = flow.kickoff()
        
        print("\n📊 Pipeline Result:")
        print(f"  - Batch rows: {state.batch.stats['rows'] if state.batch else 'N/A'}")
        print(f"  - Validation: {state.validation_report.get('status') if state.validation_report else 'N/A'}")
        print(f"  - Load result: {state.load_result.get('status') if state.load_result else 'N/A'}")
        print(f"  - Output: {state.load_result.get('path') if state.load_result else 'N/A'}")
        
        if state.errors:
            print(f"\n⚠️  Errors: {state.errors}")
        else:
            print("\n✅ Pipeline completed successfully!")
            
    except Exception as e:
        print(f"\n❌ Pipeline failed: {e}")


def run_etl_failure_case():
    """Demo: ETL pipeline with controlled failure (missing file)."""
    print("\n" + "="*60)
    print("CASO DE FALLO CONTROLADO: Archivo fuente no existe")
    print("="*60)
    
    state = ETLFlowState(
        source_uri="data/nonexistent_file.csv",
        source_format="csv",
        dest_uri="outputs/will_not_be_created.csv",
        dest_format="csv",
        mappings={},
        target_schema={},
    )
    
    flow = ETLPipelineFlow()
    flow.state = state
    
    try:
        result = flow.kickoff()
        
        if state.errors:
            print(f"\n⚠️  Errors capturados correctamente:")
            for err in state.errors:
                print(f"  - {err}")
            print("\n✅ Error handling funcionó como esperado")
        else:
            print("\n❌ Se esperaba un error pero no se capturó")
            
    except Exception as e:
        print(f"\n✅ Excepción capturada correctamente: {e}")


if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════╗
║  ETL Multi-Agent System - Hexagonal Architecture Demo     ║
║  Arquitectura: Ports & Adapters + CrewAI                  ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    # Caso 1: Éxito
    run_etl_success_case()
    
    # Caso 2: Fallo controlado
    run_etl_failure_case()
    
    print("\n" + "="*60)
    print("Demo completado. Revisa outputs/ para los resultados.")
    print("="*60)
