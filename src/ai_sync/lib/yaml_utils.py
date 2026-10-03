from pathlib import Path

import yaml


def load(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f) or {}


def load_from_files(yaml_files: list[Path]) -> dict:
    fields = dict()

    for yaml_file in yaml_files:
        if not yaml_file.exists():
            continue
        fields.update(load(yaml_file))

    return fields


class IndentDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


def get_frontmatter(fields: dict) -> str:
    body = yaml.dump(
        fields,
        Dumper=IndentDumper,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
    ).rstrip()
    if body == "{}":
        body = ""
    return f"---\n{body}\n---"


# The markdown body after the closing "---" is a second YAML document, which is never parsed.
def load_frontmatter(path: Path) -> dict:
    with open(path) as f:
        fields = next(yaml.safe_load_all(f), None)
    return fields if isinstance(fields, dict) else {}
