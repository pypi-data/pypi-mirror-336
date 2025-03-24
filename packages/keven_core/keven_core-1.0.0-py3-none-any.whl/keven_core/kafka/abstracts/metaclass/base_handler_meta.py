import logging
from abc import ABCMeta
from typing import Dict, Set, Type

from keven_core.kafka.events.event import EventNames
from keven_core.kafka.commands.command import CommandNames

class BaseHandlerMeta(ABCMeta):
    """
    A unified metaclass that handles registration for both EventHandlers and CommandHandlers.
    Inherits from ABCMeta to avoid metaclass conflicts with abc.ABC.

    Rules for non-abstract subclasses:
      - If a class defines 'event_name' (non-None) and NOT 'command_name', it is an EventHandler,
        registered in _event_registry.
      - If a class defines 'command_name' (non-None) and NOT 'event_name', it is a CommandHandler,
        registered in _command_registry.
      - If both or neither are defined, raise TypeError.
      - If 'auto_register' is False or the class is in get_excluded_names(), skip registration.
      - If the class is still abstract (has __abstractmethods__), skip registration/validation.

    Access the registries via:
        BaseHandlerMeta.get_event_registry()
        BaseHandlerMeta.get_command_registry()
    """

    _event_registry: Dict[EventNames, Set[Type]] = {}
    _command_registry: Dict[CommandNames, Set[Type]] = {}
    _excluded_names = {"LongRunningEventHandler", "LongRunningCommandHandler"}

    def __init__(cls, name, bases, namespace) -> None:
        super().__init__(name, bases, namespace)

        # Skip top-level or abstract classes that still have abstract methods.
        # They might not define event_name/command_name yet (or we simply don't want to enforce).
        if getattr(cls, "__abstractmethods__", None):
            # Class is still abstract; skip validation and registration.
            return

        if not getattr(cls, "auto_register", True):
            # auto_register = False; skip registration entirely
            return

        if name in cls.get_excluded_names():
            # Class name is in the excluded set; skip
            return

        # For non-abstract, auto-registering classes:
        event_name = getattr(cls, "event_name", None)
        command_name = getattr(cls, "command_name", None)

        has_event = event_name is not None
        has_command = command_name is not None

        if has_event and has_command:
            raise TypeError(
                f"Class {name} defines BOTH 'event_name' and 'command_name'. "
                "A handler class can only handle events OR commands, not both."
            )
        elif not has_event and not has_command:
            raise TypeError(
                f"Class {name} defines NEITHER 'event_name' nor 'command_name'. "
                "A handler class must define exactly one of these to be auto-registered."
            )

        # Register in the appropriate registry
        if has_event:
            if event_name not in cls._event_registry:
                cls._event_registry[event_name] = set()
            cls._event_registry[event_name].add(cls)
            logging.info(f"Registered {name} for event_name = {event_name}")
        else:
            if command_name not in cls._command_registry:
                cls._command_registry[command_name] = set()
            cls._command_registry[command_name].add(cls)
            logging.info(f"Registered {name} for command_name = {command_name}")

    @classmethod
    def get_event_registry(mcs) -> Dict[EventNames, Set[Type]]:
        """ Returns the registry of classes (subclasses) that define 'event_name'. """
        return mcs._event_registry

    @classmethod
    def get_command_registry(mcs) -> Dict[CommandNames, Set[Type]]:
        """ Returns the registry of classes (subclasses) that define 'command_name'. """
        return mcs._command_registry

    @classmethod
    def get_excluded_names(mcs):
        """
        Returns a set of class names that are excluded from auto-registration.
        """
        return mcs._excluded_names
