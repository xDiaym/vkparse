from dataclasses import dataclass
from datetime import datetime

from vkparse.models.attachment import Attachment
from vkparse.models.author import Author


@dataclass(frozen=True)
class Message:
    author: Author
    date: datetime
    text: str | None
    attachments: list[Attachment] | None
