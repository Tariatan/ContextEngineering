# Context Engineering

Reusable, project-agnostic agents and skills, meant to be shared across repositories.

## Agents

- **[Reviewer](.agents/reviewer.agent.md)** — senior-engineer code review for pull requests, local diffs, or uncommitted changes. Language-agnostic, with dedicated skills for C# and Rust.

## Skills

Skills refine an agent's behavior for a specific language or concern. They are referenced by agents.

- `.agents/skills/check-logging/SKILL.md` — language-agnostic structured-logging review checklist.
- `.agents/skills/review-csharp/SKILL.md` — C# / .NET review guidelines.
- `.agents/skills/review-rust/SKILL.md` — Rust review guidelines.

## Usage in another repository

Add this repository as a git submodule under `.agents/` (or a similar path) so agent definitions stay in sync across projects:

```
git submodule add https://github.com/Tariatan/ContextEngineering.git .agents/context-engineering
```

Then reference the agent from that project's own `AGENTS.md` / `CLAUDE.md`, e.g.:

```
Code review is performed by the `Reviewer` sub-agent defined in `.agents/context-engineering/.agents/reviewer.agent.md`.
```
