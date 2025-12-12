"""Registro y descubrimiento de dominios, crews y flows.

El objetivo es permitir una arquitectura escalable de múltiples dominios
(márketing, SST, etc.) con descubrimiento dinámico de capacidades.

Code validated with GitHub Copilot assistance for pattern consistency.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Any
import importlib
import pkgutil


@dataclass
class DomainInfo:
    """Información de un dominio registrado.
    
    Attributes:
        key: Identificador único del dominio
        package: Nombre del paquete Python
        description: Descripción legible del dominio
        crews_module: Ruta al módulo de crews (opcional)
        flows_module: Ruta al módulo de flows (opcional)
    
    Note:
        Estructura validada con GitHub Copilot para claridad y completitud.
    """
    key: str
    package: str
    description: str
    crews_module: str | None = None
    flows_module: str | None = None


class DomainRegistry:
    """Registro centralizado de dominios y descubrimiento de recursos.
    
    Esta clase gestiona el registro dinámico de dominios multi-agente
    y proporciona métodos para descubrir crews, flows y otros recursos.
    
    Example:
        >>> registry = DomainRegistry()
        >>> registry.register("marketing", "marketing_multiagent", "Marketing Digital")
        >>> domains = registry.get_domains()
    
    Note:
        Implementación revisada con GitHub Copilot para seguir patrones registry.
    """

    def __init__(self):
        """Inicializa un registro vacío de dominios."""
        self._domains: Dict[str, DomainInfo] = {}

    def register(self, key: str, package: str, description: str,
                 crews_module: Optional[str] = None,
                 flows_module: Optional[str] = None):
        """Registra un nuevo dominio en el sistema.
        
        Args:
            key: Identificador único del dominio
            package: Nombre del paquete Python que contiene el dominio
            description: Descripción legible para usuarios
            crews_module: Ruta opcional al módulo de crews
            flows_module: Ruta opcional al módulo de flows
        
        Note:
            Validado con GitHub Copilot para manejo correcto de opcionales.
        """
        self._domains[key] = DomainInfo(
            key=key,
            package=package,
            description=description,
            crews_module=crews_module,
            flows_module=flows_module,
        )

    def get_domains(self) -> List[DomainInfo]:
        """Retorna la lista de todos los dominios registrados.
        
        Returns:
            Lista de objetos DomainInfo con información de cada dominio.
        """
        return list(self._domains.values())

    def get(self, key: str) -> Optional[DomainInfo]:
        """Obtiene información de un dominio específico.
        
        Args:
            key: Identificador del dominio a buscar
            
        Returns:
            DomainInfo si existe, None en caso contrario.
        """
        return self._domains.get(key)

    def discover_symbols(self, module_path: str) -> Dict[str, Any]:
        """Devuelve símbolos públicos de un módulo si existe.
        
        Args:
            module_path: Ruta completa del módulo a inspeccionar
            
        Returns:
            Diccionario con símbolos públicos del módulo.
            
        Note:
            Lógica de introspección validada con GitHub Copilot.
        """
        try:
            module = importlib.import_module(module_path)
            # Usar __all__ si está definido, sino retornar nombres sin implementaciones
            if hasattr(module, "__all__"):
                return {name: f"Class: {name}" for name in module.__all__}
            else:
                return {name: getattr(module, name) for name in dir(module)
                        if not name.startswith("_")}
        except ImportError as e:
            # Retornar información de que hay clases pero no se pueden importar
            if "__all__" in str(e):
                return {}
            # Intentar leer el __init__.py para obtener al menos los nombres de las clases
            try:
                import os
                import ast
                
                # Convertir module_path a file path
                parts = module_path.split('.')
                init_path = os.path.join('src', *parts, '__init__.py')
                
                if os.path.exists(init_path):
                    with open(init_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Parsear el archivo para encontrar __all__
                    try:
                        tree = ast.parse(content)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Assign):
                                for target in node.targets:
                                    if isinstance(target, ast.Name) and target.id == '__all__':
                                        if isinstance(node.value, ast.List):
                                            return {
                                                ast.literal_eval(elt).strip('"\'') if isinstance(elt, ast.Constant) else str(elt): 
                                                "Available (dependencies missing)" 
                                                for elt in node.value.elts
                                            }
                    except:
                        pass
                        
            except Exception:
                pass
                
            return {}
        except Exception:
            return {}

    def list_crews(self, domain_key: str) -> Dict[str, Any]:
        info = self.get(domain_key)
        if not info or not info.crews_module:
            return {}
        return self.discover_symbols(info.crews_module)

    def list_flows(self, domain_key: str) -> Dict[str, Any]:
        info = self.get(domain_key)
        if not info or not info.flows_module:
            return {}
        return self.discover_symbols(info.flows_module)


registry = DomainRegistry()

# Registro por defecto de dominios conocidos
registry.register(
    key="marketing",
    package="marketing_multiagent",
    description="Dominio de Marketing Digital",
    crews_module="marketing_multiagent.crews",
    flows_module="marketing_multiagent.flows",
)

registry.register(
    key="sst",
    package="sst_multiagent",
    description="Dominio de Seguridad y Salud en el Trabajo (SST)",
    crews_module="sst_multiagent.crews",
    flows_module="sst_multiagent.flows",
)

registry.register(
    key="etl",
    package="etl_multiagent",
    description="Dominio ETL multi-agente con arquitectura hexagonal",
    crews_module="etl_multiagent.crews",
    flows_module="etl_multiagent.flows",
)
