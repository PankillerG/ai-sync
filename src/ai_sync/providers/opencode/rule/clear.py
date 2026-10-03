import json
from pathlib import Path

from ai_sync.lib import path_utils
from ai_sync.providers.opencode.rule.paths import (
    RuleDeployProjectPaths,
    RuleDeployUserPaths,
)
from ai_sync.scope import Scope


def _remove_config_instructions(config_json_file: Path, rules_dir: Path) -> None:
    if not config_json_file.exists():
        return

    data = json.loads(config_json_file.read_text())
    if "instructions" not in data:
        return

    data["instructions"] = [
        instruction for instruction in data["instructions"]
        if not Path(instruction).is_relative_to(rules_dir)
    ]
    config_json_file.write_text(json.dumps(data, indent=2) + "\n")


def clear(work_dir: Path, scope: Scope) -> None:
    if scope == Scope.USER:
        rule_deploy_paths = RuleDeployUserPaths(root=work_dir)
    elif scope == Scope.PROJECT:
        rule_deploy_paths = RuleDeployProjectPaths(root=work_dir)

    path_utils.remove_path(rule_deploy_paths.rules_dir)
    _remove_config_instructions(rule_deploy_paths.opencode_json_file, rule_deploy_paths.rules_dir)
