from typing import Optional
import asyncio


class MessageReceiverServer:
    """
    A server that manages receiving messages/events using an associated runner
    through a provided I/O server interface.

    This class acts as a simple orchestrator between an I/O server, which handles
    the lower-level message reception logic (such as Kafka or another message broker),
    and a "runner," which processes each received message.

    Example Usage:

        from my_io_server import KafkaConsumerServer
        from my_runner import PrintRunner

        # Create the runner instance that will process received messages.
        runner = PrintRunner()

        # Initialize IO server (KafkaConsumerServer or similar).
        io_server = KafkaConsumerServer(topics=["keven_events"], group_id="keven_group")

        # Initialize the receiver server with the runner and IO server.
        receiver_server = MessageReceiverServer(runner, io_server)

        # Alternatively, assign IO server after initialization:
        # receiver_server.assign_io_server(io_server)

        # To start processing asynchronously:
        await receiver_server.start()

        # Or, to start processing synchronously:
        receiver_server.start_sync()
    """

    def __init__(self, runner, io_server: Optional[object] = None) -> None:
        """
        Initializes the MessageReceiverServer with a message processing runner
        and an optional IO server.

        Args:
            runner (object):
                A message processor implementing the required logic for
                handling messages received from the I/O server.
            io_server (Optional[object]):
                An IO server instance responsible for receiving messages from an external
                source (e.g., KafkaConsumerServer). If None, it should be assigned later.
        """
        self.io_server = io_server
        self.runner = runner

        if self.io_server:
            self.io_server.add_runner(self.runner)

    def assign_io_server(self, io_server: object) -> None:
        """
        Assigns an IO server to this receiver after initialization.

        Args:
            io_server (object):
                The IO server instance responsible for fetching or polling
                messages to be processed by the runner.
        """
        self.io_server = io_server
        self.io_server.add_runner(self.runner)

    async def start(self) -> None:
        """
        Asynchronously starts the message receiver server, initiating the event/message
        listening and processing loop.

        Raises:
            ValueError: If the IO server is not assigned before starting.
        """
        if not self.io_server:
            raise ValueError("IO server must be assigned before starting the receiver server.")

        await self.io_server.run_server()

    def start_sync(self) -> None:
        """
        Synchronous wrapper for starting the message receiver server.

        This method runs the asynchronous start() method within an event loop,
        blocking until message processing completes.
        """
        asyncio.run(self.start())
