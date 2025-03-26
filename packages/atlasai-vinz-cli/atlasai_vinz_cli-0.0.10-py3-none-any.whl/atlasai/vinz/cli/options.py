
import click

export_opt = click.option('--output', 'output_file', type=str, required=False, help='Output file.')
query_opt = click.option('--query', '-q', 'query', type=str, required=False, help='Filter resource.')
limit_opt = click.option('--limit', '-l', 'limit', type=str, required=False, help='Limit the number of objects to return.')
offset_opt = click.option('--offset', '-o', 'offset', type=str, required=False, help='Offset the objects.')
