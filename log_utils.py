#!python3
# log_utils.py

import logging


def get_logger(name=None, level=None, filepath=None):
    level = level or logging.DEBUG
    filepath = filepath or 'log.log'
    logging.getLogger().setLevel(level)
    logger = logging.getLogger(name)

    # Create handlers
    c_handler = logging.StreamHandler(sys.stdout)
    f_handler = logging.FileHandler(filepath)
    c_handler.setLevel(level)
    f_handler.setLevel(level)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(name)10s : %(levelname)10s : %(message)s')
    f_format = logging.Formatter(
        '%(asctime)s | %(name)10s | %(levelname)10s : %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
    return logger
