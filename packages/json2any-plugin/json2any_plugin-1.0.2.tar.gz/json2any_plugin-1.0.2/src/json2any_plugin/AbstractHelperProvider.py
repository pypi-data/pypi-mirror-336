from abc import abstractmethod
from typing import Callable, Dict

from json2any_plugin.AbstractProvider import AbstractProvider


class AbstractHelperProvider(AbstractProvider):

    @abstractmethod
    def get_helpers(self) -> Dict[str, Callable]:
        """
        provides helper functions that can be used in the json2any templates
        :return Dict[str, Callable]: a dictionary of name => function. You will be able to access the name's in template
        """
        raise NotImplementedError()
