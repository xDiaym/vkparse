from pathlib import Path

from vkparse.converters.abstract_converter import AbstractConverter
from vkparse.dumpres.utils import create_dir, fix_ext
from vkparse.models.message import Message


class BufferedFileDumper:
    def __init__(
        self,
        root: Path,
        file_ext: str,
        converter: AbstractConverter,
        mode: str = "w+",
    ) -> None:
        self._root = root
        self._file_ext = fix_ext(file_ext)
        self._converter = converter
        self._mode = mode
        self._buffer: list[Message] = []

    def add(self, messages: list[Message]) -> None:
        self._buffer.extend(messages)

    def write(self, dir_name: str, file_name: str) -> None:
        converted = self._converter(self._buffer)
        self._buffer.clear()

        path = Path(self._root / dir_name / file_name)
        filename = path.with_suffix(self._file_ext)
        create_dir(filename)
        with open(filename, self._mode) as fp:
            fp.write(converted)

    @property
    def ext(self) -> str:
        return self._file_ext
