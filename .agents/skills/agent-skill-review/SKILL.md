---
name: agent-skill-review
description: Reviews an agent skill folder against the organisation's SKILL.md template and
  reports blockers, warnings and advisories with a PASS or FAIL verdict. Use when the user says
  "review this skill", "is my SKILL.md valid", "check this skill against the template", "can I
  publish this skill", or opens a pull request that adds or edits a SKILL.md file. Do not use
  for writing a new skill from scratch, or for reviewing ordinary application code.
metadata:
  owner: Zelda
  source-repository: https://dev.azure.com/diaitads/mollab/_git/Tool.ContextEngineering
  version: 0.3.0
  status: draft
  last-reviewed: 2026-09-15
  risk: low
---

# Agent Skill Review

## Critical

- Report findings. Do NOT rewrite the skill unless the user explicitly asks you to.
- Record `pass`, `fail` or `n/a` for all 32 IDs, and cite the line behind every finding.
- NEVER report PASS while a Blocker is open. Never estimate a character or line count.
- Read the relevant `references/` file before every verdict; never review from memory.
- `shell`/`bash` in `allowed-tools` caps the verdict at PASS WITH WARNINGS and obliges the
  report to name a required second reviewer.
- Pre-approved tools, or unconfirmed action, on High Risk (Rigor Level II) work is B12 — FAIL (roadmap §10.2).

## Scope

- Use for: a `SKILL.md` about to be merged, published or installed org-wide; a pull request
  that adds or changes a `SKILL.md`; explaining why a skill never triggers.
- Not for: authoring a new skill from scratch (a template job); reviewing application code,
  pipeline YAML or custom-instruction files; choosing a format before anything is written.
- Prerequisites: read access to the skill folder, plus the three files in this skill's
  `references/`. The reviewed repository needs no template or standards file of its own.

## Instructions

1. **INVENTORY**: List every file in the skill folder, recursively. Expected: a file tree
   naming the folder, whether `SKILL.md` sits at its root, and which of `scripts/`,
   `references/`, `assets/` and `README.md` exist. No root `SKILL.md` — stop, report B1.
2. **FRONTMATTER**: Read `references/frontmatter-rules.md` and score its check tables.
   Expected: a verdict for each of B1–B10, B12, W1–W8 and W16.
3. **BODY**: Read `references/body-rules.md` and score its check tables. Expected: a verdict
   for each of B11, W9–W15 and A1–A3.
4. **SCOPE TEST**: Only when the skill is sound but reads like standards or always-applicable
   guidance, read `references/scope-test.md` and score A4. Otherwise A4 is `n/a`.
5. **TRIGGER SUITE**: From the description derive 3 phrasings that should trigger, 3 that
   should using none of its words, and 3 that should not. Expected: 9 utterances, else W4.
6. **REPORT**: Emit the block below, then apply the verdict rules in order — any open Blocker,
   or `shell`/`bash` pre-approved without a named second reviewer, gives FAIL; otherwise any
   open Warning gives PASS WITH WARNINGS; otherwise PASS.

```text
SKILL: skill-name     VERDICT: PASS | PASS WITH WARNINGS | FAIL
BLOCKERS / WARNINGS / ADVISORIES / NOT APPLICABLE — one line per finding, or "none":
  B7  description is 1180 characters, limit is 1024   [frontmatter]
TRIGGERING TESTS   should trigger: ...   /   should not trigger: ...
```

## Examples

- "Review `.agents/skills/ado-build-failure-triage` before I raise the PR" → Steps 1–5 run;
  only `metadata.last-reviewed` is empty. Result: PASS WITH WARNINGS, W6, 9 utterances.
- "My skill never triggers on its own" → Step 2 first; a vague description fails W1–W3.

## Troubleshooting

- **No frontmatter, yet the author says it works** — it is read as a plain instructions file.
  Report B2: without it the harness cannot decide when to load the skill.
- **Frontmatter looks correct but the harness rejects it** — almost always B3 or B8. Check an
  unquoted colon-and-space first, then angle brackets hidden in a comment or an example.
- **The skill over-triggers** — a sibling competes for the same words. Report W4 against both.

## References

- `references/frontmatter-rules.md` — read at Step 2, every review: B1–B10, B12, W1–W8, W16.
- `references/body-rules.md` — read at Step 3, every review: B11, W9–W15, A1–A3 tables.
- `references/scope-test.md` — read at Step 4 only, when a sound skill looks mis-formatted (A4).
