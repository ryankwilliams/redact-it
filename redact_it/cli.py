"""Redact-it cli module."""
import functools
from typing import Any

import click

from redact_it.redact_yaml import RedactItYaml


@click.group()
def cli():
    """redact-it"""


def default_params(func) -> Any:
    """Decorator for setting common options for each command.

    :param func: the function being wrapped
    :return: the wrapped function
    """

    @click.option("-c", "--config", help="Redact it configuration file")
    @click.option("-fp", "--file-path", help="File path to redact files")
    @click.option("--dry-run", is_flag=True, help="Enable dry run")
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        return func(*args, **kwargs)

    return wrapper


@cli.command()
@default_params
def yaml(config: str, file_path: str, dry_run: bool) -> None:
    """redact-it yaml"""
    if not config:
        print(
            "No redact-it configuration file provided, pass one "
            "`-c or--config` and try again."
        )
        raise SystemExit(1)

    redact_it_yaml: RedactItYaml = RedactItYaml(config, file_path, dry_run)
    raise SystemExit(redact_it_yaml.redact())
