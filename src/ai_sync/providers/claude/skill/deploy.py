import shutil
from pathlib import Path

from ai_sync.lib import path_utils
from ai_sync.providers.claude.skill.paths import (
    SkillDeployProjectPaths,
    SkillDeployUserPaths,
)
from ai_sync.scope import Scope


def deploy(
    skill_name: str,
    skill_provider_output_dir: Path,
    work_dir: Path,
    scope: Scope,
) -> None:
    if scope == Scope.USER:
        skill_deploy_paths = SkillDeployUserPaths(root=work_dir).skill_paths(skill_name)
    elif scope == Scope.PROJECT:
        skill_deploy_paths = SkillDeployProjectPaths(root=work_dir).skill_paths(skill_name)

    path_utils.remove_path(skill_deploy_paths.root)
    shutil.copytree(skill_provider_output_dir, skill_deploy_paths.root)
