import logging


class DelayedCommandsAndEvents(object):
    def __enter__(self):
        from keven_core.kafka.commands.dispatcher import send_commands_on_commit
        from keven_core.kafka.events.logger import keven_send_events_on_commit
        keven_send_events_on_commit()
        send_commands_on_commit()
        logging.debug("Delaying Commands And Events")

    def __exit__(self, exc_type, exc_val, exc_tb):
        from keven_core.kafka.commands.dispatcher import (
            dont_send_commands_on_commit,
            keven_flush_command_cache)
        from keven_core.kafka.events.logger import (
            keven_dont_send_events_on_commit, keven_flush_event_cache)

        logging.debug("Sending Commands And Events")
        keven_flush_event_cache()
        keven_flush_command_cache()
        keven_dont_send_events_on_commit()
        dont_send_commands_on_commit()
