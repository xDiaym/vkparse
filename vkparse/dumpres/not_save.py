from typing import Any

from vkparse.dumpres.abstract_save_strategy import AbstractSaveStrategy
from vkparse.models.message import Message


class NotSave(AbstractSaveStrategy):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Do nothing."""
        pass

    def on_file(
        self, directory_name: str, file_name: str, messages: list[Message]
    ) -> None:
        """Do nothing."""
        pass

    def on_directory_end(self, directory_name: str) -> None:
        """Do nothing."""
        pass

    def on_end(self) -> None:
        """Do nothing."""
        pass
