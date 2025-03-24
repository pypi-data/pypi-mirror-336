from keven_core.kafka.abstracts.command_handler import CommandHandler
from keven_core.kafka.commands.runner import CommandRunner
from keven_core.kafka.abstracts.message_server import MessageReceiverServer


class CommandReceiverServer(MessageReceiverServer):
    """
    Server which receives commands.  The io_server provides the messages via a
    runner which this server assigns to the io_server.

    Example:

    io_server =  KafkaConsumerServer(
            topics=["keven_commands"], client_id="services_command_client"
        )

    cmd_server = CommandReceiverServer(
        command_names = [ CommandNames.TEST ],
        io_server=io_server
    )

    cmd_server.run_server()

    """

    def __init__(
        self,
        io_server=None,
        command_names=None,
        command_handler=CommandHandler.handle_commands,
    ):
        runner = CommandRunner(
            command_names=command_names, command_handler=command_handler
        )
        super().__init__(runner, io_server=io_server)


class AllCommandsReceiverServer(MessageReceiverServer):
    def __init__(
        self,
        io_server=None,
        command_handler=CommandHandler.handle_all_commands,
    ):
        runner = CommandRunner(
            command_handler=command_handler, all_commands=True
        )
        super().__init__(runner, io_server=io_server)
