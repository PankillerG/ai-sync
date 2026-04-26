from ai_sync.deploy_config import DeployConfig
from ai_sync.providers.registry import (
    SKILL_DEPLOYERS,
    SKILL_GENERATORS,
)
from ai_sync.workspace import Workspace


def generate(ws: Workspace) -> None:
    if not ws.skills_dir.exists():
        return

    for skill_dir in sorted(ws.skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue

        skill_paths = ws.skill_paths(skill_dir.name)
        skill_output_paths = ws.output_paths.skill_paths(skill_dir.name)

        for provider_name, provider_generate in SKILL_GENERATORS.items():
            skill_provider_dir = skill_paths.provider_dir(provider_name)
            if not skill_provider_dir.exists():
                continue

            provider_generate(
                skill_paths=skill_paths,
                skill_provider_dir=skill_provider_dir,
                skill_provider_output_dir=skill_output_paths.provider_dir(provider_name),
            )


def get_generated_names(ws: Workspace) -> list[str]:
    skills_dir = ws.output_paths.skills_dir
    if not skills_dir.exists():
        return []

    return sorted(
        d.name for d in skills_dir.iterdir()
        if d.is_dir()
    )


def deploy(ws: Workspace, config: DeployConfig) -> None:
    for skill_name, skill_targets in config.skills.items():
        skill_output = ws.output_paths.skill_paths(skill_name)
        if not skill_output.root.exists():
            raise RuntimeError(
                f"No output for skill '{skill_name}'. "
                f"Run 'ai-sync generate' first."
            )

        for provider_name, provider_deploy in SKILL_DEPLOYERS.items():
            provider_output_dir = skill_output.provider_dir(provider_name)
            if not provider_output_dir.exists():
                continue

            provider_deploy(
                skill_name=skill_name,
                skill_provider_output_dir=provider_output_dir,
                targets=skill_targets.targets,
            )
