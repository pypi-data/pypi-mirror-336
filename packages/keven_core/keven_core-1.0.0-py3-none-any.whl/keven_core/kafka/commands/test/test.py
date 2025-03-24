from keven_core.kafka.commands import Command, CommandNames, PickledCommand
from keven_core.kafka.commands.test import test_command_pb2 as pb


class TestCommand(Command):
    """
    This is for testing event payloads
    """

    command_name = CommandNames.TEST

    def __init__(self):
        super().__init__()
        self.test_data = ""

    def parse_payload(self, payload: bytes):
        proto = pb.TestCommand()
        proto.ParseFromString(payload)
        self.test_data = proto.test_data

    def serialize_payload(self) -> bytes:
        proto = pb.TestCommand()
        proto.test_data = self.test_data
        return proto.SerializeToString()


class TestPickledCommandDetails(object):
    def __init__(self):
        self.data = ""


class TestPickledCommand(PickledCommand):
    command_name = CommandNames.TEST_PICKLED_COMMAND
    detail_class = TestPickledCommandDetails
