from pathlib import Path

from ai_sync.lib import yaml_utils
from ai_sync.providers.claude_code.skill.paths import (
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
    skill_provider_paths = SkillProviderPaths(root=skill_provider_dir)
    skill_provider_output_paths = SkillProviderOutputPaths(root=skill_provider_output_dir)

    frontmatter_fields = yaml_utils.load_from_files(yaml_files=[
        skill_paths.meta_yaml_file,
        skill_provider_paths.meta_yaml_file,
    ])
    frontmatter = yaml_utils.get_frontmatter(frontmatter_fields)

    prompt = skill_paths.prompt_md_file.read_text().strip()

    content = SKILL_MD_TEMPLATE.format(frontmatter=frontmatter, prompt=prompt)

    skill_provider_output_paths.root.mkdir(parents=True, exist_ok=True)
    skill_provider_output_paths.skill_md_file.write_text(content)
