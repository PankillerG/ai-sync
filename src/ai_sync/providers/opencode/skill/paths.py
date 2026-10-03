from dataclasses import dataclass
from pathlib import Path


@dataclass
class SkillPaths:
    root: Path

    @property
    def meta_yaml_file(self) -> Path:
        return self.root / "meta.yaml"


@dataclass
class SkillOutputPaths:
    root: Path

    @property
    def skill_md_file(self) -> Path:
        return self.root / "SKILL.md"


@dataclass
class SkillDeployPaths:
    root: Path

    @property
    def skill_md_file(self) -> Path:
        return self.root / "SKILL.md"


@dataclass
class SkillDeployUserPaths:
    root: Path

    @property
    def skills_dir(self) -> Path:
        return self.root / ".config" / "opencode" / "skills"

    def skill_paths(self, skill_name: str) -> SkillDeployPaths:
        return SkillDeployPaths(root=self.skills_dir / skill_name)


@dataclass
class SkillDeployProjectPaths:
    root: Path

    @property
    def skills_dir(self) -> Path:
        return self.root / ".opencode" / "skills"

    def skill_paths(self, skill_name: str) -> SkillDeployPaths:
        return SkillDeployPaths(root=self.skills_dir / skill_name)
