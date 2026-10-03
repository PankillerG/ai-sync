from pathlib import Path

from ai_sync.actions.generate import run as generate
from ai_sync.entities import (
    rule as rule_entity,
    skill as skill_entity,
)
from ai_sync.providers import ProviderName
from ai_sync.scope import Scope
from ai_sync.workspace import Workspace


def run(ws: Workspace, work_dir: Path, scope: Scope, providers: list[ProviderName]) -> None:
    # The user scope always has the base preset to deploy, so its workspace may not exist yet.
    if scope == Scope.PROJECT and not ws.root.exists():
        raise Exception(f"No ai-sync workspace at {ws.root}. Create an entity with 'ai-sync init' first.")

    generate(ws, scope, providers)
    skill_entity.deploy(ws, work_dir, scope, providers)
    rule_entity.deploy(ws, work_dir, scope, providers)
