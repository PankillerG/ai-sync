import shutil
from pathlib import Path

import yaml

from ai_sync.lib import yaml_utils


MANAGED_BY = "ai-sync"
MANAGED_BY_METADATA_KEY = "managed-by"


def copy_files(src_dir: Path, dst_dir: Path, exclude: list[Path]) -> None:
    for src_file in sorted(src_dir.rglob("*")):
        if not src_file.is_file():
            continue
        if any(src_file.is_relative_to(excluded) for excluded in exclude):
            continue

        dst_file = dst_dir / src_file.relative_to(src_dir)
        # Shared and provider-specific files land in the same directory, so a name clash is ambiguous.
        if dst_file.exists():
            raise Exception(f"Cannot copy {src_file}: {dst_file} already exists")

        dst_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_file, dst_file)


def add_managed_by_ai_sync_metadata(frontmatter_fields: dict) -> dict:
    metadata = frontmatter_fields.get("metadata") or {}
    return {
        **frontmatter_fields,
        "metadata": {**metadata, MANAGED_BY_METADATA_KEY: MANAGED_BY},
    }


def is_skill_md_managed_by_ai_sync(skill_md_file: Path) -> bool:
    if not skill_md_file.is_file():
        return False

    try:
        frontmatter_fields = yaml_utils.load_frontmatter(skill_md_file)
    except yaml.YAMLError:
        # Skills installed by other tools may have broken frontmatter; either way they are not ours.
        return False

    metadata = frontmatter_fields.get("metadata")
    return isinstance(metadata, dict) and metadata.get(MANAGED_BY_METADATA_KEY) == MANAGED_BY
