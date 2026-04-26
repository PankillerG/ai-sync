import json
import shutil
from pathlib import Path

from ai_sync.deploy_config.models import ResolvedTarget
from ai_sync.providers.opencode.rule.paths import (
    RuleDeployProjectPaths,
    RuleDeployUserPaths,
)


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
    target: ResolvedTarget,
    rules: list[tuple[str, Path]],
) -> None:
    if target.kind == "user":
        rule_deploy_paths = RuleDeployUserPaths(root=target.path)
    elif target.kind == "project":
        rule_deploy_paths = RuleDeployProjectPaths(root=target.path)

    instruction_globs = []

    for rule_name, rule_provider_output_dir in rules:
        rule_deploy_dir = rule_deploy_paths.rule_dir(rule_name)
        if rule_deploy_dir.exists():
            shutil.rmtree(rule_deploy_dir)
        shutil.copytree(rule_provider_output_dir, rule_deploy_dir)

        instruction_globs.append(f"{rule_deploy_dir}/*.md")

    _update_config_instructions(rule_deploy_paths.opencode_json_file, instruction_globs)
