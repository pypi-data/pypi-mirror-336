import logging
from enum import Enum

import jsonpickle

from keven_core.kafka.commands.command_names import CommandNames
from grpc_registry_protos.kafka.commands_and_events_pb2 import Command as pbCommand
from keven_core.kafka.abstracts.message import Message


class CommandPhase(Enum):
    STARTED = "STARTED"
    ERRORED = "ERRORED"
    COMPLETED = "COMPLETED"


class Command(Message):
    """
    Base Class (abstract) and factory for loading payloads from commands.
    """

    command_name = CommandNames.NONE
    auto_register = True
    auto_create_command_events = True

    def __init__(self):
        super().__init__()
        # TODO: Use some global user id here
        self.initiated_by_user_id = None

    def __init_subclass__(cls, **kwargs):
        if cls.auto_register:
            # Command._registry[cls.command_name] = cls
            Command.register_command(cls)

    @classmethod
    def create_event_class(cls, namespace, parent_class, event_name_string):
        from keven_core.kafka.events.event import Event, EventNames
        from aenum import extend_enum

        if namespace:
            event_name_enum = namespace.event_names_enum
        else:
            event_name_enum = EventNames

        extend_enum(event_name_enum, event_name_string, event_name_string)
        event_name = event_name_enum._value2member_map_[event_name_string]
        class_name = event_name_string.title().replace("_", "")
        event_class = type(
            class_name,
            (parent_class,),
            {
                "auto_register": False,
                "namespace": namespace,
                "event_name": event_name,
            },
        )

        Event.register_event(event_class)

    @classmethod
    def create_command_phase_event_class(cls, command_class, stage):
        from keven_core.kafka.abstracts.commandevent import CommandErrorEvent, CommandEvent
        parent = (
            CommandErrorEvent
            if stage is CommandPhase.ERRORED
            else CommandEvent
        )

        event_name_string = (
            f"CMD_{command_class.command_name.value}_{stage.value}"
        )

        cls.create_event_class(
            command_class.namespace, parent, event_name_string
        )

    @classmethod
    def register_command(cls, command_class):
        if Command._registry.get(command_class.command_name):
            return
        Command._registry[command_class.command_name] = command_class

        if command_class.auto_create_command_events:
            Command.create_command_phase_event_class(
                command_class, CommandPhase.STARTED
            )
            Command.create_command_phase_event_class(
                command_class, CommandPhase.ERRORED
            )
            Command.create_command_phase_event_class(
                command_class, CommandPhase.COMPLETED
            )

    @classmethod
    def get_event_name(cls, stage, command_name=None, old_name=True):
        if cls.namespace:
            event_name_enum = cls.namespace.event_names_enum
        else:
            from keven_core.kafka.events.event_names import EventNames

            event_name_enum = EventNames

        if command_name:
            for ns in Command.namespaces:
                if (
                    command_name.value
                    in Command.namespaces[
                        ns
                    ].command_names_enum._value2member_map_
                ):
                    event_name_enum = Command.namespaces[ns].event_names_enum
        else:
            command_name = cls.command_name

        old_stages = {
            CommandPhase.COMPLETED: "COMPLETE",
            CommandPhase.STARTED: "START",
            CommandPhase.ERRORED: "ERROR",
        }

        if old_name:
            old_event_name_string = (
                f"CMD_{command_name.value}_{old_stages[stage]}"
            )
            if event_name_enum._value2member_map_.get(old_event_name_string):
                return event_name_enum._value2member_map_[
                    old_event_name_string
                ]

        event_name_string = f"CMD_{command_name.value}_{stage.value}"
        event_name = event_name_enum._value2member_map_[event_name_string]
        return event_name

    @classmethod
    def from_protobuf(cls, protobuf):
        """
        Create a command instance from a protobuf object.  The resulting object
        will be a subclass of Command
        """
        command = Command.from_name_string(protobuf.name, protobuf.namespace)

        command.originator = protobuf.originator
        command.created = protobuf.created.ToDatetime()
        command._uuid = protobuf.uuid
        command.parse_payload(protobuf.payload)

        Message.large_attribute_manager.reload(command)
        return command

    @classmethod
    def from_name_string(cls, name, namespace_name: str = None):
        """
        Create a command instance from a protobuf object.  The resulting object
        will be a subclass of Command
        """

        def create_placeholder_command():
            logging.warning(f"Command {name} is not installed")
            return cls._registry[CommandNames.NOT_INSTALLED]()

        name_enum = CommandNames
        if namespace_name:
            namespace = Command.namespaces.get(namespace_name)
            if not namespace:
                return create_placeholder_command()
            else:
                name_enum = namespace.command_names_enum

        if name not in name_enum._value2member_map_:
            return create_placeholder_command()

        return cls._registry[name_enum(name)]()

    @classmethod
    def from_bytes(cls, data: bytes):
        """
        Create the Command from a byte array
        """
        pb_command = pbCommand()
        pb_command.ParseFromString(data)

        return Command.from_protobuf(pb_command)

    def serialize_payload(self) -> bytes:
        return self.serialize()

    def serialize(self):
        """
        This is used to serialize the command using protobuf
        """
        la: [] = Message.large_attribute_manager.offload(self)

        protobuf = pbCommand()
        protobuf.name = self.command_name.value
        protobuf.originator = self.originator
        protobuf.created.FromDatetime(self.created)
        protobuf.uuid = self._uuid
        protobuf.payload = self.serialize_payload()

        # now restore the Command back to its original state with the
        # large attribute values, overriding the file path names
        # that were put in place by offload()
        Message.large_attribute_manager.restore(self, la)

        if self.namespace:
            protobuf.namespace = self.namespace.name

        return protobuf

    def set_uuid(self, uuid: str):
        """
        Sometimes (eg cron scheduler) we want to use our own
        UUID and not a new one each time
        """

        try:
            self._uuid = uuid
        except ValueError as ve:
            logging.error(f"Unable to set uuid ({uuid}) '{ve}'")
        return self._uuid

    def get_uuid(self):
        return self._uuid

    def dispatch(self, now=False):
        from keven_core.kafka.commands.dispatcher import (
            keven_dispatch_command,
            keven_dispatch_command_now)

        if now:
            keven_dispatch_command_now(self)
        else:
            keven_dispatch_command(self)

    @staticmethod
    def create_handler(
        command_name,
        handler_method,
        auto_register=True,
        delay_commands_and_events=True,
    ):
        from keven_core.kafka.abstracts.command_handler import CommandHandler
        count = CommandHandler.get_handler_count(command_name)
        handler_class_name = (
            f"{command_name.value.title().replace('_', '')}" f"Handler{count}"
        )
        handler_class = type(
            handler_class_name,
            (CommandHandler,),
            {
                "command_name": command_name,
                "auto_register": auto_register,
                "delay_commands_and_events": delay_commands_and_events,
                "handle_command": handler_method,
            },
        )
        return handler_class


class BasicDetail(object):
    def __init__(self):
        self.message = ""


class PickledCommand(Command):

    detail_class = BasicDetail

    def __init__(self):
        super().__init__()
        self.details = self.detail_class()

    def parse_payload(self, payload: bytes):
        try:
            self.details = jsonpickle.decode(payload.decode())
        except TypeError as e:
            logging.warning(f"Could not parse command: {e}")
            self.details = self.detail_class()

    def serialize_payload(self) -> bytes:
        return jsonpickle.encode(self.details).encode()
