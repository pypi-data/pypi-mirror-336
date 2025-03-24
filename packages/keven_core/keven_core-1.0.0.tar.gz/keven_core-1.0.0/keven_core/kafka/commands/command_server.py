from multiprocessing import Process
from keven_core.kafka.abstracts.consumer_server import KafkaConsumerServer


def start_command_receiver_server(
    server_name: str,
    io_server=None,
    auto_reprocess_errors=False,
    max_poll_interval=180,
    auto_start=True
) -> None:
    """
    Convenient way to receive commands in your application.  Only define
    io_server if you don't want kafka
    """
    topics = ["keven_commands"]
    from keven_core.kafka.abstracts.command_handler import CommandHandler
    for cmd in CommandHandler.commands_with_handlers():
        topics.append(f"keven_commands_{cmd}")
    command_receiver = setup_command_receiver(
        auto_reprocess_errors,
        io_server,
        server_name,
        topics=topics,
        max_poll_interval=max_poll_interval,
    )

    if auto_start:
        # Start synchronously so the code fully runs within this function.
        command_receiver.start_sync()
    else:
        # Return it so the caller can start manually (async or sync).
        return command_receiver


def setup_command_receiver(
    auto_reprocess_errors,
    io_server,
    server_name,
    reraise_exceptions=False,
    timeout=None,
    log_exceptions=True,
    topics=None,
    max_poll_interval=180,
) -> "CommandReceiverServer":
    from keven_core.kafka.abstracts.command_receiver import CommandReceiverServer
    from keven_core.kafka.abstracts.command_handler import CommandHandler
    if not io_server:
        io_server = KafkaConsumerServer(
            topics=topics or ["keven_commands"],
            client_id=server_name,
            group_id=server_name,
            auto_reprocess_errors=auto_reprocess_errors,
            reraise_exceptions=reraise_exceptions,
            timeout=timeout,
            log_exceptions=log_exceptions,
            max_poll_interval=max_poll_interval,
        )
    command_names = [command_name for command_name in CommandHandler._command_registry]
    # command_names.extend(
    #     [command_name for command_name in CommandHandler._func_registry]
    # )
    command_receiver = CommandReceiverServer(
        command_names=command_names, io_server=io_server
    )
    return command_receiver


def start_command_receiver_process(server_name: str, io_server=None):
    """
    Starts a command handler server as a separate process
    :param server_name: Name of the io_server consumer
    :param io_server: IO Server Class.  Defaults to KafkaConsumerServer
    :return: The python Process instance.  Use return_value.join() to wait for
    it to exit.
    """
    command_proc = Process(
        target=start_command_receiver_server, args=[server_name]
    )
    command_proc.start()
    return command_proc


def start_all_commands_receiver_server(
    server_name: str, io_server=None
) -> None:
    from keven_core.kafka.abstracts.command_receiver import AllCommandsReceiverServer

    if not io_server:
        io_server = KafkaConsumerServer(
            topics=["keven_commands", "^keven_commands_.*"],
            client_id=server_name,
            group_id=server_name,
        )

    command_receiver = AllCommandsReceiverServer(io_server=io_server)
    command_receiver.run_server()
