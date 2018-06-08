import logging


def enable_debug_log(logger_name,
                     logger_level=logging.DEBUG,
                     logger_formatter='%(asctime)s - %(name)s - %(levelname)s - %(message)s'):
    debug_logger = logging.getLogger(logger_name)
    ch = logging.StreamHandler()
    ch.setLevel(logger_level)
    formatter = logging.Formatter(logger_formatter)
    ch.setFormatter(formatter)
    debug_logger.addHandler(ch)
    debug_logger.setLevel(logging.DEBUG)
