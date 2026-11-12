# Memory File Management Strategies

Memory files grow because every session produces knowledge worth preserving: a decision about which API version to target, a deprecated pattern discovered during review, a trade-off resolved in a meeting. Without active management, memory files expand until they consume a meaningful fraction of the context budget, crowding out the source code and instructions that agents actually need for the task at hand. Most AI coding tools only load the first 200 lines or ~25KB of memory content at session start. Anything beyond that threshold is effectively invisible to the agent.

The following strategies address memory growth. Apply them in combination, selecting the mix that fits the repository's characteristics.

## Strategy 1: Tiered memory (active / archive / retired)

Organize memory into three tiers based on recency and relevance. This follows the same lifecycle pattern used by Architecture Decision Records (proposed → accepted → deprecated → superseded), adapted for agent-consumable context.

**Tier definitions:**

- **Active** (`memory.md`): loaded into agent context by default. Contains decisions and context from the last 6 months that are still relevant. Maximum 100 lines. This is the tier that competes with source code for attention.
- **Archive** (`memory-archive.md`): referenced via link from the active file but not loaded by default. Contains decisions from 6-18 months ago that might be needed for specific tasks. Agents follow the link only when the task touches the relevant area (Progressive Disclosure).
- **Retired** (removed from the `.agents/` directory, preserved in git history): decisions older than 18 months that have been superseded or are no longer relevant. Available through `git log` if someone needs the historical context, but completely absent from agent awareness.

**How to implement this concretely:**

The folder structure within each repository looks like this:

```
billing-service/
├── .agents/
│   ├── memory.md                 # ACTIVE: max 100 lines, always loaded
│   ├── memory-archive.md         # ARCHIVE: linked from memory.md, not auto-loaded
│   └── ...
```

The active `memory.md` file should include a pointer to the archive at the top:

```markdown
# billing-service: Active Memory

> For historical decisions older than 6 months, see [memory-archive.md](./memory-archive.md)

## Current decisions (last updated: 2026-05)

- 2026-04: Adopted MathNet.Numerics for all statistical calculations. Replaces custom NumLib.
- 2026-03: Message schema v3 is now mandatory. v2 schemas deprecated, removal planned for release 14.
- ...
```

**Migration process (run quarterly during a regular context audit):**

1. Tag the current state in git before making changes: `git tag memory-snapshot-2026-Q2`
2. Review each entry in `memory.md`. For each entry older than 6 months, ask: "Would an agent need this to make a correct decision on a task this week?" If no, move it to `memory-archive.md`.
3. For entries in `memory-archive.md` older than 18 months, check whether they have been superseded or are no longer relevant. If so, remove them from the archive (git history preserves them).
4. Commit the changes with a descriptive message: `chore: quarterly memory tier migration Q2 2026`

**Migration cadence:** quarterly, aligned with the regular context audit. Entries that should remain active despite age can be annotated with `[stable]` to signal that they should not be migrated automatically.

## Strategy 2: Promotion to instructions

Memory entries that describe stable, ongoing conventions do not belong in memory. They belong in instruction files. Memory is for evolving context ("we decided X because of Y, might revisit when Z changes"). Instructions are for settled rules ("always do X"). The graduation path follows a progression similar to how the ThoughtWorks Technology Radar moves technologies from Assess through Trial to Adopt:

| Stage | Location | Evidence required | Duration |
|---|---|---|---|
| Observation | Auto-memory or `memory.md` | Agent or developer noticed it once | Days |
| Confirmed pattern | `memory.md` with explicit entry | Same correction appeared 2-3 times | Weeks |
| Team-agreed standard | `AGENTS.md` or tool-specific instruction file | Reviewed in PR, stable for 2 quarters | Permanent until superseded |

**Promotion triggers: when to move from memory to instruction:**

1. The same correction has appeared three or more times in different sessions.
2. A code review caught a convention violation that the agent should have known.
3. The entry has not changed in two quarters and reads like a rule rather than a historical note.
4. A failure caused by the missing instruction was costly enough to warrant permanent enforcement.

**How to implement promotion concretely:**

Step 1: Identify the candidate. During the quarterly memory review, look for entries that read like rules:

