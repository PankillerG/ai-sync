import shutil

from ai_sync.entities import (
    rule as rule_entity,
    skill as skill_entity,
)
from ai_sync.workspace import Workspace


def run(ws: Workspace) -> None:
    output_dir = ws.output_paths.root
    if output_dir.exists():
        shutil.rmtree(output_dir)

    skill_entity.generate(ws)
    rule_entity.generate(ws)
