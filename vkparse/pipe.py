import os
from pathlib import Path
from typing import TYPE_CHECKING

from local_file_loader import LocalFileLoader

from vkparse import logger

if TYPE_CHECKING:
    from collections.abc import Iterator

    from vkparse.dumpres.abstract_save_strategy import AbstractSaveStrategy
    from vkparse.parsers.abstract_parser import AbstractParser


def _get_files(directory: Path) -> Iterator[Path]:
    content = os.listdir(directory.absolute())
    paths = (directory / x for x in content)
    return filter(Path.is_file, paths)


class Pipe:
    def __init__(
        self,
        dirs: list[Path],
        parser: AbstractParser,
        save_strategy: AbstractSaveStrategy,
    ) -> None:
        self._dirs = dirs
        self._parser = parser
        self._saver = save_strategy

    def process(self) -> None:
        for directory in self._dirs:
            logger.info("Preparing %s.", directory)
            if directory.is_dir():
                self._process_dir(directory)
        self._saver.on_end()

    def _process_dir(self, directory: Path) -> None:
        for file in _get_files(directory):
            if not file.is_file():
                continue

            logger.info("Parsing %s", file)
            content = LocalFileLoader(file).load()
            # FIXME: иcпoльзoвaть API итepaтopoв
            messages = list(self._parser(content))
            self._saver.on_file(directory.name, file.name, messages)
        self._saver.on_directory_end(directory.name)
