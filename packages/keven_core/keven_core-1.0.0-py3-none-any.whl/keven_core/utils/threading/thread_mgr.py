import threading
import logging
from queue import Queue, Empty
from typing import Callable, Any, Optional

MAX_QUEUE_SIZE = 128


class ThreadManager:
    """
    A manager for spawning worker threads to process items from a queue.

    Example usage:

        def sample_processing(item):
            print(f"Processing {item}")

        if __name__ == "__main__":
            logging.basicConfig(level=logging.DEBUG)
            manager = ThreadManager(worker_count=5, function=sample_processing, name="worker")
            manager.start()
            for i in range(100):
                manager.queue_object(i)
            manager.stop()
            manager.wait_for_termination()
    """

    def __init__(
            self,
            worker_count: int = 5,
            name: str = "thread",
            function: Optional[Callable[[Any], None]] = None,
            queue_timeout: int = 5,
            exit_on_timeout: bool = False,
            max_queue_size: int = MAX_QUEUE_SIZE
    ) -> None:
        """
        Initializes the ThreadManager with worker threads.

        Args:
            worker_count (int): Number of worker threads to spawn.
            name (str): Base name for worker threads.
            function (Callable[[Any], None], optional): The callable that each worker thread executes.
                Must be provided.
            queue_timeout (int): Timeout in seconds for queue operations.
            exit_on_timeout (bool): Whether workers should exit on queue timeout.
            max_queue_size (int): Maximum size of the processing queue.
        """
        if function is None:
            raise ValueError("A processing function must be provided.")

        self.queue: Queue[Any] = Queue(maxsize=max_queue_size)
        self.__terminated = threading.Event()
        self.workers: list[threading.Thread] = []
        self.worker_count: int = worker_count
        self.function: Callable[[Any], None] = function
        self.name: str = name
        self.queue_timeout: int = queue_timeout
        self.exit_on_timeout: bool = exit_on_timeout

    def start(self) -> None:
        """Starts the worker threads."""
        for i in range(self.worker_count):
            thread_name = f"{self.name}-{i + 1}"
            worker_thread = threading.Thread(target=self._worker, name=thread_name)
            worker_thread.start()
            self.workers.append(worker_thread)
            logging.debug(f"Started worker thread: {worker_thread.name}")

    def stop(self) -> None:
        """Signals all worker threads to terminate."""
        self.__terminated.set()

    def wait_for_termination(self) -> None:
        """Waits until all worker threads have finished execution."""
        for worker in self.workers:
            worker.join()

    def queue_object(self, item: Any) -> None:
        """
        Adds an item to the processing queue. Blocks if the queue is full.

        Args:
            item (Any): The item to be queued for processing.
        """
        self.queue.put(item)

    def _worker(self) -> None:
        """
        Worker thread function that processes objects from the queue.
        """
        current_thread_name = threading.current_thread().name
        while not self.__terminated.is_set():
            try:
                item = self.queue.get(timeout=self.queue_timeout)
                logging.debug(f"{current_thread_name} processing item: {item}")
                self.function(item)
                self.queue.task_done()
            except Empty:
                logging.debug(f"{current_thread_name} encountered queue timeout.")
                if self.exit_on_timeout:
                    break
            except Exception as e:
                logging.error(
                    f"Exception in {current_thread_name} while processing item: {e}",
                    exc_info=True
                )
