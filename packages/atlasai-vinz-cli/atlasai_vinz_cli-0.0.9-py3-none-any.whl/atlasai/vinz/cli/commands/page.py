import json

import click

from .cli import cli
from ..api import _delete, _get, _list, _create, _update
from ..options import (
    query_opt,
    offset_opt,
    limit_opt,
    export_opt
)
from ..output import output_result, output_message
from ..utils import create_parameters


@cli.group(help='Pages management.')
@click.pass_context
def page(ctx):
    pass

@page.command(name='list', help='List Pages.')
@click.option('--name', 'name', type=str, required=False, help='Filter by the Name of the page.')
@click.option('--hash', 'hash', type=str, required=False, help='Filter by the Hash of the page.')
@query_opt
@offset_opt
@limit_opt
@export_opt
@click.pass_context
def list_pages(ctx, name, hash, query, limit, offset, output_file):
    param_mapping = [
        (limit, 'limit'),
        (offset, 'offset'),
        (query, 'search'),
        (name, 'name'),
        (hash, 'hash')
    ]
    params = create_parameters(param_mapping)
    _, result = _list(
        ctx.obj['access_token'], 'pages', params=params
    )
    output_result(ctx, result, output_file=output_file, no_wrap_columns=['hash', 'id'])


@page.command(name='create', help='Create a new Page.')
@click.option('--name', 'name', type=str, required=True, help='Name of the page.')
@click.option('--description', 'description', type=str, required=True, help='Description of the page.')
@click.option('--page-type', 'page_type', type=str, required=False, default='signup', help='The type of the page.')
@click.option(
    '--config-file', 'config_file',
    type=click.Path(
        exists=True,
        file_okay=True,
        resolve_path=True,
        readable=True,
        writable=True,
    ),
    required=False,
    help='The path of the file that contains the config.'
)
@click.option(
    '--html-file', 'html_file',
    type=click.Path(
        exists=True,
        file_okay=True,
        resolve_path=True,
        readable=True,
        writable=True,
    ),
    required=False,
    help='The path of the file that contains the html.'
)
@click.pass_context
def create_page(ctx, name, description, page_type, config_file, html_file):
    data = {
        'name': name,
        'description': description,
        'page_type': page_type,
    }
    if config_file:
        with open(config_file) as readfile:
            config = json.loads(readfile.read())
            data['config'] = config
    if html_file:
        with open(html_file) as readfile:
            html = readfile.read()
            data['html'] = html
    _, result = _create(ctx.obj['access_token'], 'page', data=data, params={})
    output_result(ctx, result)


@page.command(name='update', help='Update a Page.')
@click.option('--name', 'name', type=str, required=False, help='Name of the page.')
@click.option('--description', 'description', type=str, required=False, help='Description of the page.')
@click.option('--page-type', 'page_type', type=str, required=False, default='signup', help='The type of the page.')
@click.option(
    '--config-file', 'config_file',
    type=click.Path(
        exists=True,
        file_okay=True,
        resolve_path=True,
        readable=True,
        writable=True,
    ),
    required=False,
    help='The path of the file that contains the config.'
)
@click.option(
    '--html-file', 'html_file',
    type=click.Path(
        exists=True,
        file_okay=True,
        resolve_path=True,
        readable=True,
        writable=True,
    ),
    required=False,
    help='The path of the file that contains the html.'
)
@click.option('--page-id', 'page_id', type=str, required=True, help='Page id to update.')
@click.pass_context
def update_page(ctx, name, description, page_type, config_file, html_file, page_id):
    data = {
        'name': name,
        'description': description,
        'page_type': page_type,
    }
    if config_file:
        with open(config_file) as readfile:
            config = json.loads(readfile.read())
            data['config'] = config
    if html_file:
        with open(html_file) as readfile:
            html = readfile.read()
            data['html'] = html
    _, result = _update(ctx.obj['access_token'], f'page/{page_id}', data=data)
    output_result(ctx, result)


@page.command(name='get', help='Get a Page.')
@click.option('--page-id', 'page_id', type=str, required=True, help='The id of the page.')
@click.pass_context
def get_page(ctx, page_id):
    _, result = _get(ctx.obj['access_token'], f'page/{page_id}')
    output_result(ctx, result, no_wrap_columns=['hash', 'id'])

@page.command(name='delete', help='Delete a Page.')
@click.option('--page-id', 'page_id', type=str, required=True, help='The id of the page.')
@click.pass_context
def delete_page(ctx, page_id):
    _delete(ctx.obj['access_token'], f'page/{page_id}')
    output_message('Page deleted successfully!')
