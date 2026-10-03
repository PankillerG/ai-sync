from typing import Callable

from ai_sync.providers import ProviderName
from ai_sync.providers.claude import (
    rule_clear as claude_rule_clear,
    rule_deploy as claude_rule_deploy,
    rule_generate as claude_rule_generate,
    skill_clear as claude_skill_clear,
    skill_deploy as claude_skill_deploy,
    skill_generate as claude_skill_generate,
)
from ai_sync.providers.codex import (
    rule_clear as codex_rule_clear,
    rule_deploy as codex_rule_deploy,
    rule_generate as codex_rule_generate,
    skill_clear as codex_skill_clear,
    skill_deploy as codex_skill_deploy,
    skill_generate as codex_skill_generate,
)
from ai_sync.providers.opencode import (
    rule_clear as opencode_rule_clear,
    rule_deploy as opencode_rule_deploy,
    rule_generate as opencode_rule_generate,
    skill_clear as opencode_skill_clear,
    skill_deploy as opencode_skill_deploy,
    skill_generate as opencode_skill_generate,
)


SKILL_GENERATORS: dict[ProviderName, Callable] = {
    ProviderName.CLAUDE: claude_skill_generate,
    ProviderName.CODEX: codex_skill_generate,
    ProviderName.OPENCODE: opencode_skill_generate,
}

SKILL_CLEANERS: dict[ProviderName, Callable] = {
    ProviderName.CLAUDE: claude_skill_clear,
    ProviderName.CODEX: codex_skill_clear,
    ProviderName.OPENCODE: opencode_skill_clear,
}

SKILL_DEPLOYERS: dict[ProviderName, Callable] = {
    ProviderName.CLAUDE: claude_skill_deploy,
    ProviderName.CODEX: codex_skill_deploy,
    ProviderName.OPENCODE: opencode_skill_deploy,
}

RULE_GENERATORS: dict[ProviderName, Callable] = {
    ProviderName.CLAUDE: claude_rule_generate,
    ProviderName.CODEX: codex_rule_generate,
    ProviderName.OPENCODE: opencode_rule_generate,
}

RULE_CLEANERS: dict[ProviderName, Callable] = {
    ProviderName.CLAUDE: claude_rule_clear,
    ProviderName.CODEX: codex_rule_clear,
    ProviderName.OPENCODE: opencode_rule_clear,
}

RULE_DEPLOYERS: dict[ProviderName, Callable] = {
    ProviderName.CLAUDE: claude_rule_deploy,
    ProviderName.CODEX: codex_rule_deploy,
    ProviderName.OPENCODE: opencode_rule_deploy,
}
