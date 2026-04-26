import jinja2


env = jinja2.Environment(trim_blocks=True, lstrip_blocks=True)


def render(template: str, template_vars: dict) -> str:
    return env.from_string(template).render(**template_vars)
