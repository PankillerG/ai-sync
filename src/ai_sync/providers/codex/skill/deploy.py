import shutil
from pathlib import Path

from ai_sync.deploy_config.models import ResolvedTarget
from ai_sync.providers.codex.skill.paths import (
    SkillDeployProjectPaths,
    SkillDeployUserPaths,
    SkillOutputPaths,
)


def deploy(
    skill_name: str,
    skill_provider_output_dir: Path,
    targets: list[ResolvedTarget],
) -> None:
    skill_output_paths = SkillOutputPaths(root=skill_provider_output_dir)

    for target in targets:
        if target.kind == "user":
            skill_deploy_paths = SkillDeployUserPaths(root=target.path).skill_paths(skill_name)
        elif target.kind == "project":
            skill_deploy_paths = SkillDeployProjectPaths(root=target.path).skill_paths(skill_name)

        skill_deploy_paths.root.mkdir(parents=True, exist_ok=True)
        shutil.copy2(skill_output_paths.skill_md_file, skill_deploy_paths.skill_md_file)
        skill_deploy_paths.agents_openai_yaml_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(skill_output_paths.agents_openai_yaml_file, skill_deploy_paths.agents_openai_yaml_file)
