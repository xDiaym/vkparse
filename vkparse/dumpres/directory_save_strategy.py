from typing import TYPE_CHECKING, Any

from vkparse.dumpres.abstract_save_strategy import AbstractSaveStrategy
from vkparse.dumpres.buffered_file_dumper import BufferedFileDumper

if TYPE_CHECKING:
    from pathlib import Path

    from vkparse.converters.abstract_converter import AbstractConverter
    from vkparse.models.message import Message


class DirectorySaveStrategy(AbstractSaveStrategy):
    def __init__(
        self,
        path: Path,
        file_ext: str,
        converter: AbstractConverter,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self._dumper = BufferedFileDumper(path, file_ext, converter, *args, **kwargs)

    def on_file(
        self,
        _directory_name: str,
        _file_name: str,
        messages: list[Message],
    ) -> None:
        self._dumper.add(messages)

    def on_directory_end(self, directory_name: str) -> None:
        # Does not create new dirs, save file in out directory as is.
        self._dumper.write("", directory_name)

    def on_end(self) -> None:
        # Do nothing.
        pass
