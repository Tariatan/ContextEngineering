---
name: check-srp
description: Checklist for whether a class fulfills a single, well-defined responsibility efficiently and without dead weight — core purpose, efficiency/robustness, and scope creep/redundant code. Used by the reviewer agent to verify adherence and by the class-optimizer agent to actively fix violations.
---

# Check: Single Responsibility & Class Design

Applies to any class, struct, or otherwise cohesive module meaningfully added or modified in the change under review — not to every file (a config or plain-data change with no real logic doesn't need this).

## Step 1 — Core purpose

- State the class's single, primary responsibility in one sentence. If you can't, or the sentence needs "and", that's itself an SRP violation — say so.
- Check the class actually fulfills that purpose completely: are there logical gaps or edge cases it silently fails to handle?

## Step 2 — Efficiency & robustness

- **Complexity** — algorithms, loops, or data structures that could be a simpler or faster shape. Don't chase micro-optimizations outside hot paths, but flag complexity that's out of proportion to what the class does.
- **Resource management** — I/O, memory, and network calls handled optimally: no redundant queries, streams/handles properly disposed.
- **Robustness** — error handling that surfaces failures rather than swallowing them silently.

## Step 3 — Scope creep & dead weight

- **Over-engineering** — is the class solving problems it doesn't actually have yet (speculative generality, unused extension points)?
- **Redundant code** — unused variables, dead methods, duplicated logic that already exists elsewhere.
- **Misplaced responsibilities** — logic that belongs to a different layer (e.g. a data model formatting for UI, a service managing its own configuration).

## Reporting (reviewer agent)

When invoked from the reviewer agent, report findings under its Priorities scale rather than fixing anything:

- A class doing multiple unrelated things, or a responsibility clearly misplaced across layers, is **Major** (architecture).
- Dead code, unused branches, or minor scope creep that isn't yet causing harm is **Minor**.
- Only escalate to **Critical** if the Step 1 gap (core purpose not fully met) causes incorrect behavior.

## Fixing (class-optimizer agent)

When invoked from the class-optimizer agent, apply Steps 1–3 as active fixes rather than a report: close the gaps found in Step 1, simplify or resolve the issues found in Step 2, and delete dead code or relocate misplaced responsibilities found in Step 3 — don't just leave a note about them.

If a fix would require a larger restructuring (e.g. splitting the class in two, or moving a responsibility to a class that doesn't exist yet), propose it and confirm before doing it, rather than silently reshaping the surrounding module.
