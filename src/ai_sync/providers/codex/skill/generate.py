from pathlib import Path

from ai_sync.lib import yaml_utils
from ai_sync.providers import utils
from ai_sync.providers.codex.skill.paths import SkillOutputPaths as SkillProviderOutputPaths
from ai_sync.workspace.skill import SkillPaths


SKILL_MD_TEMPLATE = """\
{frontmatter}

{prompt}
"""


def generate(
    skill_paths: SkillPaths,
    skill_provider_dir: Path,
    skill_provider_output_dir: Path,
) -> None:
    skill_provider_output_paths = SkillProviderOutputPaths(root=skill_provider_output_dir)

    common_meta = yaml_utils.load(skill_paths.meta_yaml_file)
    frontmatter = yaml_utils.get_frontmatter(utils.add_managed_by_ai_sync_metadata(common_meta))
    prompt = skill_paths.prompt_md_file.read_text().strip()

    content = SKILL_MD_TEMPLATE.format(frontmatter=frontmatter, prompt=prompt)

    skill_provider_output_paths.root.mkdir(parents=True, exist_ok=True)
    skill_provider_output_paths.skill_md_file.write_text(content)

    utils.copy_files(skill_paths.root, skill_provider_output_paths.root, exclude=skill_paths.reserved_paths)
    utils.copy_files(skill_provider_dir, skill_provider_output_paths.root, exclude=[])
