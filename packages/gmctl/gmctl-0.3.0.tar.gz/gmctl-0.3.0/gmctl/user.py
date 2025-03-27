
from gmctl.gmclient import GitmoxiClient
import logging
from gmctl.utils import print_table

logger = logging.getLogger(__name__)


import click
# User group with subcommands
@click.group()
@click.pass_context
def user(ctx):
    """User related commands."""
    pass

@user.command()
@click.pass_context
def add(ctx):
    click.echo(f'Adding user to {ctx.obj["ENDPOINT_URL"]}')

@user.command()
@click.pass_context
def get(ctx):
    click.echo(f'Getting users from {ctx.obj["ENDPOINT_URL"]}')