"""Paquete raíz multi-dominio para orquestar múltiples grupos de agentes.

Subpaquetes esperados:
- marketing_multiagent: Dominio de Marketing Digital
- sst_multiagent: Dominio de Seguridad y Salud en el Trabajo (SST)

Incluye utilidades de descubrimiento de dominios, carga dinámica y CLI global.
"""

from importlib import import_module
from typing import Dict, List, Optional


def load_domain_module(domain: str):
    """Carga dinámicamente el subpaquete de dominio.

    domain: nombre del dominio (e.g., 'marketing', 'sst')
    returns: módulo del dominio (e.g., marketing_multiagent)
    """
    name_map = {
        "marketing": "marketing_multiagent",
        "sst": "sst_multiagent",
    }
    pkg = name_map.get(domain, domain)
    return import_module(pkg)
