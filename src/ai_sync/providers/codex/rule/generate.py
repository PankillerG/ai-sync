import shutil
from pathlib import Path

from ai_sync.providers.codex.rule.paths import RuleOutputPaths as RuleProviderOutputPaths
from ai_sync.workspace.rule import RulePaths


def generate(
    rule_paths: RulePaths,
    rule_provider_dir: Path,
    rule_provider_output_dir: Path,
) -> None:
    subrules_md_files = sorted(file for file in rule_paths.root.glob("*.md") if file.is_file())
    if not subrules_md_files:
        return

    rule_provider_output_paths = RuleProviderOutputPaths(root=rule_provider_output_dir)
    rule_provider_output_paths.root.mkdir(parents=True, exist_ok=True)

    for subrule_md_file in subrules_md_files:
        subrule_name = subrule_md_file.stem
        shutil.copy2(subrule_md_file, rule_provider_output_paths.subrule_md_file(subrule_name))