> "2025-03: We standardized on System.Text.Json for all new serialization. Newtonsoft.Json is permitted in existing code but must not be introduced in new projects."

This is a rule, not historical context.

Step 2: Write the instruction. Add the rule to `AGENTS.md` (for cross-tool portable instructions) or the appropriate tool-specific instruction file (e.g., `.claude/rules/`, `.cursor/rules/`). The instruction should be more specific than the memory entry. It should tell the agent exactly what to do, not just what was decided:

```markdown
# Serialization conventions

- Use `System.Text.Json` for all new serialization code.
- Do not introduce `Newtonsoft.Json` (Json.NET) in new projects.
- Existing code using Newtonsoft.Json may remain until actively migrated.
- When serializing message contracts, use the `JsonSerializerOptions` from `Shared.Serialization.Defaults`.
```

Step 3: Remove from memory. Delete the original entry from `memory.md`. Having the same knowledge in two places creates drift risk and wastes context budget.

Step 4: Commit as a single PR. The promotion should be reviewable: "Promoted serialization convention from memory to instruction. Reason: stable for 2 quarters, no changes expected."

**What "done well" looks like:** Instructions grow slowly and deliberately. Memory stays lean. There is no duplication between the two. The team reviews CLAUDE.md / instruction changes in PRs, making promotion a team decision rather than an individual one.

**Common mistakes:** Promoting too eagerly (one-off corrections becoming permanent rules before they are validated). Never promoting (memory grows unbounded while instructions stay empty). Promoting without sufficient specificity ("format code properly" instead of "use 4-space indentation, no tabs, LF line endings").

## Strategy 3: Summarization and consolidation

Over time, multiple memory entries accumulate around a single topic. A repository's memory file might have five separate entries about authentication decisions made over 18 months. These can be consolidated into a single summary entry that captures the current state and the key reasoning, with a link to the archive for the full history.

**When to consolidate:** When three or more entries on the same topic exist in active memory, or when a single topic occupies more than 20% of the memory file's line budget.

**How to implement consolidation concretely:**

Step 1: Snapshot before consolidation. Always tag the repository state before aggressive summarization so you can recover if the summary loses important nuance:

```bash
git tag memory-pre-consolidation-2026-Q2
```

Step 2: Identify clusters. Group memory entries by topic. Look for entries that reference the same system, API, pattern, or decision area.

Step 3: Write a "current state" summary. The consolidated entry should answer: "What is true NOW?" and "Why?", without recounting the full journey. Link to the archive for anyone who needs the detailed history.

**Before consolidation** (5 entries, 25 lines):
```markdown
- 2024-09: Evaluated OAuth2 vs API keys. Chose API keys for internal services.
- 2024-11: Added token rotation to API key scheme.
- 2025-02: Discovered API keys inadequate for cross-organization scenarios.
- 2025-04: Migrated external-facing services to OAuth2. Internal services remain API-key.
- 2025-06: Standardized token lifetimes: 1h for OAuth2, 90d for API keys.
```

**After consolidation** (1 entry, 5 lines):
```markdown
- 2025-06 [consolidated]: Authentication uses a dual model. Internal services: API keys
  with 90-day rotation. External-facing services: OAuth2 with 1-hour token lifetime.
  Do not introduce new auth mechanisms without architecture review.
  History: see memory-archive.md#authentication-evolution
```

Step 4: Move the original entries to the archive. The archive retains the full decision trail for anyone who needs to understand why the team ended up where it is.

Step 5: Validate. After consolidation, test that the agent still behaves correctly on a task that relies on the consolidated knowledge. This is a regression test for context quality.

**The "current state + history" pattern.** This approach mirrors the Keep a Changelog convention (see keepachangelog.com): maintain a human-readable summary of what is true now, with links to the detailed change history for those who need it. The active memory is the "current state" document. The archive is the "changelog."

**Common mistakes:** Summarizing away the rationale (keeping the "what" but losing the "why", so the agent cannot judge edge cases). Auto-summarizing without human review (AI may drop nuances that matter for correctness). No git tag before consolidation (unable to recover if the summary is too aggressive).

### Strategy 4: Scope-based splitting

When a single memory file covers too many topics, split it by bounded context or concern. This applies Progressive Disclosure at the memory level: scheduling decisions do not load when the agent is working on notification code.

