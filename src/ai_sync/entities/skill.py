from pathlib import Path

from ai_sync.entities import EntityType
from ai_sync.lib import path_utils
from ai_sync.providers import ProviderName
from ai_sync.providers.registry import (
    SKILL_CLEANERS,
    SKILL_DEPLOYERS,
    SKILL_GENERATORS,
)
from ai_sync.scope import Scope
from ai_sync.workspace import (
    pkg,
    Workspace,
)
from ai_sync.workspace.skill import SkillPaths


def get_skill_dirs_to_generate(ws: Workspace, scope: Scope) -> list[Path]:
    preset_skill_dirs = path_utils.get_subdirs(pkg.base_preset_entities_dir(EntityType.SKILL))
    workspace_skill_dirs = path_utils.get_subdirs(ws.skills_dir)

    # Checked in every scope: a project skill would still clash with the user-level preset one.
    conflicting_names = {d.name for d in preset_skill_dirs} & {d.name for d in workspace_skill_dirs}
    if conflicting_names:
        raise Exception(f"Skill names reserved by the ai-sync base preset: {', '.join(sorted(conflicting_names))}")

    if scope == Scope.USER:
        return preset_skill_dirs + workspace_skill_dirs
    return workspace_skill_dirs


def generate(ws: Workspace, scope: Scope, providers: list[ProviderName]) -> None:
    for skill_dir in get_skill_dirs_to_generate(ws, scope):
        skill_paths = SkillPaths(root=skill_dir)
        skill_output_paths = ws.output_paths.skill_paths(skill_dir.name)

        for provider_name, provider_generate in SKILL_GENERATORS.items():
            if provider_name not in providers:
                continue

            provider_generate(
                skill_paths=skill_paths,
                skill_provider_dir=skill_paths.provider_dir(provider_name),
                skill_provider_output_dir=skill_output_paths.provider_dir(provider_name),
            )


def get_generated_names(ws: Workspace) -> list[str]:
    return [d.name for d in path_utils.get_subdirs(ws.output_paths.skills_dir)]


def deploy(ws: Workspace, work_dir: Path, scope: Scope, providers: list[ProviderName]) -> None:
    skill_names = get_generated_names(ws)

    for provider_name, provider_deploy in SKILL_DEPLOYERS.items():
        if provider_name not in providers:
            continue

        SKILL_CLEANERS[provider_name](work_dir=work_dir, scope=scope)

        for skill_name in skill_names:
            skill_provider_output_dir = ws.output_paths.skill_paths(skill_name).provider_dir(provider_name)
            if not skill_provider_output_dir.exists():
                continue

            provider_deploy(
                skill_name=skill_name,
                skill_provider_output_dir=skill_provider_output_dir,
                work_dir=work_dir,
                scope=scope,
            )
