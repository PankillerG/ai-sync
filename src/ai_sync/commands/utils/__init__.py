from pathlib import Path

from ai_sync import config
from ai_sync.scope import Scope


def resolve_work_dir(dir_path: Path) -> Path:
    work_dir = dir_path.expanduser().resolve()
    if not work_dir.is_dir():
        raise Exception(f"Directory not found: {work_dir}")
    return work_dir


# Compare against home instead of checking whether --dir was passed,
# so an explicit `--dir ~` still means the user scope.
def get_scope(work_dir: Path) -> Scope:
    if work_dir == Path.home().resolve():
        return Scope.USER
    return Scope.PROJECT


def get_workspace_root(work_dir: Path, scope: Scope) -> Path:
    if scope == Scope.USER:
        return work_dir / config.USER_WORK_DIR_SUFFIX
    return work_dir / config.PROJECT_WORK_DIR_SUFFIX
