# Memory strategies

Memory-management strategies for agent memory files. Most tools load only the first 200 lines or about 25KB of memory at session start, so anything past that is invisible.

## Strategy 1: Tiers (active, archive, retired)

- **Active** (`memory.md` or `MEMORY.md`): context from the last 6 months that is still relevant. At most 100 lines. Starts with a pointer such as `> Older decisions: see [memory-archive.md](./memory-archive.md)`.
- **Archive** (`memory-archive.md`): decisions 6-18 months old that a specific task might need. Linked, never auto-loaded.
- **Retired**: superseded or irrelevant entries older than 18 months. Delete them; git history keeps them.

Migration, quarterly:

1. `git tag memory-snapshot-YYYY-QN`.
2. For each active entry older than 6 months ask: would an agent need this to decide correctly on a task this week? If not, move it to the archive.
3. Remove archive entries older than 18 months that are superseded or irrelevant.
4. Entries marked `[stable]` skip age-based migration.

## Strategy 2: Promotion to instructions

Memory holds evolving context ("decided X because Y, revisit when Z"). Instructions hold settled rules ("always X").

| Stage | Location | Evidence |
|---|---|---|
| Observation | auto-memory | noticed once |
| Confirmed pattern | memory entry | same correction 2-3 times |
| Team standard | instruction file (AGENTS.md, CLAUDE.md) | reviewed in a PR, stable for 2 quarters |

Promote when: the same correction appeared 3+ times; a review caught a convention the agent should have known; the entry is unchanged for two quarters and reads like a rule; a miss was costly. Steps: identify the rule-like entry, write a more specific instruction ("use `System.Text.Json` for new serialization", not "serialize properly"), delete the memory entry, land both in one reviewable change. Avoid promoting one-off corrections and avoid never promoting.

## Strategy 3: Consolidation

Trigger: 3+ active entries on one topic, or one topic above 20% of the line budget. Tag `memory-pre-consolidation-YYYY-QN` first. Replace the cluster with one entry that states what is true now and why, then move the originals to the archive and link them.

```markdown
- 2025-06 [consolidated]: Internal services use API keys (90-day rotation); external services use OAuth2 (1-hour tokens). History: memory-archive.md#authentication-evolution
```

Keep the rationale; a summary that loses the why leaves the agent unable to judge edge cases. A human reviews the summary before it is written.

## Strategy 4: Scope-based splitting

Split when the file covers more than 3 distinct topics or unrelated topics compete for the 100-line budget. Do not split a file under about 30 lines. Keep `memory.md` as an index of one-line links to `memory-TOPIC.md` files, with no decision stated in two files. Volatility split: stable architecture facts in `memory-architecture.md` (linked), evolving context in `memory.md`, ephemeral notes only in auto-memory. Tools with path scoping (`paths:` frontmatter in Claude Code, `applyTo` in Copilot) can load a topic file only for matching source paths.

## Strategy 5: Expiration annotations

Put one inline annotation on every entry with a limited life.

| Annotation | Meaning | Action when due |
|---|---|---|
| `[EXPIRES: 2026-Q3]` or `[EXPIRES: 2026-08]` | hard end of life | remove, or update if the situation changed |
| `[REVIEW: 2026-11]` | re-evaluate then | promote, archive, update, or renew the date |
| `[TRIAL: 2026-05 - 2026-08]` | time-boxed experiment | judge against its success criteria; promote or remove |
| `[stable]` | valid indefinitely | skip age migration |

A trial entry states its success criteria and what happens on success and on failure. Avoid review dates on every entry (review fatigue). `scripts/check-memory.py` reports expired `EXPIRES` and `REVIEW` dates.