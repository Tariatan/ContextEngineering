# Context Engineering

Reusable, project-agnostic agents and skills, meant to be shared across repositories.

## Agents

- **[Reviewer](reviewer.agent.md)** — senior-engineer code review for pull requests, local diffs, or uncommitted changes. Language-agnostic, with dedicated skills for C# and Rust.
- **[Class Optimizer](class-optimizer.agent.md)** — optimizes a single class for Single Responsibility adherence, efficiency, and dead/redundant code, and applies the fixes directly (unlike Reviewer, which only reports).

## Skills

Skills refine an agent's behavior for a specific language or concern. They are referenced by agents.

- `skills/check-logging/SKILL.md` — language-agnostic structured-logging review checklist.
- `skills/check-changelog-versioning/SKILL.md` — deterministic changelog (Keep a Changelog) and SemVer version-bump check.
- `skills/check-srp/SKILL.md` — Single Responsibility, efficiency, and dead-code checklist for a class; referenced by both Reviewer (report) and Class Optimizer (fix).
- `skills/edit-memory-file/SKILL.md` — procedure for creating or editing `MEMORY.md` and its topic files (index format, load limits, what to save or prune); standalone, not referenced by an agent.
- `skills/agent-skill-review/SKILL.md` - reviews a skill folder against the SKILL.md template (frontmatter, body and scope rules in its `references/`) and reports blockers, warnings and advisories with a PASS or FAIL verdict; standalone, not referenced by an agent.
- `skills/review-csharp/SKILL.md` — C# / .NET review guidelines.
- `skills/review-rust/SKILL.md` — Rust review guidelines.

## Docs

- `docs/skill-authoring-guide.md` - how to decide whether you need a skill, write it, ship it, and test it.
- `docs/templates/skill-template.md` - copy-to-start `SKILL.md` skeleton, with every section marked required, recommended or optional. Copy it to `skills/<your-skill-name>/SKILL.md` and check the result with `skills/agent-skill-review`.
