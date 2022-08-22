#!python3
# logs.py

import logging
import logging.config
import sys
import collections.abc
import warnings

__all__ = ['get_logger', 'standard_logging_config', 'get_logger_old',
           'apply_standard_logging_config', 'NoIssueFilter',
           'parse_logging_level']


def get_logger(*args, **kwargs):
    """
    Wrapper for logging.getLogger() that adapts the returned logger with
    BraceStyleAdapter which allows for {}-style formatting for log messages.
    """
    _logger = BraceStyleAdapter(logging.getLogger(*args, **kwargs))
    return _logger


def apply_standard_logging_config(**kwargs):
    logging.config.dictConfig(standard_logging_config(**kwargs))


def parse_logging_level(level):
    if isinstance(level, str):
        return level.upper()
    else:
        return level


def standard_logging_config(*,
                            file_level='DEBUG',
                            window_level='INFO',
                            window_format='default',
                            level='DEBUG',
                            file_path='log.log'):

    file_level = parse_logging_level(file_level)
    window_level = parse_logging_level(window_level)
    level = parse_logging_level(level)

    root_handlers = ['console', 'issue_console']
    if file_path is not None:
        root_handlers.append('file')

    _config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'style': '{',
                'format': '{name:s} ({lineno:4d}): {levelname:s} : {message:s}',
            },
            'cli': {
                'style': '{',
                'format': '{message:s}',
            },
            'cli_issue': {
                'style': '{',
                'format': '{levelname:s}: {message:s}'
            },
            'file_default': {
                'style': '{',
                'format': '{asctime:s} | {name:>25s} ({lineno:4d}) | '
                          '{levelname:>8s} : {message:s}',
            },
            'debug': {
                'style': '{',
                'format': '{pathname:s}:{lineno:d}\n'
                          '{name:s} | {funcName:s} | {levelname:s}\n'
                          '> {message}\n',
            },
        },
        'filters': {
            'no_issues': {
                '()': NoIssueFilter,
            },

        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': window_level,
                'formatter': window_format,
                'stream': sys.stdout,
                'filters': ['no_issues']
            },
            'issue_console': {
                'class': 'logging.StreamHandler',
                'level': 'WARNING',
                'formatter': ('cli_issue' if window_format == 'cli'
                              else window_format),
                'stream': sys.stderr,
            },
            'file': {
                'class': 'logging.FileHandler',
                'filename': file_path,
                'level': file_level,
                'formatter': 'file_default',
                'encoding': 'utf8',
            }
        },
        'root': {
            'level': level,
            'handlers': root_handlers,

        },
    }
    return _config


def get_logger_old(name: str = None,
                   window_level: int = None,
                   level: int = None,
                   filepath: str = None):
    """creates a `logging.Logger` object"""

    warnings.warn('`get_logger_old` is deprecated.')

    level = level if level is not None else logging.DEBUG
    window_level = level if window_level is None else window_level
    filepath = filepath if filepath is not None else 'log.log'
    logging.getLogger().setLevel(level)
    logger = logging.getLogger(name)

    # Create handlers
    c_handler = logging.StreamHandler(sys.stdout)
    f_handler = logging.FileHandler(filepath, encoding='utf8')
    c_handler.setLevel(window_level)
    f_handler.setLevel(level)

    # Create formatters and add it to handlers
    c_format = logging.Formatter(u'%(name)10s : %(levelname)10s : %(message)s')
    f_format = logging.Formatter(
        '%(asctime)s | %(name)10s | %(levelname)10s : %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
    return logger


class BraceFormatMessage:
    def __init__(self, fmt, args):
        self._fmt = fmt

        # Performs a check to see if a single dict-like argument is passed;
        # if so, that argument is used to pass keyword args to str.format().
        # Otherwise, only positional arguments can be passed to str.format().
        # Adapted from the implementation in logging.LogRecord.__init__().
        if (args
                and len(args) == 1
                and isinstance(args[0], collections.abc.Mapping)
                and args[0]):
            self.fmt_args = ()
            self.fmt_kwargs = args[0]
        else:
            self.fmt_args = args
            self.fmt_kwargs = {}

    def __str__(self):
        return self._fmt.format(*self.fmt_args, **self.fmt_kwargs)


class BraceStyleAdapter(logging.LoggerAdapter):
    def __init__(self, logger, extra=None):
        super().__init__(logger, {} if extra is None else extra)

    def log(self, level, msg, /, *args, **kwargs):
        if self.isEnabledFor(level):
            msg, kwargs = self.process(msg, kwargs)
            self.logger._log(level, BraceFormatMessage(msg, args), (), **kwargs)


class NoIssueFilter(logging.Filter):
    def filter(self, record: logging.LogRecord):
        return record.levelno < logging.WARNING


if __name__ == '__main__':
    log = get_logger(__name__)
    apply_standard_logging_config(window_level='debug')
    log.debug('This is a debug message.')
    x = 1
    log.info('Here is the value of x, {}', x)
    log.error('It is important to see that this is {ten:f}', {'ten': 10.0})