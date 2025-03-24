
from keven_core.kafka.events.runner import EventRunner
from keven_core.kafka.abstracts.message_server import MessageReceiverServer

def get_evt_handler_class():
    from keven_core.kafka.abstracts.event_handler import EventHandler
    return EventHandler

class EventReceiverServer(MessageReceiverServer):
    """
    Server which receives events.  The io_server provides the messages via a
    runner which this server assigns to the io_server.

    kafka_io_server = KafkaConsumerServer(
            topics=["keven_events"], client_id="services_event_client"
        )

    event_receiver = EventReceiverServer(
            event_names=[EventNames.ARTIFACT_UPLOAD],
            io_server=kafka_io_server,
    )

    event_receiver.run_server()
    """

    def __init__(
        self,
        io_server=None,
        event_names=None,
        event_handler=get_evt_handler_class().handle_events,
    ):
        runner = EventRunner(
            event_names=event_names, event_handler=event_handler
        )
        super().__init__(runner, io_server=io_server)


class AllEventsReceiverServer(MessageReceiverServer):
    def __init__(
        self, io_server=None, event_handler=get_evt_handler_class().handle_all_events
    ):
        runner = EventRunner(event_handler=event_handler, all_events=True)
        super().__init__(runner, io_server=io_server)
