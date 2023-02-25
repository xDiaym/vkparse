import dataclasses
from datetime import datetime
from json import JSONEncoder, dumps
from typing import TYPE_CHECKING, Any

from vkparse.converters.abstract_converter import AbstractConverter

if TYPE_CHECKING:
    from vkparse.models.message import Message


class ExtendedJSONEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        if isinstance(o, datetime):
            return o.timestamp()
        return super().default(o)


class JsonConverter(AbstractConverter):
    def convert(self, messages: list[Message]) -> str:
        return dumps(messages, cls=ExtendedJSONEncoder)
