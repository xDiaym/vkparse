from abc import abstractmethod, ABC

from vkparse.models.message import Message


class AbstractParser(ABC):
    @abstractmethod
    def parse(self, content: str) -> list[Message]:
        pass

    def __call__(self, content: str) -> list[Message]:
        return self.parse(content)
