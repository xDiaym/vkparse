from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from vkparse.models.attachment import Attachment
from vkparse.models.author import Author


@dataclass(frozen=True)
class Message:
    author: Author
    date: datetime
    text: Optional[str]
    attachments: Optional[list[Attachment]]
