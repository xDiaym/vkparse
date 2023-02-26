import dataclasses
from datetime import datetime
from json import JSONEncoder, dump
from pathlib import Path
from typing import Any

from vkparse.driver.driver import Driver
from vkparse.models.message import Message

__all__ = ("JsonDriver",)


class ExtendedJSONEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        if isinstance(o, datetime):
            return o.timestamp()
        return super().default(o)


class JsonDriver(Driver):
    def __init__(self, output: Path) -> None:
        self._out_dir = output
        self._dialogue_folder = output
        self._message: list[Message] = []

    def on_message(self, message: Message) -> None:
        self._message.append(message)

    def before_directory(self, directory: Path) -> None:
        self._dialogue_folder = self._out_dir / directory.name
        if not self._dialogue_folder.exists():
            self._dialogue_folder.mkdir(parents=True)

    def after_file(self, file: Path) -> None:
        destination = (self._dialogue_folder / file.name).with_suffix(".json")
        with destination.open("w") as fp:
            dump(self._message, fp, cls=ExtendedJSONEncoder, ensure_ascii=False)
        self._message.clear()
