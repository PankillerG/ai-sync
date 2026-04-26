from typing import Callable

from ai_sync.providers import ProviderName
from ai_sync.providers.claude_code import (
    rule_deploy as claude_code_rule_deploy,
    rule_generate as claude_code_rule_generate,
    skill_deploy as claude_code_skill_deploy,
    skill_generate as claude_code_skill_generate,
)
from ai_sync.providers.codex import (
    rule_deploy as codex_rule_deploy,
    rule_generate as codex_rule_generate,
    skill_deploy as codex_skill_deploy,
    skill_generate as codex_skill_generate,
)
from ai_sync.providers.opencode import (
    rule_deploy as opencode_rule_deploy,
    rule_generate as opencode_rule_generate,
    skill_deploy as opencode_skill_deploy,
    skill_generate as opencode_skill_generate,
)


SKILL_GENERATORS: dict[ProviderName, Callable] = {
    ProviderName.CLAUDE_CODE: claude_code_skill_generate,
    ProviderName.CODEX: codex_skill_generate,
    ProviderName.OPENCODE: opencode_skill_generate,
}

SKILL_DEPLOYERS: dict[ProviderName, Callable] = {
    ProviderName.CLAUDE_CODE: claude_code_skill_deploy,
    ProviderName.CODEX: codex_skill_deploy,
    ProviderName.OPENCODE: opencode_skill_deploy,
}

RULE_GENERATORS: dict[ProviderName, Callable] = {
    ProviderName.CLAUDE_CODE: claude_code_rule_generate,
    ProviderName.CODEX: codex_rule_generate,
    ProviderName.OPENCODE: opencode_rule_generate,
}

RULE_DEPLOYERS: dict[ProviderName, Callable] = {
    ProviderName.CLAUDE_CODE: claude_code_rule_deploy,
    ProviderName.CODEX: codex_rule_deploy,
    ProviderName.OPENCODE: opencode_rule_deploy,
}
