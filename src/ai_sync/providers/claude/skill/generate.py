from pathlib import Path

from ai_sync.lib import yaml_utils
from ai_sync.providers import utils
from ai_sync.providers.claude.skill.paths import (
    CLAUDE_RESERVED_SKILL_NAMES,
    SkillOutputPaths as SkillProviderOutputPaths,
    SkillPaths as SkillProviderPaths,
)
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
    skill_name = skill_paths.root.name
    if skill_name in CLAUDE_RESERVED_SKILL_NAMES:
        raise Exception(f"Skill name '{skill_name}' is reserved by Claude Code")

    skill_provider_paths = SkillProviderPaths(root=skill_provider_dir)
    skill_provider_output_paths = SkillProviderOutputPaths(root=skill_provider_output_dir)

    frontmatter_fields = yaml_utils.load_from_files(yaml_files=[
        skill_paths.meta_yaml_file,
        skill_provider_paths.meta_yaml_file,
    ])
    frontmatter = yaml_utils.get_frontmatter(utils.add_managed_by_ai_sync_metadata(frontmatter_fields))

    prompt = skill_paths.prompt_md_file.read_text().strip()

    content = SKILL_MD_TEMPLATE.format(frontmatter=frontmatter, prompt=prompt)

    skill_provider_output_paths.root.mkdir(parents=True, exist_ok=True)
    skill_provider_output_paths.skill_md_file.write_text(content)

    utils.copy_files(skill_paths.root, skill_provider_output_paths.root, exclude=skill_paths.reserved_paths)
    utils.copy_files(
        skill_provider_paths.root,
        skill_provider_output_paths.root,
        exclude=[skill_provider_paths.meta_yaml_file],
    )
