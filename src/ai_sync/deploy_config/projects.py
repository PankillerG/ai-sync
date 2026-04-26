from ai_sync.lib import jinja_utils


PROJECTS_TEMPLATE = """\
projects:
{% if projects %}
{% for alias, path in projects %}
  {{ alias }}: {{ path }}
{% endfor %}
{% else %}
  # <alias>: /path/to/your/project
{% endif %}
"""


def render(projects: dict[str, str]) -> str:
    return jinja_utils.render(PROJECTS_TEMPLATE, {
        "projects": projects.items() if projects else None,
    })
