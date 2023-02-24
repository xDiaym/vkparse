import os
from pathlib import Path
from typing import Iterator

from vkparse.dumpres.abstract_save_strategy import AbstractSaveStrategy
from local_file_loader import LocalFileLoader
from vkparse.parsers.abstract_parser import AbstractParser


def _get_files(directory: Path) -> Iterator[Path]:
    content = os.listdir(directory.absolute())
    paths = map(lambda x: directory / x, content)
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
            print(f"Preparing {directory}.")
            if directory.is_dir():
                self._process_dir(directory)
        self._saver.on_end()

    def _process_dir(self, directory: Path) -> None:
        for file in _get_files(directory):
            if not file.is_file():
                continue

            print(f"Parsing {file}")
            content = LocalFileLoader(file).load()
            messages = self._parser(content)
            self._saver.on_file(directory.name, file.name, messages)
        self._saver.on_directory_end(directory.name)
