from enum import unique, auto
from keven_core.kafka.utils import AutoName


@unique
class CommandNames(AutoName):
    """
    All commands must be registered here
    """

    NONE = auto()
    NOT_INSTALLED = auto()
    TEST = auto()
    TEST_PICKLED_COMMAND = auto()
    PRINT_COMMAND = auto()