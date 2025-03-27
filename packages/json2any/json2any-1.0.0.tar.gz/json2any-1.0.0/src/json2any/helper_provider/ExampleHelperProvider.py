from argparse import Namespace, ArgumentParser
from pathlib import Path
from typing import Dict, Callable

from json2any_plugin.AbstractHelperProvider import AbstractHelperProvider

def minv(a,b):
    r = min(a, b)
    return r

def maxv(a,b):
    r = max(a, b)
    return r

def to_upper(s: str):
    return s.upper()


def get_cwd():
    return Path.cwd()


def include_raw(path: str):
    if path is None or str.strip(path) == "":
        return ""

    path = Path(path)
    if path.is_file():
        return path.read_text()
    else:
        raise FileNotFoundError(path)


class ExampleHelperProvider(AbstractHelperProvider):

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def arg_prefix(self) -> str:
        return ''

    @property
    def has_arguments(self) -> bool:
        return False

    def update_arg_parser(self, parser: ArgumentParser) -> None:
        pass

    def process_args(self, args: Namespace) -> bool:
        return True

    def init(self, **kwargs) -> None:
        pass

    def get_helpers(self) -> Dict[str, Callable]:
        helpers = {
            "to_upper": to_upper,
            "get_cwd": get_cwd,
            "include_raw": include_raw,
            "min": minv,
            "max": maxv,
        }
        return helpers
