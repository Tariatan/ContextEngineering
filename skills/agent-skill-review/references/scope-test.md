# Scope test — should this be a skill at all?

Reference for the `agent-skill-review` skill. Open only when reviewing a skill that looks
structurally fine but feels like it is in the wrong format. Supports finding A4.

Most reviews never need this file. Do not open it routinely.

---

## The one-line test

> If it must apply to **every** task, it is an instruction.
> If the human **always asks for it by name**, it is a prompt file.
> If the agent must **decide** when it applies, it is a skill.

## The roadmap's decision rule

The chapter defines **seven** context primitives (roadmap §6.2). A skill is one of them. The rule
(roadmap §9.1):

> How to work **inside** a repository → instruction file.
> How to consume a shared library **from outside** → `SKILL.md`.
> Specialist judgement → agent configuration.
> A repeatable process → prompt.
> Why things are the way they are → memory.
> What to build → orchestration spec.
> An automated reaction to an event → hook.

## Full decision table

| Format | Correct when | Why |
|---|---|---|
| **Instruction file** (`AGENTS.md`, `copilot-instructions.md`, `CLAUDE.md`) | conventions for working inside a repository — code style, build command, branch naming, threading rules | always loaded for the matching scope; no triggering risk; no maintenance surface |
| **Skill** | how an external consumer uses a shared library, or a detailed multi-step conditional procedure the agent should load *only when relevant* | progressive disclosure earns its keep |
| **Agent configuration** | a different persona, model or tool allow-list is needed for a whole class of work | skills cannot change the agent's identity |
| **Prompt file / slash command** | a repeatable process the human invokes by name every time | no triggering logic needed at all |
| **Memory file** | decisions, trade-offs and history that explain *why* | dated background context, not a rule |
| **Orchestration spec** | a specification of what to build — components, contracts, acceptance criteria | carries traceability metadata a skill cannot |
| **Hook** | an automated reaction to a development event | event-driven; needs no agent invocation |
| **MCP server** | the agent needs *access* to a system it cannot reach | skills add knowledge, not connectivity |

Skills and MCP are complements, not alternatives. An MCP server without skills produces support
tickets that read "I connected it, now what?"

## The three-part design test

Roadmap §6.2, Primitive 3. It is a skill only if **all three** hold:

- The knowledge applies across multiple files.
- It takes more than a few rules to express.
- It is triggered by a detectable code pattern.

One file or directory → instruction. A general disposition → agent configuration.

## Signals that a reviewed skill should be custom instructions instead

Raise A4 when two or more of these hold:

- The `## Scope` section's `Use for:` bullet amounts to "whenever working in this repository".
- The content is a list of standards or preferences with no ordered procedure.
- There is no conditional logic — no branching, no validation gates, no failure paths.
- Silent non-triggering would be harmful and undetectable. This is the strongest signal.

That last point is the real argument. Consider a skill carrying a team's C# conventions:

```yaml
# Should not be a skill
name: csharp-coding-standards
description: Our C# coding standards — nullable enabled, file-scoped namespaces,
  no regions, xUnit with FluentAssertions.
```

It applies to every C# task, so it must never be conditionally loaded. As a skill it will
sometimes fail to trigger, and the agent will silently write non-conforming code with no signal
that anything went wrong. Its correct home is repository custom instructions.

## Signals that a reviewed skill should be a different primitive

Raise A4 when the content matches another primitive's job:

| Observed | Belongs in |
|---|---|
| dated notes explaining a past decision or a deprecation still in flight | memory file |
| component interfaces, contracts and acceptance criteria for something not yet built | orchestration spec |
| "whenever a file in `schemas/` changes, run the validator" | hook |
| a persona — priorities, expertise, forbidden operations — with no procedure | agent configuration |

## Signals that a reviewed skill should be split

Raise A4 when:

- The description carries two unrelated trigger clusters joined by "or".
- The instructions contain a top-level branch — "if X do steps 1–4, if Y do steps 5–9" — where
  the two paths share nothing.
- The body exceeds 80 lines and the excess is a second procedure, not detail.

## Signals that a skill is context tax

The skill triggers correctly and is well written, but adds nothing the model does not already
do. Raise A4 and ask the author for a baseline comparison: the same request run with and
without the skill, comparing turns, tool calls, failed tool calls and user corrections.

If the "with" column is not clearly better, the skill costs always-loaded description tokens
for no return. A skill that restates default behaviour should be deleted, not merged.

## How to report A4

A4 is an **advisory**, never a blocker. Structural compliance and format choice are separate
questions, and a compliant skill in the wrong format is still compliant.

State the recommended format, the two or more signals observed, and leave the decision with the
author. Do not fail the review on it.
