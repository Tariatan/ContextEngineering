---
name: edit-memory-file
description: Creates, edits, and prunes MEMORY.md and its topic or archive files using tiered memory (active, archive, retired), promotion to instruction files, consolidation, scope splitting, and expiry annotations. Use when the user says "remember this", "add to memory", "update MEMORY.md", "clean up memory", "prune memory files", "memory is too long", or "promote this memory to the instruction file". Do not use to generate a repo's instruction and memory files from scratch, or for rules that apply to every task (those belong in the instruction file, such as AGENTS.md or CLAUDE.md).
metadata:
  version: 2.0.0
  status: active
  last-reviewed: 2026-10-15
  risk: low
---

# Edit Memory File

## Critical

- NEVER commit or push memory files without explicit user confirmation. A local `git tag` snapshot is allowed.
- NEVER write a consolidated or promoted entry before showing the user the proposed text and getting a go-ahead. Automatic summaries drop nuance.
- NEVER store secrets, credentials, personal data, transcripts, or guesses.
- Preserve the file's original EOF newline style.

## Scope

- Use for: adding, updating, consolidating, splitting, promoting, archiving, or removing memory entries; the periodic memory review.
- Not for: generating a repo's instruction and memory files from scratch; settled rules (the instruction file); hooks.
- Prerequisites: Python 3 (`python3`, `python` or `py -3` on Windows) and `git` on PATH; verify with `python3 --version`. If absent, stop and report.

## Instructions

1. **IDENTIFY**: Auto-memory index is `MEMORY.md` in the agent's own memory directory (Claude Code: `~/.claude/projects/PROJECT/memory/`); it holds pointer lines only, with facts in topic files and a 200 line or 25KB load limit. Repo memory is the repo-root `MEMORY.md` or `.agents/memory.md` (facts inline, active tier at most 100 lines). Agents without auto-memory use the repo kind only. Expected: one of the two kinds. A rule that applies to every task goes to the instruction file (AGENTS.md, CLAUDE.md or equivalent) instead; say so and stop.
2. **BASELINE**: Read the whole file and every topic file that overlaps the new fact. Run `python3 -I scripts/check-memory.py FILE` (add `200` as the second argument for an index). Expected: line and byte counts plus a problem list, recorded as the pre-edit state.
3. **ADMIT**: Keep a candidate only if it changes a future decision, preserves a workaround, or lets unfinished work resume. The four kinds: counterintuitive finding with its evidence; decision with the rejected alternative and the reason; workaround with trigger and removal condition; unfinished task with blocker and next step. Skip release history, facts visible in code, git, README or the instruction file, and one-off session context. Auto-memory also accepts `user`, `feedback` and `reference` entries that record how the user works. Update an existing entry before adding one. Expected: a keep or skip verdict per candidate.
4. **WRITE**: Repo memory takes one bullet `- YYYY-MM: fact and why`, absolute dates only, plus `[EXPIRES: date]`, `[REVIEW: date]`, `[TRIAL: start - end]` or `[stable]` as in `references/memory-strategies.md` (Strategy 5). Auto-memory takes one fact per topic file and one index line, as in `references/auto-memory-format.md`. Expected: no new problem in the next check run.
5. **PROMOTE**: An entry that reads as a rule (same correction 3+ times, caught in review, unchanged for two quarters, or a costly miss) moves to the instruction file with more specific wording. Show the draft, then add it there and delete it from memory in the same change. Expected: the rule exists in exactly one place.
6. **TIER**: When the check reports OVER-LINES or entries are older than 6 months, read `references/memory-strategies.md` (Strategies 1, 3, 4). Run `git tag memory-snapshot-YYYY-QN` first. Move 6-18 month entries not needed this week to `memory-archive.md` (linked from the top of the active file). Consolidate 3+ entries on one topic into a current-state entry that keeps the why. Split by topic when the file covers more than 3. Remove superseded entries older than 18 months (git history keeps them). Skip `[stable]` entries. Expected: active file within budget.
7. **VERIFY**: Re-run `python3 -I scripts/check-memory.py FILE`. Expected: exit 0. Confirm every file, function, flag and path named in touched entries exists. Resolve contradictions with the instruction file by keeping the newer evidenced statement. After a consolidation, answer one task question that depends on it from the new text alone.
8. **REPORT**: Hand back the added, promoted, archived and removed entries with a one-line reason each, and the pre- and post-edit line counts. Do not commit.

## Examples

- "Remember we picked Postgres over Mongo for audit logs" → Steps 1-4. Result: one dated bullet naming the rejected option and the reason.
- "MEMORY.md is 140 lines, clean it up" → Steps 2, 6, 7. Result: snapshot tag, archive file, active file under 100 lines.
- "We always use System.Text.Json now, promote that" → Step 5. Result: rule added to the instruction file, entry deleted from memory.

## Troubleshooting

- **EXPIRED line reported** - the annotation date has passed. Remove the entry, or update it and set a new date.
- **ORPHAN or BROKEN-LINK reported** - an index line and a file name disagree. Fix both in the same edit.

## References

- `references/memory-strategies.md` - read in Step 4 for annotations and in Steps 5-6 for promotion, tiering, consolidation and splitting.
- `references/auto-memory-format.md` - read in Step 4 when editing an auto-memory index or topic file.
- `scripts/check-memory.py` - run in Steps 2 and 7 (use `python` or `py -3` where `python3` is missing); argument 1 is the memory file, optional argument 2 the line limit (default 100).