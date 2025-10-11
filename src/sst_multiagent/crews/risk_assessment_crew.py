"""Crew de Evaluación de Riesgos (SST)

Stub funcional mínimo para demostrar ejecución desde CLI global.
"""
from __future__ import annotations

from crewai import Agent, Task, Crew, Process


class RiskAssessmentCrew:
    """Crew básico para evaluar riesgos en un sitio de trabajo."""

    def __init__(self):
        # Agentes mínimos (pueden ser configurados vía YAML después)
        self.risk_analyst = Agent(
            role="SST Risk Analyst",
            goal="Identificar y priorizar riesgos laborales",
            backstory="Experto en evaluaciones de SST, normativa local e ISO 45001.",
            verbose=True,
            allow_delegation=False,
        )

        self.compliance_officer = Agent(
            role="SST Compliance Officer",
            goal="Verificar cumplimiento normativo de las recomendaciones",
            backstory="Especialista en cumplimiento SST y mejores prácticas.",
            verbose=True,
            allow_delegation=False,
        )

        self._crew = None

    def crew(self) -> Crew:
        if self._crew:
            return self._crew

        assess_task = Task(
            description=(
                "Realiza una evaluación inicial de riesgos para el sitio de trabajo, "
                "identificando peligros críticos, probabilidad, severidad y recomendaciones iniciales."
            ),
            agent=self.risk_analyst,
            expected_output=(
                "Lista priorizada de riesgos con nivel (Alto/Medio/Bajo), causas, consecuencias "
                "y medidas preventivas propuestas."
            ),
        )

        compliance_task = Task(
            description=(
                "Valida el plan de medidas preventivas con la normativa vigente (ISO 45001/OSHA) "
                "y agrega requisitos específicos aplicables."
            ),
            agent=self.compliance_officer,
            expected_output=(
                "Checklist de cumplimiento con referencias normativas y acciones de cierre."
            ),
        )

        self._crew = Crew(
            agents=[self.risk_analyst, self.compliance_officer],
            tasks=[assess_task, compliance_task],
            process=Process.sequential,
            verbose=True,
        )
        return self._crew
