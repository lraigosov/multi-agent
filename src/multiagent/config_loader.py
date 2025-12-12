"""Cargador de configuración global desde config/domains.yaml
Permite habilitar/deshabilitar dominios y sobreescribir el registro por defecto.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Any
import yaml

from .registry import registry


def load_domains_config(config_path: str | Path = "config/domains.yaml") -> Dict[str, Any]:
    p = Path(config_path)
    if not p.exists():
        return {}
    with p.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data


def apply_domains_config(config: Dict[str, Any]) -> None:
    domains = (config or {}).get("domains", {})
    # Por ahora, asumimos que registry ya contiene entradas. Aquí podríamos deshabilitar.
    for key, meta in domains.items():
        enabled = meta.get("enabled", True)
        if not enabled:
            # Nota: simplificado, en una versión futura podríamos remover del registry
            pass
        # En el futuro: actualizar módulos o descripciones si difieren
