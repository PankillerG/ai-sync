from ai_sync.deploy_config.models import SkillTargets
from ai_sync.lib import jinja_utils


SKILLS_TEMPLATE = """\
skills:
{% for name, targets in active_skills_targets %}
  {{ name }}:
  {% for target in targets %}
    - {{ target }}
  {% endfor %}
{% endfor %}
{% for name in new_skill_names %}
  # {{ name }}:
  #   - user
  #   - project:<your-project>
{% endfor %}
"""


def render(
    active_skills: dict[str, SkillTargets],
    new_skill_names: list[str],
) -> str:
    active_skills_raw_targets = {
        name: entry.raw_targets
        for name, entry in active_skills.items()
    }
    return jinja_utils.render(SKILLS_TEMPLATE, {
        "active_skills_targets": active_skills_raw_targets.items(),
        "new_skill_names": new_skill_names,
    })
