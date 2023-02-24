from abc import ABC, abstractmethod

from vkparse.models.message import Message


class AbstractSaveStrategy(ABC):
    @abstractmethod
    def on_file(
        self, directory_name: str, file_name: str, messages: list[Message]
    ) -> None:
        pass

    @abstractmethod
    def on_directory_end(self, directory_name: str) -> None:
        pass

    @abstractmethod
    def on_end(self) -> None:
        pass
