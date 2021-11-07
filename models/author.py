from dataclasses import dataclass


# TODO: Author caching
@dataclass(frozen=True)
class Author:
    id: int
    name: str


YOU = Author(0, "You")
