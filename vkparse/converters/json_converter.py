import dataclasses
from datetime import datetime
from json import dumps, JSONEncoder
from typing import Any

from vkparse.converters.abstract_converter import AbstractConverter
from vkparse.models.message import Message


class ExtendedJSONEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        elif isinstance(o, datetime):
            return o.timestamp()
        return super().default(o)


class JsonConverter(AbstractConverter):
    def convert(self, messages: list[Message]) -> str:
        return dumps(messages, cls=ExtendedJSONEncoder)
