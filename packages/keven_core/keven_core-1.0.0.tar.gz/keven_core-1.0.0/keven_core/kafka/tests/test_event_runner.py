from keven_core.kafka.events.runner import EventRunner
from keven_core.kafka.events.event import Event
from grpc_registry_protos.kafka.commands_and_events_pb2 import Event as pbEvent


# Dummy event handler function.
def dummy_event_handler(event):
    dummy_event_handler.called = True
    dummy_event_handler.event = event

dummy_event_handler.called = False
dummy_event_handler.event = None

def test_event_runner_parsing(monkeypatch):
    # Monkey-patch Event.from_protobuf to return a dummy event.
    dummy_event = pbEvent(name="dummy")
    dummy_message = dummy_event.SerializeToString()
    monkeypatch.setattr(Event, "from_protobuf", lambda pb: dummy_event)

    runner = EventRunner(event_names={"dummy"}, event_handler=dummy_event_handler)
    #dummy_message = b"dummy protobuf data"
    runner.run(dummy_message)

    assert dummy_event_handler.called, "The event handler function should have been called."
    assert dummy_event_handler.event == dummy_event, "The parsed event should match the dummy event."
