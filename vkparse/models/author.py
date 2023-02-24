from dataclasses import dataclass


# TODO: Author caching
@dataclass(slots=True)
class Author:
    id: int
    name: str


YOU = Author(0, "You")