**When to split:** When memory.md covers more than three distinct topics, or when entries from unrelated concerns compete for the 100-line budget.

**How to implement scope-based splitting concretely:**

A multi-repo setup gives a natural first-level split: each repository has its own memory file. Within a single repository, further splitting is needed when the domain is broad enough to have separable concerns.

**Splitting by bounded context subdomain:**

```
platform-service/
├── .agents/
│   ├── memory.md                     # Index: links to topic files
│   ├── memory-scheduling.md          # Decisions about job scheduling
│   ├── memory-storage.md             # Decisions about persistence and caching
│   └── memory-notifications.md       # Decisions about delivery channels
```

The top-level `memory.md` becomes an index that agents read first, following links to topic-specific files only when relevant:

```markdown
# platform-service: Memory Index

This repository spans three subdomains. Load the relevant topic file for context:

- [Scheduling decisions](./memory-scheduling.md): job queues, retries, back-off sequences
- [Storage decisions](./memory-storage.md): schema migrations, cache invalidation, retention
- [Notification decisions](./memory-notifications.md): channel selection, templates, rate limits
```

**Splitting by volatility:**

An alternative split axis groups entries by how frequently they change:

| Volatility | File | Content | Loaded |
|---|---|---|---|
| Stable (changes yearly) | `memory-architecture.md` | Fundamental design choices, technology selections | Via link, on-demand |
| Evolving (changes monthly) | `memory.md` | Current sprint context, recent decisions, active migrations | Always (this is the active tier) |
| Ephemeral (changes weekly) | Not persisted in files | Debugging notes, session-specific context | Agent auto-memory only |

**Path-scoped memory loading.** For tools that support path-based activation (Claude Code's `paths:` frontmatter, GitHub Copilot's `applyTo`), memory topic files can be configured to load only when the agent is working on relevant source files:

```markdown
---
paths:
  - "src/scheduling/**"
  - "src/jobs/**"
---
# Scheduling decisions
...
```

This ensures that an agent modifying storage code does not have scheduling decisions consuming its context budget.

**Common mistakes:** Splitting too early (a 30-line memory file does not need splitting). Overlapping scopes between split files (the same decision appears in two topic files). No index file to help agents navigate the split structure.

### Strategy 5: Expiration annotations

For entries that are known to have a limited shelf life, add explicit expiration metadata. This prevents the accumulation of transitional context that outlives its usefulness: temporary workarounds, beta dependencies, time-boxed experiments, and migration-period guidance.

**How to implement expiration annotations concretely:**

Each memory entry that has a known end-of-life date receives an inline annotation using a consistent format:

```markdown
## Active decisions

- 2026-03: [EXPIRES: 2026-Q3] Using RabbitMQ.Client 7.0-beta. Switch to GA release when
  available; remove this entry after migration. Tracking: TICKET-123.
- 2026-04: [EXPIRES: 2026-08] Temporary workaround for upstream API timeout (increased
  from 500ms to 2000ms). Revert after upstream v3.2 is deployed to all environments.
- 2026-05: [REVIEW: 2026-11] Trial: using record types for all new message DTOs. Evaluate
  serialization performance impact after 3 months of usage.
```

**Annotation types:**

| Annotation | Meaning | Action when triggered |
|---|---|---|
| `[EXPIRES: date]` | This entry has a hard end-of-life. | Remove the entry (or update if the situation changed). |
| `[REVIEW: date]` | This entry should be re-evaluated at the given date. | Review: promote, archive, update, or renew the review date. |
| `[TRIAL: start - end]` | This is a time-boxed experiment with defined boundaries. | At end date: evaluate success criteria. Promote if successful, remove if not. |
| `[stable]` | This entry is expected to remain valid indefinitely. | Skip during age-based tier migration. Only remove if explicitly superseded. |

**Trial entries with success criteria:**

For experimental decisions, the annotation should include explicit success/failure criteria so the review is objective rather than subjective:

```markdown
- 2026-05: [TRIAL: 2026-05 - 2026-08] Evaluating source-generated JSON serializers
  for message contracts. Success criteria: 20% reduction in serialization allocations
  without regression in schema compatibility tests. If successful: promote to instruction
  in AGENTS.md (serialization section). If not: revert to reflection-based serialization
  and archive this entry.
```

