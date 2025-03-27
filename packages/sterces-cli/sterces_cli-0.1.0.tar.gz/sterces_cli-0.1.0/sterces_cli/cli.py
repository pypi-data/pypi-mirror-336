"""Top level module cli from package sterces."""

import sys
from pathlib import Path
from typing import NoReturn, Optional

import click
from loguru import logger
from pykeepass.pykeepass import debug_setup
from sterces.db import ATTRIBUTES, StercesDatabase

from sterces_cli.constants import CONTEXT_SETTINGS, VERSION
from sterces_cli.entries import commands as entry_actions
from sterces_cli.foos import StrIntStrBool, add_arg_if
from sterces_cli.groups import commands as group_actions

HOME = Path.home()
DEFAULT_PASSWORD_FILE = HOME / ".sterces/.ssapeek"
DEFAULT_DATABASE_FILE = HOME / ".sterces/db.kdbx"


def _configure_logging(verbose: int) -> None:
    logger.remove()  # Remove the default handler.
    if verbose > 0:
        logger.add(sys.stderr, level="INFO")
    else:
        logger.add(sys.stderr, level="WARNING")


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option("-d", "--debug", count=True, default=0, help="increment debug level")
@click.option(
    "-D",
    "--db",
    "--database-file",
    default=DEFAULT_DATABASE_FILE,
    help="keepass db file ( default ~/.sterces/db.kdbx)",
)
@click.option(
    "-k",
    "--key-file",
    type=str,
    required=False,
    help="keepass key file (default None)",
)
@click.option(
    "-p",
    "--passphrase-file",
    default=DEFAULT_PASSWORD_FILE,
    help="passphrase file default ~/.sterces/.ssapeek",
)
@click.option(
    "-t",
    "--transformed-key",
    type=str,
    required=False,
    help="keepass transformed key (default None)",
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    default=0,
    help="increment verbosity level",
)
@click.option(
    "--warn/--no-warn", default=True, help="Warn permissions flag (default True)"
)
@click.version_option(VERSION)
@click.pass_context
def cli(
    ctx: click.Context,
    debug: int,
    db: str,
    key_file: Optional[str],
    transformed_key: Optional[str],
    passphrase_file: str,
    verbose: int,
    warn: bool,
) -> int:
    """Command interface for a KeePass database."""
    if debug == 0:
        _configure_logging(verbose)
    elif debug > 1:
        debug_setup()
    dbargs: StrIntStrBool = {"debug": debug, "verbose": verbose, "warn": warn}
    add_arg_if(dbargs, "db_fn", db)
    add_arg_if(dbargs, "pwd_fn", passphrase_file)
    add_arg_if(dbargs, "key_fn", key_file)
    add_arg_if(dbargs, "tf_key", transformed_key)
    ctx.obj = StercesDatabase(**dbargs)
    return 0


cli.add_command(group_actions.group)
cli.add_command(entry_actions.entry)

LU_HELP1 = """Lookup attribute of an entry.

ATTR must be one of:
   {0}

ATTR defaults to password when not specified
"""

LU_HELP = """
ATTR must be one of: {0}

ATTR defaults to password when not specified
"""

# class HelpLookupCmd(click.Command):
#     def format_help(self, ctx, formatter):
#         al = list(ATTRIBUTES)
#         al.sort()
#         click.echo(LU_HELP.format(", ".join(al)))

LUH = "{0}\n\nATTR must be one of: {1}\n\nATTR defaults to password when not specified"


def lu_help(ff):
    """
    Customize the lookup help message.

    :param f: function to decorate
    :return: decorated function
    """
    al = list(ATTRIBUTES)
    al.sort()
    ff.__doc__ = LUH.format(ff.__doc__, ", ".join(al))

    return ff


# @cli.command(cls=HelpLookupCmd)
@cli.command()
@click.argument("path", type=str)
@click.argument("attr", default="password")
@click.pass_obj
@lu_help
def lookup(ctx: StercesDatabase, path: str, attr: str) -> NoReturn:
    """Lookup attribute of an entry."""
    sys.exit(ctx.lookup(path, attr))


if __name__ == "__main__":
    sys.exit(cli())  # pragma no cover
