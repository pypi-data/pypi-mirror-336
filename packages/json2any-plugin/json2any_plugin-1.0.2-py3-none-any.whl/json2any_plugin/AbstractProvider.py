from abc import ABC, abstractmethod
from argparse import Namespace, _ArgumentGroup


class AbstractProvider(ABC):
    """
        Abstract base class for a provider. Ues this interface to create a provider. Provider uses ArgumentParser for
        configuration and activation.
        Life cycle of Provider:
        1. Construction - __init__() constructor is called without any arguments. This is done for all available
           providers in random order.
        2. Argument Parser update - update_arg_parser(self, parser: ArgumentParser) at this stage plugin can add entries
           into argument parser.
        3. Provider arguments validation - compliance with prefix
        4. Parsed argument validation and store - returns Active/Not Active atatus
        5. All providers that returned Active status above are initialised. Provider should make sure it has access to
           relevant resources.
        6. Provider specific actions - see higher level classes for details

        """



    @property
    @abstractmethod
    def name(self) -> str:
        """
        Name of the Provider. Ensure no exception can be thrown, and string is always returned not None
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def arg_prefix(self) -> str:
        """
        prefix used for arguments of Data Provider. Ensure no exception can be thrown, and string is always returned not None
        all arguments have to start with that prefix
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def has_arguments(self) -> bool :
        """
        returns True if provider uses arguments, otherwise False
        """
        raise NotImplementedError()

    @abstractmethod
    def update_arg_parser(self, parser: '_ArgumentGroup') -> None:
        """
        This is opportunity for plugin to add command-line arguments definitions
         - Data Provider will need at least one optional argument to activate it
         - Do not use mandatory or positional arguments as this will always activate the plugin
         - All arguments have to start with prefix arg_prefix property implemented above
         - Ensure this is light and fast function as all plugins will execute it, leave heavy lifting for init
        :param parser:
        """

        raise NotImplementedError()

    @abstractmethod
    def process_args(self, args: Namespace) -> bool:
        """
        This method provide ability for plugin to process, validate and store data from command-line.
        Do not instantiate "heavy" object yet, store the relevant data, validate it, leave the heavy listing for init
        and load_data functions. Keep this stage light and fast as all plugins have to be processed at this stage to
        figure-out which is active.

        :param args: parsed command-line arguments
        :return: True if args are valid and indicate this object is active, False otherwise. For example there may be
                 multiple data providers installed and user may activate one by providing relevant argument
        """

        raise NotImplementedError()


    @abstractmethod
    def init(self, **kwargs) -> None:
        """
        Initialisation function. In this function ensure the Data Provider can access relevant resources and is ready in
        """
        raise NotImplementedError()