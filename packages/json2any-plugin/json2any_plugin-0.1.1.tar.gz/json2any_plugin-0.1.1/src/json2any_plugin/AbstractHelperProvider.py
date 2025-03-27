from abc import abstractmethod
from typing import Any

from json2any_plugin.AbstractProvider import AbstractProvider


class AbstractHelperProvider(AbstractProvider):
    """
    Helper Method provider
    By implementing this interface you can add functionality to json2any generator.
    Object created by get_helper_object() method will be available under get_helper_ns() name in templates
    """

    @abstractmethod
    def get_helper_object(self) -> Any:
        """
        provides helper object that can be used in the json2any templates. The helper object can be access via namespace set by get_helper_ns() method
        :return object with helper methods
        """
        raise NotImplementedError()

    @abstractmethod
    def get_helper_ns(self) -> str:
        """
        Provides namespace under which the helper object can be accessed.
        :return string
        """
        raise NotImplementedError()
