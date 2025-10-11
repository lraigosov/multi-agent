"""Tool: Búsqueda de normativa aplicable (SST)

Ejemplo de herramienta simple que en el futuro consultará bases normativas.
"""
from __future__ import annotations

try:
    from crewai_tools import BaseTool
    from pydantic import BaseModel, Field
except Exception:
    # Stubs mínimos si aún no está instalado
    class BaseModel:  # type: ignore
        pass

    class BaseTool:  # type: ignore
        name: str = ""
        description: str = ""

        def _run(self, *args, **kwargs):
            raise NotImplementedError

    def Field(*args, **kwargs):  # type: ignore
        return None


class RegulatorySearchInput(BaseModel):
    query: str = Field(description="Búsqueda o código de normativa")
    country: str = Field(description="País o jurisdicción", default="ES")


class RegulatorySearchTool(BaseTool):
    name: str = "Regulatory Search Tool"
    description: str = (
        "Busca normativa SST aplicable a una consulta dada (stub)."
    )

    args_schema = RegulatorySearchInput

    def _run(self, query: str, country: str = "ES") -> str:
        # En una versión real, consultaría fuentes normativas
        return (
            f"Resultados simulados para '{query}' en jurisdicción {country}: "
            f"ISO 45001:2018, RD 1215/1997, Ley 31/1995"
        )
