"""Commands module group of package sterces."""

import sys
from typing import NoReturn

import click
from sterces.constants import ADD, REMOVE, SHOW
from sterces.db import StercesDatabase

from sterces_cli.constants import CONTEXT_SETTINGS


@click.group()
@click.pass_context
def group(ctx: click.Context, context_settings=CONTEXT_SETTINGS):
    """Command group for group management."""


@group.command()
@click.option("-p", "--path", type=str, help="specify group path")
@click.option("--quiet/--no-quiet", default=True, help="specify quiet flag")
@click.pass_obj
def add(ctx: StercesDatabase, path: str, quiet: bool) -> NoReturn:
    """Add group and show."""
    sys.exit(ctx.group(path, ADD, quiet))


@group.command()
@click.option("-p", "--path", type=str, help="specify group path")
@click.option("--quiet/--no-quiet", default=True, help="specify quiet flag")
@click.pass_obj
def remove(ctx: StercesDatabase, path: str, quiet: bool) -> NoReturn:
    """Remove group and show."""
    sys.exit(ctx.group(path, REMOVE, quiet))


@group.command()
@click.pass_obj
def show(ctx: StercesDatabase) -> NoReturn:
    """Show groups."""
    sys.exit(ctx.group(None, SHOW, quiet=False))
