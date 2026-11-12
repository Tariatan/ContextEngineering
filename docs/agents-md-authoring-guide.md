# `AGENTS.md` Authoring Guide

This guide defines the standards, rules, and best practices for creating and maintaining **`AGENTS.md`** files. It is grounded in the _PROSE Context Engineering Framework_.

Companion files:

- [agents-template.md](templates/agents-template.md) - copy this to start a new `AGENTS.md`.

**Contents.**

§1-§5 are what you need to write an `AGENTS.md`; §6-§8 are what you need to keep it alive.

1. [What is `AGENTS.md`](#1-what-is-agentsmd)
2. [What knowledge belongs in `AGENTS.md`](#2-what-knowledge-belongs-in-agentsmd)
3. [Architectural constraints](#3-architectural-constraints)
4. [How to write instructions](#4-how-to-write-instructions)
5. [Tool bridging strategy (multi-tool compatibility)](#5-tool-bridging-strategy-multi-tool-compatibility)
6. [Governance & maintenance](#6-governance--maintenance)
7. [Troubleshooting](#7-troubleshooting)
8. [Example](#8-example)

---

## 1. What is `AGENTS.md`

`AGENTS.md` is an instruction file. It's the primary **Instruction Primitive** for a repository: it externalizes codebase conventions, architectural boundaries, safety rules, and domain constraints into a format AI coding agents read automatically, with no invocation needed.

### Why `AGENTS.md`?

- **Canonical Portability:** `AGENTS.md` is the single most portable instruction format available. It is natively read by **GitHub Copilot, Cursor, Codex and Claude Code**.
- **It is always-on, unlike a skill.** There is no triggering logic and no relevance check. Every line is paid for on every request touching that scope, whether or not it's relevant to the current task. That is exactly why §3's line budget is not a suggestion.
- **Agents are stateless between sessions.** Without a committed `AGENTS.md`, an agent defaults to generic training data, which reliably produces hallucinated interfaces, broken error handling, and convention violations.
- **Specificity:** Agents automatically read the nearest `AGENTS.md` file in the directory tree, which completely replaces a parent's rules by default. Add an actionable instruction telling the agent to read the parent first if you want it to inherit instead (see §4.3). Explicit user chat prompts override everything.

Read more at https://agents.md/.

### What it's not

It's not an _agent file_.

In VS Code/GitHub Copilot, `*.agent.md` files define custom chat agent modes (persona, tools, scope) and live under `.github/agents/` or `.vscode/agents/`.

In Claude Code, the equivalent is a subagent definition: a plain `<name>.md` file under `.claude/agents/`.

Neither replaces `AGENTS.md`: use instruction files (in sub-directories when needed) in collaboration with skill files to achieve this behavior.

---

## 2. What knowledge belongs in `AGENTS.md`

&check; If the agent currently gets it wrong, repeatedly.

&check; If it governs how to work **inside** this repository.

&cross; If it governs how an **outside consumer** uses this repository as a library -> use `SKILL.md`.

&cross; If it's dated trade-off history explaining _why_ the code looks the way it does -> use `MEMORY.md`.

&cross; If it's already documented elsewhere (architecture docs, design records or the `README`), it doesn't belong here.

&cross; If a linter or the compiler already catches it, it doesn't need to be here.

&cross; If it restates what the agent already does correctly, don't.

> A piece of knowledge can fit more than one of the context primitives, e.g. a rule whose reasoning doubles as useful trade-off history. Don't duplicate it: put the rule in `AGENTS.md`, and let `MEMORY.md` carry only the surrounding _history_, or the two copies will drift out of sync.

---

## 3. Architectural constraints

When authoring an `AGENTS.md` file, adhere strictly to the following constraints.

### Strict line budget (40–50 lines max)

- **The rule:** Keep every `AGENTS.md` file under 40 to 50 lines.
- **Rationale:** Every line of instruction competes for attention with the source code the agent needs to analyze. Large, un-scoped instruction files cause attention degradation, causing agents to ignore critical rules.
- **Guideline:** If your file exceeds 50 lines, split it into directory-level instruction files or extract decision frameworks into _SKILL_ files.

### Single-scope discipline

- **The rule:** Match each instruction file to one clear domain or file pattern.
- **Rationale:** Irrelevant rules pollute the agent's context.
- **Guideline:** If an `AGENTS.md` contains rules for two or more domains (e.g. UI and E2E testing), split it into directory-level instruction files. A directory-scoped rule belongs in a directory-level `AGENTS.md`, not the root.

### Front-load safety boundaries

- **The rule:** Sections in `AGENTS.md` should always follow this exact top-to-bottom sequence:
  1. **Core Principles & Safety Boundaries**
      > Top Priority! Safety rules and hard prohibitions (Do NOT...) must be parsed before the agent writes any code. Prohibitions must lead, not sit buried below lower-priority sections an agent on a tight context budget may never reach.
  2. **Architecture & Design Patterns**
      > Establishes high-level design guidelines and lazy-loading pointers (e.g. `docs/architecture/index.md`) before implementation details. Only the root `AGENTS.md` needs these links (see §4.3). A directory-level file only needs its own copy if it doesn't explicitly instruct the agent to read the root first.
  3. **Coding & Error Handling Standards**
      > Defines concrete code-level standards: serialization, DTO immutability, exception wrappers, and structured logging.
  4. **Development & Workflow Conventions**
      > Governs terminal behavior, workspace CLI shortcuts (e.g., `pnpm dlx turbo run where`), git commit styles, PR title formatting.
  5. **Testing & Quality Gates**
      > Defines unit testing requirements, coverage thresholds, and test runner commands to execute before submitting code.
  6. **Context & Memory References**
      > Bottom Anchor. Houses lazy-loading pointers to dynamic execution state (`.agents/memory.md` and `.agents/skills/`).
- **Rationale:** To maximize LLM attention efficiency and maintain consistency across repositories.
- **Guideline:** Include only the relevant sections with instructions that are not already covered by existing documentation. None of them are mandatory, but whichever you include, keep them in this order. Copy [agents-template.md](templates/agents-template.md) as the starting point: it already encodes this ordering.

> **Note:** Directory-level `AGENTS.md` files are optional: only add one once the root file exceeds the [strict line budget](#strict-line-budget-4050-lines-max), or once it mixes rules for two or more unrelated domains ([single-scope discipline](#single-scope-discipline)), whichever comes first.

---

## 4. How to write instructions

### Be literal

Every rule needs an observable condition or a concrete prohibition. Be precise and don't write wishes.

```markdown
<!-- GOOD -->

- Wrap all service-level exceptions using `DomainExceptionWrapper.CatchAndMap()`.
- Use `pnpm dlx turbo run where <project_name>` to jump to a package instead of scanning with `ls`.
- Do NOT modify existing test infrastructure files without explicit human approval.

<!-- BAD -->

- Handle errors properly.
- Make sure the code is clean and follows best practices.
- Try to write good tests.
```

### Progressive disclosure (lazy-loading)

Don't copy or reference other human-facing docs. Provide context _just-in-time_, not _just-in-case_. Telling the agent to "read the README" wastes context-window tokens on every request. Establish clear boundaries instead so the agent knows where to find high-level domain information without reading it immediately.

```markdown
<!-- BAD -->

- Foo Bar is a service that started in 2021 to solve... (the rest of the README, restated)
- See `CONTRIBUTING.md` for how to contribute.

<!-- GOOD -->

- High-level architecture and project purpose: see `README.md`. Do not read it unless the task is to update that documentation.
- For calibration uncertainty rules, see [calibration-guidelines.md](docs/calibration-guidelines.md).
```

### Explicit hierarchy

`AGENTS.md` files do not merge automatically, and a link to a parent file is not guaranteed to be followed: tools only auto-load the nearest file, so anything else is read only if the agent chooses to open it. A directory-level `AGENTS.md` therefore completely replaces its nearest parent for any edits made within that folder, unless it gives the agent an explicit, actionable instruction to read that parent first. Phrase it as an action per §4.1 "Be literal," not a description:

```markdown
<!-- BAD: a description, not an instruction. The agent is never told to do anything -->
Inherits from [`UI/AGENTS.md`](../AGENTS.md); this file only adds rules and does not restate it.

<!-- GOOD: an actionable instruction -->
Before making any change here, read [`AGENTS.md`](../AGENTS.md) and follow its rules together with the ones below; this file does not replace it.
```

The tree below is therefore the intended precedence *when every level is authored to extend the one above it*. It is not something the tooling enforces for you:

1. **Global Principles:** Organization-wide standards, kept in a shared architecture or guidelines repository.
2. **Product Principles:** Product-level architecture standards.
3. **Repository Level:** Root `AGENTS.md` covering repository-wide rules.
4. **Directory Level:** Scoped `AGENTS.md` in subfolders for specific domains or components. Write these as explicit extensions of the root, not standalone replacements, unless the directory truly needs different rules.

---

## 5. Tool bridging strategy (multi-tool compatibility)

To prevent duplication and context drift across different AI coding assistants, write the canonical instruction content **once** in root `AGENTS.md` and use thin bridging files.

### Claude Code

**No bridging needed.**

When no `CLAUDE.md` exists, Claude Code falls back to reading the root `AGENTS.md` natively. Only add a `CLAUDE.md` if you need Claude-specific content beyond what `AGENTS.md` covers. In that case, add the directive `@AGENTS.md` at its top so the root instructions are still imported instead of being silently shadowed.

### GitHub Copilot

**No bridging needed.**

Reads `AGENTS.md` natively from the root and nested AGENTS.md files which apply to specific parts of your project. Use `.github/instructions/*.instructions.md` with `applyTo` frontmatter for Copilot specific rules.

### Cursor
**No bridging needed.**

Reads `AGENTS.md` natively from root and subdirectories. Use `.cursor/rules/` only for tool-specific glob triggers.

### Other tools (Windsurf, OpenCode, etc.)

Verify native `AGENTS.md` support before relying on it. Support varies by tool and changes quickly, so check each tool's own documentation rather than assuming parity with the tools above.

---

## 6. Governance & maintenance

`AGENTS.md` is an active engineering artifact that requires continuous maintenance, not a document you write once and forget.

**The "Fix the Primitive" rule.** When an AI agent generates code that violates a convention, do not just fix the generated code. Update `AGENTS.md` so the mistake is permanently prevented across future sessions. Correcting the output and moving on guarantees the same failure next session, with the next agent, on the next task.

**Source-first principle.** If an audit reveals a missing _global_ guideline, update the human source repository (the shared architecture or guidelines docs) first, then reference it from `AGENTS.md`. Don't let the repository-level file become the only place the rule lives.

**Staleness cap.** No instruction file should go unreviewed for more than 90 days. A rule that references a file, class, or pattern that has since moved is worse than no rule at all, because it actively misleads the agent.

---

## 7. Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Agent ignores a rule that's clearly in `AGENTS.md` | File exceeds the [line budget](#strict-line-budget-4050-lines-max); the rule is buried below less critical content | Cut to budget; move the rule into the first section, under the safety-boundaries heading |
| Different AI tools behave inconsistently in the same repo | Missing or misconfigured bridge file for that tool | Re-check [§5](#5-tool-bridging-strategy-multi-tool-compatibility); confirm the tool actually reads `AGENTS.md` natively before assuming it does |
| An agent in a sub-folder ignores a root-level rule | The directory-level `AGENTS.md` either silently replaced its nearest parent file, or only *described* inheritance | Re-read [§4.3](#explicit-hierarchy). Phrase it as "read X before doing Y," not "inherits from X"; duplicate the rule if all else fails |
| The same mistake recurs every few sessions despite "fixing" it each time | The generated code was corrected but the primitive never was | Apply the "Fix the Primitive" rule in [§6](#6-governance--maintenance): edit `AGENTS.md`, not just the output |
| File has grown past 50 lines and nobody wants to trim it | Two unrelated domains sharing one file | Split per [§3.2 (single-scope discipline)](#single-scope-discipline) into directory-level files, or extract a decision framework into a skill |

---

## 8. Example

This example deliberately nests three levels deep to mirror §3's "Front-load safety boundaries" list, applied with concrete, repository-specific phrasing. It's not meant to be merged or cut. It shows both a root-level file and some directory-level files that explicitly extend it, per §4.3:

```
webapp/
├── api-spec/
│   ├── AGENTS.md                # Directory-Scoped Rules for API endpoints
│   └── ...
├── API/
│   ├── AGENTS.md                # Directory-Scoped Rules for backend
│   └── ...
├── UI/
│   ├── AGENTS.md                # Directory-Scoped Rules for frontend
│   ├── e2e/
│   │   ├── AGENTS.md            # Directory-Scoped Rules for frontend acceptance tests
│   │   └── ...
│   └── ...
└── AGENTS.md                    # Global Repository Rules & Guardrails
```

### Root-level: `webapp/AGENTS.md`

```markdown
# webapp Development Instructions

## Core Principles & Safety Boundaries
- Do NOT modify existing test infrastructure files without explicit human approval.

## Architecture & Design Patterns
- Architectural decisions and development practices: see [architecture docs](docs/architecture/index.md).
- Coding guidelines and design decision records: see [coding guidelines](docs/coding-guidelines.md).

## Development & Workflow Conventions
- Commit messages format: use [Conventional Commits Specification](https://www.conventionalcommits.org/en/v1.0.0/#specification).

## Context & Memory References
- Active decisions & trade-off history: see [.agents/memory.md](.agents/memory.md).
- Shared skills: see [.agents/skills/](.agents/skills/).
```

### Directory-level: `webapp/UI/AGENTS.md`

```markdown
# webapp/UI Development Instructions

> Before making any change here, read the root [`AGENTS.md`](../AGENTS.md) and follow its rules together with the ones below; this file does not replace it.

## Core Principles & Safety Boundaries
- Do NOT bypass `window.Bridge` to call Electron/Node APIs directly from the renderer.
- Do NOT log raw HTTP request options or headers. The `Authorization` header carries the session token.

## Architecture & Design Patterns
- Every API/SignalR response follows a `{results, error}` envelope; check `.error` before trusting `.results` (schemas in `api-spec`).
- All micro-frontends run zoneless (`provideZonelessChangeDetection()`); mutate state via signals, not raw event-listener callbacks.

## Coding & Error Handling Standards
- Place `inject()` calls in the constructor body, not as field initializers, to avoid losing the DI context across Module Federation boundaries.
- Use the design-system components first; only override their styles via a scoped `:host` selector when no customization token exists.
- Every public service method returns `Result<T, DomainError>` (via `BaseHttpClass`); never throw across a module boundary.

## Development & Workflow Conventions
- Package Navigation: use `pnpm dlx turbo run where <project_name>` to locate package roots directly instead of running recursive directory scans or `ls`.
- To start the mocked backend run `pnpm run start-mock`.

## Testing & Quality Gates
- Every new feature must include unit tests achieving ≥80% branch coverage.
- Run `pnpm test` and `pnpm run lint` before submitting a pull request.
```

### Directory-level: `webapp/UI/e2e/AGENTS.md`

```markdown
# webapp/UI/e2e Development Instructions

> Before making any change here, read [`UI/AGENTS.md`](../AGENTS.md) and follow its rules together with the ones below; this file does not replace it.

## Core Principles & Safety Boundaries
- Do NOT assert directly on a Playwright locator. Go through a `support/expect-functions` helper (add one if missing).

## Architecture & Design Patterns
- Mock data lives in a co-located `*.mock.ts` file per spec; never inline it in the spec.

## Coding & Error Handling Standards
- Data-driven `.forEach()` tests carry a `@RequirementID:REQ-<id>` JSDoc block above the array; split into separate `test()` blocks instead of branching inside one.
```