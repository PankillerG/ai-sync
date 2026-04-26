import shutil
from pathlib import Path

from ai_sync.deploy_config.models import ResolvedTarget
from ai_sync.providers.claude_code.rule.paths import (
    RuleDeployProjectPaths,
    RuleDeployUserPaths,
)


def deploy(
    target: ResolvedTarget,
    rules: list[tuple[str, Path]],
) -> None:
    if target.kind == "user":
        rule_deploy_paths = RuleDeployUserPaths(root=target.path)
    elif target.kind == "project":
        rule_deploy_paths = RuleDeployProjectPaths(root=target.path)

    for rule_name, rule_provider_output_dir in rules:
        rule_deploy_dir = rule_deploy_paths.rule_dir(rule_name)

        if rule_deploy_dir.exists():
            shutil.rmtree(rule_deploy_dir)
        shutil.copytree(rule_provider_output_dir, rule_deploy_dir)
