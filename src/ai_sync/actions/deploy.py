from ai_sync import deploy_config
from ai_sync.entities import (
    rule as rule_entity,
    skill as skill_entity,
)
from ai_sync.workspace import Workspace


def run(ws: Workspace) -> None:
    config = deploy_config.load(ws)
    skill_entity.deploy(ws, config)
    rule_entity.deploy(ws, config)
