"""
Logging utilities.

Some interesting uses of logging in Flask: https://flask.palletsprojects.com/en/2.3.x/logging/

Author: Johannes Traa
"""

from typing import Optional
import logging
import time
import inspect

from mh_logtools.constants import LOG_LEVEL, LOG_TIMESTAMP, LOG_CLASS, LOG_MESSAGE, LOG_FUNCTION




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
                     logfile_level: str | None = None):
    """Initialize root logger"""
    # get formatter
    formatter = get_formatter()

    # configure root logger for stdout
    logger_root = logging.getLogger()
    logging.basicConfig(level=logging.INFO)

    # create file handler
    if logfile_path is not None:
        add_file_handler(logger_root, logfile_path, level=logfile_level, formatter=formatter, filter=LogFilter())

def add_file_handler(logger: logging.Logger,
                     logfile_path: str,
                     level = None,
                     formatter: Optional[logging.Formatter] = None,
                     filter: Optional[logging.Filter] = None,
                     encoding: str = 'utf-8',
                     mode: str = 'a'):
    """Add file handler to logger"""
    if level is None:
        level = logging.INFO

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

