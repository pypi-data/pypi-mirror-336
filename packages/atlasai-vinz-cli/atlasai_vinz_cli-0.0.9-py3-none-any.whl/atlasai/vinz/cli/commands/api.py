import click

from .cli import cli
from ..api import _list
from ..options import (
    export_opt,
    limit_opt,
    offset_opt,
    query_opt
)
from ..output import output_result

@cli.group(help="Api management.")
@click.pass_context
def api(ctx):
    pass


@api.command(name='list', help='List Apis.')
@query_opt
@offset_opt
@limit_opt
@export_opt
@click.pass_context
def list_apis(ctx, query, limit, offset, output_file):
    params = {
        'limit': limit,
        'offset': offset,
        'search': query,
    }
    _, result = _list(
        ctx.obj['access_token'], 'apis', params=params
    )
    output_result(ctx, result, output_file=output_file)


@api.group(name='permissions', help='Api Permissions')
@click.pass_context
def permissions(ctx):
    pass


@permissions.command(name='list', help='Retrieve permissions of an api.')
@click.option('--api-id', 'api_id', type=str, required=True, help='The id of the api.')
@query_opt
@offset_opt
@limit_opt
@export_opt
@click.pass_context
def list_permissions(ctx, api_id, limit, offset, query, output_file):
    params = {
        'limit': limit,
        'offset': offset,
        'search': query
    }

    _, result = _list(
        ctx.obj['access_token'], f'apis/{api_id}/permissions', params=params
    )
    output_result(ctx, result, output_file=output_file)
