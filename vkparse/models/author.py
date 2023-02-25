from dataclasses import dataclass


# TODO: Author caching
@dataclass(slots=True)
class Author:
    id_: int
    name: str


YOU = Author(0, "You")
