from pathlib import Path


def fix_ext(ext: str) -> str:
    if ext.startswith("."):
        return ext
    return f".{ext}"


def create_dir(path: Path) -> None:
    parent = path.parent
    if not parent.exists():
        parent.mkdir(parents=True)
