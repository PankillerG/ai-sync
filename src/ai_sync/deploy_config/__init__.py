from ai_sync.deploy_config import (
    projects as deploy_config_projects,
    rules as deploy_config_rules,
    skills as deploy_config_skills,
)
from ai_sync.deploy_config.models import (
    DeployConfig,
    RuleTargets,
    SectionNames,
    SkillTargets,
)
from ai_sync.deploy_config import utils as deploy_config_utils
from ai_sync.lib import yaml_utils
from ai_sync.workspace import Workspace


def load(ws: Workspace) -> DeployConfig:
    path = ws.deploy_yaml_file
    if not path.exists():
        return DeployConfig()

    data = yaml_utils.load(path)
    projects = data.get(SectionNames.projects) or {}
    raw_skills = data.get(SectionNames.skills) or {}
    raw_rules = data.get(SectionNames.rules) or {}

    skills = {}
    for name, raw_targets in raw_skills.items():
        resolved_targets = deploy_config_utils.resolve_targets(raw_targets, projects)
        skills[name] = SkillTargets(raw_targets=raw_targets, targets=resolved_targets)

    rules = {}
    for name, raw_targets in raw_rules.items():
        resolved_targets = deploy_config_utils.resolve_targets(raw_targets, projects)
        rules[name] = RuleTargets(raw_targets=raw_targets, targets=resolved_targets)

    return DeployConfig(projects=projects, skills=skills, rules=rules)


def render(
    config: DeployConfig,
    new_skill_names: list[str],
    new_rule_names: list[str],
) -> str:
    sections = [
        deploy_config_projects.render(config.projects),
        deploy_config_skills.render(
            active_skills=config.skills,
            new_skill_names=new_skill_names,
        ),
        deploy_config_rules.render(
            active_rules=config.rules,
            new_rule_names=new_rule_names,
        ),
    ]
    return "\n\n".join(s.strip("\n") for s in sections if s.strip()) + "\n"
