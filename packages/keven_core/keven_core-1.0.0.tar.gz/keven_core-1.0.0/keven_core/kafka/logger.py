import logging
import os
from confluent_kafka import Producer, SerializingProducer
from collections import deque

from keven_core.logging import Logger, init_logging


class KafkaLogger(Logger):
    """
    Kafka-based logger for single-message logging.

    This logger sends individual log messages to a Kafka topic using a SerializingProducer.
    Each message is immediately flushed to ensure delivery within the specified timeout.
    """

    def __init__(self, kafka_address="keven-kafka:9092", topic=None, timeout=30):
        """
        Initializes the KafkaLogger.

        Args:
            kafka_address (str): Address of the Kafka broker (default: "keven-kafka:9092").
                                 This can be overridden by the 'KAFKA' environment variable.
            topic (str): Default Kafka topic to which messages will be logged.
            timeout (int): Timeout in seconds for flushing the producer.
        """
        # Initialize logging configuration
        init_logging()
        # Allow environment variable to override the default Kafka address
        kafka_address = os.getenv("KAFKA", kafka_address)

        logging.debug(f"↳ KafkaLogger initialized with broker {kafka_address} and topic '{topic}'")
        # Create a SerializingProducer for sending messages to Kafka
        self.producer = SerializingProducer({"bootstrap.servers": kafka_address})
        self.topic = topic
        self.timeout = timeout

    def log(self, data: bytes, topic=None) -> None:
        """
        Logs a single message to a Kafka topic.

        Produces a message containing the given data and flushes the producer to ensure immediate delivery.

        Args:
            data (bytes): The log message data as bytes.
            topic (str, optional): Kafka topic to which the message should be logged.
                                   If not provided, the default topic is used.
        """
        if topic is None:
            topic = self.topic

        logging.info(f"⇒ Logging {len(data)} bytes to Kafka Topic: {topic}")

        # Produce the message asynchronously with a callback for delivery reporting
        self.producer.produce(topic, value=data, on_delivery=self.delivery_report)
        # Flush the producer to ensure the message is delivered within the timeout period
        self.producer.flush(self.timeout)

        logging.info("⇐ Message Logged to Kafka")

    def delivery_report(self, err, msg):
        """
        Callback function for Kafka message delivery.

        Logs an error if the delivery fails or a debug message if successful.

        Args:
            err: An error object if delivery failed, otherwise None.
            msg: The Kafka message object.
        """
        if err:
            logging.error(f"Kafka delivery failure: {err}")
        else:
            logging.debug(f"Kafka message delivered: {msg.topic()} [{msg.partition()}]")


class KafkaBatchLogger(Logger):
    """
    Kafka-based logger for batch message logging.

    This logger collects messages in a queue and sends them in a batch when flush() is called.
    It uses a standard Producer and tracks both produced and delivered message counts.
    """

    def __init__(self, kafka_address="keven-kafka:9092", topic=None, timeout=30):
        """
        Initializes the KafkaBatchLogger.

        Args:
            kafka_address (str): Address of the Kafka broker (default: "keven-kafka:9092").
                                 This can be overridden by the 'KAFKA' environment variable.
            topic (str): Kafka topic to which batch messages will be logged.
            timeout (int): Timeout in seconds for flushing the producer.
        """
        init_logging()
        # Allow environment variable to override the default Kafka address
        kafka_address = os.getenv("KAFKA", kafka_address)

        # Create a Producer for batch processing
        self.producer = Producer({"bootstrap.servers": kafka_address})
        self.topic = topic
        # Use a deque for efficient FIFO queue management of messages
        self.queue = deque()
        self.timeout = timeout
        # Counters for tracking message production and successful delivery
        self.produced_count = 0
        self.received_count = 0

    def log(self, data: bytes) -> None:
        """
        Adds a message to the batch queue.

        Args:
            data (bytes): The log message data as bytes.
        """
        self.queue.append(data)

    def flush(self) -> None:
        """
        Sends all queued messages to Kafka and flushes the producer.

        Produces each message in the queue with a delivery callback, flushes the producer,
        and logs the counts of produced and delivered messages. If the counts do not match,
        an error is logged.
        """
        self.produced_count = 0
        self.received_count = 0

        # Produce each queued message with a delivery callback
        while self.queue:
            data = self.queue.popleft()
            self.producer.produce(self.topic, data, on_delivery=self.delivery_report)
            self.produced_count += 1

        # Flush the producer to ensure all messages are sent within the timeout period
        self.producer.flush(self.timeout)

        msg = f"Produced: {self.produced_count}, Received: {self.received_count}"
        if self.produced_count == self.received_count:
            logging.info(msg)
        else:
            logging.error(msg)

    def delivery_report(self, err, msg):
        """
        Callback function for Kafka batch message delivery.

        Increments the received message count on successful delivery, or logs an error if delivery fails.

        Args:
            err: An error object if delivery failed, otherwise None.
            msg: The Kafka message object.
        """
        if err:
            logging.error(f"Kafka delivery failure: {err}")
        else:
            self.received_count += 1
            logging.debug(f"Kafka batch message delivered: {msg.topic()} [{msg.partition()}]")
