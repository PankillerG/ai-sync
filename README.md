# ai-sync

> Write AI skills and rules once, then use them across Claude Code, Codex, and OpenCode.

## Why

AI coding tools use different file formats and different config locations for
the same kind of instructions. If you use more than one tool, keeping the same
skills and rules in sync by hand becomes repetitive and easy to get wrong.

`ai-sync` gives you one place to maintain that content. It generates the files
each provider expects and deploys them either globally or into specific
projects.

## Features

- Keep shared skills and rules in one place.
- Generate provider-ready files for Claude Code, Codex, and OpenCode.
- Deploy globally or to selected projects.
- Use provider-specific metadata when a provider supports it.

## Requirements

- Python >= 3.12
- [pipx](https://pipx.pypa.io/) recommended, or plain `pip`

## Installation

```bash
# from GitHub
pipx install git+https://github.com/pankillerg/ai-sync.git

# from a local clone
pipx install .
```

After install, the `ai-sync` command is available on your `PATH`.

## Quick start

Create a skill:

```bash
ai-sync init skill research
```

Edit the generated files:

```text
~/.config/ai-sync/skills/research/meta.yaml
~/.config/ai-sync/skills/research/prompt.md
```

Generate provider-specific output:

```bash
ai-sync generate
```

Refresh the deploy config:

```bash
ai-sync update deploy-config
```

Open `~/.config/ai-sync/deploy.yaml`, uncomment the new skill, and choose where
to deploy it:

```yaml
skills:
  research:
    - user
```

Deploy:

```bash
ai-sync deploy
```

## Commands

| Command | Description |
| --- | --- |
| `ai-sync init <skill\|rule> <name>` | Create a new skill or rule from a template. |
| `ai-sync generate` | Generate provider-specific files. |
| `ai-sync update deploy-config` | Refresh `deploy.yaml` from generated skills and rules. |
| `ai-sync deploy` | Copy generated files to the selected targets. |

Use `--dir <path>` to choose a different working directory. The default is
`~/.config/ai-sync`.

## Skills

A skill has shared content plus optional provider-specific metadata:

```text
skills/research/
  meta.yaml
  prompt.md
  providers/
    claude-code/
      meta.yaml
    codex/
      agents/openai.yaml
```

`meta.yaml` and `prompt.md` are the content you maintain. A provider directory
enables that provider for the skill.

Provider metadata follows the provider's own format:

- Claude Code skill fields: [Claude Code skills](https://code.claude.com/docs/en/skills)
- Codex skill fields: [Codex skills](https://developers.openai.com/codex/skills)
- OpenCode skill fields: [OpenCode skills](https://opencode.ai/docs/skills/)

## Rules

A rule is one or more Markdown files:

```text
rules/python-standards/
  style.md
  imports.md
  async.md
```

Rules are generated for every supported rule provider. For Claude Code, you can
add provider metadata when you need provider-specific behavior such as scoped
paths:

```text
rules/python-standards/
  providers/
    claude-code/
      meta.yaml
      imports.yaml
```

Claude Code rule metadata follows the provider's format:
[Claude Code memory](https://code.claude.com/docs/en/memory).

## Deploy config

`deploy.yaml` decides what gets deployed and where:

```yaml
projects:
  work: /home/me/code/work-monorepo
  side: /home/me/code/side-project

skills:
  research:
    - user
    - project:work

rules:
  security:
    - user
  python-standards:
    - user
    - project:work
```

- `projects` maps aliases to project paths.
- `user` deploys to your global provider config.
- `project:<alias>` deploys to a project from `projects`.

Run `ai-sync update deploy-config` after adding or removing skills and rules.
New entries are added as commented templates, so you can opt in before deploy.

For Codex rules, the order of entries under `rules` is the order used in the
generated `AGENTS.md`.

## Generated files

You edit the source files under `skills/`, `rules/`, and `deploy.yaml`.
`ai-sync generate` writes provider-specific files under `output/`; that
directory is generated and can be recreated at any time.

`ai-sync deploy` treats deployed files as managed output:

- Claude Code and OpenCode rule directories for selected rules are replaced.
- Codex `AGENTS.md` is rewritten from selected rules.
- OpenCode `opencode.json` is preserved, with missing `instructions` entries
  appended.

## Provider support

| Entity | Claude Code | Codex | OpenCode |
| --- | :---: | :---: | :---: |
| skill | ✓ | ✓ | ✓ |
| rule  | ✓ | ✓ | ✓ |

## Deploy locations

Most users do not need these paths day to day, but they are useful when you
want to inspect what `ai-sync deploy` changed.

| Entity | Provider | User target | Project target | Provider docs |
| --- | --- | --- | --- | --- |
| skill | Claude Code | `~/.claude/skills/<name>/SKILL.md` | `<project>/.claude/skills/<name>/SKILL.md` | [skills](https://code.claude.com/docs/en/skills) |
| skill | Codex | `~/.agents/skills/<name>/` | `<project>/.agents/skills/<name>/` | [skills](https://developers.openai.com/codex/skills) |
| skill | OpenCode | `~/.config/opencode/skills/<name>/SKILL.md` | `<project>/.opencode/skills/<name>/SKILL.md` | [skills](https://opencode.ai/docs/skills/) |
| rule | Claude Code | `~/.claude/rules/<name>/*.md` | `<project>/.claude/rules/<name>/*.md` | [memory](https://code.claude.com/docs/en/memory) |
| rule | Codex | `~/.codex/AGENTS.md` | `<project>/AGENTS.md` | [rules](https://developers.openai.com/codex/rules) |
| rule | OpenCode | `~/.config/opencode/ai-sync-rules/<name>/*.md` | `<project>/ai-sync-rules/<name>/*.md` | [rules](https://opencode.ai/docs/rules/) |

## License

[MIT](LICENSE)
