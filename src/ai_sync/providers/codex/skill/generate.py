import shutil
from pathlib import Path

from ai_sync.lib import yaml_utils
from ai_sync.providers.codex.skill.paths import (
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

    common_meta = yaml_utils.load(skill_paths.meta_yaml_file)
    frontmatter = yaml_utils.get_frontmatter(common_meta)
    prompt = skill_paths.prompt_md_file.read_text().strip()

    content = SKILL_MD_TEMPLATE.format(frontmatter=frontmatter, prompt=prompt)

    skill_provider_output_paths.root.mkdir(parents=True, exist_ok=True)
    skill_provider_output_paths.skill_md_file.write_text(content)

    skill_provider_output_paths.agents_openai_yaml_file.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(skill_provider_paths.agents_openai_yaml_file, skill_provider_output_paths.agents_openai_yaml_file)
