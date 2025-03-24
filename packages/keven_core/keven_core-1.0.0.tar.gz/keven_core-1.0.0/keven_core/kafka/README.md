# KEVEN Kafka Foundation

The KEVEN Kafka Foundation provides a unified and extensible framework for handling Kafka-based messaging across KEVEN's microservices. This foundation consolidates the core messaging components—including event handling, consumers, runners, and loggers—into a single reusable package that future microservices can extend.

## Overview

This Kafka section of `keven_core` is built around several key components:

- **Abstract Event Handlers**  
  - **`EventHandler` and `EventHandlerMeta`:**  
    An abstract base class for event handlers using a registry metaclass for automatic registration.  
    Concrete subclasses define an `event_name` and implement `handle_event()`.  
    Pre-handler and post-handler hooks can be registered for additional processing.
  - **Usage Example:**  
    A new handler simply inherits from `EventHandler` and is automatically registered.
  
- **Consumer and Message Servers**  
  - **`KafkaConsumerServer`:**  
    Encapsulates the Kafka consumer logic including asynchronous polling, error handling, and offset management.
  - **`MessageReceiverServer`:**  
    Acts as an orchestrator that connects an I/O server (like `KafkaConsumerServer`) with a runner that processes incoming messages.
  - **`EventReceiverServer` and `AllEventsReceiverServer`:**  
    Specialized implementations that route events to registered handlers based on event types.

- **Event Runners**  
  - **`EventRunner`:**  
    Bridges raw Kafka messages and higher-level application events by parsing incoming messages and invoking the appropriate event handler(s).

- **Kafka Loggers**  
  - **`KafkaLogger` and `KafkaBatchLogger`:**  
    Provide utilities for logging messages to Kafka, supporting both individual message logging and batch operations.

- **Event Server Utilities**  
  - Functions such as `start_events_receiver_server`, `setup_event_listener`, `start_events_receiver_process`, and `start_all_events_receiver_server` offer multiple entry points for launching event processing.  
  - Both synchronous and asynchronous execution are supported via dedicated wrappers.

## Usage Examples

### 1. Defining an Event Handler

Create a concrete event handler by subclassing `EventHandler`. For example, assume you have an event type `PRINT_EVENT` defined in your `EventNames` enum:

```python
from keven_core.kafka.events.event import EventNames
from keven_core.kafka.abstracts.event_handler import EventHandler

class PrintEventHandler(EventHandler):
    event_name = EventNames.PRINT_EVENT

    def handle_event(self, event):
        print(f"PrintEventHandler received event: {event}")
```
This handler is automatically registered via the metaclass and will be available to process events of type PRINT_EVENT.

### 2. Running the Event Receiver Server
Use the provided utilities to configure and run the event receiver. The following example demonstrates synchronous startup:

```python
from keven_core.kafka.events.server import start_events_receiver_server

# Start the event receiver server with a given server name.
start_events_receiver_server(server_name="my_event_server")
```
To run the server in a separate process:
```python
from keven_core.kafka.events.server import start_events_receiver_process

# Start the event receiver server as a separate process.
process = start_events_receiver_process(server_name="my_event_server")
process.join()  # Wait for the process to finish.
```

### 3. Logging Messages to Kafka
For single-message logging, use the KafkaLogger:
```python
from keven_core.kafka.logger import KafkaLogger

logger = KafkaLogger(topic="my_logs")
logger.log(b"Sample log message")
```
For batch logging:
```python
from keven_core.kafka.logger import KafkaBatchLogger

batch_logger = KafkaBatchLogger(topic="my_batch_logs")
batch_logger.log(b"Batch message 1")
batch_logger.log(b"Batch message 2")
batch_logger.flush()  # Sends all queued messages.
```
### 4. Integrating with Your Microservices
When building new microservices:

  - **Extend** the foundation by adding new event types, commands, and corresponding handlers.
  - **Leverage** the automatic registration mechanism provided by the registry metaclass for event handlers.
  - **Configure** the consumer and logger settings as needed using environment variables or by overriding defaults.
## Testing and Integration
Before deploying to production:

  - Develop unit tests for individual components.
  - Perform integration testing under load and simulate network failures.
  - Verify that event schemas and handler registrations remain backward compatible as you extend the foundation.

## Conclusion
The KEVEN Kafka Foundation is designed to be a robust, scalable, and modular messaging backbone for KEVEN's microservices. By standardizing on common abstractions and providing flexible configuration options, it enables rapid development and consistent handling of Kafka events and commands across the project.

For additional details, refer to the inline documentation in each module.

