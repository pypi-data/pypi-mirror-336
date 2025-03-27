import sys
from argparse import ArgumentParser, Namespace
from logging import getLogger

from json2any.cli.cmd_dump_schema import cmd_dump_schema_setup
from json2any.cli.cmd_run import cmd_run_setup
from json2any.cli_logg_utils import cli_logg_util_setup_parser, cli_logg_util_setup

log = getLogger(__name__)


def main():
    parser = ArgumentParser(description='Convert JSON to any format', prog='json2any')

    cli_logg_util_setup_parser(parser)
    subparsers = parser.add_subparsers(title='commands')

    cmd_run_setup(subparsers)
    cmd_dump_schema_setup(subparsers)

    args: Namespace = parser.parse_args()

    cli_logg_util_setup(args)

    if hasattr(args, 'func'):
        try:
            args.func(args)
        except Exception as e:
            if args.verbose == 0:
                log.error(f'Failed to execute; error: {e}')
            else:
                log.error(f'Failed to execute', exc_info=e)
            sys.exit(1)


    else:
        parser.print_help()


if __name__ == '__main__':
    main()
