import copy
import inspect
import logging
from datetime import datetime, timezone
from typing import Optional


class MessagePublisher:
    """
    MessagePublisher enables structured logging of messages to Kafka topics,
    automatically augmenting each message with metadata such as the originating
    function and timestamp.

    It ensures message integrity by preventing external modification once logged.

    Usage:
        - Subclass or instantiate directly and invoke `log_message` to publish messages.
        - The Kafka publishing logic should be implemented in subclasses inheriting this base class.


    # Assume KafkaLogger class is implemented elsewhere and imported.
    from kafka_logger import KafkaLogger

    # Assume MyProtoMessage is a protobuf-generated message class with appropriate fields.
    from grpc_registry_protos.kafka.commands_and_events_pb2 import Event

    # Initialize your KafkaLogger
    kafka_logger = KafkaLogger(kafka_address="localhost:9092", topic="events")

    # Initialize MessagePublisher with the KafkaLogger instance
    publisher = MessagePublisher(kafka_logger)

    # Create a message instance (assuming your proto message structure)
    event_message = Event(
        name="example_event",
        payload=b"Example payload data",
        uuid="12345-67890",
        namespace="example_namespace",
    )

    # Publish the message
    publisher.log_message(event_message, topic="my_topic")
    """

    def __init__(self, publisher):
        """
        Initializes the MessagePublisher with a specified message publisher backend.

        Args:
            publisher: An object capable of publishing messages (e.g., KafkaLogger).
                       Must have a callable `log(data: bytes, topic: Optional[str])` method.
        """
        self.publisher = publisher

    def log_message(self, message, topic: Optional[str] = None) -> None:
        """
        Publishes a message after augmenting it with origin metadata.

        Args:
            message: The message object to be logged. Expected to implement
                     attributes: `originator`, `created`, `_is_internal`.
            topic (Optional[str]): Kafka topic to publish the message to. Defaults
                                   to the topic configured in the publisher backend.

        Raises:
            ValueError: If the provided message is None or invalid.
        """
        if message is None:
            logging.error("MessagePublisher.log_message called with None message.")
            raise ValueError("Cannot log None as a message.")

        prepared_message = self._prepare_message(message).serialize()
        serialized_message = self.serialize_message(prepared_message)

        self.publisher.log(serialized_message, topic)
        logging.info(f"Message published to topic '{topic}' by '{prepared_message.originator}'")

    def _prepare_message(self, message):
        """
        Prepares a deep copy of the message to prevent modification of the original message,
        automatically setting the originator function and creation timestamp.

        Args:
            message: Original message object to prepare.

        Returns:
            A deep copy of the message object with additional metadata set.
        """
        if message._is_internal:
            return message

        send_message = copy.deepcopy(message)
        caller_function = inspect.stack()[2].function
        send_message.originator = caller_function
        send_message.created = datetime.now(timezone.utc)
        send_message._is_internal = True

        return send_message

    def get_deep_copy(self, message):
        return self._prepare_message(message)

    @staticmethod
    def serialize_message(message) -> bytes:
        """
        Serializes the message into bytes. Override this method if the serialization
        logic differs from calling `.SerializeToString()`.

        Args:
            message: The message object to serialize.

        Returns:
            bytes: Serialized byte representation of the message.
        """
        return message.SerializeToString()
