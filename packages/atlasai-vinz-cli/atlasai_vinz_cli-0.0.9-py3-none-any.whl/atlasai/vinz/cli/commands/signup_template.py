import click

from .cli import cli
from ..api import _get, _update
from ..options import (
    export_opt
)
from ..output import output_message


@cli.group(name='signup-template', help='Pages management.')
@click.pass_context
def signup_template(ctx):
    pass


@signup_template.command(name='get', help='Get signup template.')
@export_opt
@click.pass_context
def get_signup_template(ctx, output_file):
    _, result = _get(
        ctx.obj['access_token'], 'template/signup', params={}
    )
    if not result:
        output_message('Signup template not found!')
        return
    output_message(result['html'], output_file=output_file)


@signup_template.command(name='set', help='Update signup template.')
@click.option(
    '--html-file', 'html_file',
    type=click.Path(
        exists=True,
        file_okay=True,
        resolve_path=True,
        readable=True,
        writable=True,
    ),
    required=True,
    help='The path of the file that contains the html.'
)
@click.pass_context
def set_signup_template(ctx, html_file):
    data = {}
    _, result = _get(
        ctx.obj['access_token'], 'template/signup', params={}
    )
    if not result:
        output_message('Signup template not found!')
        return
    if html_file:
        with open(html_file) as readfile:
            html = readfile.read()
            data['html'] = html
    _, result = _update(
        ctx.obj['access_token'], f'template/{result["id"]}', params={}, data=data
    )
    output_message('Signup template updated successfully!')
