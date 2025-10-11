"""Flow de Investigación de Incidentes (SST)

Stub funcional para orquestar una investigación básica de incidente.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any

try:
    from crewai.flow.flow import Flow, start, listen
except Exception:
    # Permite que el archivo exista aunque crewai no esté instalado aún
    class Flow:  # type: ignore
        def kickoff(self):
            return {
                "status": "ok",
                "message": "CrewAI no instalado. Stub ejecutado.",
            }

    def start():  # type: ignore
        def deco(fn):
            return fn
        return deco

    def listen(*_args, **_kwargs):  # type: ignore
        def deco(fn):
            return fn
        return deco


@dataclass
class IncidentState:
    site: str
    incident_type: str
    description: str
    witnesses: List[str] = field(default_factory=list)
    evidence: List[str] = field(default_factory=list)
    root_cause_analysis: Dict[str, Any] = field(default_factory=dict)
    corrective_actions: List[str] = field(default_factory=list)


class IncidentInvestigationFlow(Flow):
    """Flow simple de investigación de incidentes"""

    def __init__(self):
        super().__init__()
        self.state = IncidentState(
            site="",
            incident_type="",
            description="",
        )

    @start()
    def initialize(self):
        return {
            "message": "Inicializando investigación de incidente",
        }

    @listen(initialize)
    def collect_evidence(self, _):
        # Aquí podríamos invocar un crew de SST o herramientas
        self.state.evidence.extend(["foto_zona", "registro_mantenimiento", "testimonios"])
        return {
            "message": "Evidencia recopilada",
            "evidence": self.state.evidence,
        }

    @listen(collect_evidence)
    def analyze_root_cause(self, _):
        self.state.root_cause_analysis = {
            "method": "5 Whys",
            "root_cause": "Falta de mantenimiento preventivo",
        }
        return {
            "message": "Análisis de causa raíz completado",
        }

    @listen(analyze_root_cause)
    def propose_corrective_actions(self, _):
        self.state.corrective_actions = [
            "Implementar plan de mantenimiento preventivo",
            "Capacitaciones específicas para el equipo",
            "Actualización de procedimientos de seguridad",
        ]
        return {
            "message": "Acciones correctivas propuestas",
            "actions": self.state.corrective_actions,
        }
