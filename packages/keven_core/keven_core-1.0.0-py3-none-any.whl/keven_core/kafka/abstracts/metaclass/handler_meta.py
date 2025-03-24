from typing import Dict, Set, Type

from keven_core.kafka.abstracts.metaclass.base_registry import BaseRegistryMeta
from keven_core.kafka.events.event import EventNames
from keven_core.kafka.commands.command import CommandNames


class EventHandlerMeta(BaseRegistryMeta):
    """
    Metaclass for automatically registering EventHandler subclasses.

    Uses the `event_name` attribute of subclasses as the registration key.

    Any concrete subclass of EventHandler that defines a non-None `event_name` is automatically
    registered into a central registry. The registry maps EventNames to sets of EventHandler subclasses.

    This design centralizes handler registration and enables easy lookup when an event occurs.

    Usage:
        The EventHandler base class (and its subclasses) automatically use this metaclass.
        To retrieve the registry, call:

            registry = EventHandlerMeta.get_registry()
            handlers = registry.get(EventNames.PRINT_EVENT, set())

    Note:
        In the future, additional validation or configuration of registered handlers can be performed here.
    """

    _registry: Dict[EventNames, Set[Type]] = {}
    registration_attr: str = "event_name"

    @classmethod
    def get_registry(mcs) -> Dict[EventNames, Set[Type]]:
        return mcs._registry

    @classmethod
    def get_registration_attr(mcs) -> str:
        return mcs.registration_attr

    @classmethod
    def get_excluded_names(mcs) -> Set[str]:
        # For example, LongRunningEventHandler might be excluded.
        return {"LongRunningEventHandler"}


class CommandHandlerMeta(BaseRegistryMeta):
    """
    Metaclass for automatically registering CommandHandler subclasses.

    Uses the `command_name` attribute of subclasses as the registration key.
    """
    _registry: Dict[CommandNames, Set[Type]] = {}
    registration_attr: str = "command_name"

    @classmethod
    def get_registry(mcs) -> Dict[CommandNames, Set[Type]]:
        return mcs._registry

    @classmethod
    def get_registration_attr(mcs) -> str:
        return mcs.registration_attr

    @classmethod
    def get_excluded_names(mcs) -> Set[str]:
        # For example, LongRunningCommandHandler might be excluded.
        return {"LongRunningCommandHandler"}


###############################################################################
# Example Abstract Classes Using the Derived Metaclasses
###############################################################################
# class EventHandler(ABC, metaclass=EventHandlerMeta):
#     """
#     Abstract base class for handling events with automatic registration.
#
#     Subclasses must define an `event_name` (of type EventNames) and implement the
#     `handle_event` method.
#
#     Example:
#         from keven_core.kafka.events.event import EventNames
#
#         class PrintEventHandler(EventHandler):
#             event_name = EventNames.PRINT_EVENT
#
#             def handle_event(self, event: object) -> None:
#                 print(f"Handling event: {event}")
#
#         # PrintEventHandler is auto-registered in EventHandlerMeta._registry.
#     """
#     event_name: Any = None  # Expected to be of type EventNames
#     auto_register: bool = True
#     delay_commands_and_events: bool = True
#     capture_exception_handler: Optional[Callable[[Exception], None]] = None
#
#     @abstractmethod
#     def handle_event(self, event: object) -> None:
#         pass
#
#
# class CommandHandler(ABC, metaclass=CommandHandlerMeta):
#     """
#     Abstract base class for handling commands with automatic registration.
#
#     Subclasses must define a `command_name` (of type CommandNames) and implement the
#     `handle_command` method.
#
#     Example:
#         from keven_core.kafka.commands.command import CommandNames
#
#         class MyCommandHandler(CommandHandler):
#             command_name = CommandNames.MY_COMMAND
#
#             def handle_command(self, command: object) -> None:
#                 print(f"Processing command: {command}")
#
#         # MyCommandHandler is auto-registered in CommandHandlerMeta._registry.
#     """
#     command_name: Any = None  # Expected to be of type CommandNames
#     auto_register: bool = True
#     delay_commands_and_events: bool = True
#     capture_exception_handler: Optional[Callable[[Exception], None]] = None
#
#     @abstractmethod
#     def handle_command(self, command: object) -> None:
#         pass
