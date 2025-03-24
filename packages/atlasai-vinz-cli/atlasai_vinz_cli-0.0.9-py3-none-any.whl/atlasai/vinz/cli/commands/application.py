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

@cli.group(help="Application management.")
@click.pass_context
def application(ctx):
    pass


@application.command(name='list', help='List Applications.')
@query_opt
@offset_opt
@limit_opt
@export_opt
@click.pass_context
def list_applications(ctx, query, limit, offset, output_file):
    params = {
        'limit': limit,
        'offset': offset,
        'search': query,
    }
    _, result = _list(
        ctx.obj['access_token'], 'applications', params=params
    )
    output_result(ctx, result, output_file=output_file)
