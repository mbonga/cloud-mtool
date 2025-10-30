import logging
from typing import Optional

from .singleton import SingletonMeta


class Logger(metaclass=SingletonMeta):
    """Wrapper around standard library logging configured as a singleton.

    Use `Logger().get()` to retrieve the underlying `logging.Logger` instance.
    """

    def __init__(self, name: str = 'cloud-mtool', level: int = logging.INFO) -> None:
        self._logger = logging.getLogger(name)
        # Only configure handlers once
        if not self._logger.handlers:
            handler = logging.StreamHandler()
            fmt = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
            handler.setFormatter(fmt)
            self._logger.addHandler(handler)
        self._logger.setLevel(level)

    def get(self) -> logging.Logger:
        return self._logger

    def set_level(self, level: int) -> None:
        self._logger.setLevel(level)
