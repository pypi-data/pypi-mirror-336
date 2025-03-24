import logging
import threading
from keven_core.kafka.commands.publisher import CommandPublisher
from keven_core.kafka.logger import KafkaLogger

__command_publishers = dict()
__command_send_messages_on_commit = False
__command_write_cache = dict()
__command_lock = threading.Lock()


def clear_command_publishers():
    global __command_publishers
    with __command_lock:
        __command_publishers.clear()


def send_commands_on_commit():
    global __command_send_messages_on_commit
    __command_send_messages_on_commit = True


def dont_send_commands_on_commit():
    global __command_send_messages_on_commit
    __command_send_messages_on_commit = False


def last_publisher():
    global __command_publishers
    ident = threading.current_thread().ident
    pub = __command_publishers.get(ident)
    if not pub:
        logger = KafkaLogger(topic="keven_commands", timeout=30)
        pub = CommandPublisher(logger)
        with __command_lock:
            __command_publishers[ident] = pub

    logging.verbose(f"⇔ Command Publisher: {pub} (ident '{ident}')")
    return pub


def get_write_cache():
    ident = threading.current_thread().ident
    cache = __command_write_cache.get(ident)
    if not cache:
        with __command_lock:
            __command_write_cache[ident] = list()
            cache = __command_write_cache[ident]

    return cache


def set_publisher(publisher):
    ident = threading.current_thread().ident
    with __command_lock:
        __command_publishers[ident] = publisher


def keven_dispatch_command(command):
    global __command_send_messages_on_commit
    if __command_send_messages_on_commit:
        get_write_cache().append(command)
    else:
        last_publisher().dispatch_command(command)


def keven_dispatch_command_now(command):
    last_publisher().dispatch_command(command)


def keven_flush_command_cache():
    for command in get_write_cache():
        logging.verbose(f"↹ Cache flush {command.command_name}")
        last_publisher().dispatch_command(command)
    get_write_cache().clear()
