import functools
import logging
from abc import ABC, abstractmethod
from multiprocessing import Process
from typing import Any, Callable, Dict, List, Optional, Type, Set

from keven_core.kafka.events.event import EventNames
from keven_core.kafka.abstracts.delayed import DelayedCommandsAndEvents
from keven_core.utils.threading.thread_mgr import ThreadManager
from keven_core.kafka.abstracts.metaclass.base_handler_meta import BaseHandlerMeta

class EventHandler(ABC, metaclass=BaseHandlerMeta):
    """
    Abstract base class for handling events with automatic registration via BaseHandlerMeta.

    A subclass must define event_name = <some EventNames> and must ensure command_name = None.
    If both or neither are defined, a TypeError will be raised.

    Features:
      - Function registry (register_function).
      - Pre- and post-handler hooks.
      - Delayed execution (via DelayedCommandsAndEvents) if delay_commands_and_events is True.
      - A create_handler_server_process method to spin up a separate process.

    Usage Example:
        class PrintEventHandler(EventHandler):
            event_name = EventNames.PRINT_EVENT  # Required
            command_name = None  # Must remain None

            def handle_event(self, event: Any) -> None:
                print(f"Handling PRINT_EVENT: {event}")
    """

    # For an EventHandler, we define only event_name; command_name must remain None.
    event_name: Optional[EventNames] = None
    command_name = None  # Must be None to avoid conflicts in BaseHandlerMeta
    auto_register: bool = True
    delay_commands_and_events: bool = True
    capture_exception_handler: Optional[Callable[[Exception], None]] = None

    # Class-level registries for function handlers and hooks
    _func_registry: Dict[EventNames, List[Callable[[Any], None]]] = {}
    _func_pre_handler_hooks: List[Callable[[], None]] = []
    _func_post_handler_hooks: List[Callable[[], None]] = []

    @classmethod
    def register_function(cls, event_name: EventNames, func: Callable[[Any], None]) -> None:
        """
        Registers a function to be called when an event with the specified event_name is received.
        """
        if event_name not in cls._func_registry:
            cls._func_registry[event_name] = []
        cls._func_registry[event_name].append(func)

    @classmethod
    def register_pre_handler_hook(cls, func: Callable[[], None]) -> None:
        """
        Registers a pre-handler hook that is executed before an event handler runs.
        """
        cls._func_pre_handler_hooks.append(func)

    @classmethod
    def register_post_handler_hook(cls, func: Callable[[], None]) -> None:
        """
        Registers a post-handler hook that is executed after an event handler runs.
        """
        cls._func_post_handler_hooks.append(func)

    @classmethod
    def handle_all_events(cls, event: Any) -> None:
        """
        Processes an event with all registered EventHandlers across all event types.
        """
        # We retrieve the event registry from BaseHandlerMeta directly.
        from keven_core.kafka.abstracts.metaclass.base_handler_meta import BaseHandlerMeta
        registry = BaseHandlerMeta.get_event_registry()
        for event_name, handler_set in registry.items():
            for handler_class in handler_set:
                cls.execute_handler_according_to_protocol(event, handler_class)

    @classmethod
    def handle_events(cls, event: Any) -> None:
        """
        Processes an event with all handlers and functions associated with the event's type.
        """
        from keven_core.kafka.abstracts.metaclass.base_handler_meta import BaseHandlerMeta
        registry = BaseHandlerMeta.get_event_registry()

        # 1) Invoke class-based event handlers
        if event.event_name in registry:
            for handler_class in registry[event.event_name]:
                cls.execute_handler_according_to_protocol(event, handler_class)

        # 2) Invoke function-based event handlers
        if event.event_name in cls._func_registry:
            for handler_func in cls._func_registry[event.event_name]:
                cls.execute_pre_handler_hooks()
                handler_func(event)
                cls.execute_post_handler_hooks()

    @classmethod
    def execute_handler_according_to_protocol(cls, event: Any, handler_class: Type["EventHandler"]) -> None:
        """
        Executes the event handler, optionally within a DelayedCommandsAndEvents context.
        Exceptions are handled via capture_exception_handler if set.
        """
        try:
            if cls.delay_commands_and_events:
                with DelayedCommandsAndEvents():
                    cls.execute_event_handler(event, handler_class)
            else:
                cls.execute_event_handler(event, handler_class)
        except Exception as e:
            if cls.capture_exception_handler:
                cls.capture_exception_handler(e)
            else:
                logging.error(f"Error executing handler: {e}", exc_info=True)

    @classmethod
    def execute_event_handler(cls, event: Any, handler_class: Type["EventHandler"]) -> None:
        """
        Instantiates the handler_class, runs pre-handler hooks, calls handle_event,
        then runs post-handler hooks.
        """
        cls.execute_pre_handler_hooks()
        handler = handler_class()
        handler.handle_event(event)
        cls.execute_post_handler_hooks()

    @classmethod
    def execute_pre_handler_hooks(cls) -> None:
        """
        Executes all pre-handler hooks in the order they were registered.
        """
        for hook in cls._func_pre_handler_hooks:
            hook()

    @classmethod
    def execute_post_handler_hooks(cls) -> None:
        """
        Executes all post-handler hooks in the order they were registered.
        """
        for hook in cls._func_post_handler_hooks:
            hook()

    @classmethod
    def events_with_handlers(cls) -> Set[str]:
        """
        Returns a set of event names (as lowercase strings) for which handlers are registered.
        """
        from keven_core.kafka.abstracts.metaclass.base_handler_meta import BaseHandlerMeta
        registry = BaseHandlerMeta.get_event_registry()
        return {event_name.value.lower() for event_name in registry.keys()}

    @classmethod
    def get_handler_count(cls, message_name: EventNames) -> int:
        """
        Returns the number of registered handlers for a given event name.
        """
        from keven_core.kafka.abstracts.metaclass.base_handler_meta import BaseHandlerMeta
        registry = BaseHandlerMeta.get_event_registry()
        if message_name in registry:
            return len(registry[message_name])
        return 0

    @classmethod
    def create_handler_server_process(cls, name: str, io_server: Optional[Any] = None) -> Process:
        """
        Creates and returns a new Process that runs an event receiver server.

        Clears command and event publishers prior to starting the server.
        """
        def process_method(a_name: str) -> None:
            from keven_core.kafka.events.server import start_events_receiver_server
            from keven_core.kafka.commands.dispatcher import clear_command_publishers
            from keven_core.kafka.events.logger import keven_clear_event_publishers

            clear_command_publishers()
            keven_clear_event_publishers()

            start_events_receiver_server(a_name, io_server=io_server, auto_reprocess_errors=True)

        return Process(target=process_method, args=(name,))

    @abstractmethod
    def handle_event(self, event: Any) -> None:
        """
        Must be implemented by each concrete subclass, defining how it processes events.
        """
        pass

