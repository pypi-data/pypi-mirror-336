from argparse import Namespace, ArgumentParser
from logging import getLogger
from pathlib import Path
from typing import List, Optional

from jinja2 import BaseLoader, FileSystemLoader
from json2any_plugin.AbstractTemplateProvider import AbstractTemplateProvider

from json2any.Json2AnyException import Json2AnyException


class FileSystemTemplateProvider(AbstractTemplateProvider):
    def __init__(self):
        self.log = getLogger(self.__class__.__name__)
        self.template_paths: List[Path] = []
        self.override_paths = False
        self.__loader: Optional[FileSystemLoader] = None

    @property
    def arg_prefix(self) -> str:
        return 'fstp'

    @property
    def has_arguments(self) -> bool:
        return True

    @property
    def name(self) -> str:
        return self.__class__.__name__

    def update_arg_parser(self, parser: ArgumentParser) -> None:
        parser.add_argument('--fstp-dir', help='Path to template  directory', type=Path,
                            action='append')
        parser.add_argument('--fstp-override-paths',
                            action='store_true',
                            help='If supplied the "--fstp-dir" paths are override "rds.template_location" otherwise '
                                 'paths are appended to "rds.template_location" otherwise replaced')

    def process_args(self, args: Namespace) -> bool:
        if args.fstp_dir is None:
            return False

        self.override_paths = args.fstp_override_paths

        for template_path in args.fstp_dir:
            template_path: Path
            template_path = Path.cwd() / template_path
            template_path = template_path.resolve().absolute()

            if not template_path.is_dir():
                raise NotADirectoryError(f'{template_path} is not a directory')
            self.template_paths.append(template_path)
        return True

    def init(self, rds_dir: Path, template_location: str) -> None:
        paths = []

        if template_location is not None:
            template_location = rds_dir / template_location
            template_location = template_location.resolve().absolute()

            if not template_location.is_dir():
                raise NotADirectoryError(f'rds.template_location "{template_location}" is not a directory')
            paths.append(template_location)

        if self.override_paths:
            paths = self.template_paths
        else:
            paths.extend(self.template_paths)

        if len(paths) == 0:
            raise Json2AnyException('At least one path is required')
        self.__loader = FileSystemLoader(paths)
        self.log.debug('FileSystemLoader initialised with paths: %s', ', '.join(f'"{str(p)}"' for p in paths))

    def get_loader(self) -> BaseLoader:
        return self.__loader
