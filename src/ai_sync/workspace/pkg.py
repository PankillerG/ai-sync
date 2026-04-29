from dataclasses import dataclass
from pathlib import Path

from ai_sync import config
from ai_sync.entities import EntityType
from ai_sync.providers import ProviderName
from ai_sync.workspace.entity import ENTITY_TYPE_DIRS
from ai_sync.workspace.rule import RulePaths
from ai_sync.workspace.skill import SkillPaths


@dataclass
class Pkg:
    root: Path

    @property
    def providers_dir(self) -> Path:
        return self.root / "providers"

    def provider_dir(self, provider_name: ProviderName) -> Path:
        return self.providers_dir / provider_name

    @property
    def templates_dir(self) -> Path:
        return self.root / "templates"

    def entity_template_dir(self, entity_type: EntityType) -> Path:
        return self.templates_dir / ENTITY_TYPE_DIRS[entity_type]

    @property
    def skill_template_dir(self):
        return self.entity_template_dir(EntityType.SKILL)

    @property
    def skill_template_paths(self) -> SkillPaths:
        return SkillPaths(root=self.skill_template_dir)

    @property
    def rule_template_dir(self):
        return self.entity_template_dir(EntityType.RULE)

    @property
    def rule_template_paths(self) -> RulePaths:
        return RulePaths(root=self.rule_template_dir)


pkg = Pkg(root=config.PACKAGE_DIR)
