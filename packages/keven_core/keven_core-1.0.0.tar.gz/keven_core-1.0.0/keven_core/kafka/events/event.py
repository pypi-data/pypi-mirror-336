import logging

import jsonpickle
from keven_core.kafka.events.event_names import EventNames
from grpc_registry_protos.kafka.commands_and_events_pb2 import Event as pbEvent
from keven_core.kafka.abstracts.message import Message
from keven_core.kafka.events.logger import (
    keven_log_event,
    keven_log_event_now,
)


class Event(Message):
    """
    Base Class (abstract) and factory for loading payloads from events.
    """

    event_name = EventNames.NONE
    auto_register = True

    def __init__(self):
        super().__init__()
        self._source_command_uuid = ""
        self.is_audit_event = False

    def __init_subclass__(cls, **kwargs):
        if cls.auto_register:
            Event._registry[cls.event_name] = cls

    @classmethod
    def register_event(cls, event_class):
        if Event._registry.get(event_class.event_name):
            return
        Event._registry[event_class.event_name] = event_class

    @classmethod
    def register_handler(cls, handler_class):
        cls._registry[cls.event_name] = handler_class

    @classmethod
    def from_protobuf(cls, protobuf):
        """
        Create an event instance from a protobuf object.  The resulting object
        will be a subclass of Event
        """
        event = cls.from_name_string(protobuf.name, protobuf.namespace)
        event.originator = protobuf.originator
        event.created = protobuf.created.ToDatetime()
        event._uuid = protobuf.uuid
        event._source_command_uuid = protobuf.source_command_uuid
        event.parse_payload(protobuf.payload)

        Message.large_attribute_manager.reload(event)
        return event

    @classmethod
    def from_name_string(cls, name, namespace_name: str = None):
        """
        Create an event instance from a protobuf object.  The resulting object
        will be a subclass of Event
        """

        def create_placeholder_event():
            logging.warning(f"Event {name} is not installed")
            return cls._registry[EventNames.NOT_INSTALLED]()

        name_enum = EventNames
        if namespace_name:
            namespace = Event.namespaces.get(namespace_name)
            if not namespace:
                return create_placeholder_event()
            else:
                name_enum = namespace.event_names_enum

        if name not in name_enum._value2member_map_:
            return create_placeholder_event()

        return cls._registry[name_enum(name)]()

    @classmethod
    def from_bytes(cls, data: bytes):
        """
        Create the Event from a byte array
        """
        pb_event = pbEvent()
        pb_event.ParseFromString(data)

        if EventNames(pb_event.name) not in cls._registry:
            logging.warning(f"Event {pb_event.name} not found")
            pb_event.name = EventNames.NOT_INSTALLED

        return Event.from_protobuf(pb_event)

    def serialize(self):
        """
        This is used to serialize the event using protobuf
        """
        la = Message.large_attribute_manager.offload(self)

        protobuf = pbEvent()
        protobuf.name = self.event_name.value
        protobuf.originator = self.originator
        protobuf.created.FromDatetime(self.created)
        protobuf.uuid = self._uuid
        if self._source_command_uuid:
            protobuf.source_command_uuid = self._source_command_uuid
        protobuf.payload = self.serialize_payload()

        # now restore the Event back to its original state with the
        # large attribute values, overriding the file path names
        # that were put in place by offload()
        Message.large_attribute_manager.restore(self, la)

        if self.namespace:
            protobuf.namespace = self.namespace.name
        return protobuf

    def log(self, now=False):


        if now:
            keven_log_event_now(self)
        else:
            keven_log_event(self)

    @staticmethod
    def create_handler(
        event_name,
        handler_method,
        auto_register=True,
        delay_commands_and_events=True,
    ):
        from keven_core.kafka.abstracts.event_handler import EventHandler
        count = EventHandler.get_handler_count(event_name)
        handler_class_name = (
            f"{event_name.value.title().replace('_', '')}" f"Handler{count}"
        )
        handler_class = type(
            handler_class_name,
            (EventHandler,),
            {
                "event_name": event_name,
                "auto_register": auto_register,
                "delay_commands_and_events": delay_commands_and_events,
                "handle_event": handler_method,
            },
        )
        return handler_class


class BasicDetail(object):
    def __init__(self):
        self.message = ""


class PickledEvent(Event):
    """
    This event serialised itself to JSON.  Use the detail_class Class member
    to set the structure for the JSON object to be pickled.
    """

    detail_class = BasicDetail

    def __init__(self):
        super().__init__()
        self.details = self.detail_class()

    def parse_payload(self, payload: bytes):
        try:
            self.details = jsonpickle.decode(payload.decode())
        except TypeError as e:
            logging.warning(f"Could not parse event: {e}")
            self.details = self.detail_class()

    def serialize_payload(self) -> bytes:
        # TODO: See whether we can introspect the details members and
        #       automatically convert datetime attributes to naive utc
        return jsonpickle.encode(self.details).encode()
