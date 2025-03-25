import os
import sys
import posixpath
import click
from click import Command

from rcdb.app_context import RcdbApplicationContext, parse_run_range
from rcdb import RCDBProvider
from rcdb.model import ConfigurationFile

from .ls import ls as ls_cmd
from .repair import repair as repair_grp
from .db import db as db_grp
from .rp import rp as rp_grp
from .web import web as web_cmd


pass_rcdb_context = click.make_pass_decorator(RcdbApplicationContext)


def get_default_config_path():
    return os.path.join(os.path.expanduser('~'), '.rcdb_user')


@click.group(invoke_without_command=True)
@click.option('--user-config', envvar='RCDB_USER_CONFIG', default=get_default_config_path,
              metavar='PATH', help='Changes the user config location.')
@click.option('--connection', '-c', envvar='RCDB_CONNECTION', help='Database connection string',
              default=None, required=False)
@click.option('--config', nargs=2, multiple=True,
              metavar='KEY VALUE', help='Overrides a config key/value pair.')
@click.option('--verbose', '-v', is_flag=True, help='Enables verbose mode.')
@click.version_option('1.0')
@click.pass_context
def rcdb_cli(ctx, user_config, connection, config, verbose):
    """'rcdb' is a RCDB (run conditions database) command line tool
    This tool allows to select runs and get values as well as manage RCDB values

    RCDB CLI needs a DB connection string which could be provided via:
    - RCDB_CONNECTION environment variable
    - -c/--connection flag
    """

    # Create a rcdb_app_context object and remember it as the context object.  From
    # this point onwards other commands can refer to it by using the
    # @pass_rcdb_context decorator.
    if not connection:
        print("(!)WARNING no connection provided! "
              "Provide DB connection string via --connection/-c or RCDB_CONNECTION environment variable.")
    ctx.obj = RcdbApplicationContext(os.path.abspath(user_config), connection)
    ctx.obj.verbose = verbose
    for key, value in config:
        ctx.obj.set_config(key, value)

    if ctx.invoked_subcommand is None:
        "No command was specified"
        click.echo(ctx.get_help())


# Add ls command
# noinspection PyTypeChecker
rcdb_cli.add_command(ls_cmd)

# Add 'repair' group of commands
# noinspection PyTypeChecker
rcdb_cli.add_command(repair_grp)

# Add 'db' group of commands
# noinspection PyTypeChecker
rcdb_cli.add_command(db_grp)

# Add 'rp' group of commands
# noinspection PyTypeChecker
rcdb_cli.add_command(rp_grp)

# Add 'web' group of commands
# noinspection PyTypeChecker
rcdb_cli.add_command(web_cmd)


@rcdb_cli.command()
@pass_rcdb_context
@click.argument('run', required=True)
@click.option('--long', '-l', 'is_long', is_flag=True, help='Prints condition full information')
def files(context, run, is_long):
    """
    Shows files stored for a current run:

    RUN: Run number to show files for
    """
    db = context.db
    assert isinstance(db, RCDBProvider)

    run = db.get_run(int(run))

    for file in run.files:
        assert isinstance(file, ConfigurationFile)
        click.echo(file.path)


def cat():
    pass

def dump():
    pass

