import os
import logging
import logging.handlers
from logging import Logger
from constants import BOT_LOGS_DIR, SCRIPT_LOGS_DIR


def get_logger(name: str, dir: str, file_name: str) -> Logger:

    if not os.path.exists(dir):
        os.makedirs(dir, exist_ok=True)

    log_file = os.path.join(dir, f'{file_name}.log')
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.hasHandlers():

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        stream_handler.setFormatter(stream_formatter)
        logger.addHandler(stream_handler)

    return logger


def get_bot_logger(name: str) -> Logger:
    return get_logger(name, BOT_LOGS_DIR, 'bot')


def get_script_logger(script_name: str) -> Logger:
    return get_logger(script_name, SCRIPT_LOGS_DIR, script_name)