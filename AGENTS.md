# ContextEngineering

Source library of reusable agents (`*.agent.md`) and skills (`SKILL.md`) that other repositories copy or link in. It holds no application code, build or tests. This file complements `README.md` (agent and skill catalogue) and `docs/skill-authoring-guide.md` (how to write a skill); it does not repeat them.

## Layout

- `.agents/<name>/<name>.agent.md` - agents, one folder each (reviewer, class-optimizer, harness-generator). The folder, the file stem and the frontmatter `name` are identical.
- `.agents/skills/<name>/SKILL.md` - skills, with optional `references/` and `scripts/`. The folder name equals the skill `name`.
- `docs/` - the skill authoring guide and `templates/skill-template.md` (the only copy of the template).
- `README.md` - catalogue of agents and skills. Update it in the same change that adds, renames or removes one.

## Conventions

- Refer to a skill by name ("Load the `check-srp` skill"), never by file path, so the reference survives however the skill is installed.
- An agent points to a skill with a one-line reference. Do not inline skill content into an agent.
- New and edited skills follow the `skill-creator` skill: description with trigger phrases, `metadata` block, body of at most 80 lines (blank lines count), detail moved to `references/`.
- Agent frontmatter: `name` equals the agent's folder and file stem in kebab-case, there is no `model` pin, and `argument-hint` examples use placeholders instead of personal paths. Each description ends with a `Do not use for ...` sentence that names the sibling agent or skill.
- After writing or editing a skill, check it with the `agent-skill-review` skill. There is no CI here, so this is the only gate.

## Gotchas

- This repo is standalone. Agent and skill files reference only each other and `docs/`. Do not add references to agents, skills, repos or tooling outside it, and do not write stubs for such files.
- `edit-memory-file` ships a script (`scripts/check-memory.py`). Run it as `python3 -I`, as the skill instructs.

## Verification

No tests or build. After a change, grep for stale paths (`grep -rn "skills/" .agents README.md docs`) and confirm every `[link](path)` in `README.md` and `docs/` resolves.