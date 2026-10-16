---
name: your-skill-name
description: WHAT the skill does, in one clause. Use when the user WHEN-CONDITION,
  says "TRIGGER PHRASE A", "TRIGGER PHRASE B", or works with FILE-TYPE. Do not use
  for NEGATIVE-CASE (use OTHER-SKILL instead).
# ── OPTIONAL below - delete every line you do not use ──────────────────
license: MIT                       # only for skills you open-source
allowed-tools: TOOL-NAME           # eg. shell. Syntax differs per harness; see guide §9.
metadata:                          # documented for Claude only
  owner: TEAM-OR-HANDLE            # someone who will still own it next year
  source-repository: REPO-URL      # https://github.com/OWNER/REPO - see guide §8
  version: 1.0.0
  status: draft                    # draft | active | deprecated
  last-reviewed: YYYY-MM-DD        # the date the skill was last reviewed
  risk: low                        # low | high - the SKILL's blast radius, see guide §9. Binary.
---

<!--
HOW TO USE: copy to skills-root/your-skill-name/SKILL.md (the filename is case-sensitive),
replace every UPPERCASE-PLACEHOLDER, delete every unused section and every HTML comment
including this one, and keep the finished file at 80 lines or fewer - blank lines count -
with rarely-needed detail in `references/`. Then check it with the `agent-skill-review`
skill. Which sections are required and why, and whether a skill is the right primitive at
all: docs/skill-authoring-guide.md §6 and §2.
-->

# Human-Readable Skill Name

## Critical <!-- RECOMMENDED - omit only if no step is destructive or irreversible. -->

- NEVER do X.
- ALWAYS confirm with the user before Y.
- If PRECONDITION is not met, stop and report; do not improvise.

## Scope <!-- REQUIRED - all three bullets; write `none` rather than dropping one. -->

- Use for: CONCRETE-TASK-1; CONCRETE-TASK-2.
- Not for: NEAR-MISS-CASE - use OTHER-SKILL or plain agent behaviour instead.
- Prerequisites: REQUIREMENT (an MCP server, a CLI on PATH, an env var); verify with
  `COMMAND`, expecting `EXPECTED-OUTPUT`. If absent: STOP-OR-FALLBACK-INSTRUCTION.

## Instructions <!-- REQUIRED - one numbered line per step, each naming its output or gate. -->

1. **STEP NAME**: WHAT-HAPPENS. Run `CONCRETE COMMAND --with REAL-FLAGS`. Expected:
   WHAT-SUCCESS-LOOKS-LIKE. On OBSERVABLE-FAILURE, see Troubleshooting.
2. **STEP NAME**: WHAT-HAPPENS, using OUTPUT-OF-STEP-1. Expected: CHECKABLE-CONDITION.
3. **STEP NAME**: WHAT-HAPPENS. Do not continue until CHECKABLE-CONDITION holds.

## Definition of done <!-- OPTIONAL - when "done" is not self-evident from the last step. -->

- ARTEFACT exists at LOCATION, and `CHECK-COMMAND` exits 0.

## Usage <!-- REQUIRED for a shared-library skill (guide §5); delete it otherwise. -->

```LANGUAGE
GOLDEN-PATH CODE EXAMPLE
```

- Misuse: COMMON-MISTAKE - do THIS instead.
- Contracts: MESSAGE-EMITTED / MESSAGE-CONSUMED, or `none`.
- Threading and lifecycle: CONSTRAINT.

## Examples <!-- RECOMMENDED - one bullet per realistic scenario. -->

- "REALISTIC USER UTTERANCE" → ACTION (Step 1), ACTION (Step 2). Result: CONCRETE OUTCOME.

## Troubleshooting <!-- RECOMMENDED - one entry per failure you have actually seen. -->

- **ERROR-STRING-AS-THE-USER-SEES-IT** - cause: WHY-IT-HAPPENS. Fix: EXACT-REMEDY.

## References <!-- OPTIONAL - progressive disclosure. Link, never inline. -->

- `references/policy.md` - read before STEP-N when CONDITION.
- `scripts/validate-some-example-skill.ps1` - run from the skill's base directory; argument 1 is INPUT-PATH.
