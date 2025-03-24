import click

from .cli import cli
from ..api import _get, _list, _update
from ..options import (
    export_opt,
    limit_opt,
    offset_opt,
    query_opt
)
from ..output import output_result, output_message
from ..types import JSON


@cli.group(help='Account management.')
@click.pass_context
def account(ctx):
    pass

@account.command(name='info', help='Get account info.')
@export_opt
@click.pass_context
def get_info(ctx, output_file):
    _, result = _get(
        ctx.obj['access_token'], '/account'
    )
    output_result(ctx, result, output_file=output_file)

@account.command(name='update', help='Update the account.')
@click.option('--user-metadata', 'user_metadata', type=JSON, required=False, help='User metadata.')
@click.option('--app-metadata', 'app_metadata', type=JSON, required=False, help='App metadata.')
@export_opt
@click.pass_context
def update_info(ctx, user_metadata, app_metadata, output_file):
    data = {
        "user_metadata": user_metadata,
        "app_metadata": app_metadata
    }
    _, result = _update(ctx.obj['access_token'], 'account', data=data)
    output_result(ctx, result, output_file=output_file)

@account.command(name='reset-password', help='Reset password of the account.')
@click.pass_context
def reset_password(ctx):
    _update(ctx.obj['access_token'], 'account/reset-password')
    output_message('Reset password sent successfully!')


@account.command(name='roles', help='List roles of the account.')
@query_opt
@offset_opt
@limit_opt
@export_opt
@click.pass_context
def list_roles(ctx, query, limit, offset, output_file):
    params = {
        'limit': limit,
        'offset': offset,
        'search': query,
    }
    _, result = _list(
        ctx.obj['access_token'], 'account/roles', params=params
    )
    output_result(ctx, result, output_file=output_file)
