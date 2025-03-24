from keven_core.kafka.abstracts.metaclass.base_handler_meta import BaseHandlerMeta
from keven_core.kafka.abstracts.event_handler import EventHandler
from keven_core.kafka.events.event import EventNames

# Dummy event handler for testing auto-registration and execution.
class DummyEventHandler(EventHandler):
    event_name = EventNames.PRINT_EVENT

    def handle_event(self, event: object) -> None:
        self.received_event = event

def test_event_handler_registration():
    # Verify that DummyEventHandler is automatically registered.
    registry = BaseHandlerMeta.get_event_registry()
    assert EventNames.PRINT_EVENT in registry, "PRINT_EVENT should be in the registry."
    assert DummyEventHandler in registry[EventNames.PRINT_EVENT], "DummyEventHandler should be registered for PRINT_EVENT."

def test_event_handler_hooks(monkeypatch):
    # Test that pre- and post-handler hooks execute in order.
    pre_called = False
    post_called = False

    def pre_hook():
        nonlocal pre_called
        pre_called = True

    def post_hook():
        nonlocal post_called
        post_called = True

    # Register hooks using the class methods.
    EventHandler.register_pre_handler_hook(pre_hook)
    EventHandler.register_post_handler_hook(post_hook)
    EventHandler.execute_pre_handler_hooks()
    EventHandler.execute_post_handler_hooks()

    assert pre_called, "Pre-handler hook should have been called."
    assert post_called, "Post-handler hook should have been called."

def test_event_handler_execution(monkeypatch):
    # Create a dummy event with minimal attributes.
    class DummyEvent:
        pass

    dummy_event = DummyEvent()

    # Create a fake event object with the required 'event_name' and 'value' method.
    FakeEvent = type(
        "FakeEvent",
        (),
        {"event_name": EventNames.PRINT_EVENT, "value": lambda self: dummy_event}
    )
    fake_event_instance = FakeEvent()
    # Execute handlers for the fake event. This test mainly verifies that no exceptions occur.
    EventHandler.handle_events(fake_event_instance)
