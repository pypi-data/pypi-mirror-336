from keven_core.kafka.commands.command import Command, CommandNames
from keven_core.kafka.abstracts.consumer_server import Runner
from grpc_registry_protos.kafka import commands_and_events_pb2 as pb

import logging


class CommandRunner(Runner):
    def __init__(
        self,
        command_names: set = None,
        command_handler=None,
        all_commands=False,
    ):
        """
        Set the events names you want to listen for and pass in the callback
        which will handle the events as they are received.
        """
        self.command_names = command_names or set()
        self.command_handler = command_handler
        self.all_commands = all_commands

    def run(self, message):
        """
        Handle the message. This is called by the EventServer.
        """

        pb_command = pb.Command()
        pb_command.ParseFromString(message)
        logging.debug(f" ⚪ Command⚪ {pb_command.name}")
        command = Command.from_protobuf(pb_command)
        if command.command_name is CommandNames.NOT_INSTALLED:
            return
        self.command_handler(command)
