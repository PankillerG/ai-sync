from dataclasses import dataclass
from pathlib import Path

from ai_sync.providers import ProviderName


@dataclass
class SkillPaths:
    root: Path

    @property
    def meta_yaml_file(self) -> Path:
        return self.root / "meta.yaml"

    @property
    def prompt_md_file(self) -> Path:
        return self.root / "prompt.md"

    @property
    def providers_dir(self) -> Path:
        return self.root / "providers"

    def provider_dir(self, provider_name: ProviderName) -> Path:
        return self.providers_dir / provider_name


@dataclass
class SkillOutputPaths:
    root: Path

    @property
    def providers_dir(self) -> Path:
        return self.root / "providers"

    def provider_dir(self, provider_name: ProviderName) -> Path:
        return self.providers_dir / provider_name
