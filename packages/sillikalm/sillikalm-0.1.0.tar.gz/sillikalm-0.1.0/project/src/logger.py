# Summary: This module sets up and configures the logging for the SillikaLM application.
# It includes functions to start, stop, and resume logging, as well as example log messages.
# Author: Krishnakanth Allika
# Email: speed-acorn-whiff@duck.com
# Copyright (c) 2025 Krishnakanth Allika, speed-acorn-whiff@duck.com
# Licensed under the GNU General Public License v3 (GPLv3).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see https://www.gnu.org/licenses/gpl-3.0-standalone.html.

import logging
import os

log_dir = "project/logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, "sillikalm.log")

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")

# Open the file in write mode to clear its contents initially
file_handler = logging.FileHandler(log_file, mode="w")
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)


def setup_logger(name):
    """
    Sets up and returns a logger instance.

    Args:
        name (str): The name of the logger (defaults to __name__).

    Returns:
        logging.Logger: A configured logger instance.
    """
    global file_handler, stream_handler
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Avoid adding handlers multiple times
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger


logger = setup_logger("SillikaLM")
logger.info("Logger initialized and ready to log messages.")

# Example log messages to verify logging is working
# logger.debug("This is a test debug message from logger.py")
# logger.info("This is a test info message from logger.py")
# logger.warning("This is a test warning message from logger.py")
# logger.error("This is a test error message from logger.py")
# logger.critical("This is a test critical message from logger.py")

# Reopen the file handler in append mode for subsequent log messages
logger.removeHandler(file_handler)
file_handler = logging.FileHandler(log_file, mode="a")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def stop_logging(logger, file_handler):
    """Stops logging by removing handlers and closing file handler."""
    logger.info("Stopping logging...")
    logger.removeHandler(file_handler)
    file_handler.close()  # close the file
    logger.info("Logging stopped.")


def resume_logging(logger):
    """Resumes logging by re-attaching handlers and reopening the file handler."""

    # Reopen the file handler in append mode
    global formatter, log_file
    file_handler = logging.FileHandler(log_file, mode="a")
    file_handler.setFormatter(formatter)

    # Re-attach the handlers
    logger.addHandler(file_handler)
    logger.info("Starting logging...")
