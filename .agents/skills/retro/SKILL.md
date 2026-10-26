---
name: retro
description: Runs a retrospective on a coding session and proposes improvements to the coding agent's environment (navigation pointers, automated checks, coding standards, steering files, tooling, information access), ordered by severity. Use when the user says "/retro", "run a retro", "what would have prevented this", "why did the agent struggle in this session", or asks to improve AGENTS.md or CLAUDE.md after a session. Do not use for reviewing a change (use the reviewer agent) or for making the proposed edits, which wait for the user's pick.
metadata:
  version: 1.0.1
  status: active
  last-reviewed: 2026-10-26
  risk: low
  adapted-from: https://github.com/mattpocock/skills (skills/engineering/retro, MIT, Copyright (c) 2026 Matt Pocock)
---

# Retro

The user has asked for a **retrospective**. You are suggesting improvements to the coding agent's **environment** to improve future runs.

## Critical

- Present candidates only. Edit no steering file, hook, check or CI job until the user picks a candidate.

## Scope

- Use for: a retrospective on one coding session, current or named by the user.
- Not for: reviewing a change (use the reviewer agent); applying the improvements before the user chooses.
- Prerequisites: the `writing-for-agents` skill installed in the same skills folder; verify it appears in the skill list. If absent, stop and tell the user.

## Instructions

1. **LOAD STYLE**: Call the Skill tool with `writing-for-agents` for the writing style guide. Expected: its levers on hand before any candidate is judged.
2. **READ SESSION**: Read the primary sources for the session the user specifies. This may mean searching through session logs on this machine. If the user doesn't specify a session, default to the current one. Expected: the session's friction points listed (long searches, mistakes, costly tool calls, missing information).
3. **FIND CANDIDATES**: Walk each category under Categories against the session. Expected: each category resolved as a candidate with its session evidence, or as none.
4. **PRESENT**: Present the candidates to the user, in order of severity. Expected: a severity-ordered list, each entry naming the category, the session evidence and the proposed change.

## Categories

- **Navigation**: how easy was it for the agent to find the right files? Are there hidden dependencies between files? Would a **navigation pointer** make it easier? _Use when_ the session took a long time to find a piece of information.
- **Automated checks**: are there automated checks that could catch errors the agent made? Linting, typing, tests, filesystem linters? Read the repo's own check command first (its `package.json`/build-tool `lint`/`check` scripts, its CI workflow), so a check that already exists but sits unwired or silently broken is the finding. A repo with no **guardrail** (no pre-commit hook and no CI job running its lint/typecheck/test command) is itself a finding: an un-linted repo is a standing missed opportunity. _Use when_ the agent made a mistake an automated check could have caught, or the repo has no guardrail at all.
- **Coding standards**: should the **reviewer agent** be given a new rule to enforce? Should an existing rule be removed or clarified? Classify the violation first: a **mechanical** one (a fixed syntactic pattern, a banned API, an import shape, a file-location rule) gets a deterministic check, full stop: a custom rule in the repo's own linter, a new pre-commit hook, or a new CI job, whichever the repo's language and existing guardrail make cheapest. Default to building the check over writing the rule. Reserve `CODING_STANDARDS.md` for genuine **judgement calls** (cross-file consistency, "matches the surrounding style," anything no guardrail could ever substitute for). _Use when_ the reviewer agent failed to catch a mistake.
- **Global AGENTS.md**: are there any steering instructions that should be moved to coding standards (or automated checks) instead? _Use when_ the AGENTS.md file is over its budget (about 40-50 lines for a root file) or carries history, procedures or rules a linter enforces - in the repo OR the user's global scope.
- **Tool economy**: did the agent make expensive tool calls that could be streamlined? Is there any custom tooling (CLI's, MCP's) that is particularly token-inefficient? _Use when_ the agent made an expensive tool call.
- **No-ops**: look for instructions in steering files that don't modify the agent's behavior. _Use when_ the steering files are large and unwieldy.
- **Information access**: look for opportunities to increase the agent's access to information. Teeing dev server logs, readonly access to third-party services. _Use when_ a crucial piece of information was not available to the agent.

## Reference

### Implementation vs Review

Remember that all work goes through two stages: implementation and review. The implementation agent has the most **context pressure**. They are responsible for exploration, writing code, and debugging failures.

The review agent has the least context pressure - it receives a diff, so no exploration needed. It often does not need to write code or debug.

This means that the review agent should be responsible for imposing coding standards.

### Files

You have access to several files in the repo:

- `CLAUDE.md`/`AGENTS.md`: these files are pushed to the context window of any agent working in this repo. Keep the root file to about 40-50 lines: rules the agent would get wrong or never know, prohibitions first ("Do NOT ..." with the reason in one clause), plus **navigation pointers** to other files with the condition for following each. History goes to `MEMORY.md`, conditional procedures to skills, and anything a linter or compiler enforces is omitted.
- `CODING_STANDARDS.md`: this file is read during review, not implementation. Add **navigation pointers** to docs folders if the standards file gets more than 1,000 lines long.
- Docs: use docs as references files, pointed to by other files. Look for existing docs before writing new ones.
- Skills: use skills for docs the agent must decide to load, since their description goes into the agent's context window. Commands the human always invokes by name are prompt files here (see the `skill-creator` skill, Step 1). Follow the advice in the `writing-for-agents` skill.

## Examples

- "Run a retro on this session, the agent kept searching for the config loader" → Steps 1-4. Result: a Navigation candidate (a pointer line in `AGENTS.md`) ordered by severity with the others.
