from pathlib import Path

from ai_sync.deploy_config.models import ResolvedTarget


def resolve_target(raw_target: str, projects: dict[str, str]) -> ResolvedTarget:
    if raw_target == "user":
        return ResolvedTarget(kind="user", path=Path.home())

    elif raw_target.startswith("project:"):
        project_alias = raw_target.split(":", 1)[1]
        if project_alias not in projects:
            raise ValueError(f"Unknown project alias '{project_alias}' in deploy config")
        return ResolvedTarget(kind="project", path=Path(projects[project_alias]))
    
    else:
        raise ValueError(f"Unknown target type: '{raw_target}'") 


def resolve_targets(targets: list[str], projects: dict[str, str]) -> list[ResolvedTarget]:
    resolved_targets = []
    for target in targets:
        resolved_targets.append(resolve_target(target, projects))
    return resolved_targets
