import logging

from grpc_registry_protos.kafka.commands_and_events_pb2 import Event
from keven_core.kafka.abstracts.consumer_server import Runner
from keven_core.kafka.events.event import Event


class EventRunner(Runner):
    def __init__(
        self, event_names: set = None, event_handler=None, all_events=False
    ):
        """
        Set the events names you want to listen for and pass in the callback
        which will handle the events as they are received.
        Setting all_events to True handles everything (used in GCD)
        """
        self.event_names = event_names or set()
        self.event_handler = event_handler
        self.all_events = all_events

    def run(self, message):
        """
        Handle the message. This is called by the EventServer.
        """

        pb_event = Event()
        pb_event.ParseFromString(message)

        logging.debug(f" ⚫ Event  ⚫ {pb_event.name}")
        event = Event.from_protobuf(pb_event)
        self.event_handler(event)
