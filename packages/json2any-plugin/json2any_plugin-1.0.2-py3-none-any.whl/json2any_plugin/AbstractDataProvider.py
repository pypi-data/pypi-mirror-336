from abc import abstractmethod
from argparse import ArgumentParser, Namespace
from typing import Dict, Any

from json2any_plugin.AbstractProvider import AbstractProvider


class AbstractDataProvider(AbstractProvider):
    """
    Abstract base class for creating data loader
    """

    def __init__(self, data_key='data'):
        super().__init__()
        self.__data_key = data_key
        self.__json_path_query = None

    @property
    def data_key(self) -> str:
        """
        variable name under which the data will be available in template
        """
        return self.__data_key

    @abstractmethod
    def update_arg_parser(self, parser: ArgumentParser) -> None:
        """

        :param parser:
        :return:
        """

        parser.add_argument(f'--{self.arg_prefix}-key',
                            help='name of key under which the data will be available in template')
        parser.add_argument(f'--{self.arg_prefix}-query',
                            help='JSONPath Query applied to loaded data')

    @abstractmethod
    def process_args(self, args: Namespace) -> bool:
        if hasattr(args, f'--{self.arg_prefix}-key'):
            self.__data_key = getattr(args, f'--{self.arg_prefix}-key')

        # this return is here to silent the warning only. Implement your own logic.
        return False

    @abstractmethod
    def load_data(self) -> Dict[str, Any]:
        """
        loads the data for template.
        Do not use the "FORBIDDEN_KEYS"
        :return Dict[str, Any]: the data for template. This dictionary will be "mounted" at "root" in template,
         along with the "DATA_KEY_XXX" data. Do not use the "FORBIDDEN_KEYS" as keys in returned data.
         i.e. if you return {"some_key": "Key Data"} you will access it in template {{ some_key }}
        """
        raise NotImplementedError()

    def query_data(self, data: Any) -> Any:
        if self.__json_path_query is None:
            return data

        matcher = jpng.parse(self.__json_path_query)
        values = [m.value for m in matcher.find(data)]
        return values
