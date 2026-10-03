from pathlib import Path

from ai_sync.lib import path_utils
from ai_sync.providers.claude.rule.paths import (
    RuleDeployProjectPaths,
    RuleDeployUserPaths,
)
from ai_sync.scope import Scope


def clear(work_dir: Path, scope: Scope) -> None:
    if scope == Scope.USER:
        rule_deploy_paths = RuleDeployUserPaths(root=work_dir)
    elif scope == Scope.PROJECT:
        rule_deploy_paths = RuleDeployProjectPaths(root=work_dir)

    path_utils.remove_path(rule_deploy_paths.rules_dir)
