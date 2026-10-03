import shutil
from pathlib import Path

from ai_sync.providers.claude.rule.paths import (
    RuleDeployProjectPaths,
    RuleDeployUserPaths,
)
from ai_sync.scope import Scope


def deploy(
    work_dir: Path,
    scope: Scope,
    rules: list[tuple[str, Path]],
) -> None:
    if scope == Scope.USER:
        rule_deploy_paths = RuleDeployUserPaths(root=work_dir)
    elif scope == Scope.PROJECT:
        rule_deploy_paths = RuleDeployProjectPaths(root=work_dir)

    for rule_name, rule_provider_output_dir in rules:
        shutil.copytree(rule_provider_output_dir, rule_deploy_paths.rule_dir(rule_name))
