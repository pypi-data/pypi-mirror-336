from multiprocessing import Process
from typing import Optional, List

from keven_core.kafka.abstracts.consumer_server import KafkaConsumerServer


def start_events_receiver_server(
        server_name: str,
        io_server: Optional[object] = None,
        auto_reprocess_errors: bool = False
) -> None:
    """
    Convenient entry point for receiving events in your application.

    This function sets up the appropriate topics based on registered event handlers,
    configures an event receiver, and starts the event processing loop synchronously.

    Args:
        server_name (str): Identifier for the server instance.
        io_server (object, optional): Custom I/O server instance. If not provided, a default KafkaConsumerServer is created.
        auto_reprocess_errors (bool): Whether to enable automatic reprocessing of error messages.
    """
    from keven_core.kafka.abstracts.event_handler import EventHandler
    # Build topics list: start with a base topic, then add specific event topics
    topics: List[str] = ["keven_events"]
    for event in EventHandler.events_with_handlers():
        topics.append(f"keven_events_{event}")

    # Set up the event listener using the provided or default I/O server
    event_receiver = setup_event_listener(
        auto_reprocess_errors=auto_reprocess_errors,
        io_server=io_server,
        server_name=server_name,
        topics=topics,
    )

    # Use the synchronous wrapper to run the event server
    event_receiver.start_sync()


def setup_event_listener(
        auto_reprocess_errors: bool,
        io_server: Optional[object],
        server_name: str,
        timeout: Optional[int] = None,
        reraise_exceptions: bool = False,
        log_exceptions: bool = True,
        topics: Optional[List[str]] = None,
) -> "EventReceiverServer":
    """
    Configures and returns an EventReceiverServer for processing events.

    If no I/O server is provided, a KafkaConsumerServer is instantiated with default settings.
    Also, collects event names from both the auto-registered handler registry and the function registry.

    Args:
        auto_reprocess_errors (bool): Whether to enable auto-reprocessing of errors.
        io_server (object, optional): An I/O server instance (e.g., KafkaConsumerServer). If None, a default instance is created.
        server_name (str): Identifier for the server instance.
        timeout (int, optional): Timeout for consumption.
        reraise_exceptions (bool): Whether to reraise exceptions after logging.
        log_exceptions (bool): Whether to log exceptions.
        topics (List[str], optional): List of Kafka topics to subscribe to.

    Returns:
        EventReceiverServer: Configured event receiver.
    """
    from keven_core.kafka.abstracts.event_handler import EventHandler
    from keven_core.kafka.abstracts.eventreceiver_server import EventReceiverServer
    if not io_server:
        io_server = KafkaConsumerServer(
            topics=topics or ["keven_events", "keven_events.audit"],
            client_id=server_name,
            group_id=server_name,
            auto_reprocess_errors=auto_reprocess_errors,
            timeout=timeout,
            reraise_exceptions=reraise_exceptions,
            log_exceptions=log_exceptions,
        )

    # Retrieve event names from the auto-registered registry.
    # Use the public method 'events_with_handlers' instead of accessing _registry directly.
    event_names = list(EventHandler.events_with_handlers())
    # Also include any event names from the function registry.
    if hasattr(EventHandler, "_func_registry"):
        event_names.extend(list(EventHandler._func_registry.keys()))

    # Instantiate the EventReceiverServer with the collected event names.
    event_receiver = EventReceiverServer(
        event_names=event_names,
        io_server=io_server,
    )

    return event_receiver


def start_events_receiver_process(server_name: str, io_server: Optional[object] = None) -> Process:
    """
    Starts an event handler server as a separate process.

    Args:
        server_name (str): Name of the I/O server consumer.
        io_server (object, optional): Custom I/O server instance; if not provided, a default KafkaConsumerServer is used.

    Returns:
        Process: A multiprocessing.Process instance running the event receiver server.
                 Use process.join() to wait for it to exit.
    """
    event_proc = Process(
        target=start_events_receiver_server,
        args=[server_name],
        kwargs={"io_server": io_server},
    )
    event_proc.start()
    return event_proc


def start_all_events_receiver_server(
        server_name: str,
        io_server: Optional[object] = None,
        include_audit: bool = False
) -> None:
    """
    Convenient entry point to start a server that receives all events.

    This variant subscribes to all topics matching the pattern and optionally includes audit topics.

    Args:
        server_name (str): Identifier for the server instance.
        io_server (object, optional): Custom I/O server instance.
        include_audit (bool): Whether to include audit events.
    """
    from keven_core.kafka.abstracts.eventreceiver_server import AllEventsReceiverServer
    if not io_server:
        topics: List[str] = ["keven_events", "^keven_events_.*"]
        if include_audit:
            topics.append("keven_events.audit")
        io_server = KafkaConsumerServer(
            topics=topics,
            client_id=server_name,
            group_id=server_name
        )

    event_receiver = AllEventsReceiverServer(io_server=io_server)
    event_receiver.start_sync()
