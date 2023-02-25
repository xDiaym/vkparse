from abc import ABC, abstractmethod

from vkparse.models.message import Message


class AbstractConverter(ABC):
    @abstractmethod
    def convert(self, message: list[Message]) -> str:
        pass

    def __call__(self, message: list[Message]) -> str:
        return self.convert(message)
