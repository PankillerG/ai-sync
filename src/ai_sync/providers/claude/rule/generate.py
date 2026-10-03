from pathlib import Path

from ai_sync.lib import yaml_utils
from ai_sync.providers.claude.rule.paths import (
    RuleOutputPaths as RuleProviderOutputPaths,
    RuleProviderPaths,
)
from ai_sync.workspace.rule import RulePaths


RULE_MD_TEMPLATE = """\
{frontmatter}

{body}
"""


def generate(
    rule_paths: RulePaths,
    rule_provider_dir: Path,
    rule_provider_output_dir: Path,
) -> None:
    subrules_md_files = sorted(file for file in rule_paths.root.glob("*.md") if file.is_file())
    if not subrules_md_files:
        return

    rule_provider_paths = RuleProviderPaths(root=rule_provider_dir)
    rule_provider_output_paths = RuleProviderOutputPaths(root=rule_provider_output_dir)
    rule_provider_output_paths.root.mkdir(parents=True, exist_ok=True)

    for subrule_md_file in subrules_md_files:
        subrule_name = subrule_md_file.stem

        frontmatter_fields = yaml_utils.load_from_files([
            rule_provider_paths.meta_yaml_file,
            rule_provider_paths.subrule_meta_yaml_file(subrule_name),
        ])
        frontmatter = yaml_utils.get_frontmatter(frontmatter_fields) if frontmatter_fields else ""

        content = RULE_MD_TEMPLATE.format(
            frontmatter=frontmatter,
            body=subrule_md_file.read_text(),
        ).strip()

        rule_provider_output_paths.subrule_md_file(subrule_name).write_text(content)
