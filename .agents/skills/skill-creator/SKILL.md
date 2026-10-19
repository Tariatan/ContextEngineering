---
name: skill-creator
description: Authors, extracts, or updates a SKILL.md per the Roche Skill Authoring Guide - skill vs instruction-file decision, description with trigger phrases, 80-line body template, metadata, risk, semver, and the four body shapes. Use when the user says "create a skill", "new SKILL.md", "extract this into a skill", or "update a skill", or when duplicated instructions should leave an agent file. Do not use for .agent.md files or for always-applicable rules (those belong in AGENTS.md).
metadata:
  version: 2.0.0
  status: active
  last-reviewed: 2026-10-15
  risk: low
---

# Skill Creator

## Critical

- NEVER commit or push a skill without explicit user confirmation.
- NEVER leave template placeholders, unused sections, or HTML comments in a finished skill.
- If Step 1 fails, stop and recommend the cheaper primitive. Do not write the skill.

## Scope

- Use for: creating a skill; extracting a duplicated or conditional procedure from an agent; bringing an existing skill in line with the guide.
- Not for: agent files; rules that apply to every task; one-off prompts.
- Prerequisites: `docs/templates/skill-template.md` exists in this repo; verify with `ls docs/templates/`.

## Instructions

1. **DECIDE**: A rule that applies to every task is an instruction. Something the human always invokes by name is a prompt file. Only knowledge the agent must decide to load is a skill, and it must also span multiple files, need more than a few rules, and have a detectable trigger pattern. Expected: a one-line verdict.
2. **PLAN**: Write 2-3 use cases (trigger phrases, steps, result). Record what the agent gets wrong today and leave out what the model already does well. Fewer than 2 cases means an instruction; more than 3 means two skills.
3. **SCAFFOLD**: Copy `docs/templates/skill-template.md` to `.agents/skills/<name>/SKILL.md`. The name is kebab-case `domain-object-action`, equals the directory name, and never starts with `claude` or `anthropic` or is `helper`/`utils`/`misc`.
4. **DESCRIBE**: Write what it does, then "Use when" with literal phrases and artefact names users type (file extensions, repo and tool names), then "Do not use for" a near miss. Under 1024 characters, no angle brackets, never starting with "This skill". It is the only always-loaded part.
5. **WRITE THE BODY**: At most 80 lines including blanks. Order: H1, `## Critical` (destructive rules first), `## Scope` (three bullets, `none` when empty), `## Instructions`. One numbered line per step: `N. **NAME**: what happens. Expected: observable result.` Use literal commands and explicit gates, and bundle a script for anything with a definite right answer. Pick the shape from `references/body-shapes.md` before writing steps. Shared-library skills also need `## Usage`: purpose, golden-path example, misuse, message contracts, threading and lifecycle.
6. **SET METADATA**: `version` (semver: major for changed triggers, steps or script arguments; minor for new step, file or broader description; patch for wording), `status` (draft, active, deprecated), `last-reviewed` date, `risk`, `owner` (a team), `source-repository` (bare https URL). `risk: high` applies when the skill pre-approves `shell` or acts irreversibly without confirmation, and then needs a `## Critical` list of what it never does unasked. Never pre-approve tools on High Risk units.
7. **BUNDLE**: Put rare detail in `references/`, each file linked with the condition for opening it. Scripts go in `scripts/`, fill-in templates in `assets/`. No secrets, internal hostnames, or verbatim third-party copyrighted text.
8. **VERIFY**: Check the list below, then in a fresh session ask "When would you use the NAME skill?" Expected: the answer matches the intent. Edit the description for any gap.
9. **LAND**: Shared skills follow the repo's documented commit and PR procedure after user confirmation. A private skill gets a `.gitignore` containing `*` inside its directory.

## Definition of done

- [ ] `name` equals the directory name; description meets Step 4; body is at most 80 lines.
- [ ] No placeholder text, unused section, or HTML comment remains.
- [ ] Every extracted block in its former caller is now a pointer to this skill.
- [ ] Placement: written once under `.agents/skills/`. No second copy.

## Examples

- "Create a skill for triaging failing pipelines" → Step 1 (conditional, multi-file: skill), Step 2 (three use cases), Steps 3-5. Result: `.agents/skills/ado-build-failure-triage/SKILL.md`.
- "Always use file-scoped namespaces, make that a skill" → Step 1 fails. Result: recommend a line in `AGENTS.md`.

## Troubleshooting

- **Skill does not load, or its frontmatter shows up as text** - cause: an unquoted description containing a colon followed by a space (for example "rule keys such as rust: or secrets:") breaks YAML parsing. Fix: reword the sentence without it or wrap the description in double quotes, then parse the frontmatter with a YAML parser to confirm.
- **Review reports an unreferenced file** - cause: a file in `references/` or `scripts/` has no line in SKILL.md saying when to open it. Fix: add that line.

## References

- `docs/templates/skill-template.md` - copy in Step 3; its inline markers say which sections are required.
- `references/body-shapes.md` - read before Step 5 to choose between checklist, procedure, lookup and handoff shapes.
