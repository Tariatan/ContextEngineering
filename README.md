# Context Engineering

Reusable, project-agnostic agents and skills, meant to be shared across repositories.

## Agents

- **[Reviewer](reviewer.agent.md)** — senior-engineer code review for pull requests, local diffs, or uncommitted changes. Language-agnostic, with dedicated skills for C# and Rust.

## Skills

Skills refine an agent's behavior for a specific language or concern. They are referenced by agents.

- `skills/check-logging/SKILL.md` — language-agnostic structured-logging review checklist.
- `skills/check-changelog-versioning/SKILL.md` — deterministic changelog (Keep a Changelog) and SemVer version-bump check.
- `skills/review-csharp/SKILL.md` — C# / .NET review guidelines.
- `skills/review-rust/SKILL.md` — Rust review guidelines.
