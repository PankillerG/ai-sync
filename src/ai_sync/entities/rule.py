from pathlib import Path

from ai_sync.entities import EntityType
from ai_sync.lib import path_utils
from ai_sync.providers import ProviderName
from ai_sync.providers.registry import (
    RULE_CLEANERS,
    RULE_DEPLOYERS,
    RULE_GENERATORS,
)
from ai_sync.scope import Scope
from ai_sync.workspace import (
    pkg,
    Workspace,
)
from ai_sync.workspace.rule import RulePaths


def get_rule_dirs_to_generate(ws: Workspace, scope: Scope) -> list[Path]:
    preset_rule_dirs = path_utils.get_subdirs(pkg.base_preset_entities_dir(EntityType.RULE))
    workspace_rule_dirs = path_utils.get_subdirs(ws.rules_dir)

    # Checked in every scope: a project rule would still clash with the user-level preset one.
    conflicting_names = {d.name for d in preset_rule_dirs} & {d.name for d in workspace_rule_dirs}
    if conflicting_names:
        raise Exception(f"Rule names reserved by the ai-sync base preset: {', '.join(sorted(conflicting_names))}")

    if scope == Scope.USER:
        return preset_rule_dirs + workspace_rule_dirs
    return workspace_rule_dirs


def generate(ws: Workspace, scope: Scope, providers: list[ProviderName]) -> None:
    for rule_dir in get_rule_dirs_to_generate(ws, scope):
        rule_paths = RulePaths(root=rule_dir)
        rule_output_paths = ws.output_paths.rule_paths(rule_dir.name)

        for provider_name, provider_generate in RULE_GENERATORS.items():
            if provider_name not in providers:
                continue

            provider_generate(
                rule_paths=rule_paths,
                rule_provider_dir=rule_paths.provider_dir(provider_name),
                rule_provider_output_dir=rule_output_paths.provider_dir(provider_name),
            )


def get_generated_names(ws: Workspace) -> list[str]:
    return [d.name for d in path_utils.get_subdirs(ws.output_paths.rules_dir)]


def deploy(ws: Workspace, work_dir: Path, scope: Scope, providers: list[ProviderName]) -> None:
    rule_names = get_generated_names(ws)

    for provider_name, provider_deploy in RULE_DEPLOYERS.items():
        if provider_name not in providers:
            continue

        RULE_CLEANERS[provider_name](work_dir=work_dir, scope=scope)

        rules = []
        for rule_name in rule_names:
            rule_provider_output_dir = ws.output_paths.rule_paths(rule_name).provider_dir(provider_name)
            if rule_provider_output_dir.exists():
                rules.append((rule_name, rule_provider_output_dir))

        # Codex would write an empty AGENTS.md instead of leaving it cleared.
        if not rules:
            continue

        provider_deploy(work_dir=work_dir, scope=scope, rules=rules)
