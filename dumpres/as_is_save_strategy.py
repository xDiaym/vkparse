from pathlib import Path
from typing import Any

from converters.abstract_converter import AbstractConverter
from dumpres.abstract_save_strategy import AbstractSaveStrategy
from dumpres.buffered_file_dumper import BufferedFileDumper
from models.message import Message


class AsIsSaveStrategy(AbstractSaveStrategy):
    def __init__(
        self,
        path: Path,
        file_ext: str,
        converter: AbstractConverter,
        *args: Any,
        **kwargs: Any
    ) -> None:
        self._dumper = BufferedFileDumper(
            path, file_ext, converter, *args, **kwargs
        )

    def on_file(
        self, directory_name: str, file_name: str, messages: list[Message]
    ) -> None:
        self._dumper.add(messages)
        self._dumper.write(directory_name, file_name)

    def on_directory_end(self, directory_name: str) -> None:
        # Do nothing
        pass

    def on_end(self) -> None:
        # Do nothing
        pass
