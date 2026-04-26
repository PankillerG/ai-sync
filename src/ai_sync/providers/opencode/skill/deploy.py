import shutil
from pathlib import Path

from ai_sync.deploy_config.models import ResolvedTarget
from ai_sync.providers.opencode.skill.paths import (
    SkillDeployProjectPaths,
    SkillDeployUserPaths,
    SkillOutputPaths,
)


def deploy(
    skill_name: str,
    skill_provider_output_dir: Path,
    targets: list[ResolvedTarget],
) -> None:
    skill_md_file = SkillOutputPaths(root=skill_provider_output_dir).skill_md_file

    for target in targets:
        if target.kind == "user":
            skill_deploy_paths = SkillDeployUserPaths(root=target.path).skill_paths(skill_name)
        elif target.kind == "project":
            skill_deploy_paths = SkillDeployProjectPaths(root=target.path).skill_paths(skill_name)

        skill_deploy_paths.root.mkdir(parents=True, exist_ok=True)
        shutil.copy2(skill_md_file, skill_deploy_paths.skill_md_file)
