from ai_sync import deploy_config
from ai_sync.entities import (
    rule as rule_entity,
    skill as skill_entity,
)
from ai_sync.workspace import Workspace


def _get_skills_updates(ws: Workspace, config: deploy_config.DeployConfig):
    generated_skill_names = skill_entity.get_generated_names(ws)
    generated_set = set(generated_skill_names)

    config.skills = {
        name: targets
        for name, targets in config.skills.items()
        if name in generated_set
    }

    new_skill_names = [
        name for name in generated_skill_names
        if name not in config.skills
    ]

    return config, new_skill_names


def _get_rules_updates(ws: Workspace, config: deploy_config.DeployConfig):
    generated_rule_names = rule_entity.get_generated_names(ws)
    generated_set = set(generated_rule_names)

    config.rules = {
        name: targets
        for name, targets in config.rules.items()
        if name in generated_set
    }

    new_rule_names = [
        name for name in generated_rule_names
        if name not in config.rules
    ]

    return config, new_rule_names


def run(ws: Workspace) -> None:
    config = deploy_config.load(ws)

    config, new_skill_names = _get_skills_updates(ws, config)
    config, new_rule_names = _get_rules_updates(ws, config)

    content = deploy_config.render(config, new_skill_names, new_rule_names)
    ws.deploy_yaml_file.write_text(content)
