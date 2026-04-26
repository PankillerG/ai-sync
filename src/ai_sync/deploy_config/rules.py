from ai_sync.deploy_config.models import RuleTargets
from ai_sync.lib import jinja_utils


RULES_TEMPLATE = """\
rules:
{% for name, targets in active_rules_targets %}
  {{ name }}:
  {% for target in targets %}
    - {{ target }}
  {% endfor %}
{% endfor %}
{% for name in new_rule_names %}
  # {{ name }}:
  #   - user
  #   - project:<your-project>
{% endfor %}
"""


def render(
    active_rules: dict[str, RuleTargets],
    new_rule_names: list[str],
) -> str:
    active_rules_raw_targets = {
        name: entry.raw_targets
        for name, entry in active_rules.items()
    }
    return jinja_utils.render(RULES_TEMPLATE, {
        "active_rules_targets": active_rules_raw_targets.items(),
        "new_rule_names": new_rule_names,
    })
