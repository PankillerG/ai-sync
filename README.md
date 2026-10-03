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

Run a first deploy right away. It installs the built-in `ai-sync` skill and
rule, so your agents create skills and rules through `ai-sync` from now on
(see [Base preset](#base-preset)):

```bash
ai-sync deploy
```

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

Deploy it to your user-level configs of every provider:

```bash
ai-sync deploy
```

To keep skills and rules inside a project instead, pass the project directory:

```bash
ai-sync init skill research --dir ~/code/my-project
ai-sync deploy --dir ~/code/my-project
```

## Commands

| Command | Description |
| --- | --- |
| `ai-sync init <skill\|rule> <name> [--dir PATH]` | Create a new skill or rule from a template. |
| `ai-sync deploy [--dir PATH] [-p/--providers P ...]` | Generate provider-specific files and deploy them. |

`--dir` selects the scope, see [Scopes](#scopes). `-p`/`--providers` limits the
deploy to the listed providers (`claude`, `codex`, `opencode`); by
default every provider is used.

## Skills

A skill has shared content, optional supporting files, and optional
provider-specific metadata and files:

```text
skills/research/
  meta.yaml
  prompt.md
  scripts/
    fetch.py
  references/
    api.md
  providers/
    claude/
      meta.yaml
    codex/
      agents/openai.yaml
```

`meta.yaml` and `prompt.md` become the provider's `SKILL.md`. A provider
directory holds optional provider-specific settings; without it the skill is
still deployed for that provider, just without extra settings.

Every other file in the skill directory, such as `scripts/`, `references/` or
`assets/`, is copied next to `SKILL.md` for every provider. Files in a provider
directory, except its `meta.yaml`, are copied only for that provider. Reference
them from `prompt.md` with paths relative to the skill directory, such as
`scripts/fetch.py`. A file that would end up at the same path twice, including
`SKILL.md`, stops the deploy with an error.

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
    claude/
      meta.yaml
      imports.yaml
```

Claude Code rule metadata follows the provider's format:
[Claude Code memory](https://code.claude.com/docs/en/memory).

## Base preset

`ai-sync` ships with a base preset that every user-level deploy adds to your
own skills and rules:

- the `ai-sync` skill teaches agents where ai-sync sources live, how to pick
  the user or project scope, and how to lay out skills and rules;
- the `ai-sync` rule tells agents to create and edit skills and rules through
  `ai-sync` and run `ai-sync deploy`, instead of writing into provider
  directories.

When you ask an agent to add a skill or a rule, it writes the source under
`~/.config/ai-sync/` or `<project>/.ai-sync/` and deploys it to every provider.

The preset is not deployed to projects. Its skill and rule names are reserved:
`ai-sync init` and `ai-sync deploy` fail if your own skill or rule is named
`ai-sync`, in any scope.

## Scopes

`--dir` points to the scope root. The scope decides where skills and rules are
read from and where they are deployed:

| `--dir` | Reads from | Deploys to |
| --- | --- | --- |
| your home directory (default) | `~/.config/ai-sync/` | user-level provider configs |
| any other directory | `<dir>/.ai-sync/` | that project |

After `ai-sync deploy`, providers have exactly the skills and rules from
`~/.config/ai-sync/` plus the [base preset](#base-preset) (or
`<dir>/.ai-sync/`). Deleting a skill or rule there and
deploying again removes it from every provider. Skills and rules managed by
other tools or written by hand are left untouched.

Rules are deployed in alphabetical order of their names, which is also their
order in the generated Codex `AGENTS.md`.

## Generated files

You edit the source files under `skills/` and `rules/`. `ai-sync deploy`
first writes provider-specific files under `output/` next to them; that
directory is regenerated on every deploy. In a project, add `.ai-sync/output/`
to `.gitignore`.

For every provider it deploys to, `ai-sync deploy` first deletes what it
manages there and then writes the current skills and rules:

- skills whose `SKILL.md` frontmatter contains
  `metadata: {managed-by: ai-sync}`; `ai-sync` adds this field to every skill
  it deploys, so other skills are left untouched;
- the `ai-sync/` directory inside Claude Code `rules/` and the OpenCode
  `ai-sync-rules/` directory;
- the Codex `AGENTS.md`, even if it was not created by `ai-sync`; it is not
  recreated when there are no rules.

A skill directory with the same name as a deployed skill is replaced. OpenCode
`opencode.json` is preserved: only its `instructions` entries pointing into
`ai-sync-rules/` are replaced. The skill names `synced`, `anthropic-skills` and
`.trash` are reserved by Claude Code.

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
| skill | Claude Code | `~/.claude/skills/<name>/` | `<project>/.claude/skills/<name>/` | [skills](https://code.claude.com/docs/en/skills) |
| skill | Codex | `~/.agents/skills/<name>/` | `<project>/.agents/skills/<name>/` | [skills](https://developers.openai.com/codex/skills) |
| skill | OpenCode | `~/.config/opencode/skills/<name>/` | `<project>/.opencode/skills/<name>/` | [skills](https://opencode.ai/docs/skills/) |
| rule | Claude Code | `~/.claude/rules/ai-sync/<name>/*.md` | `<project>/.claude/rules/ai-sync/<name>/*.md` | [memory](https://code.claude.com/docs/en/memory) |
| rule | Codex | `~/.codex/AGENTS.md` | `<project>/AGENTS.md` | [rules](https://developers.openai.com/codex/rules) |
| rule | OpenCode | `~/.config/opencode/ai-sync-rules/<name>/*.md` | `<project>/ai-sync-rules/<name>/*.md` | [rules](https://opencode.ai/docs/rules/) |

## License

[MIT](LICENSE)
