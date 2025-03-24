import importlib
import os
import uuid
from abc import abstractmethod, ABC
from datetime import datetime

from keven_core.utils.large_attribute_mgr import LargeAttributeManager

large_att_config = (
    os.getenv("LARGE_ATTRIBUTE_HOST", '/'),
    os.getenv("LARGE_ATTRIBUTE_FOLDER", '/'),
    os.getenv("LARGE_ATTRIBUTE_PARTITION"),
    os.getenv("LARGE_ATTRIBUTE_BYTE_THRESHOLD"))

class MessageNamespace:
    def __init__(self, name, command_names_enum, event_names_enum):
        self.name = name
        self.command_names_enum = command_names_enum
        self.event_names_enum = event_names_enum


class MessageServiceProcessManager:
    registry = list()

    @classmethod
    def register_service(cls, service):
        cls.registry.append(service)

    @classmethod
    def register_handlers(cls, module_name: str):
        importlib.import_module(module_name)

    @classmethod
    def start_all_services(cls, name):
        """
        Start all services, then wait for them to termination
        """
        from keven_core.kafka.abstracts.command_handler import CommandHandler
        from keven_core.kafka.abstracts.event_handler import EventHandler

        MessageServiceProcessManager.register_service(
            CommandHandler.create_handler_server_process(name)
        )
        MessageServiceProcessManager.register_service(
            EventHandler.create_handler_server_process(name)
        )
        for proc in cls.registry:
            proc.start()

    @classmethod
    def join_services(cls):
        for proc in cls.registry:
            print(proc)
            proc.join()


class Message(ABC):
    """
    Base Class (abstract) and factory for loading payloads from events.
    """

    _registry = dict()
    namespace = None
    namespaces = {}
    # large_attribute_manager automatically manages attributes that are too
    # large for Kafka by putting them in a file during transit.
    # This is based on the attributes listed in large_attributes for a
    # Message subclass
    large_attribute_manager = LargeAttributeManager(*large_att_config)
    large_attributes = None

    def __init__(self):
        self.payload = None
        self.originator = ""
        self.created = datetime.now()
        self._uuid = uuid.uuid4().__str__()
        self._is_internal = False

    def __init_subclass__(cls, **kwargs):
        """
        implement this in your sub class
        """
        pass

    @classmethod
    def register_namespace(cls, namespace_def: MessageNamespace):
        if cls.namespaces.get(namespace_def.name):
            ValueError(f"Namespace exists: {namespace_def.name}")
        cls.namespaces[namespace_def.name] = namespace_def

    @classmethod
    @abstractmethod
    def from_protobuf(cls, protobuf):
        """
        Create an message instance from a protobuf object.  The resulting
        object will be a subclass of whatever concrete base message type you
        define
        """
        pass

    @classmethod
    def from_name(cls, name):
        """
        Create a new event object based on the name passed in
        """
        message_class = cls._registry.get(name)
        if not message_class:
            raise Exception(f"Message (Command/Event) not found for: {name}")
        return message_class()

    @classmethod
    @abstractmethod
    def from_name_string(cls, name):
        """
        Get the class from a string
        """
        pass

    @abstractmethod
    def parse_payload(self, payload: bytes):
        """
        Your subclass implements this to parse the payload.  The payload can
        be in any format.
        """
        pass

    @abstractmethod
    def serialize(self):
        """
        This is used to serialize the event using protobuf
        """
        pass

    @abstractmethod
    def serialize_payload(self) -> bytes:
        """
        Implement this to serialize the payload.  It could serialize to
        anything :)  Protobuf is the format of choice.
        """
        pass
