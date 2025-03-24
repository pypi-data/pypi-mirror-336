import asyncio
import logging
import os
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import jsonpickle
from confluent_kafka import Consumer, KafkaError
from keven_core.kafka.logger import KafkaLogger


KAFKA_CONSUMER_BOOTSTRAP_SERVERS = "keven-kafka:9092"
KAFKA_CONSUMER_CLIENT_ID = "client-1"
KAFKA_CONSUMER_GROUP_ID = "default_group"
KAFKA_CONSUMER_PASS_TOPIC_PARAM = False
KAFKA_CONSUMER_AUTO_REPROCESS_ERRORS = False
KAFKA_CONSUMER_RETRY_INTERVAL = 30  # in seconds
KAFKA_CONSUMER_MAX_RETRIES = 3
KAFKA_CONSUMER_NO_COMMIT = False
KAFKA_CONSUMER_RERAISE_EXCEPTIONS = False
KAFKA_CONSUMER_LOG_EXCEPTIONS = True
KAFKA_CONSUMER_MAX_POLL_INTERVAL = 180  # in seconds
KAFKA_CONSUMER_SESSION_TIMEOUT = 6      # in seconds
KAFKA_CONSUMER_HEARTBEAT_INTERVAL = 2     # in seconds


class Runner(ABC):
    """
    Abstract base class for processing messages consumed from Kafka.

    Subclass this to implement custom message-handling logic.
    """

    @abstractmethod
    def run(self, message: Any, topic: Optional[str] = None) -> None:
        """
        Process the incoming Kafka message.

        Args:
            message: The message payload from Kafka.
            topic (str, optional): The Kafka topic from which the message was consumed.
        """
        pass


class PrintRunner(Runner):
    """
    Example Runner implementation that prints incoming messages.
    Useful for debugging or basic logging scenarios.
    """

    def run(self, message: Any, topic: Optional[str] = None) -> None:
        print(f"[{topic}] Message Received: {message}")


