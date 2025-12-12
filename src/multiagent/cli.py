#!/usr/bin/env python3
"""CLI Global para gestionar múltiples dominios de agentes (marketing, sst, etc.).

Permite:
- Listar dominios, crews y flows disponibles
- Ejecutar crews y flows por dominio
- Gestionar configuración global desde la raíz del repositorio
"""
from __future__ import annotations

import os
import json
from pathlib import Path
from typing import Optional

import click
from dotenv import load_dotenv

from .registry import registry

# Compute domain choices dynamically to avoid hardcoding
DOMAIN_CHOICES = [d.key for d in registry.get_domains()]


def setup_env():
    load_dotenv()
    Path("outputs").mkdir(exist_ok=True, parents=True)
    Path("logs").mkdir(exist_ok=True, parents=True)


@click.group()
@click.version_option("1.0.0")
def cli():
    """CLI Global - Multi-Agent Orchestrator"""
    setup_env()


@cli.command("domains")
def list_domains():
    """Lista dominios disponibles"""
    domains = registry.get_domains()
    if not domains:
        click.echo("No hay dominios registrados.")
        return
    click.echo("Dominios disponibles:")
    for d in domains:
        click.echo(f"- {d.key}: {d.description} (package: {d.package})")


@cli.command("crews")
@click.option("--domain", required=True, help="Dominio a inspeccionar (e.g., marketing, sst)")
def list_crews(domain: str):
    """Lista crews disponibles para un dominio"""
    symbols = registry.list_crews(domain)
    if not symbols:
        click.echo("No se encontraron crews o el dominio no existe.")
        return
    click.echo(f"Crews en dominio '{domain}':")
    for name, sym in symbols.items():
        click.echo(f"- {name}")


@cli.command("flows")
@click.option("--domain", required=True, help="Dominio a inspeccionar (e.g., marketing, sst)")
def list_flows(domain: str):
    """Lista flows disponibles para un dominio"""
    symbols = registry.list_flows(domain)
    if not symbols:
        click.echo("No se encontraron flows o el dominio no existe.")
        return
    click.echo(f"Flows en dominio '{domain}':")
    for name, sym in symbols.items():
        click.echo(f"- {name}")


@cli.command("run-crew")
@click.option("--domain", required=True, type=click.Choice(DOMAIN_CHOICES))
@click.option("--crew", required=True, help="Nombre de la clase del crew a ejecutar")
@click.option("--inputs", help="JSON string con inputs para kickoff")
def run_crew(domain: str, crew: str, inputs: Optional[str]):
    """Ejecuta un crew por dominio"""
    from importlib import import_module

    info = registry.get(domain)
    if not info or not info.crews_module:
        click.echo("Dominio o módulo de crews no disponible")
        raise SystemExit(1)

    mod = import_module(info.crews_module)
    if not hasattr(mod, crew):
        click.echo(f"Crew '{crew}' no encontrado en dominio '{domain}'")
        raise SystemExit(1)

    crew_cls = getattr(mod, crew)
    inputs_dict = json.loads(inputs) if inputs else {}

    instance = crew_cls()
    result = instance.crew().kickoff(inputs=inputs_dict)

    out_file = Path("outputs") / f"{domain}_{crew}_result.md"
    out_file.write_text(str(result), encoding="utf-8")
    click.echo(f"Resultado guardado en {out_file}")


@cli.command("run-flow")
@click.option("--domain", required=True, type=click.Choice(DOMAIN_CHOICES))
@click.option("--flow", required=True, help="Nombre de la clase del flow a ejecutar")
@click.option("--state", help="JSON string con estado inicial del flow")
def run_flow(domain: str, flow: str, state: Optional[str]):
    """Ejecuta un flow por dominio"""
    from importlib import import_module

    info = registry.get(domain)
    if not info or not info.flows_module:
        click.echo("Dominio o módulo de flows no disponible")
        raise SystemExit(1)

    mod = import_module(info.flows_module)
    if not hasattr(mod, flow):
        click.echo(f"Flow '{flow}' no encontrado en dominio '{domain}'")
        raise SystemExit(1)

    flow_cls = getattr(mod, flow)
    flow_instance = flow_cls()

    # Si el flow define un State pydantic/dataclass, el usuario puede pasar JSON
    if state:
        try:
            data = json.loads(state)
            if hasattr(flow_instance, "state") and hasattr(flow_instance.state, "__class__"):
                # Si la clase state existe y es instanciable con **data
                try:
                    state_type = type(flow_instance.state)
                    flow_instance.state = state_type(**data)
                except Exception:
                    # Fallback: asignación directa
                    flow_instance.state = data
            else:
                flow_instance.state = data
        except json.JSONDecodeError:
            click.echo("El parámetro --state no es JSON válido")
            raise SystemExit(1)

    result = flow_instance.kickoff()

    out_file = Path("outputs") / f"{domain}_{flow}_result.md"
    out_file.write_text(str(result), encoding="utf-8")
    click.echo(f"Resultado guardado en {out_file}")


def main():
    cli()


if __name__ == "__main__":
    main()
