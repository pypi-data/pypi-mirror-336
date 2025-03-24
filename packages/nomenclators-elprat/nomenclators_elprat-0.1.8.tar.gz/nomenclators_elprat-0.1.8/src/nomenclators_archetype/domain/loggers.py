"""
----------------------------------------------------------------------------------------------------
Written by:
  - Yovany Dominico Girón(y.dominico.giron@elprat.cat)

for Ajuntament del Prat de Llobregat
----------------------------------------------------------------------------------------------------

----------------------------------------------------------------------------------------------------
"""
import logging
import sys
import os

from typing import Optional

LOGGER_LEVEL_ENV_NAME = "LOGGER_LEVEL"
LOGGER_LEVEL_DEFAULT = "INFO"
LOGGER_LEVEL = os.getenv(LOGGER_LEVEL_ENV_NAME, LOGGER_LEVEL_DEFAULT).upper()

DEFAULT_LOGGER_ENV_NAME = "DEFAULT_LOGGER_NAME"
DEFAULT_LOGGER_NAME_DEFAULT = "default_logger"
DEFAULT_LOGGER_NAME = os.getenv(
    DEFAULT_LOGGER_ENV_NAME, DEFAULT_LOGGER_NAME_DEFAULT)


class LoggerBuilder:
    """Logger builder class"""

    def __init__(self,
                 name: Optional[str] = None,
                 level: Optional[str] = None,
                 logger: Optional[logging.Logger] = None,
                 propagate: Optional[bool] = False):

        if not name and not logger:
            raise ValueError("Either name or logger must be provided")

        self.propagate = propagate
        if name:
            self.logger = logging.getLogger(name)
        else:
            self.logger = logger

        if level:
            self.logger.setLevel(getattr(logging, level, logging.INFO))

        self.register_handler()

    def get_handler(self):
        """Gets the handler of the logger"""
        return logging.StreamHandler(sys.stdout)

    def get_formatter(self):
        """Gets the formatter of the logger"""
        return logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

    def register_handler(self):
        """Registers the handler of the logger"""
        handler = self.get_handler()
        handler.setFormatter(self.get_formatter())

        if not self.logger.hasHandlers():
            self.logger.addHandler(handler)
            self.logger.propagate = self.propagate

    def build(self):
        """Builds the logger"""
        return self.logger


# Default Logger
default_logger = LoggerBuilder(
    name=DEFAULT_LOGGER_NAME, level=LOGGER_LEVEL).build()
