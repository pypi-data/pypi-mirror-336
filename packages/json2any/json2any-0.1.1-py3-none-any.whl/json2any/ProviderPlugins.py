from argparse import ArgumentParser, Namespace
from logging import getLogger
from pathlib import Path
from typing import List, Optional

from json2any_plugin.AbstractDataProvider import AbstractDataProvider
from json2any_plugin.AbstractHelperProvider import AbstractHelperProvider
from json2any_plugin.AbstractProvider import AbstractProvider
from json2any_plugin.AbstractTemplateProvider import AbstractTemplateProvider
from pkg_resources import iter_entry_points

from json2any.Json2AnyException import Json2AnyException
from json2any.data_provider.EnvDataProvider import EnvDataProvider
from json2any.data_provider.JSONDataProvider import JSONDataProvider
from json2any.helper_provider.ExampleHelperProvider import ExampleHelperProvider
from json2any.template_provider.FileSystemTemplateProvider import FileSystemTemplateProvider


class ProviderPlugins:

    def __init__(self):
        self.log = getLogger(self.__class__.__name__)

        self.default_template_provider = FileSystemTemplateProvider()

        self.providers: List[AbstractProvider] = [ExampleHelperProvider(), JSONDataProvider(), EnvDataProvider(),
                                                  self.default_template_provider]
        self.active_providers: List[AbstractProvider] = []

        self.find_plugins_has_run = False

    def find_plugins(self):

        # Already initialised?
        if self.find_plugins_has_run:
            return

        for entry_point in iter_entry_points(group='json2any.plugin', name=None):
            ep_class = entry_point.load()
            if issubclass(ep_class, AbstractProvider):
                try:
                    self.providers.append(ep_class())
                except Exception as e:
                    self.log.error(f'Helper Provider "{ep_class}" thrown exception during construction', exc_info=e)
        self.find_plugins_has_run = True

    def update_arg_parser(self, parser: ArgumentParser):
        for provider in self.providers:
            if not provider.has_arguments:
                continue

            provider_name = 'Invalid provider'
            try:

                provider_name = provider.name
                arg_grp = parser.add_argument_group(provider_name, f'Arguments related to {provider_name}')

                provider.update_arg_parser(arg_grp)
            except Exception as e:
                self.log.error(f'Provider "{provider_name}" ({provider.__class__.__name__}) has thrown exception'
                               f' - removed', exc_info=e)
                self.providers.remove(provider)

    def process_args(self, args: Namespace):

        n_data_providers = 0
        n_template_providers = 0
        for provider in self.providers:

            is_active = provider.process_args(args)
            if is_active:
                if isinstance(provider, AbstractDataProvider):
                    n_data_providers += 1
                elif isinstance(provider, AbstractTemplateProvider):
                    n_template_providers += 1
                self.active_providers.append(provider)

        if n_data_providers == 0:
            raise Json2AnyException('No Data Provider was configured')

        if n_template_providers == 0:
            self.log.trace('No Template Provider was configured - adding default: %s',
                           self.default_template_provider.name)
            self.active_providers.append(self.default_template_provider)
        if n_template_providers > 1:
            tp_names = [f'"{p.name}"' for p in self.active_providers if isinstance(p, AbstractTemplateProvider)]
            tp_names_str = ', '.join(tp_names)

            raise Json2AnyException(f'More than one Template Provider was configured: {tp_names_str} ')

    def init_active_providers(self, rds_dir: Path, template_location: str):

        for provider in self.active_providers:

            self.log.debug(f'Initialising Provider: {provider.name}')
            provider.init(rds_dir=rds_dir, template_location=template_location)

    @property
    def active_data_providers(self) -> List[AbstractDataProvider]:
        return [p for p in self.active_providers if isinstance(p, AbstractDataProvider)]

    @property
    def active_help_providers(self) -> List[AbstractHelperProvider]:
        return [p for p in self.active_providers if isinstance(p, AbstractHelperProvider)]

    @property
    def active_template_provider(self) -> Optional[AbstractTemplateProvider]:
        atps = [p for p in self.active_providers if isinstance(p, AbstractTemplateProvider)]
        if len(atps) == 0:
            return None
        elif len(atps) == 1:
            return atps[0]
        else:
            names = [f'"{p.name}"' for p in atps]
            names_s = ', '.join(names)
            raise Json2AnyException(f'Multiple template providers selected: {names_s}')
