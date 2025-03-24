import functools
import logging
import traceback
from abc import ABC, abstractmethod
from datetime import datetime
from multiprocessing import Process

from keven_core.kafka.commands.command import Command, CommandPhase, CommandNames
from keven_core.kafka.commands.dispatcher import (
keven_dispatch_command,
clear_command_publishers,
)
from keven_core.kafka.events.event import Event
from keven_core.kafka.events.logger import keven_clear_event_publishers
from keven_core.kafka.abstracts.delayed import DelayedCommandsAndEvents
from keven_core.utils.threading.thread_mgr import ThreadManager


class CommandHandler(ABC):
    """
    This is the main CommandHandler class.  As commands are received it creates
    instances of registered CommandHandler Subclasses to handle events.  It
    also has a function/method registry.  Theses functions are called when
    commands are received.  A single command can trigger many subclasses and
    functions.

    NOTE: Handlers implemented as functions should be used with care as they
    do not have the capability of dispatching start, complete and error events.

    TODO: See if we can make some sort of registry metaclass
          Create Parent Class for CommandHandler and EventHandler

    """

    command_name = None
    _registry = dict()
    _func_registry = dict()
    _func_pre_handler_hooks = list()
    _func_post_handler_hooks = list()
    delay_commands_and_events = True
    auto_register = True
    capture_exception_handler = None

    def __init__(self, command):
        self.command: Command = command
        self.additional_commands = list()
        self.error_message = ""

    def __init_subclass__(cls, **kwargs):
        if cls.auto_register and cls.__name__ != "LongRunningCommandHandler":
            CommandHandler.register_handler(cls)

    @classmethod
    def register_handler(cls, handler_class):
        logging.info(
            f"⚙️ Register Command Handler {handler_class.command_name.value} ⚙"
        )
        if not cls._registry.get(handler_class.command_name):
            cls._registry[handler_class.command_name] = set()
        if handler_class not in cls._registry[handler_class.command_name]:
            cls._registry[handler_class.command_name].add(handler_class)

    @classmethod
    def register_function(cls, command_name: CommandNames, func):
        if not CommandHandler._func_registry.get(command_name):
            CommandHandler._func_registry[command_name] = list()
        CommandHandler._func_registry[command_name].append(func)

    @classmethod
    def register_pre_handler_hook(cls, func):
        cls._func_pre_handler_hooks.append(func)

    @classmethod
    def register_post_handler_hook(cls, func):
        cls._func_post_handler_hooks.append(func)

    @classmethod
    def handle_all_commands(cls, command):
        for command_name in cls._registry:
            for handler_class in cls._registry[command_name]:
                cls.execution_handler_according_to_protocol(
                    command, handler_class
                )

    @classmethod
    def handle_commands(cls, command):
        if cls._registry.get(command.command_name):
            for handler_class in cls._registry[command.command_name]:
                cls.execution_handler_according_to_protocol(
                    command, handler_class
                )

        func_list = cls._func_registry.get(command.command_name)
        if func_list:
            for func in func_list:
                cls.execute_pre_handler_hooks()
                func(command)
                cls.execute_post_handler_hooks()

    @classmethod
    def execution_handler_according_to_protocol(cls, command, handler_class):
        if cls.delay_commands_and_events:
            with DelayedCommandsAndEvents():
                handler = cls.execute_handler(command, handler_class)
        else:
            handler = cls.execute_handler(command, handler_class)
        for add_cmd in handler.additional_commands:
            keven_dispatch_command(add_cmd)

    @classmethod
    def execute_handler(cls, command, handler_class):
        from keven_core.kafka.events.event import keven_log_event_now

        cls.execute_pre_handler_hooks()
        handler: CommandHandler = handler_class(command)

        started_event = handler.start_event(get_old_event=False)
        started_time = datetime.now()
        if started_event is not None:  # otherwise do nothing
            started_time = started_event.created
            keven_log_event_now(started_event)
        try:
            handler.handle_command(command)
        except Exception as e:
            import traceback

            if cls.capture_exception_handler:
                cls.capture_exception_handler(e)
            logging.error(traceback.format_exc())

            cls.execute_post_handler_hooks()
            errored_event = handler.error_event(get_old_event=False)

            if errored_event is not None:  # otherwise do nothing
                errored_event.error_message = str(e)
                # errored_event.traceback = e.__traceback__
                errored_time = datetime.now()
                errored_event.compute_time = (
                    errored_time - started_time
                ).microseconds
                keven_log_event_now(errored_event)
            return handler

        cls.execute_post_handler_hooks()
        completed_event = handler.complete_event(get_old_event=False)

        if completed_event is not None:  # otherwise do nothing
            a_completed_time = datetime.now()
            completed_event.compute_time = (
                a_completed_time - started_time
            ).microseconds
            keven_log_event_now(completed_event)

        return handler

    @classmethod
    def execute_pre_handler_hooks(cls):
        for hook in cls._func_pre_handler_hooks:
            hook()

    @classmethod
    def execute_post_handler_hooks(cls):
        for hook in cls._func_post_handler_hooks:
            logging.verbose(f"Post handler: {hook.__name__}")
            hook()

    @classmethod
    def commands_with_handlers(cls):
        commands = set()
        for cmd_name in cls._registry.keys():
            commands.add(cmd_name.value.lower())
        return commands

    @abstractmethod
    def handle_command(self, command):
        pass

    def start_event(self, include_source=True, get_old_event=True):
        event = Event.from_name(
            self.command.get_event_name(
                CommandPhase.STARTED, old_name=get_old_event
            )
        )
        if include_source is True:
            event.source_command = self.command
        return event

    def complete_event(self, include_source=True, get_old_event=True):
        event = Event.from_name(
            self.command.get_event_name(
                CommandPhase.COMPLETED, old_name=get_old_event
            )
        )
        if include_source is True:
            event.source_command = self.command
        return event

    def error_event(self, msg="", include_source=True, get_old_event=True):
        error_message = msg or self.error_message or ""
        logging.error(error_message)

        event = Event.from_name(
            self.command.get_event_name(
                CommandPhase.ERRORED, old_name=get_old_event
            )
        )
        if include_source is True:
            event.source_command = self.command
        event.error_message = error_message
        event.traceback = traceback.format_exc()
        return event

    @classmethod
    def get_handler_count(cls, message_name):
        if cls._registry.get(message_name):
            return len(cls._registry[message_name])
        else:
            return 0

    @classmethod
    def create_handler_server_process(cls, name: str, io_server_factory=None):
        def process_method(a_name, p_io_server):
            from keven_core.kafka.commands.command_server import start_command_receiver_server

            clear_command_publishers()
            keven_clear_event_publishers()

            start_command_receiver_server(
                a_name,
                auto_reprocess_errors=True,
                max_poll_interval=5 * 60,
                io_server=p_io_server,
            )

        return Process(target=process_method, args=(name, None))


def command_handler(
    command_name, delay_commands_and_events=True, exception_handler=None
):
    """
    This is a decorator to create a command handler.
    e.g.:
        @command_handler(COMMAND_NAME)
        def my_func(command):
            pass
    """

    def command_handler_decorator(func):
        # CommandHandler.register_function(command_name, func)
        cls = Command.create_handler(
            command_name,
            func,
            delay_commands_and_events=delay_commands_and_events,
        )
        cls.capture_exception_handler = exception_handler
        print(cls)

        @functools.wraps(func)
        def command_handler_wrapper(*args, **kwargs):
            return cls.func(*args, **kwargs)

        return command_handler_wrapper

    return command_handler_decorator


class LongRunningCommandHandler(CommandHandler):
    thread_manager: ThreadManager = None

    def long_running_handle_command(self, command):
        raise NotImplementedError("Please implement me")

    def handle_command(self, command):
        if not self.thread_manager:
            raise ValueError("You must set a thread_manager")
        self.thread_manager.queue_object(self)


def long_running_command_handler(command_handler: LongRunningCommandHandler):
    command_handler.long_running_handle_command(command_handler.command)
