import functools
import logging
from abc import ABC, abstractmethod
from multiprocessing import Process
from typing import Any, Callable, Dict, List, Optional, Set, Type

from keven_core.kafka.events.event import EventNames
from keven_core.kafka.abstracts.delayed import DelayedCommandsAndEvents
from keven_core.utils.threading.thread_mgr import ThreadManager

# NOTE: In the future, consider using a registry metaclass instead of __init_subclass__
# for automatic registration of EventHandler subclasses.

class EventHandler(ABC):
    """
    Main abstract base class for handling events.

    As events are received, instances of registered EventHandler subclasses
    are created to process those events. Additionally, a function registry
    is maintained; functions registered via register_function() are also executed
    when events are received.

    Subclasses are auto-registered (unless explicitly disabled) via __init_subclass__.
    """
    event_name: Optional[EventNames] = None
    _registry: Dict[EventNames, Set[Type["EventHandler"]]] = dict()
    _func_registry: Dict[EventNames, List[Callable[[Any], None]]] = dict()
    _func_pre_handler_hooks: List[Callable[[], None]] = list()
    _func_post_handler_hooks: List[Callable[[], None]] = list()
    delay_commands_and_events: bool = True
    auto_register: bool = True
    capture_exception_handler: Optional[Callable[[Exception], None]] = None

    def __init_subclass__(cls, **kwargs) -> None:
        if cls.auto_register and cls.__name__ != "LongRunningEventHandler":
            EventHandler.register_handler(cls)

    @classmethod
    def register_handler(cls, handler_class: Type["EventHandler"]) -> None:
        """
        Registers an event handler class for the event specified by handler_class.event_name.
        """
        logging.info(f"⚙️ Register Event Handler {handler_class.event_name.value} ⚙")
        if not cls._registry.get(handler_class.event_name):
            cls._registry[handler_class.event_name] = set()
        cls._registry[handler_class.event_name].add(handler_class)

    @classmethod
    def register_function(cls, event_name: EventNames, func: Callable[[Any], None]) -> None:
        """
        Registers a function to be called when an event with the specified event_name is received.
        """
        if not cls._func_registry.get(event_name):
            cls._func_registry[event_name] = []
        cls._func_registry[event_name].append(func)

    @classmethod
    def register_pre_handler_hook(cls, func: Callable[[], None]) -> None:
        """
        Registers a function to be executed before an event handler runs.
        """
        cls._func_pre_handler_hooks.append(func)

    @classmethod
    def register_post_handler_hook(cls, func: Callable[[], None]) -> None:
        """
        Registers a function to be executed after an event handler runs.
        """
        cls._func_post_handler_hooks.append(func)

    @classmethod
    def handle_all_events(cls, event: Any) -> None:
        """
        Handles an event by invoking all registered handlers and functions for all event types.
        """
        for event_name in cls._registry:
            for handler_class in cls._registry[event_name]:
                cls.execute_handler_according_to_protocol(event, handler_class)

    @classmethod
    def handle_events(cls, event: Any) -> None:
        """
        Handles an event by invoking all registered handlers and functions associated with the event's type.
        """
        if cls._registry.get(event.event_name):
            for handler_class in cls._registry[event.event_name]:
                cls.execute_handler_according_to_protocol(event, handler_class)

        if cls._func_registry.get(event.event_name):
            for handler_func in cls._func_registry[event.event_name]:
                cls.execute_pre_handler_hooks()
                handler_func(event)
                cls.execute_post_handler_hooks()

    @classmethod
    def execute_handler_according_to_protocol(cls, event: Any, handler_class: Type["EventHandler"]) -> None:
        """
        Executes an event handler for the given event, wrapping execution in a DelayedCommandsAndEvents context if configured.
        Catches and handles exceptions based on capture_exception_handler.
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
        Executes the given handler_class's event processing method with the provided event.
        Pre- and post-handler hooks are executed in the order they were registered.
        """
        cls.execute_pre_handler_hooks()
        handler = handler_class()
        handler.handle_event(event)
        cls.execute_post_handler_hooks()

    @classmethod
    def execute_pre_handler_hooks(cls) -> None:
        """
        Executes all registered pre-handler hooks in order.
        """
        for hook in cls._func_pre_handler_hooks:
            hook()

    @classmethod
    def execute_post_handler_hooks(cls) -> None:
        """
        Executes all registered post-handler hooks in order.
        """
        for hook in cls._func_post_handler_hooks:
            hook()

    @classmethod
    def events_with_handlers(cls) -> set:
        """
        Returns a set of event names (lowercase strings) that have registered handlers.
        """
        events = set()
        for event_name in cls._registry.keys():
            events.add(event_name.value.lower())
        return events

    @abstractmethod
    def handle_event(self, event: Any) -> None:
        """
        Processes an individual event. Must be implemented by subclasses.
        """
        pass

    @classmethod
    def get_handler_count(cls, message_name: EventNames) -> int:
        """
        Returns the number of registered handlers for the given message name.
        """
        if cls._registry.get(message_name):
            return len(cls._registry[message_name])
        return 0

    @classmethod
    def create_handler_server_process(cls, name: str, io_server: Optional[Any] = None) -> Process:
        """
        Creates and returns a new process that runs an event receiver server.

        This function clears command and event publishers before starting the server.
        Future modifications could include enhanced error handling or configuration options.

        Args:
            name (str): The name for the server process.
            io_server (object, optional): An I/O server instance to be used by the event receiver server.

        Returns:
            Process: A new multiprocessing.Process instance.
        """
        def process_method(a_name: str) -> None:
            from keven_core.kafka.events.server import start_events_receiver_server
            from keven_core.kafka.commands.dispatcher import clear_command_publishers
            from keven_core.kafka.events.logger import keven_clear_event_publishers

            clear_command_publishers()
            keven_clear_event_publishers()

            start_events_receiver_server(
                a_name,
                io_server=io_server,
                auto_reprocess_errors=True,
            )

        # Future enhancements might add additional logging or error handling here.
        return Process(target=process_method, args=(name,))


def event_handler(event_name: EventNames, delay_commands_and_events: bool = True) -> Callable:
    """
    Decorator to create an event handler from a function.

    Example:
        @event_handler(EVENT_NAME)
        def my_func(event):
            pass

    Args:
        event_name (EventNames): The event name that this handler should process.
        delay_commands_and_events (bool): Whether to delay commands and events during processing.

    Returns:
        Callable: A decorated function that acts as an event handler.
    """
    def event_handler_decorator(func: Callable) -> Callable:
        from keven_core.kafka.events.event import Event
        cls = Event.create_handler(
            event_name,
            func,
            delay_commands_and_events=delay_commands_and_events,
        )
        print(cls)

        @functools.wraps(func)
        def event_handler_wrapper(*args, **kwargs):
            return cls.func(*args, **kwargs)

        return event_handler_wrapper

    return event_handler_decorator


class LongRunningEventHandler(EventHandler):
    """
    A specialized EventHandler for long-running tasks that are processed using a ThreadManager.

    This class is rarely used and requires a ThreadManager to be assigned.
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
    Helper function to execute the long-running event handler.

    Args:
        event_handler (LongRunningEventHandler): An instance of LongRunningEventHandler.
    """
    event_handler.long_running_handle_event(event_handler.event)
