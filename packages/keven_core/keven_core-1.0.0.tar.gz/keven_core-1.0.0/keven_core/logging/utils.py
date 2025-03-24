import logging
import os
from typing import Optional


APP_NAME = "KEVEN"


class LogpidFormatter(logging.Formatter):
    """Logging formatter including PID."""
    def __init__(
        self,
        fmt="%(asctime)s %(process)5d %(levelname)7s %(message)s",
        datefmt="%Y%m%d %H%M%S",
    ):
        super().__init__(fmt, datefmt)


class NopidFormatter(logging.Formatter):
    """Logging formatter excluding PID."""
    def __init__(
        self,
        fmt="%(asctime)s %(levelname)7s %(message)s",
        datefmt="%Y%m%d %H%M%S",
    ):
        super().__init__(fmt, datefmt)


def add_verbose_level():
    """Adds VERBOSE (level 5) logging level to the logging module."""
    if not hasattr(logging, 'VERBOSE'):
        logging.VERBOSE = 5
        logging.addLevelName(logging.VERBOSE, "VERBOSE")
        logging.Logger.verbose = lambda inst, msg, *args, **kwargs: inst.log(logging.VERBOSE, msg, *args, **kwargs)
        logging.LoggerAdapter.verbose = lambda inst, msg, *args, **kwargs: inst.log(logging.VERBOSE, msg, *args, **kwargs)
        logging.verbose = lambda msg, *args, **kwargs: logging.log(logging.VERBOSE, msg, *args, **kwargs)


def determine_log_level():
    """Determines log level from environment variable."""
    os_debug = os.getenv(f"{APP_NAME}_DEBUG", "")
    if os_debug.isdigit():
        os_debug = int(os_debug)
        if os_debug == 1:
            return logging.DEBUG
        elif os_debug == 2:
            return logging.VERBOSE
    return logging.INFO


def use_pid_formatter(pid: Optional[int] = None) -> logging.Formatter:
    """Determines formatter based on PID requirement."""
    if pid is not None:
        return LogpidFormatter() if pid > 1 else NopidFormatter()
    os_logpid = os.getenv(f"{APP_NAME}_LOGPID", "")
    return LogpidFormatter() if os_logpid.isdigit() and int(os_logpid) else NopidFormatter()


def set_formatter(pid: Optional[int] = None):
    """Sets formatter for all handlers of the root logger."""
    formatter = use_pid_formatter(pid)
    for handler in logging.getLogger().handlers:
        handler.setFormatter(formatter)


def init_logging():
    """Initializes logging system with verbosity and formatting."""
    add_verbose_level()
    lvl = determine_log_level()
    fmt = "%(asctime)s %(levelname)7s %(message)s"

    # Configure basic logging
    logging.basicConfig(level=lvl, format=fmt, datefmt="%Y%m%d %H%M%S")
    logging.getLogger().setLevel(lvl)  # Explicitly ensure correct level is set
    set_formatter()


def debug_logging(lvl: int = 0):
    """Adjusts log verbosity at runtime."""
    levels = {0: logging.INFO, 1: logging.DEBUG, 2: logging.VERBOSE}
    logging.getLogger().setLevel(levels.get(lvl, logging.INFO))
    set_formatter(pid=lvl)
    show_loggers()


def show_loggers():
    """Outputs current logging configuration."""
    all_loggers = [logging.getLogger()] + [
        logging.getLogger(name) for name in logging.root.manager.loggerDict
    ]
    for logger in sorted(all_loggers, key=lambda l: l.name):
        logging.debug(f"ㄲ Logger: {logger.getEffectiveLevel():<2} | {logger.name}")


def set_all_loggers(pid: Optional[bool] = None):
    """Sets formatter (PID or no-PID) for all existing loggers."""
    formatter = use_pid_formatter(2 if pid else 0)
    for logger in [logging.getLogger()] + list(logging.root.manager.loggerDict.values()):
        if hasattr(logger, 'handlers'):
            for handler in logger.handlers:
                handler.setFormatter(formatter)
