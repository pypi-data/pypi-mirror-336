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


@cli.group(help='Role management.')
@click.pass_context
def role(ctx):
    pass

@role.command(name='list', help='List Roles.')
@click.option('--name', 'name', type=str, required=False, help='Filter by name')
@click.option('--description', 'description', type=str, required=False, help='Filter by description')
@click.option('--org-id', 'org_id', type=str, required=False, help='Organization id to use. If not specified, it will return your own organization. This is the field org_id returned in the list method.')
@query_opt
@offset_opt
@limit_opt
@export_opt
@click.pass_context
def list_roles(ctx, query, limit, offset, org_id, name, description, output_file):
    param_mapping = [
        (name, 'name'),
        (description, 'description'),
        (limit, 'limit'),
        (offset, 'offset'),
        (query, 'search'),
        (org_id, 'org_id')
    ]
    params = create_parameters(param_mapping)
    _, result = _list(
        ctx.obj['access_token'], 'roles', params=params
    )
    output_result(ctx, result, output_file=output_file)


@role.command(name='create', help='Create a Role.')
@click.option('--description', 'description', type=str, required=True, help='Description of the role.')
@click.option('--name', 'name', type=str, required=True, help='The name of this role.')
@click.option('--org-id', 'org_id', type=str, required=False, help='Organization id to use. If not specified, it will return your own organization. This is the field org_id returned in the list method.')
@click.pass_context
def create_role(ctx, description, name, org_id):
    data = {'description': description, 'name': name}
    params = {'org_id': org_id}
    _, result = _create(ctx.obj['access_token'], 'role', data=data, params=params)
    output_result(ctx, result)


@role.command(name='update', help='Update a Role.')
@click.option('--description', 'description', type=str, required=False, help='Description of the role.')
@click.option('--name', 'name', type=str, required=False, help='The name of this role.')
@click.option('--role-id', 'role_id', type=str, required=True, help='Role id to update. This field is the role_id field from get/list')
@click.pass_context
def update_role(ctx, description, name, role_id):
    data = {'description': description, 'name': name}
    _, result = _update(ctx.obj['access_token'], f'role/{role_id}', data=data)
    output_result(ctx, result)


@role.command(name='get', help='Get a Role.')
@click.option('--role-id', 'role_id', type=str, required=True, help='The id of the role. This field is the role_id field from get/list')
@click.pass_context
def get_role(ctx, role_id):
    _, result = _get(ctx.obj['access_token'], f'role/{role_id}')
    output_result(ctx, result)

@role.command(name='delete', help='Delete a Role.')
@click.option('--role-id', 'role_id', type=str, required=True, help='The id of the role. This field is the role_id field from get/list')
@click.pass_context
def delete_role(ctx, role_id):
    _delete(ctx.obj['access_token'], f'role/{role_id}')
    output_message('Role deleted successfully!')
