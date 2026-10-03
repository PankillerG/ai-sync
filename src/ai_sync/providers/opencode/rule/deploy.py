import json
import shutil
from pathlib import Path

from ai_sync.providers.opencode.rule.paths import (
    RuleDeployProjectPaths,
    RuleDeployUserPaths,
)
from ai_sync.scope import Scope


def _update_config_instructions(config_json_file: Path, globs: list[str]) -> None:
    data = json.loads(config_json_file.read_text()) if config_json_file.exists() else {}

    instructions = data.get("instructions") or []
    for glob in globs:
        if glob not in instructions:
            instructions.append(glob)
    data["instructions"] = instructions

    config_json_file.parent.mkdir(parents=True, exist_ok=True)
    config_json_file.write_text(json.dumps(data, indent=2) + "\n")


def deploy(
    work_dir: Path,
    scope: Scope,
    rules: list[tuple[str, Path]],
) -> None:
    if scope == Scope.USER:
        rule_deploy_paths = RuleDeployUserPaths(root=work_dir)
    elif scope == Scope.PROJECT:
        rule_deploy_paths = RuleDeployProjectPaths(root=work_dir)

    instruction_globs = []

    for rule_name, rule_provider_output_dir in rules:
        rule_deploy_dir = rule_deploy_paths.rule_dir(rule_name)
        shutil.copytree(rule_provider_output_dir, rule_deploy_dir)

        instruction_globs.append(f"{rule_deploy_dir}/*.md")

    _update_config_instructions(rule_deploy_paths.opencode_json_file, instruction_globs)
