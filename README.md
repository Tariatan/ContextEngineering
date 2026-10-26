# Context Engineering

Reusable, project-agnostic agents and skills, meant to be shared across repositories.

This repository is standalone: its agents and skills reference only each other and the files under `docs/`, and never anything outside the repository.

## Agents

- **[Reviewer](.agents/reviewer/reviewer.agent.md)** — senior-engineer code review for pull requests, local diffs, or uncommitted changes. Language-agnostic, with dedicated skills for C# and Rust.
- **[Class Optimizer](.agents/class-optimizer/class-optimizer.agent.md)** — optimizes a single class for Single Responsibility adherence, efficiency, and dead/redundant code, and applies the fixes directly (unlike Reviewer, which only reports).
- **[Harness Generator](.agents/harness-generator/harness-generator.agent.md)** - bootstraps or refreshes a repository's `AGENTS.md` and `MEMORY.md` from git history and the repo's own docs. Presents drafts for review and never commits.

## Skills

Skills refine an agent's behavior for a specific language or concern. They are referenced by agents.

- `.agents/skills/check-logging/SKILL.md` — language-agnostic structured-logging review checklist.
- `.agents/skills/check-changelog-versioning/SKILL.md` — deterministic changelog (Keep a Changelog) and SemVer version-bump check.
- `.agents/skills/check-srp/SKILL.md` — Single Responsibility, efficiency, and dead-code checklist for a class; referenced by both Reviewer (report) and Class Optimizer (fix).
- `.agents/skills/edit-memory-file/SKILL.md` — procedure for creating or editing `MEMORY.md` and its topic files (index format, load limits, what to save or prune); standalone, not referenced by an agent.
- `.agents/skills/agent-skill-review/SKILL.md` - reviews a skill folder against the SKILL.md template (frontmatter, body and scope rules in its `references/`) and reports blockers, warnings and advisories with a PASS or FAIL verdict; standalone, not referenced by an agent.
- `.agents/skills/check-code-quality/SKILL.md` - correctness, security, architecture, dependency and design-complexity checklist; referenced by Reviewer, and usable by an implementing agent while it writes code.
- `.agents/skills/skill-creator/SKILL.md` - authors, extracts or updates a `SKILL.md` per the skill authoring guide and template; standalone, not referenced by an agent.
- `.agents/skills/writing-for-agents/SKILL.md` - reference for writing any document an agent consumes (skills, `AGENTS.md` / `CLAUDE.md`, pointed-at docs): context pointers, information hierarchy, completion criteria, leading words, with skill mechanics and pruning in its `references/`; adapted from an MIT-licensed upstream (credit in its `metadata`); standalone, not referenced by an agent.
- `.agents/skills/grilling/SKILL.md` - relentless interview in rounds of numbered questions with recommended answers, until every branch of a plan's design tree is resolved; usable inside other skills; adapted from an MIT-licensed upstream (credit in its `metadata`).
- `.agents/skills/grill-me/SKILL.md` - named entry point that starts a `grilling` session; requires `grilling` installed beside it; adapted from the same upstream.
- `.agents/skills/review-csharp/SKILL.md` — C# / .NET review guidelines.
- `.agents/skills/review-rust/SKILL.md` — Rust review guidelines.

## Docs

- `docs/skill-authoring-guide.md` - how to decide whether you need a skill, write it, ship it, and test it.
- `docs/templates/skill-template.md` - copy-to-start `SKILL.md` skeleton, with every section marked required, recommended or optional. Copy it to `.agents/skills/<your-skill-name>/SKILL.md` and check the result with `.agents/skills/agent-skill-review`.
