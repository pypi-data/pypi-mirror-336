from keven_core.kafka.abstracts.metaclass.base_handler_meta import BaseHandlerMeta
from keven_core.kafka.abstracts.command_handler import CommandHandler
from keven_core.kafka.commands.command import Command, CommandNames


# Create a dummy command class for testing.
class DummyCommand(Command):
    command_name = CommandNames.PRINT_COMMAND
    # def get_event_name(self, phase, old_name=True):
    #     # For testing, return the PRINT_EVENT for any phase.
    #     from keven_core.kafka.events.event import EventNames
    #     return EventNames.PRINT_EVENT

    def parse_command(self):
        pass

    def serialize_command(self):
        return b""

    def parse_payload(self, payload: bytes):
        pass


# Dummy command handler that processes the command.
class DummyCommandHandler(CommandHandler):
    command_name = CommandNames.PRINT_COMMAND

    def handle_command(self, command: Command) -> None:
        self.processed = True

def test_command_handler_registration():
    registry = BaseHandlerMeta.get_command_registry()
    assert CommandNames.PRINT_COMMAND in registry, "PRINT_COMMAND should be in the registry."
    assert DummyCommandHandler in registry[CommandNames.PRINT_COMMAND], "DummyCommandHandler should be registered for PRINT_COMMAND."

# def test_command_handler_execution(monkeypatch):
#     dummy_command = DummyCommand()
#     pre_called = False
#     post_called = False
#
#     def pre_hook():
#         nonlocal pre_called
#         pre_called = True
#
#     def post_hook():
#         nonlocal post_called
#         post_called = True
#
#     CommandHandler.register_pre_handler_hook(pre_hook)
#     CommandHandler.register_post_handler_hook(post_hook)
#
#     # Execute the handler using the protocol.
#     result_handler = CommandHandler.execute_handler(dummy_command, DummyCommandHandler)
#     assert hasattr(result_handler, "processed"), "Handler should have processed the command."
#     assert pre_called, "Pre-handler hook should be executed."
#     assert post_called, "Post-handler hook should be executed."
#
# def test_command_handler_error(monkeypatch):
#     # Define a command handler that raises an exception.
#     class ErrorCommandHandler(CommandHandler):
#         command_name = CommandNames.PRINT_COMMAND
#         def handle_command(self, command: Command) -> None:
#             raise ValueError("Test error")
#
#     dummy_command = DummyCommand()
#
#     logged = False
#     def fake_exception_handler(e: Exception):
#         nonlocal logged
#         logged = True
#
#     ErrorCommandHandler.capture_exception_handler = fake_exception_handler
#
#     handler = CommandHandler.execute_handler(dummy_command, ErrorCommandHandler)
#     assert logged, "Exception handler should be called on error."
#     errored_event = handler.error_event(get_old_event=False)
#     assert "Test error" in errored_event.error_message, "Error event should contain the exception message."
from keven_core.kafka.commands import CommandPublisher, start_command_receiver_server, CommandRunner, CommandNames, Command
from keven_core.kafka.abstracts import CommandHandler, CommandReceiverServer
from keven_core.kafka.commands.test.test import TestCommand
from grpc_registry_protos.kafka import commands_and_events_pb2 as pb
from keven_core.kafka.events.event import EventNames
import pytest


@pytest.fixture
def basic_command():
    source_command = Command.from_name(CommandNames.TEST)
    source_command.originator = "unit_test"
    source_command.test_data = "Hello World!"
    return source_command


def test_new_command():
    """
    Test that we can construct a command using the "factory"
    """
    command = Command.from_name(CommandNames.TEST)
    assert isinstance(command, TestCommand)


def test_serialize_command(basic_command):
    proto = basic_command.serialize()
    assert proto.name == CommandNames.TEST.value
    assert proto.originator == "unit_test"
    assert proto.created.seconds != 0
    assert proto.payload == b"\n\x0cHello World!"


def test_parse_command(basic_command):
    proto = basic_command.serialize()

    dest_command = Command.from_protobuf(proto)
    assert dest_command.command_name == CommandNames.TEST
    assert dest_command.originator == "unit_test"
    assert dest_command.created == basic_command.created
    assert dest_command.test_data == "Hello World!"


