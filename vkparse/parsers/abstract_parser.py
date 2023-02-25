from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator

    from vkparse.models.message import Message


class AbstractParser(ABC):
    @abstractmethod
    def parse(self, content: str) -> Generator[Message, None, None]:
        pass

    def __call__(self, content: str) -> Generator[Message, None, None]:
        yield from self.parse(content)
