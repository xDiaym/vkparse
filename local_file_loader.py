import logging
import os
from pathlib import Path


class LocalFileLoader:
    def __init__(self, path: Path, encoding: str = "cp1251") -> None:
        self._path = os.path.abspath(path)
        self._encoding = encoding
        self._logger = logging.getLogger(self.__class__.__name__)

    def load(self) -> str:
        try:
            with open(self._path, encoding=self._encoding) as fp:
                return fp.read()
        except OSError as err:
            self._logger.exception(err)
            exit(-1)

    def __call__(self) -> str:
        return self.load()
