import warnings

from keven_core.kafka.commands.command import Command
from keven_core.kafka.abstracts.message_publisher import MessagePublisher


class CommandPublisher(MessagePublisher):
    """
    Class to enable you to publish commands to.
    To instantiate the command do (replace TEST with your command):
    Then populate the event data

    command = Command.from_name(CommandNames.TEST)
    ... populate here

    pub = CommandPublisher(logger)
    pub.log_command(my_command: Command)

    """

    def dispatch_command(self, command: Command):
        """
        Logs the event to Publisher.  Serialized as a protobuf. Note that
        originator is set here and created to prevent forgeries :P or
        copy paste errors.
        """
        topic = command.command_name.value.lower()
        self.log_message(command, topic=f"keven_commands_{topic}")

    def synchronous_command(self, command):
        warnings.warn(f"{__name__} has not been implemented yet")
        pass
