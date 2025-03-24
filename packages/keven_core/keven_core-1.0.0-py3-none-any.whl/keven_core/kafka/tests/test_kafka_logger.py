import logging
from keven_core.kafka.logger import KafkaLogger, KafkaBatchLogger

# Dummy producer to simulate Kafka behavior.
class DummyProducer:
    def __init__(self):
        self.produced = []

    def produce(self, topic, value, on_delivery=None):
        self.produced.append((topic, value))
        if on_delivery:
            # Simulate a successful delivery.
            on_delivery(None, type("DummyMsg", (), {"topic": lambda: topic, "partition": lambda: 0}))

    def flush(self, timeout):
        pass

def test_kafka_logger_log(monkeypatch):
    logger_instance = KafkaLogger(topic="test_topic", timeout=1)
    dummy_producer = DummyProducer()
    logger_instance.producer = dummy_producer

    logged_messages = []
    monkeypatch.setattr(logging, "info", lambda msg: logged_messages.append(msg))

    data = b"test message"
    logger_instance.log(data, topic="test_topic")
    assert any("Logging" in msg for msg in logged_messages), "Log message should indicate logging started."
    assert any(val == data for topic, val in dummy_producer.produced), "Data should be produced to Kafka."

def test_kafka_batch_logger_flush(monkeypatch):
    batch_logger = KafkaBatchLogger(topic="batch_topic", timeout=1)
    dummy_producer = DummyProducer()
    batch_logger.producer = dummy_producer

    batch_logger.log(b"message1")
    batch_logger.log(b"message2")
    batch_logger.produced_count = 0
    batch_logger.received_count = 0

    def fake_flush(timeout):
        batch_logger.received_count = 2
    monkeypatch.setattr(dummy_producer, "flush", fake_flush)

    batch_logger.flush()
    assert batch_logger.produced_count == 2, "Produced count should be 2."
    assert batch_logger.received_count == 2, "Received count should match produced count."
