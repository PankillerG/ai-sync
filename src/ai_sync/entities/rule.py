from collections import defaultdict

from ai_sync.deploy_config import DeployConfig
from ai_sync.deploy_config.models import ResolvedTarget
from ai_sync.providers.registry import (
    RULE_DEPLOYERS,
    RULE_GENERATORS,
)
from ai_sync.workspace import Workspace


def generate(ws: Workspace) -> None:
    if not ws.rules_dir.exists():
        return

    for rule_dir in sorted(ws.rules_dir.iterdir()):
        if not rule_dir.is_dir():
            continue

        rule_paths = ws.rule_paths(rule_dir.name)
        rule_output_paths = ws.output_paths.rule_paths(rule_dir.name)

        for provider_name, provider_generate in RULE_GENERATORS.items():
            provider_generate(
                rule_paths=rule_paths,
                rule_provider_dir=rule_paths.provider_dir(provider_name),
                rule_provider_output_dir=rule_output_paths.provider_dir(provider_name),
            )


def get_generated_names(ws: Workspace) -> list[str]:
    rules_dir = ws.output_paths.rules_dir
    if not rules_dir.exists():
        return []

    return sorted(
        d.name for d in rules_dir.iterdir()
        if d.is_dir()
    )


def deploy(ws: Workspace, config: DeployConfig) -> None:
    for provider_name, provider_deploy in RULE_DEPLOYERS.items():
        rules_by_target: defaultdict[ResolvedTarget, list] = defaultdict(list)

        for rule_name, rule_targets in config.rules.items():
            rule_output_paths = ws.output_paths.rule_paths(rule_name)
            if not rule_output_paths.root.exists():
                raise RuntimeError(
                    f"No output for rule '{rule_name}'. "
                    f"Run 'ai-sync generate' first."
                )

            rule_provider_output_dir = rule_output_paths.provider_dir(provider_name)
            if not rule_provider_output_dir.exists():
                continue

            for rule_target in rule_targets.targets:
                rules_by_target[rule_target].append((rule_name, rule_provider_output_dir))

        for target, rules in rules_by_target.items():
            provider_deploy(target=target, rules=rules)
