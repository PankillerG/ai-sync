from ai_sync.entities import (
    rule as rule_entity,
    skill as skill_entity,
)
from ai_sync.lib import path_utils
from ai_sync.providers import ProviderName
from ai_sync.scope import Scope
from ai_sync.workspace import Workspace


def run(ws: Workspace, scope: Scope, providers: list[ProviderName]) -> None:
    path_utils.remove_path(ws.output_paths.root)

    skill_entity.generate(ws, scope, providers)
    rule_entity.generate(ws, scope, providers)
