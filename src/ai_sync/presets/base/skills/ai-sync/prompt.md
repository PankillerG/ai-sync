# ai-sync

Skills and rules on this machine are managed by `ai-sync`. Each skill or rule is written once in an ai-sync source directory, and `ai-sync deploy` generates the files Claude Code, Codex, and OpenCode expect and puts them where each provider looks for them.

## Never edit deployed files

Do not create or edit skills and rules in provider directories: `~/.claude/skills/`, `~/.claude/rules/`, `~/.agents/skills/`, `~/.codex/AGENTS.md`, `~/.config/opencode/`, or their project counterparts `.claude/`, `.agents/`, `.opencode/`, `AGENTS.md`, `ai-sync-rules/`.

`ai-sync deploy` deletes and rewrites what it manages, so manual edits there are lost:

- skills whose `SKILL.md` frontmatter has `metadata: {managed-by: ai-sync}`;
- Claude Code `rules/ai-sync/` and OpenCode `ai-sync-rules/`;
- Codex `AGENTS.md`, even if it was written by hand.

Skills without the `managed-by: ai-sync` marker belong to other tools or were written by hand. Leave them alone. If the user asks to change one, offer to move it into ai-sync first.

## Choose the scope

| Scope | Source directory | `--dir` | Deployed to |
| --- | --- | --- | --- |
| user | `~/.config/ai-sync/` | omit it | user-level configs of every provider |
| project | `<project>/.ai-sync/` | `--dir <project>` | that project |

Pick the scope in this order:

1. The user said where it goes ("for this project", "globally", "for all my projects").
2. Project: the current repository already has `.ai-sync/`, or the content is about this project only (its code, build, conventions).
3. User: the content is personal or applies across projects (preferences, general workflows).
4. Otherwise ask the user.

`<project>` is the repository root, not the current subdirectory. In a project, make sure `.ai-sync/output/` is in `.gitignore`.

## Workflow

1. Look for an existing entity first: `<source>/skills/<name>/` or `<source>/rules/<name>/`. If it exists, edit it instead of creating a new one.
2. Create a new one from the template:
   ```bash
   ai-sync init skill <name> [--dir <project>]
   ai-sync init rule <name> [--dir <project>]
   ```
   Use lowercase names with hyphens. The name `ai-sync` is reserved.
3. Fill in the generated files and remove every template placeholder (`TODO`, `describe what this skill does`).
4. Deploy it yourself and report the result:
   ```bash
   ai-sync deploy [--dir <project>]
   ```
   `ai-sync deploy` covers every provider by default; `--providers claude codex opencode` limits it. If deploy fails, fix the source files and run it again.
5. To delete a skill or rule, remove its source directory and deploy again.

`ai-sync <command> --help` lists all options.

## Skill layout

```text
skills/<name>/
  meta.yaml                    shared frontmatter: name, description
  prompt.md                    skill body, becomes SKILL.md after the frontmatter
  scripts/, references/, ...   any other files, copied next to SKILL.md for every provider
  providers/
    claude/meta.yaml           extra Claude Code frontmatter
    opencode/meta.yaml         extra OpenCode frontmatter
    codex/agents/openai.yaml   Codex UI and invocation policy
    <provider>/<other files>   copied only for that provider
```

- `name` in `meta.yaml` must match the directory name.
- `description` says what the skill does and when to use it; agents decide whether to load the skill from it alone.
- Reference supporting files from `prompt.md` by paths relative to the skill directory, such as `scripts/fetch.py`.
- Do not write `SKILL.md` in the source. Two files that end up at the same path stop the deploy with an error.
- Codex takes frontmatter only from the shared `meta.yaml`.

## Rule layout

```text
rules/<name>/
  <part>.md                    rule text; a rule may have several parts
  providers/
    claude/meta.yaml           Claude Code frontmatter for every part, such as `paths`
    claude/<part>.yaml         frontmatter for one part, merged over meta.yaml
```

- Rules are always in the agent's context: keep them short and imperative, and move long procedures into a skill.
- Claude Code gets each part as a separate file under `rules/ai-sync/<name>/`; `paths` limits a part to matching files.
- Codex gets all rules concatenated into one `AGENTS.md`, sorted by rule name, with `## <name>` and `### <part>` headings.
- OpenCode gets the parts under `ai-sync-rules/<name>/`, listed in `opencode.json` `instructions`.

## Provider metadata

Provider-specific fields follow each provider's own format:

- Claude Code skills: https://code.claude.com/docs/en/skills
- Claude Code rules: https://code.claude.com/docs/en/memory
- Codex skills: https://developers.openai.com/codex/skills
- OpenCode skills: https://opencode.ai/docs/skills/