**Automation: CI check for expired entries.**

Enforce expiration hygiene with a simple CI pipeline step that fails the build (or produces a warning) when expired entries remain in memory files:

```bash
#!/bin/bash
# check-memory-expiry.sh: add to CI pipeline

TODAY=$(date +%Y-%m-%d)
QUARTER_TODAY=$(date +%Y-Q)$(( ($(date +%-m) - 1) / 3 + 1 ))
WARNINGS=0

for file in .agents/memory*.md; do
  [ -f "$file" ] || continue
  
  # Check for expired date-based annotations
  while IFS= read -r line; do
    EXPIRES=$(echo "$line" | grep -oP '\[EXPIRES: \K[^\]]+')
    if [ -n "$EXPIRES" ]; then
      # Handle both YYYY-MM-DD and YYYY-QN formats
      if [[ "$EXPIRES" =~ ^[0-9]{4}-Q[1-4]$ ]] && [[ "$EXPIRES" < "$QUARTER_TODAY" ]]; then
        echo "EXPIRED: $file: $line"
        WARNINGS=$((WARNINGS + 1))
      elif [[ "$EXPIRES" =~ ^[0-9]{4}-[0-9]{2} ]] && [[ "$EXPIRES" < "$TODAY" ]]; then
        echo "EXPIRED: $file: $line"
        WARNINGS=$((WARNINGS + 1))
      fi
    fi
  done < "$file"
done

if [ $WARNINGS -gt 0 ]; then
  echo "WARNING: $WARNINGS memory entries have expired and need attention."
  exit 1
fi
```

Run this step as a non-blocking warning at first and promote it to a blocking check once the team is used to the practice.

**Automation: pre-commit hook for new entries.**

To ensure new memory entries always include lifecycle metadata, a pre-commit hook can validate that any new line added to a memory file includes a date prefix:

```bash
#!/bin/bash
# .git/hooks/pre-commit (or equivalent in CI)

for file in $(git diff --cached --name-only | grep '.agents/memory.*\.md'); do
  ADDED_LINES=$(git diff --cached --unified=0 "$file" | grep '^+' | grep -v '^+++' | grep -v '^+#' | grep -v '^+$')
  while IFS= read -r line; do
    if [ -n "$line" ] && ! echo "$line" | grep -qP '^\+- \d{4}-\d{2}'; then
      echo "ERROR: New memory entry in $file missing date prefix (expected format: '- YYYY-MM: ...')"
      echo "  Line: $line"
      exit 1
    fi
  done <<< "$ADDED_LINES"
done
```

**What "done well" looks like:** Every non-permanent entry has either an `[EXPIRES]` or `[REVIEW]` annotation. The CI pipeline catches entries that have outlived their relevance. Trial entries have explicit success criteria, so the review conversation is "did we meet the bar?" rather than "do we feel good about this?" The team treats the quarterly review as a 15-minute housekeeping task, not a day-long exercise, because most expired entries are flagged automatically.

**Common mistakes:** Adding expiration dates but never automating the check (silent rot). Setting unrealistic review dates on every entry ("review in 1 month" on 50 entries creates review fatigue). No graduation path: entries expire and nothing replaces them, leaving a knowledge gap.

### References

- Michael Nygard, "Documenting Architecture Decisions" (2011): the original ADR proposal with lifecycle statuses (proposed/accepted/deprecated/superseded). The memory tier model extends this lifecycle to agent-consumable context.
- MADR (Markdown Any Decision Records), https://adr.github.io/madr/: YAML frontmatter with status fields, adapted here for memory entry annotations.
- Keep a Changelog, https://keepachangelog.com/: the "current state + history" pattern for human-readable summaries alongside detailed change logs.
- Kubernetes Deprecation Policy, https://kubernetes.io/docs/reference/using-api/deprecation-policy/: the announce-deprecate-remove lifecycle with time gates, adapted here as the three-tier migration cadence.
- RFC 8594 (The Sunset HTTP Header): time-based unavailability announcements, adapted as the `[EXPIRES]` annotation pattern.
- ThoughtWorks Technology Radar (Assess → Trial → Adopt → Hold): the graduation model applied to the memory → instruction promotion path.