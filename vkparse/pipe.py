import os
from collections.abc import Iterator
from pathlib import Path

from vkparse import logger
from vkparse.driver.driver import Driver, process_directory, process_dump, process_file
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
        driver: Driver,
    ) -> None:
        self._dirs = dirs
        self._parser = parser
        self._driver = driver

    def process(self) -> None:
        with process_dump(self._driver):
            for directory in self._dirs:
                logger.info("Preparing %s.", directory)
                if directory.is_dir():
                    self._process_dir(directory)
                else:
                    logger.warning("%s is not a directory", directory)

    def _process_dir(self, directory: Path) -> None:
        with process_directory(self._driver, directory):
            for file in _get_files(directory):
                with process_file(self._driver, file):
                    logger.info("Parsing %s", file)
                    with file.open("r", encoding="cp1251") as fp:
                        content = fp.read()
                    for message in self._parser(content):
                        self._driver.on_message(message)
