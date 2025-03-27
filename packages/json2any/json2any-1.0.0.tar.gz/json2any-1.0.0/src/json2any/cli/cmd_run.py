import json
from argparse import Namespace
from logging import getLogger
from pathlib import Path

from marshmallow_dataclass import class_schema

from json2any.JinjaExecutor import JinjaExecutor
from json2any.Json2AnyException import Json2AnyException
from json2any.ProviderPlugins import ProviderPlugins
from json2any.project.Json2AnyDescriptor import Json2AnyDescriptor

plugins = ProviderPlugins()

log = getLogger(__name__)


def cmd_run_setup(subparsers):
    global plugins

    parser = subparsers.add_parser('run', help='Generate the output according to RDS')

    parser.add_argument('rds_file', type=Path, help='Path to runs descriptor file')
    parser.add_argument('-o', '--out-dir', type=Path, help='Path to output directory', default=Path.cwd())

    plugins.update_arg_parser(parser)

    parser.set_defaults(func=cmd_run_execute)


def load_runs_descriptor(rds_file: Path) -> Json2AnyDescriptor:
    if not rds_file.is_file():
        raise ValueError('File: "%s" is not a file' % rds_file)

    with rds_file.open(mode='r') as f:
        j_data = json.load(f)
        schema = class_schema(Json2AnyDescriptor)()
        runs_descriptor = schema.load(j_data)
        return runs_descriptor


def cmd_run_execute(args: Namespace):
    global plugins

    plugins.process_args(args)

    rds_file: Path = args.rds_file
    rds_file = rds_file.resolve().absolute()

    log.debug('Loading Runs Descriptor from "%s"', rds_file)
    rds = load_runs_descriptor(rds_file)
    rds_dir: Path = rds_file.parent

    plugins.init_active_providers(rds_dir, rds.template_location)

    log.debug('Creating Template Loader: %s(rds_dir: "%s", template_location: "%s")',
              plugins.active_template_provider.name, rds_dir, rds.template_location)
    loader = plugins.active_template_provider.get_loader()

    out_dir: Path = args.out_dir
    out_dir = out_dir.resolve().absolute()
    if not out_dir.is_dir():
        log.trace('Output Folder does not exists - creating: %s', out_dir)
        out_dir.mkdir(parents=True)
    log.debug('Output will be written to: "%s"', out_dir)

    data = {}
    for provider in plugins.active_data_providers:
        log.debug('Loading data using Data provider: %s', provider.name)
        try:
            data[provider.data_key] = provider.load_data()

        except Exception as e:
            raise Json2AnyException(f'Failed to load data using provider "{provider.name}"') from e

    executor = JinjaExecutor(loader, rds, data, out_dir=out_dir)
    for hp in plugins.active_help_providers:
        log.debug('Initialising Helper Provider: %s', hp.__class__.__name__)

        helpers = hp.get_helpers()
        executor.environment.globals.update(helpers)
    executor.execute_runs()
