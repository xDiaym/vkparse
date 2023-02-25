from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vkparse.models.message import Message


class AbstractConverter(ABC):
    @abstractmethod
    def convert(self, message: list[Message]) -> str:
        pass

    def __call__(self, message: list[Message]) -> str:
        return self.convert(message)
