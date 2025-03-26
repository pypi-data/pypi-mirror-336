"""
Logging utilities.

Some interesting uses of logging in Flask: https://flask.palletsprojects.com/en/2.3.x/logging/

Author: Johannes Traa, 2025
"""

import os
import sys
from typing import Optional
import logging
import time
import inspect

from mh_logtools.constants import LOG_LEVEL, LOG_TIMESTAMP, LOG_CLASS, LOG_MESSAGE, LOG_FUNCTION



### Custom filters ###
class LogFilter(logging.Filter):
    """This is a filter which injects contextual information into the log."""
    def filter(self, record):
        if not hasattr(record, 'className_'):
            record.className_ = ''
        if not hasattr(record, 'funcName_'):
            record.funcName_ = ''
        return True


### Logger setup ###
def init_root_logger(logfile_path: str | None = None,
                     root_level: int = logging.INFO,
                     stdout_level: int | None = None,
                     logfile_level: int = logging.DEBUG):
    """Initialize root logger and handlers for stdout and file."""
    # get formatter
    formatter = get_formatter()

    # configure root logger for stdout
    logger_root = logging.getLogger()
    logging.basicConfig(level=root_level) # global log level (overrides levels in handlers)

    # create stream handler (stdout)
    if stdout_level is not None:
        add_stream_handler(logger_root, stdout_level, formatter=formatter, filter=LogFilter())

    # create file handler
    if logfile_path is not None:
        add_file_handler(logger_root, logfile_path, logfile_level, formatter=formatter, filter=LogFilter())

def add_stream_handler(logger: logging.Logger,
                       level: int,
                       formatter: logging.Formatter | None = None,
                       filter: logging.Filter | None = None):
    """Add stream handler for writing logs to stdout"""
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(level)
    if formatter is not None:
        sh.setFormatter(formatter)
    if filter is not None:
        sh.addFilter(filter)
    logger.addHandler(sh)

def add_file_handler(logger: logging.Logger,
                     logfile_path: str,
                     level: int,
                     formatter: Optional[logging.Formatter] = None,
                     filter: Optional[logging.Filter] = None,
                     encoding: str = 'utf-8',
                     mode: str = 'a'):
    """Add file handler to logger"""
    fh = logging.FileHandler(logfile_path, encoding=encoding, mode=mode)
    fh.setLevel(level)
    if formatter is not None:
        fh.setFormatter(formatter)
    if filter is not None:
        fh.addFilter(filter)
    logger.addHandler(fh)

def get_formatter() -> logging.Formatter:
    terms = [
        f'"{LOG_CLASS}": "%(className_)s"',
        f'"{LOG_FUNCTION}": "%(funcName_)s"',
        f'"{LOG_LEVEL}": "%(levelname)s"',
        f'"{LOG_MESSAGE}": "%(message)s"',
        f'"{LOG_TIMESTAMP}": "%(asctime)s"',
    ]
    fmt = "{" + ", ".join(terms) + "}"  # TODO: update this to use a JSON formatter and json.dumps()

    formatter = logging.Formatter(fmt)
    formatter.converter = time.gmtime

    return formatter


### Log write ###
def write_log(logger: logging.Logger,
              msg: str,
              method: str = 'info'):
    """Write a log message"""
    # get extra info
    prev_frame = inspect.currentframe().f_back
    extra = {
        'funcName_': prev_frame.f_code.co_name  # calling function name
    }
    try:
        class_name = prev_frame.f_locals["self"].__class__.__name__ # calling class name
    except:
        class_name = ''
    extra['className_'] = class_name

    # log the message
    func = getattr(logger, method)
    func(msg, extra=extra)


### Log dir setup ###
def setup_log_dir(log_dpath: str,
                  log_fname: str | None = None) \
        -> str:
    """Set up log directory and file."""
    if log_fname is None:
        log_fname = f'{int(time.time())}.log'

    os.makedirs(log_dpath, exist_ok=True)
    logfile_path = os.path.join(log_dpath, log_fname)

    return logfile_path