def test_parse_command_from_bytes(basic_command):
    proto = basic_command.serialize()
    data = proto.SerializeToString()

    dest_command = Command.from_bytes(data)
    assert dest_command.command_name == CommandNames.TEST
    assert dest_command.originator == "unit_test"
    assert dest_command.created == basic_command.created
    assert dest_command.test_data == "Hello World!"


def test_runner(basic_command):
    """
    This tests the event runner.  We make sure that events that are listened
    for are parsed and returned to the handler.
    """

    def handler(command):
        assert command.command_name == CommandNames.TEST
        assert command.originator == "unit_test"
        assert command.created == basic_command.created
        assert command.test_data == "Hello World!"

    runner = CommandRunner(
        command_names={CommandNames.TEST}, command_handler=handler
    )
    runner.run(basic_command.serialize().SerializeToString())


def test_publisher(basic_command):
    """
    Basic sanity check of the publisher
    """

    class MyLogger(object):
        def __init__(self):
            self.messages = list()

        def log(self, data: bytes, topic: str=""):
            self.messages.append(data)

    logger = MyLogger()
    publisher = CommandPublisher(logger)
    publisher.dispatch_command(basic_command)
    raw_event = pb.Command()
    raw_event.ParseFromString(logger.messages[0])

    command = Command.from_protobuf(raw_event)

    assert command.command_name == basic_command.command_name
    assert command.test_data == basic_command.test_data


def test_command_receiver_server():
    """
        Tests that our code calls the Kafka producer as expected.

        Note:
            This test uses a fake/dummy broker address ("keven-kafka:9092") so you
            may see warning messages like "Failed to resolve 'keven-kafka:9092'...".
            These can be ignored for this unit test since we're only verifying that
            our code attempts to produce messages, not actual broker connectivity.
            Actual integration tests will be run against a real Kafka broker.
        """
    class MockIOServer(object):
        def __init__(self, name, runner=None):
            self.runner = runner
            self.client_id = name

        def add_runner(self, runner):
            self.runner = runner

        async def run_server(self):
            test_command = Command.from_name(CommandNames.TEST)
            test_command.test_data = "Hello!"
            self.runner.run(test_command.serialize().SerializeToString())
            return

    class TestHandleTestCommand(CommandHandler):
        command_name = CommandNames.TEST
        handler_called_count = 0

        def handle_command(self, command):
            assert command.command_name == CommandNames.TEST
            self.__class__.handler_called_count += 1

    server = CommandReceiverServer(
        io_server=MockIOServer("test"), command_names=[CommandNames.TEST]
    )
    server.start_sync()

    assert TestHandleTestCommand.handler_called_count == 1


def test_command_receiver_server2():
    """
            Tests that our code calls the Kafka producer as expected.

            Note:
                This test uses a fake/dummy broker address ("keven-kafka:9092") so you
                may see warning messages like "Failed to resolve 'keven-kafka:9092'...".
                These can be ignored for this unit test since we're only verifying that
                our code attempts to produce messages, not actual broker connectivity.
                Actual integration tests will be run against a real Kafka broker.
            """
    class MockIOServer(object):
        def __init__(self, name, runner=None):
            self.runner = runner
            self.client_id = name

        def add_runner(self, runner):
            self.runner = runner

        async def run_server(self):
            test_command = Command.from_name(CommandNames.TEST)
            test_command.test_data = "Hello!"
            self.runner.run(test_command.serialize().SerializeToString())

    class TestHandleTestCommand(CommandHandler):
        command_name = CommandNames.TEST
        handler_called_count = 0

        def handle_command(self, command):
            assert command.command_name == CommandNames.TEST
            TestHandleTestCommand.handler_called_count += 1
            assert self.start_event().event_name == EventNames.CMD_TEST_STARTED

    server = start_command_receiver_server("unit_test", io_server=MockIOServer("utest"), auto_start=False)
    server.start_sync()

    assert TestHandleTestCommand.handler_called_count == 1

