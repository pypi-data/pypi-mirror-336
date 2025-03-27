"""Commands module entry of app package sterces-cli."""

import getpass
import sys
from typing import NoReturn, Optional

import click
import pyotp
from sterces.db import ATTRIBUTES, StercesDatabase
from sterces.foos import str_to_date

from sterces_cli.constants import CONTEXT_SETTINGS
from sterces_cli.foos import StrIntStrBool, add_arg, add_arg_if


@click.group()
@click.pass_context
def entry(ctx: click.Context, context_settings=CONTEXT_SETTINGS):
    """Command group for entry management."""


@entry.command()
@click.option("-e", "--expires", type=str, help="specify expire date/time")
@click.option("-n", "--notes", type=str, help="specify notes")
@click.option("-o", "--otp", type=str, help="specify notes")
@click.option("-p", "--password", type=str, help="specify password")
@click.option("-P", "--path", type=str, required=True, help="specify path of entry")
@click.option("-T", "--tags", type=str, multiple=True, help="specify tags")
@click.option("-u", "--username", type=str, help="specify username")
@click.option("--url", type=str, help="specify url")
@click.pass_obj
def add(  # noqa: WPS231, C901
    ctx: StercesDatabase,
    expires: Optional[str],
    notes: Optional[str],
    otp: Optional[str],
    password: Optional[str],
    path: str,
    tags: Optional[list[str]],
    url: Optional[str],
    username: Optional[str],
) -> NoReturn:
    """Add or update an entry."""
    sgrawk: StrIntStrBool = {}
    if not path:
        raise ValueError("Path option cannot be empty")
    if expires:
        expiry = str_to_date(expires)
        if expiry is None:
            raise ValueError("Invalid date time string: {0}".format(expires))
    else:
        expiry = None
    if otp:
        parsed = pyotp.parse_uri(otp)
        if parsed is None:
            raise ValueError("Invalid otp uri: {0}".format(otp))
    if not password:
        password = getpass.getpass()
    add_arg_if(sgrawk, "notes", notes)
    add_arg_if(sgrawk, "otp", otp)
    add_arg_if(sgrawk, "password", password)
    add_arg_if(sgrawk, "url", url)
    add_arg_if(sgrawk, "username", username)
    sys.exit(ctx.store(path, expiry, tags, **sgrawk))


@entry.command()
@click.option(
    "-a",
    "--attrs",
    multiple=True,
    required=True,
    type=str,
    help="specify attributes to update",
)
@click.option("-e", "--expires", type=str, help="specify expire date/time")
@click.option("-n", "--notes", type=str, help="specify notes")
@click.option("-o", "--otp", type=str, help="specify notes")
@click.option("-p", "--password", type=str, help="specify password")
@click.option("-P", "--path", type=str, required=True, help="specify path of entry")
@click.option("-T", "--tags", type=str, multiple=True, help="specify tags")
@click.option("-u", "--username", type=str, help="specify username")
@click.option("--url", type=str, help="specify url")
@click.pass_obj
def update(
    ctx: StercesDatabase,
    attrs: list[str],
    expires: Optional[str],
    notes: Optional[str],
    otp: Optional[str],
    password: Optional[str],
    path: str,
    tags: Optional[list[str]],
    url: Optional[str],
    username: Optional[str],
) -> NoReturn:
    """Update specified attributes of entry."""
    sgrawk: dict[str, Optional[str]] = {}
    for attr in attrs:
        if attr not in ATTRIBUTES:
            raise ValueError(
                "Invalid attribute: {0} Must be one of: {1}".format(
                    attr, ",".join(ATTRIBUTES)
                )
            )
        add_arg(sgrawk, attr, eval(attr))  # noqa: WPS421
    sys.exit(ctx.update(path, **sgrawk))


@entry.command()
@click.option("-P", "--path", type=str, required=True, help="specify path of entry")
@click.pass_obj
def remove(ctx: StercesDatabase, path: str) -> NoReturn:
    """Remove specified entry."""
    sys.exit(ctx.remove(path))


@entry.command()
@click.option("-P", "--path", type=str, help="specify path of entry")
@click.option(
    "--mask/--no-mask", default=True, help="mask password flag (default True)"
)
@click.pass_obj
def show(ctx: StercesDatabase, path: Optional[str], mask: bool) -> NoReturn:
    """Show specified entry or all entries if path not specified."""
    sys.exit(ctx.show(path, mask))


@entry.command()
@click.option("-P", "--path", type=str, help="specify path of entry")
@click.option(
    "-i", "--indent", type=int, default=0, help="specify indent level, default 0"
)
@click.option(
    "--mask/--no-mask", default=True, help="mask password flag (default True)"
)
@click.pass_obj
def dump(
    ctx: StercesDatabase, path: Optional[str], mask: bool, indent: int
) -> NoReturn:
    """Dump specified entry or all entries if path not specified."""
    sys.exit(ctx.dump(path, mask, indent))
