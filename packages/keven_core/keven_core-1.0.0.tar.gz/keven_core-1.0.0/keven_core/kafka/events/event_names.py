from enum import unique, auto
from keven_core.kafka.utils import AutoName


@unique
class EventNames(AutoName):
    """
    All events must be registered here
    """

    NONE = auto()
    TEST = auto()
    COMMAND_EVENT = auto()
    COMMAND_ERROR_EVENT = auto()
    PRINT_EVENT = auto()