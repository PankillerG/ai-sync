import shutil
from pathlib import Path


def get_subdirs(parent_dir: Path) -> list[Path]:
    if not parent_dir.exists():
        return []

    return sorted(d for d in parent_dir.iterdir() if d.is_dir())


def remove_path(path: Path) -> None:
    # A symlinked dir is unlinked rather than emptied, so its target is left intact.
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)
