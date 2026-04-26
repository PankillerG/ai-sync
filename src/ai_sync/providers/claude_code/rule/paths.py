from dataclasses import dataclass
from pathlib import Path


@dataclass
class RuleProviderPaths:
    root: Path

    @property
    def meta_yaml_file(self) -> Path:
        return self.root / "meta.yaml"

    def subrule_meta_yaml_file(self, subrule_name: str) -> Path:
        return self.root / f"{subrule_name}.yaml"


@dataclass
class RuleOutputPaths:
    root: Path

    def subrule_md_file(self, subrule_name: str) -> Path:
        return self.root / f"{subrule_name}.md"


@dataclass
class RuleDeployUserPaths:
    root: Path

    @property
    def rules_dir(self) -> Path:
        return self.root / ".claude" / "rules"

    def rule_dir(self, rule_name) -> Path:
        return self.rules_dir / rule_name


@dataclass
class RuleDeployProjectPaths:
    root: Path

    @property
    def rules_dir(self) -> Path:
        return self.root / ".claude" / "rules"
    
    def rule_dir(self, rule_name) -> Path:
        return self.rules_dir / rule_name
