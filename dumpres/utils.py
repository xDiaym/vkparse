import os
from pathlib import Path


def fix_ext(ext: str) -> str:
    if ext.startswith("."):
        return ext
    return f".{ext}"


def fix_file_ext(path: Path, ext: str) -> Path:
    ext = fix_ext(ext)
    if not path.is_file():
        return path
    name, _ = os.path.splitext(path)
    return Path(name + ext)


def create_dir(path: Path) -> None:
    parent = path.parent
    if not parent.exists():
        parent.mkdir(parents=True)
