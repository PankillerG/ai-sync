from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

from ai_sync.entities import EntityType
from ai_sync.workspace.entity import ENTITY_TYPE_DIRS
from ai_sync.workspace.rule import RuleOutputPaths
from ai_sync.workspace.skill import SkillOutputPaths


@dataclass
class OutputPaths:
    root: Path

    @property
    def skills_dir(self) -> Path:
        return self.root / ENTITY_TYPE_DIRS[EntityType.SKILL]

    def skill_paths(self, name) -> SkillOutputPaths:
        return SkillOutputPaths(root=self.skills_dir / name)

    @property
    def rules_dir(self) -> Path:
        return self.root / ENTITY_TYPE_DIRS[EntityType.RULE]

    def rule_paths(self, name) -> RuleOutputPaths:
        return RuleOutputPaths(root=self.rules_dir / name)


@dataclass
class Workspace:
    root: Path

    def entities_dir(self, entity_type: EntityType) -> Path:
        return self.root / ENTITY_TYPE_DIRS[entity_type]

    def entity_dir(self, entity_type: EntityType, name: str) -> Path:
        return self.entities_dir(entity_type) / name

    @property
    def skills_dir(self) -> Path:
        return self.entities_dir(EntityType.SKILL)

    @property
    def rules_dir(self) -> Path:
        return self.entities_dir(EntityType.RULE)

    @cached_property
    def output_paths(self) -> OutputPaths:
        return OutputPaths(self.root / "output")

    @property
    def deploy_yaml_file(self) -> Path:
        return self.root / "deploy.yaml"
