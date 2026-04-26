from dataclasses import (
    dataclass,
    field,
)

from pathlib import Path


class SectionNames:
    projects = "projects"
    skills = "skills"
    rules = "rules"


@dataclass(frozen=True)
class ResolvedTarget:
    kind: str
    path: Path


@dataclass
class SkillTargets:
    raw_targets: list[str]
    targets: list[ResolvedTarget]


@dataclass
class RuleTargets:
    raw_targets: list[str]
    targets: list[ResolvedTarget]


@dataclass
class DeployConfig:
    projects: dict[str, str] = field(default_factory=dict)
    skills: dict[str, SkillTargets] = field(default_factory=dict)
    rules: dict[str, RuleTargets] = field(default_factory=dict)
