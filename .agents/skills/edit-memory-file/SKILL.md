---
name: edit-memory-file
description: Decides what earns a place in agent memory, then adds, updates, retires, archives, promotes and consolidates entries in MEMORY.md and its topic or archive files. Use when the user says "remember this", "add to memory", "forget this", "update MEMORY.md", "clean up memory", "memory is too long", or "promote this memory to the instruction file". Also use unprompted when the user corrects the agent, an investigation ends with a finding the code does not show, a decision picks between alternatives, a workaround is added, a session ends with unfinished work, or a recalled memory entry proves wrong or stale. Do not use to generate a repo's instruction and memory files from scratch (use harness-generator), to tighten an instruction file's wording (use writing-for-agents), or for rules that apply to every task (those belong in AGENTS.md or CLAUDE.md).
metadata:
  version: 2.2.0
  status: active
  last-reviewed: 2026-11-03
  risk: low
---

# Edit Memory File

## Critical

- NEVER commit or push memory files without explicit user confirmation. A local `git tag` snapshot is allowed.
- NEVER write a consolidated or promoted entry before showing the user the proposed text and getting a go-ahead. Automatic summaries drop nuance.
- NEVER store secrets, credentials, personal data, transcripts, or guesses.
- NEVER delete an entry for a subjective reason ("probably irrelevant"); archive it or ask. Entries that evidence shows false or moot (Step 6) are deleted without asking and reported.
- Preserve the file's original EOF newline style.

## Scope

- Use for: deciding whether a fact belongs in memory; adding, updating, retiring, consolidating, splitting, promoting or archiving entries; the periodic memory review.
- Not for: generating a repo's instruction and memory files from scratch; settled rules (the instruction file); hooks.
- Prerequisites: Python 3 (`python3`, `python` or `py -3` on Windows) and `git` on PATH; verify with `python3 --version`. If absent, stop and report.

## Instructions

1. **IDENTIFY**: Auto-memory index is `MEMORY.md` in the agent's own memory directory (Claude Code: `~/.claude/projects/PROJECT/memory/`); it holds pointer lines only, with facts in topic files and a 200 line or 25KB load limit. Repo memory is the repo-root `MEMORY.md` or `.agents/memory.md` (facts inline, active tier at most 100 lines). Agents without auto-memory use the repo kind only. Expected: one of the two kinds. A rule that applies to every task goes to the instruction file (AGENTS.md, CLAUDE.md or equivalent) instead; say so and stop.
2. **BASELINE**: Read the whole file and every topic file that overlaps the new fact. Run `python3 -I scripts/check-memory.py FILE` (add `200` as the second argument for an index). Expected: line and byte counts plus a problem list, recorded as the pre-edit state.
3. **ADMIT**: Read `references/memory-lifecycle.md`. Apply its admit test and operation table to each candidate; the moments under "When to evaluate" qualify without a user request. Most candidates end in NOOP, and saving something every session is a failure. Expected: one verdict per candidate (ADD, UPDATE, DELETE, NOOP, PROMOTE or ASK) with a one-line reason.
4. **WRITE**: Repo memory takes one bullet `- YYYY-MM: fact and why`, absolute dates only, with a checkable anchor (path, symbol, command, PR or ticket), plus `[EXPIRES: date]`, `[REVIEW: date]`, `[TRIAL: start - end]` or `[stable]` as in `references/memory-strategies.md` (Strategy 5). Auto-memory takes one fact per topic file and one index line, as in `references/auto-memory-format.md`. UPDATE rewrites the existing entry in place and sets its date to today; never leave the old and new statement side by side. Expected: no new problem in the next check run.
5. **PROMOTE**: An entry that reads as a rule (same correction 3+ times, caught in review, unchanged for two quarters, or a costly miss) moves to the instruction file with more specific wording; word it per `writing-for-agents`. Show the draft, then add it there and delete it from memory in the same change. Expected: the rule exists in exactly one place.
6. **RETIRE**: Check each entry the edit touches, and every entry on the same topic, against the retire table in `references/memory-lifecycle.md`: contradicted, condition cleared, referent gone, superseded, now derivable. Confirm named paths, symbols and flags with a search. Run this step alone on any single recalled entry that proves wrong during other work. Expected: every stale entry deleted or updated, each with a one-line reason for the report.
7. **TIER**: When the check reports OVER-LINES or AGED, read `references/memory-strategies.md` (Strategies 1, 3, 4). Run `git tag memory-snapshot-YYYY-QN` first. Re-confirm each aged entry that is still true and set today's date; move 6-18 month entries not needed this week to `memory-archive.md` (linked from the top of the active file). Consolidate 3+ entries on one topic into a current-state entry that keeps the why. Split by topic when the file covers more than 3. Remove superseded entries older than 18 months (git history keeps them). Skip `[stable]` entries. Expected: active file within budget.
8. **VERIFY**: Re-run `python3 -I scripts/check-memory.py FILE`. Expected: exit 0. Confirm every file, function, flag and path named in touched entries exists. Resolve contradictions with the instruction file by keeping the newer evidenced statement. After a consolidation, answer one task question that depends on it from the new text alone. When Step 5 touched an instruction file, run `writing-for-agents/references/pruning.md` on it.
9. **REPORT**: Hand back the added, updated, promoted, archived and removed entries with a one-line reason each, and the pre- and post-edit line counts. An auto-memory directory is not versioned, so name each deleted entry's gist. Do not commit.

## Examples

- "Remember we picked Postgres over Mongo for audit logs" → Steps 1-4. Result: one dated bullet naming the rejected option and the reason.
- "MEMORY.md is 140 lines, clean it up" → Steps 2, 6-8. Result: snapshot tag, archive file, active file under 100 lines.
- "We always use System.Text.Json now, promote that" → Step 5. Result: rule added to the instruction file, entry deleted from memory.
- A recalled entry names a flag the code no longer has → Step 6. Result: entry updated to the replacement flag and a one-line note to the user.

## Troubleshooting

- **EXPIRED line reported** - the annotation date has passed. Remove the entry, or update it and set a new date.
- **AGED line reported** - the entry was last confirmed over 6 months ago. Re-confirm it and set today's date, archive it, or retire it.
- **ORPHAN or BROKEN-LINK reported** - an index line and a file name disagree. Fix both in the same edit.

## References

- `references/memory-lifecycle.md` - read in Steps 3 and 6 for the admit test, operation table, verify-on-use and retire table, with sources.
- `references/memory-strategies.md` - read in Step 4 for annotations and in Steps 5 and 7 for promotion, tiering, consolidation and splitting.
- `references/auto-memory-format.md` - read in Step 4 when editing an auto-memory index or topic file.
- `scripts/check-memory.py` - run in Steps 2 and 8 (use `python` or `py -3` where `python3` is missing); argument 1 is the memory file, optional argument 2 the line limit (default 100).