import pytest
from keven_core.kafka.abstracts.message_server import MessageReceiverServer

# Dummy I/O server is provided by conftest.py as 'dummy_io_server'.

class DummyRunner:
    def __init__(self):
        self.processed = False
    def __call__(self, message=None):
        self.processed = True

class DummyMessageReceiverServer(MessageReceiverServer):
    pass

@pytest.mark.asyncio
async def test_message_receiver_server_async(dummy_io_server):
    runner = DummyRunner()
    receiver = DummyMessageReceiverServer(runner, io_server=dummy_io_server)
    await receiver.start()
    assert dummy_io_server.started, "IO server should have been started asynchronously."

def test_message_receiver_server_sync(monkeypatch, dummy_io_server):
    runner = DummyRunner()
    receiver = DummyMessageReceiverServer(runner, io_server=dummy_io_server)

    async def dummy_run_server():
        dummy_io_server.started = True
    monkeypatch.setattr(dummy_io_server, "run_server", dummy_run_server)

    receiver.start_sync()
    assert dummy_io_server.started, "IO server should have been started in synchronous mode."
