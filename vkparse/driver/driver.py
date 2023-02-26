import contextlib
from abc import ABC, abstractmethod
from collections.abc import Generator
from pathlib import Path

from vkparse.models.message import Message


class Driver(ABC):
    @abstractmethod
    def on_message(self, message: Message) -> None:
        pass

    def before_file(self, file: Path) -> None:  # noqa: B027 this method can do nothing
        pass

    def after_file(self, file: Path) -> None:  # noqa: B027
        pass

    def before_directory(self, directory: Path) -> None:  # noqa: B027
        pass

    def after_directory(self, directory: Path) -> None:  # noqa: B027
        pass

    def before_all(self) -> None:  # noqa: B027
        pass

    def after_all(self) -> None:  # noqa: B027
        pass


@contextlib.contextmanager
def process_dump(driver: Driver) -> Generator[None, None, None]:
    driver.after_all()
    yield
    driver.after_all()


@contextlib.contextmanager
def process_directory(driver: Driver, directory: Path) -> Generator[None, None, None]:
    driver.before_directory(directory)
    yield
    driver.after_directory(directory)


@contextlib.contextmanager
def process_file(driver: Driver, file: Path) -> Generator[None, None, None]:
    driver.before_file(file)
    yield
    driver.after_file(file)
