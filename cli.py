#!/usr/bin/env python3
"""CLI Global - Punto de entrada desde la raíz del repositorio.

Permite ejecutar dominios de agentes desde cualquier ubicación en el repositorio.
"""

import sys
from pathlib import Path

# Agregar src al path para importar multiagent
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from multiagent.cli import main

if __name__ == "__main__":
    main()