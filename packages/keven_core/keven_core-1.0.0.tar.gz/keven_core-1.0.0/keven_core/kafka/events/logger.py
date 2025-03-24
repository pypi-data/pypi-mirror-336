import threading
import logging

from keven_core.kafka.events.publisher import EventPublisher
from keven_core.kafka.logger import KafkaLogger

"""

# Example Usage:

from keven_core.kafka.events.event import Event

# Initialize a publisher explicitly (optional)
logger = KafkaLogger(topic="keven_events", timeout=30)
publisher = EventPublisher(logger=logger)
keven_set_publisher(publisher)

# Log events immediately
event1 = Event(name="example_event_1")
keven_log_event(event1)

# Enable event caching mode
keven_send_events_on_commit()

event2 = Event(name="example_event_2")
event3 = Event(name="example_event_3")

# These events will be cached
keven_log_event(event2)
keven_log_event(event3)

# Explicitly flush cached events
keven_flush_event_cache()

# Disable caching to revert to immediate event publishing
keven_dont_send_events_on_commit()
"""

# Thread-local publisher instances and event caching management
__event_publishers = dict()
__send_events_on_commit = False
__event_write_cache = dict()
__event_lock = threading.Lock()


def keven_send_events_on_commit():
    """Activate event caching. Events will be sent upon explicit flush."""
    global __send_events_on_commit
    __send_events_on_commit = True


def keven_dont_send_events_on_commit():
    """Deactivate event caching. Events will be sent immediately upon logging."""
    global __send_events_on_commit
    __send_events_on_commit = False


def keven_clear_event_publishers():
    """Clear all cached thread-specific EventPublisher instances."""
    global __event_publishers
    with __event_lock:
        __event_publishers.clear()


def keven_last_publisher():
    """
    Retrieve or create the EventPublisher instance for the current thread.

    Returns:
        EventPublisher: Thread-specific Kafka event publisher.
    """
    ident = threading.current_thread().ident
    with __event_lock:
        pub = __event_publishers.get(ident)
        if not pub:
            logger = KafkaLogger(topic="keven_events", timeout=30)
            pub = EventPublisher(logger)
            __event_publishers[ident] = pub

    logging.info(f"⇔ Event Publisher: {pub} (thread ident: '{ident}')")
    return pub


def keven_set_publisher(publisher):
    """
    Explicitly set the EventPublisher instance for the current thread.

    Args:
        publisher (EventPublisher): The event publisher to assign.
    """
    ident = threading.current_thread().ident
    with __event_lock:
        __event_publishers[ident] = publisher


def keven_get_write_cache():
    """
    Retrieve or initialize the event cache list for the current thread.

    Returns:
        list: Thread-specific cached event list.
    """
    ident = threading.current_thread().ident
    with __event_lock:
        cache = __event_write_cache.get(ident)
        if cache is None:
            cache = []
            __event_write_cache[ident] = cache

    return cache


def keven_log_event(event):
    """
    Log an event according to the current commit mode.

    If caching is active, the event will be cached and sent upon flush.
    If caching is inactive, the event will be immediately published.

    Args:
        event: Event instance to be logged.
    """
    global __send_events_on_commit
    if __send_events_on_commit:
        keven_get_write_cache().append(event)
    else:
        __keven_log_event_now(event)


def keven_log_event_now(event):
    """
    Immediately log the event, bypassing the caching mechanism.

    Args:
        event: Event instance to be logged immediately.
    """
    __keven_log_event_now(event)


def __keven_log_event_now(event):
    """
    Internal helper to publish an event immediately.

    Args:
        event: Event instance to be published.
    """
    if not event.is_audit_event:
        topic = event.event_name.value.lower()
        keven_last_publisher().log_event(event, topic=f"keven_events_{topic}")
    # Uncomment and adjust if audit events are handled separately:
    # else:
    #     keven_last_publisher().log_event(event, topic="keven_events.audit")


def keven_flush_event_cache():
    """Flush all cached events by publishing them immediately."""
    cache = keven_get_write_cache()
    for event in cache:
        __keven_log_event_now(event)
    cache.clear()
