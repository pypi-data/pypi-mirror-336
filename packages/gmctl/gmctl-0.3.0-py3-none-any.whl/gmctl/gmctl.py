from dotenv import load_dotenv
load_dotenv() 

import logging
logging.basicConfig(level=logging.ERROR, format='gmctl - %(name)s - %(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import click
from gmctl.repository import repo
from gmctl.commit import commit
from gmctl.ecs_deployment import ecs
from gmctl.lambda_deployment import faas
from gmctl.user import user
from gmctl.gmclient import GitmoxiClient
from gmctl.utils import print_table
import os

@click.group()
@click.option('-e', '--endpoint-url', default="env(GITMOXI_ENDPOINT_URL), fallback to http://127.0.0.1:8080", help='The Gitmoxi FastAPI endpoint URL', show_default=True)
@click.option('-l', '--log-level', default="ERROR", type=click.Choice(["DEBUG","INFO","WARNING","ERROR","CRITICAL"], case_sensitive=False), help='The log level', show_default=True)
@click.pass_context
def cli(ctx, endpoint_url ,log_level):
    logging.getLogger().setLevel(getattr(logging, log_level.upper()))
    ctx.ensure_object(dict)
    endpoint_url = ctx.obj.get('ENDPOINT_URL', None)
    if not endpoint_url:
        endpoint_url = os.getenv('GITMOXI_ENDPOINT_URL', 'http://127.0.0.1:8080')
    ctx.obj['ENDPOINT_URL'] = endpoint_url

cli.add_command(commit)
cli.add_command(repo)


# Deployment group with subcommands
@cli.group()
@click.pass_context
def deployment(ctx):
    """User related commands."""
    pass

deployment.add_command(ecs)
deployment.add_command(faas)