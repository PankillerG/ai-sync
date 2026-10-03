import shutil
from pathlib import Path

from ai_sync.lib import path_utils
from ai_sync.providers import utils
from ai_sync.providers.claude.skill.paths import (
    SkillDeployProjectPaths,
    SkillDeployUserPaths,
)
from ai_sync.scope import Scope


def clear(work_dir: Path, scope: Scope) -> None:
    if scope == Scope.USER:
        skill_deploy_paths = SkillDeployUserPaths(root=work_dir)
    elif scope == Scope.PROJECT:
        skill_deploy_paths = SkillDeployProjectPaths(root=work_dir)

    # A symlink or a file in place of the skills dir is replaced by a real dir on deploy.
    if skill_deploy_paths.skills_dir.is_symlink() or not skill_deploy_paths.skills_dir.is_dir():
        path_utils.remove_path(skill_deploy_paths.skills_dir)
        return

    for skill_dir in skill_deploy_paths.skills_dir.iterdir():
        deployed_skill_paths = skill_deploy_paths.skill_paths(skill_dir.name)
        # ai-sync deploys real directories, so a symlinked skill belongs to another tool.
        if deployed_skill_paths.root.is_symlink():
            continue
        if utils.is_skill_md_managed_by_ai_sync(deployed_skill_paths.skill_md_file):
            shutil.rmtree(deployed_skill_paths.root)
