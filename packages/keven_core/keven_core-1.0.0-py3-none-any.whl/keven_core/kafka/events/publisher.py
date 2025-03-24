import logging
from keven_core.kafka.abstracts.message_publisher import MessagePublisher


class EventPublisher(MessagePublisher):
    """
    Class to enable you to publish events to Kafka.
    To instantiate the event do (replace TEST with your event):
    Then populate the event data

    event = Event.from_name(EventNames.TEST)
    ... populate here

    Now publish.  Good to just keep the publisher object somewhere for
    future if you can.
    logger needs to have a "log" method which accepts a single
    argument of `bytes`.  Currently we are using the KafkaLogger to publish.
    See kafka_logger.py

    pub = EventPublisher(logger)
    pub.log_event(EventNames.TEST)

    """

    def log_event(self, event, source_command=None, topic=None):
        """
        Logs the event to Publisher.  Serialized as a protobuf. Note that
        originator is set here and created to prevent forgeries :P or
        copy/paste errors.

        :param event is the event to be logged
        :param source_command is used to link this event to an issued command
        """
        if not event:
            logging.error("publisher.log_event called without event")
            return

        if source_command:
            send_event = self.get_deep_copy(event)
            send_event._source_command_uuid = source_command._uuid
            self.log_message(send_event)
        else:
            self.log_message(event, topic=topic)