# Optional decorator for function-based event handlers:
def event_handler(event_name: EventNames, delay_commands_and_events: bool = True) -> Callable:
    """
    Decorator to convert a function into an event handler for the given event_name.
    """
    def event_handler_decorator(func: Callable) -> Callable:
        from keven_core.kafka.events.event import Event
        cls = Event.create_handler(event_name, func, delay_commands_and_events=delay_commands_and_events)
        print(cls)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return cls.func(*args, **kwargs)

        return wrapper

    return event_handler_decorator


class LongRunningEventHandler(EventHandler):
    """
    Specialized EventHandler for long-running tasks using a ThreadManager.

    Must assign a ThreadManager to the thread_manager attribute.
    """
    thread_manager: Optional[ThreadManager] = None

    def __init__(self) -> None:
        self.event = None

    def long_running_handle_event(self, event: Any) -> None:
        raise NotImplementedError("Please implement me")

    def handle_event(self, event: Any) -> None:
        if not self.thread_manager:
            raise ValueError("You must set a thread_manager")
        self.event = event
        self.thread_manager.queue_object(self)


def long_running_event_handler(event_handler: LongRunningEventHandler) -> None:
    """
    Helper for executing a long-running event handler (once dequeued by the ThreadManager).
    """
    event_handler.long_running_handle_event(event_handler.event)
