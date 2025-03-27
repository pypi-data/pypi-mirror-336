import click
from gmctl.gmclient import GitmoxiClient
from gmctl.utils import print_table
import logging

logger = logging.getLogger(__name__)

@click.group()
@click.pass_context
def faas(ctx):
    pass

@faas.command()
@click.option('-r', '--repo-url', help='The repository URL')
@click.option('-c', '--commit-hash', help='The commit hash')
@click.option('-a', '--account-id', help='The AWS account ID')
@click.option('-re', '--region', help='The AWS region')
@click.option('-fn', '--function-name', help='The Lambda function name')
@click.option('-st', '--status', type=click.Choice(["PROCESSING", "PROCESSED_ERROR", "PROCESSED_SUCCESS"]), help='The deployment status')
@click.option('-n', '--number-of-records', help='Number of records', default=10)
@click.option('-v', '--verbose', is_flag=True, help='Verbose output')
@click.option('-A', '--show-all', is_flag=True, help='Verbose for all deployments')
@click.pass_context
def get(ctx, repo_url, commit_hash, account_id, region, 
        function_name, status, number_of_records, verbose, show_all):        

    resource_path = "/deployments/lambda"
    conditions = []
    if repo_url:
        conditions.append(f"repo_url={repo_url}")
    if commit_hash:
        conditions.append(f"commit_hash={commit_hash}")
    if function_name:
        conditions.append(f"function_name={function_name}")
    if account_id:
        conditions.append(f"account_id={account_id}")
    if region:
        conditions.append(f"region={region}")
    if status:
        conditions.append(f"status={status}")
    if number_of_records:
        conditions.append(f"n={number_of_records}")
    if conditions:
        resource_path += "?" + "&".join(conditions)
    logger.info(f'Getting Lambda deployments: {resource_path}')
    # make a GET call to the /deployments/lambda endpoint with the repository URL
    gmclient = GitmoxiClient(ctx.obj['ENDPOINT_URL'])
    response = gmclient.get(resource_path)
    if not response:
        logger.error(f'Failed to get Lambda deployments for: {resource_path}')
        return
    deployments = response.get('deployments', [])
    if not deployments:
        logger.warning(f'Did not get any Lambda deployments for: {resource_path}')
        return

    to_display = []
    summary_keys = ["repo_url", "commit_hash", "account_id", "region", "function_name", 
                    "create_timestamp", "status", "file_prefix"]
    for deployment in deployments:
        to_display.append({k: deployment.get(k) for k in summary_keys})
         
    print_table(to_display)
    if verbose:
        for deployment in deployments:
            if not show_all and deployment.get("status") != "PROCESSED_ERROR":
                continue
            print("-------------------------------")
            print(f"\n{deployment.get('status')}, {deployment.get('repo_url')}, {deployment.get('file_prefix')}, "
                  f"{deployment.get('function_name')}, {deployment.get('account_id')}, {deployment.get('region')}: \n")
            for status_detail in deployment.get("status_details", []):
                print(f"{status_detail}\n")
            print("-------------------------------")
    return