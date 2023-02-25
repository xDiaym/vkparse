import logging
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


class LocalFileLoader:
    def __init__(self, path: Path, encoding: str = "cp1251") -> None:
        self._path = path.resolve()
        self._encoding = encoding
        self._logger = logging.getLogger(self.__class__.__name__)

    def load(self) -> str:
        try:
            with open(self._path, encoding=self._encoding) as fp:
                return fp.read()
        except OSError as err:
            self._logger.exception("an exception occurred", exc_info=err)
            sys.exit(-1)

    def __call__(self) -> str:
        return self.load()
