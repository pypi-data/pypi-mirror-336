from abc import abstractmethod
from pathlib import Path
from typing import Optional

from jinja2 import BaseLoader
from json2any_plugin.AbstractProvider import AbstractProvider


class AbstractTemplateProvider(AbstractProvider):
    """
    Provides jinja2 template loader.
    """

    @abstractmethod
    def init(self, rds_dir: Path, template_location:str) -> None:
        """
        Initialisation function. In this function ensure the Data Provider can access relevant resources and is ready in
        """
        raise NotImplementedError()

    @abstractmethod
    def get_loader(self) -> BaseLoader:
        """
        If activated via commandline Creates jinja2 template loader
        :return BaseLoader: instance of jinja2.BaseLoader
        """
        raise NotImplementedError()
