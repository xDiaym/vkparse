from typing import TYPE_CHECKING, Any

from vkparse.dumpres.abstract_save_strategy import AbstractSaveStrategy
from vkparse.dumpres.buffered_file_dumper import BufferedFileDumper

if TYPE_CHECKING:
    from pathlib import Path

    from vkparse.converters.abstract_converter import AbstractConverter
    from vkparse.models.message import Message


class AllInOneSaveStrategy(AbstractSaveStrategy):
    OUT_FILE_NAME_WITHOUT_EXT = "messages"

    def __init__(
        self,
        path: Path,
        extension: str,
        converter: AbstractConverter,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self._dumper = BufferedFileDumper(path, extension, converter, *args, **kwargs)

    def on_file(
        self,
        _directory_name: str,
        _file_name: str,
        messages: list[Message],
    ) -> None:
        self._dumper.add(messages)

    def on_directory_end(self, directory_name: str) -> None:
        # Do nothing.
        pass

    def on_end(self) -> None:
        # Does not create dirs. Converted result saves in out dir in single file
        self._dumper.write("", self.OUT_FILE_NAME_WITHOUT_EXT)

    @property
    def filename(self) -> str:
        return self.OUT_FILE_NAME_WITHOUT_EXT + self._dumper.ext