class KafkaConsumerServer:
    """
    Kafka consumer server supporting asynchronous message processing,
    retry mechanisms, and customizable error handling strategies.

    Messages are not auto-committed to ensure reliable processing.
    """

    def __init__(
        self,
        topics: Optional[List[str]] = None,
        bootstrap_servers: str = KAFKA_CONSUMER_BOOTSTRAP_SERVERS,
        client_id: str = KAFKA_CONSUMER_CLIENT_ID,
        group_id: str = KAFKA_CONSUMER_GROUP_ID,
        runners: Optional[List[Runner]] = None,
        pass_topic_param: bool = KAFKA_CONSUMER_PASS_TOPIC_PARAM,
        auto_reprocess_errors: bool = KAFKA_CONSUMER_AUTO_REPROCESS_ERRORS,
        retry_interval: int = KAFKA_CONSUMER_RETRY_INTERVAL,
        max_retries: int = KAFKA_CONSUMER_MAX_RETRIES,
        no_commit: bool = KAFKA_CONSUMER_NO_COMMIT,
        timeout: Optional[int] = None,
        reraise_exceptions: bool = KAFKA_CONSUMER_RERAISE_EXCEPTIONS,
        log_exceptions: bool = KAFKA_CONSUMER_LOG_EXCEPTIONS,
        max_poll_interval: int = KAFKA_CONSUMER_MAX_POLL_INTERVAL,
        session_timeout: int = KAFKA_CONSUMER_SESSION_TIMEOUT,
        heartbeat_interval: int = KAFKA_CONSUMER_HEARTBEAT_INTERVAL,
        retry_detail: Optional[Dict[str, Any]] = None,
        on_assign_topics: Optional[Any] = None,
    ):
        """
        Initializes the KafkaConsumerServer.

        Args:
            topics (List[str], optional): List of Kafka topics to subscribe to.
            bootstrap_servers (str): Kafka broker address.
                                     This can be overridden by the 'KAFKA' environment variable.
            client_id (str): Client identifier.
            group_id (str): Kafka consumer group ID.
            runners (List[Runner], optional): List of Runner instances to process messages.
            pass_topic_param (bool): Whether to pass the topic name to the runner.
            auto_reprocess_errors (bool): Enable automatic reprocessing of error messages.
            retry_interval (int): Default retry interval in seconds.
            max_retries (int): Maximum number of retries before sending to dead letter.
            no_commit (bool): If True, disable offset commits.
            timeout (int, optional): Timeout in seconds for stopping consumption.
            reraise_exceptions (bool): If True, re-raise exceptions after logging.
            log_exceptions (bool): If True, log exceptions during processing.
            max_poll_interval (int): Maximum poll interval in seconds.
            session_timeout (int): Session timeout in seconds.
            heartbeat_interval (int): Heartbeat interval in seconds.
            retry_detail (dict, optional): Dictionary containing retry configuration per topic.
            on_assign_topics: Optional callback for topic assignment.
        """
        self.topics: List[str] = topics or []
        self.bootstrap_servers: str = os.getenv("KAFKA", bootstrap_servers)
        self.group_id: str = group_id
        self.runners: List[Runner] = runners or []
        self.pass_topic_param: bool = pass_topic_param
        self.no_commit: bool = no_commit
        self.timeout: Optional[int] = timeout
        self.reraise_exceptions: bool = reraise_exceptions
        self.log_exceptions: bool = log_exceptions
        self.auto_reprocess_errors: bool = auto_reprocess_errors
        self.retry_interval: int = retry_interval
        self.max_retries: int = max_retries
        self.retry_detail: Dict[str, Any] = retry_detail or {}

        # Configure the Kafka consumer with timeouts converted to milliseconds.
        self.consumer: Consumer = Consumer(
            {
                "bootstrap.servers": self.bootstrap_servers,
                "group.id": self.group_id,
                "enable.auto.commit": False,
                "session.timeout.ms": session_timeout * 1000,
                "heartbeat.interval.ms": heartbeat_interval * 1000,
                "max.poll.interval.ms": max_poll_interval * 1000,
                "auto.offset.reset": "earliest",
            }
        )

        self.consumer.subscribe(self.topics, on_assign=on_assign_topics)

        self.terminated: bool = False
        self.retry_logger: Optional[KafkaLogger] = None
        self.dead_letter_logger: Optional[KafkaLogger] = None

        if self.auto_reprocess_errors:
            retry_topic = f"kafka_server.{client_id}.retry"
            dead_letter_topic = f"kafka_server.{client_id}.dead"
            self.retry_logger = KafkaLogger(topic=retry_topic)
            self.dead_letter_logger = KafkaLogger(topic=dead_letter_topic)

    def terminate(self) -> None:
        """
        Signals the server to gracefully terminate consumption.
        """
        self.terminated = True

    def add_runner(self, runner: Runner) -> None:
        """
        Adds a new Runner instance for processing messages.

        Args:
            runner (Runner): A Runner implementation to handle messages.
        """
        self.runners.append(runner)

    async def run_server(self) -> None:
        """
        Runs Kafka message consumption asynchronously.

        Launches both the main message consumer loop and, if enabled,
        the retry message consumer loop concurrently.
        """
        tasks = [self._run_message_server()]
        if self.auto_reprocess_errors:
            tasks.append(self._run_retry_server())
        await asyncio.gather(*tasks)

    async def _run_message_server(self) -> None:
        """
        Main asynchronous loop for consuming and processing Kafka messages.

        Polls for messages continuously, processes them using the registered runners,
        and commits offsets if processing succeeds.
        """
        last_message_time: datetime = datetime.now(timezone.utc)

        while not self.terminated:
            msg = self.consumer.poll(0.01)
            if msg is None:
                # If a timeout is specified and no message has been received within the timeout interval, stop.
                if self.timeout and (datetime.now(timezone.utc) - last_message_time).total_seconds() > self.timeout:
                    logging.debug("KafkaConsumerServer: Timeout reached, stopping consumption.")
                    break
                await asyncio.sleep(0.01)
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    logging.info(f"Reached end of partition for topic: {msg.topic()}")
                else:
                    logging.error(f"Kafka error: {msg.error().str()}")
                continue

            last_message_time = datetime.now(timezone.utc)
            self._process_message(msg)

        try:
            self.consumer.close()
        except Exception as e:
            logging.error(f"Error closing consumer: {e}")

    async def _run_retry_server(self) -> None:
        """
        Asynchronous loop for processing retried Kafka messages.

        Consumes messages from a dedicated retry topic, checks if the retry interval has passed,
        and reprocesses the message using the registered runners.
        """
        retry_consumer: Consumer = Consumer(self.consumer.config)
        retry_topic: str = self.retry_logger.topic  # type: ignore
        retry_consumer.subscribe([retry_topic])

        while not self.terminated:
            msg = retry_consumer.poll(0.01)
            if msg is None:
                await asyncio.sleep(0.01)
                continue

            if not msg.error():
                decoded = jsonpickle.decode(msg.value())
                # Ensure the decoded timestamp is timezone-aware; assume UTC if naive.
                msg_timestamp: datetime = decoded["timestamp"]
                if msg_timestamp.tzinfo is None:
                    msg_timestamp = msg_timestamp.replace(tzinfo=timezone.utc)

                elapsed_time = (datetime.now(timezone.utc) - msg_timestamp).total_seconds()
                # Allow per-topic retry intervals via retry_detail if provided.
                interval: int = self.retry_detail.get(decoded["topic"], {}).get("retry_interval", self.retry_interval)

                if elapsed_time < interval:
                    await asyncio.sleep(interval - elapsed_time)

                self._reprocess_message(decoded, msg, retry_consumer)
            else:
                logging.error(f"Retry Kafka error: {msg.error().str()}")

        try:
            retry_consumer.close()
        except Exception as e:
            logging.error(f"Error closing retry consumer: {e}")

    def _process_message(self, msg: Any) -> None:
        """
        Processes a single Kafka message using the registered runners and commits the offset.

        In case of processing errors, logs the error and, if enabled, sends the message to a retry topic.
        """
        try:
            for runner in self.runners:
                if self.pass_topic_param:
                    runner.run(msg.value(), topic=msg.topic())
                else:
                    runner.run(msg.value())

            if not self.no_commit:
                try:
                    self.consumer.commit(msg)
                except Exception as commit_err:
                    logging.error(f"Commit error for message at offset {msg.offset()} in topic {msg.topic()}: {commit_err}")
        except Exception as e:
            logging.error(
                f"Exception processing message: offset {msg.offset()}, topic {msg.topic()}, error: {e}"
            )

            if self.reraise_exceptions:
                raise e

            if self.auto_reprocess_errors:
                error_payload = jsonpickle.encode(
                    {
                        "timestamp": datetime.now(timezone.utc),
                        "failure_count": 1,
                        "message": msg.value(),
                        "topic": msg.topic(),
                        "errors": [str(e)],
                    }
                )
                self.retry_logger.log(error_payload)  # type: ignore
                try:
                    self.consumer.commit(msg)
                except Exception as commit_err:
                    logging.error(f"Commit error after error processing: {commit_err}")

    def _reprocess_message(self, decoded: Dict[str, Any], msg: Any, retry_consumer: Consumer) -> None:
        """
        Reprocesses a message that was previously sent to the retry topic.

        If processing still fails, updates the failure count and either requeues the message
        for retry or sends it to a dead-letter topic after exceeding max retries.
        """
        try:
            for runner in self.runners:
                runner.run(decoded["message"], topic=decoded["topic"])
            try:
                retry_consumer.commit(msg)
            except Exception as commit_err:
                logging.error(f"Commit error in reprocessing: {commit_err}")
        except Exception as e:
            decoded["errors"].append(str(e))
            decoded["failure_count"] += 1

            max_retries = self.retry_detail.get(decoded["topic"], {}).get("max_retries", self.max_retries)
            error_payload = jsonpickle.encode(decoded)

            if decoded["failure_count"] < max_retries:
                self.retry_logger.log(error_payload)  # type: ignore
            else:
                self.dead_letter_logger.log(error_payload)  # type: ignore

            try:
                retry_consumer.commit(msg)
            except Exception as commit_err:
                logging.error(f"Commit error after reprocessing failure: {commit_err}")
