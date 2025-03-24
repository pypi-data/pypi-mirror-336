import asyncio
import tempfile
import os
import pytest

from keven_core.kafka.abstracts.consumer_server import KafkaConsumerServer

# Fixture for a temporary directory used for file-system based tests.
@pytest.fixture(scope="session")
def temp_dir():
    with tempfile.TemporaryDirectory() as tmp:
        yield tmp

# Fixture for a dummy I/O server that simulates a Kafka consumer.
# This dummy server can be used for tests in MessageReceiverServer and similar.
class DummyIOServer:
    def __init__(self):
        self.runners = []
        self.started = False

    def add_runner(self, runner):
        self.runners.append(runner)

    async def run_server(self):
        self.started = True
        # Simulate some async processing delay.
        await asyncio.sleep(0.1)
        return "done"

@pytest.fixture
def dummy_io_server():
    return DummyIOServer()

# For asynchronous tests, pytest-asyncio provides an event_loop fixture by default.
# If you need a custom one, uncomment the following:

# @pytest.fixture(scope="session")
# def event_loop():
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()
