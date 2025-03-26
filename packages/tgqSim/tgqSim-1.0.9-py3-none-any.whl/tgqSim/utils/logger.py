"""
-*- coding: utf-8 -*-
@Author : Cui Jinghao
@Time : 2024/7/17 16:24
@Function: logger.py
@Contact: cuijinghao@tgqs.net
"""
import logging


class Logger:
    def __init__(self, name: str, level: int = logging.INFO, log_file: str = None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        # Create a formatter and set it for the console handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)

        # Add the console handler to the logger
        self.logger.addHandler(console_handler)

        # If a log file is specified, create a file handler
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def debug(self, message: str):
        self.logger.debug(message)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def critical(self, message: str):
        self.logger.critical(message)


if __name__ == "__main__":
    log = Logger(name="tgqsim", level=logging.DEBUG, log_file="app.log")
    log.debug("This is a debug message")
    log.info("This is an info message")
    log.warning("This is a warning message")
    log.error("This is an error message")
    log.critical("This is a critical message")
