# Context Engineering

Reusable, project-agnostic agents and skills, meant to be shared across repositories.

## Agents

- **[Reviewer](reviewer.agent.md)** — senior-engineer code review for pull requests, local diffs, or uncommitted changes. Language-agnostic, with dedicated skills for C# and Rust.

## Skills

Skills refine an agent's behavior for a specific language or concern. They are referenced by agents.

- `skills/check-logging/SKILL.md` — language-agnostic structured-logging review checklist.
- `skills/review-csharp/SKILL.md` — C# / .NET review guidelines.
- `skills/review-rust/SKILL.md` — Rust review guidelines.

## Usage in another repository

Add this repository as a git submodule under `.agents/` (or a similar path) so agent definitions stay in sync across projects:

```
git submodule add https://github.com/Tariatan/ContextEngineering.git .agents/context-engineering
```

Then reference the agent from that project's own `AGENTS.md` / `CLAUDE.md`, e.g.:

```
Code review is performed by the `Reviewer` sub-agent defined in `.agents/context-engineering/reviewer.agent.md`.
```

### Keeping the submodule in sync

After cloning the consuming project (or pulling a commit that adds this submodule for the first time), populate it with:

```
git submodule update --init --recursive
```

A plain `git pull` afterwards does **not** automatically move the submodule forward, even if a later commit bumps its pointer to a newer commit here — you'd need to run `git submodule update --recursive` again whenever that happens. To avoid remembering this, set it once per machine:

```
git config --global submodule.recurse true
```

This makes `git pull` / `git checkout` keep submodules in sync automatically (the initial `--init` on a fresh clone is still required, since this setting doesn't cover that one-time step).
