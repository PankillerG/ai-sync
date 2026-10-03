from pathlib import Path

from ai_sync.entities import EntityType
from ai_sync.lib import jinja_utils
from ai_sync.workspace import (
    pkg,
    Workspace,
)


def run(ws: Workspace, entity_type: EntityType, entity_name: str) -> Path:
    if pkg.base_preset_entity_dir(entity_type, entity_name).exists():
        raise Exception(f"{entity_type} name '{entity_name}' is reserved by the ai-sync base preset")

    template_dir = pkg.entity_template_dir(entity_type)
    if not template_dir.exists():
        raise Exception(f"Template not found at {template_dir}")

    target_dir = ws.entity_dir(entity_type, entity_name)
    if target_dir.exists():
        raise Exception(f"{entity_type} '{entity_name}' already exists at {target_dir}")

    target_dir.mkdir(parents=True)

    for src_file in template_dir.rglob("*"):
        if not src_file.is_file():
            continue
        dst = target_dir / src_file.relative_to(template_dir)
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(jinja_utils.render(src_file.read_text(), {"name": entity_name}))

    return target_dir
