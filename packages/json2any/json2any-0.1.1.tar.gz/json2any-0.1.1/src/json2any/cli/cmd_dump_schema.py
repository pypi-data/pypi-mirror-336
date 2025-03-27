import json
from argparse import Namespace
from pathlib import Path

from marshmallow_dataclass import class_schema

from json2any.project.Json2AnyDescriptor import Json2AnyDescriptor
from json2any.JSONSchemaWithUnion import JSONSchemaWithUnion


def cmd_dump_schema_setup(subparsers):
    parser = subparsers.add_parser('dump-rds', aliases=['rds'], help='Generate RDS JSON schema to file')
    parser.add_argument('schema_file', help='file to write schema to ', type=Path)

    parser.set_defaults(func=cmd_dump_schema_execute)


def cmd_dump_schema_execute(args: Namespace):
    schema = class_schema(Json2AnyDescriptor)()

    json_schema = JSONSchemaWithUnion()
    schema_d = json_schema.dump(schema)
    schema_d['$id'] = 'https://gitlab.com/maciej.matuszak/json2any/rds'
    schema_d['title'] = 'json2any Runs description schema'
    schema_d['description'] = 'Describes how the templates and data are put together to generate output'
    with args.schema_file.open('w') as schema_file:
        json.dump(schema_d, schema_file, indent=4)

