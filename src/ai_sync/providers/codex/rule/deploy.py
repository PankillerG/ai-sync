from pathlib import Path

from ai_sync.deploy_config.models import ResolvedTarget
from ai_sync.lib import jinja_utils
from ai_sync.providers.codex.rule.paths import (
    RuleDeployProjectPaths,
    RuleDeployUserPaths,
)


RULE_BLOCK_TEMPLATE = """\
## {{ rule_name }}

{% for sub_rule in sub_rules %}
### {{ sub_rule.name }}

{{ sub_rule.content }}
{% if not loop.last %}

{% endif %}
{% endfor %}
"""


def _render_rule_text(rule_name: str, rule_provider_output_dir: Path) -> str:
    subrules_md_files = sorted(f for f in rule_provider_output_dir.glob("*.md") if f.is_file())
    sub_rules = [
        {"name": f.stem, "content": f.read_text().strip()}
        for f in subrules_md_files
        if f.read_text().strip()
    ]
    rule_text = jinja_utils.render(
        RULE_BLOCK_TEMPLATE,
        template_vars={
            "rule_name": rule_name,
            "sub_rules": sub_rules,
        },
    )
    return rule_text


def deploy(
    target: ResolvedTarget,
    rules: list[tuple[str, Path]],
) -> None:
    if target.kind == "user":
        rule_deploy_paths = RuleDeployUserPaths(root=target.path)
    elif target.kind == "project":
        rule_deploy_paths = RuleDeployProjectPaths(root=target.path)

    rules_texts = [
        _render_rule_text(rule_name, rule_provider_output_dir)
        for rule_name, rule_provider_output_dir in rules
    ]
    content = "\n".join(rules_texts)

    rule_deploy_paths.agents_md_file.parent.mkdir(parents=True, exist_ok=True)
    rule_deploy_paths.agents_md_file.write_text(content)
