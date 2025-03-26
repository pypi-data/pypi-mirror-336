import csv
import io
import json

from rich.console import Console
from rich.table import Table
from rich.syntax import Syntax

import yaml

console = Console()

def output_result(ctx, result, no_wrap_columns=None, output_file=None):
    if no_wrap_columns is None:
        no_wrap_columns = []
    print_method = console.print
    output_type = ctx.obj['config'].get('output', 'yaml').lower()
    if output_type == 'json':
        data = json.dumps(result, indent=4)
        print_method = console.print_json
    elif output_type == 'table':
        data = json_to_table(result, no_wrap_columns)
    elif output_type == 'csv':
        data = json_to_csv(result)
    else:
        data = yaml.dump(result, default_flow_style=False)

    if output_file:
        if output_type == 'table':
            console.print('Table output format does not support export to file.')
            return
        output_to_file(output_file, data)
    else:
        if output_type == 'yaml':
            data = Syntax(data, 'yaml')
        print_method(data)


def output_to_file(f, data):
    with open(f, 'w') as rf:
        rf.write(data)


def json_to_table(data, no_wrap_columns=None):
    if no_wrap_columns is None:
        no_wrap_columns = []
    if not data:
        return ''
    if not isinstance(data, list):
        data = [data]
    table = Table(title='')
    for key in sorted(data[0].keys()):
        if key in no_wrap_columns:
            table.add_column(key.title(), justify='right', no_wrap=True)
        else:
            table.add_column(key.title(), justify='right')
    for record in data:
        d = []
        for key in sorted(record.keys()):
            value = record[key]
            if not isinstance(value, str):
                d.append(json.dumps(value))
            else:
                d.append(value)
        table.add_row(*d)
    return table

def json_to_csv(data):
    if not data:
        return ''
    if not isinstance(data, list):
        data = [data]
    output = io.StringIO()

    csv_writer = csv.DictWriter(output, fieldnames=sorted(data[0].keys()))
    csv_writer.writeheader()
    csv_writer.writerows(data)

    content = output.getvalue()
    output.close()
    return content


def output_message(output, style=None, newline=False, output_file=None):
    if output_file:
        output_to_file(output_file, output)
    else:
        console.print(output, style=style)
        if newline:
            console.print("\n")
