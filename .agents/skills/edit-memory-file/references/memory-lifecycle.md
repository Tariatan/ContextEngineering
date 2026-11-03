# Memory lifecycle: admit, update, retire

Decision rules for what earns a place in memory, when to rewrite an entry and when to remove it. Distilled from the Claude Code memory docs, the Claude memory tool docs, GitHub Copilot Memory docs, OpenAI Codex memories docs and Anthropic's context-engineering posts (sources at the end).

## Principle

Memory holds claims about the past that the repo cannot show: why something is the way it is, what was rejected, what is half-done, how this user works. Every claim can go stale, so every entry must be cheap to verify and cheap to drop. Memory is context the agent weighs, not enforcement.

## When to evaluate (unprompted)

Run the admit test at these moments without waiting for "remember this":

- The user corrects the agent, or confirms a non-obvious approach ("yes, exactly that").
- An investigation ends with a finding that contradicts the obvious reading of the code.
- A decision is made between alternatives.
- A workaround is added or a blocker is found.
- The session ends with unfinished work.
- A recalled entry proves wrong, stale or already applied.

Most moments end in NOOP. Saving something every session is a failure mode.

## Admit test

The first matching rule decides.

1. Holds a secret, credential, personal or confidential data, raw tool output, a transcript or a guess: NOOP.
2. A reader finds it in the code, git history, tests, README or instruction file within a minute: NOOP.
3. Matters only for this session: NOOP. Unfinished work with its blocker and next step is the exception: ADD with `[EXPIRES: date]`.
4. Must hold on every task: PROMOTE to the instruction file. A hard guarantee belongs in a hook.
5. A future agent holding only code, git and the instruction file would decide worse without it: continue to the table. Otherwise NOOP.

Entries that pass step 5 are one of four kinds: counterintuitive finding with its evidence; decision with the rejected alternative and the reason; workaround with trigger and removal condition; unfinished task with blocker and next step. Auto-memory adds `user`, `feedback` and `reference` kinds.

## Operation table

| Candidate against existing entries | Operation | Do |
|---|---|---|
| New subject | ADD | One entry |
| Same subject, new fact refines the old | UPDATE | Rewrite in place, keep the why, set the date to today |
| Same subject, old statement is false now | UPDATE or DELETE | State the current truth. Keep the old value only when the reversal is the lesson ("moved from X to Y because Z") |
| Already covered | NOOP | Re-confirm the date if you just verified it |
| Unclear whether it applies to the repo or to this user | ASK | Scope follows who the fact applies to, not who said it |

Prefer UPDATE over ADD. Never leave a contradicting pair; the agent picks one arbitrarily.

## Entry quality

- Self-contained, absolute date, with the why and the trigger for applying it.
- A checkable anchor: path, symbol, command, PR or ticket. Retirement checks run against it.
- Limited life carries `[EXPIRES]`, `[REVIEW]` or `[TRIAL]` (see `memory-strategies.md`, Strategy 5).
- The date means last confirmed. Finding an entry still true moves its date to today. Merely reading it does not.

## Verify on use

An entry is what was true when written. Before acting on one that names a file, symbol, flag, command, version or state, confirm it exists now. On failure, fix or delete the entry in the same turn and tell the user in one line. When the user's statement contradicts an entry, trust the user and the present state, and update.

## Retire

Validity decides; age only breaks ties. Check on every edit of the file, on every failed verify-on-use and in each periodic review.

| Signal | Action | Ask first |
|---|---|---|
| Contradicted by current code, docs or the user | DELETE or UPDATE | No, report |
| Condition cleared: workaround removable, blocker gone, task merged, trial ended, `EXPIRES` passed | DELETE | No, report |
| Referent gone: file, symbol, flag or ticket no longer exists | UPDATE to the replacement, else DELETE | No, report |
| Superseded by a newer entry | DELETE the older one | No, report |
| Now stated in code, README or instruction file, or promoted there | DELETE | No, report |
| True but not confirmed for 6+ months and not needed this week | ARCHIVE | No |
| In the archive 18+ months and superseded or irrelevant | DELETE | No, git keeps it |
| "Probably irrelevant" with no evidence | ARCHIVE, or ASK | Yes before any delete |

`[stable]` entries skip the age rows and never skip the validity rows. Repo memory is versioned, so deletions are recoverable; an auto-memory directory is not, so the report names each deleted entry in one line.

## Sources

- Claude Code memory: https://code.claude.com/docs/en/memory (four auto-memory types; skips what is derivable or already in CLAUDE.md; 200 line or 25KB index limit; "merge or drop stale entries"; `/doctor prompt-audit` for instruction files).
- Claude memory tool: https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool (keep memory up to date, coherent and organized; rename or delete irrelevant files; create files only when necessary; delete files unused for a long time).
- GitHub Copilot Memory: https://docs.github.com/en/copilot/concepts/agents/copilot-memory (facts cite code and are checked against the current branch; expiry without reinforcement, 90 days default; validation resets the clock, retrieval does not; short-lived instructions are not stored; must-always rules go to instructions).
- OpenAI Codex memories: https://developers.openai.com/codex/memories (memory is a recall layer, not the only source for rules that must always apply; no secrets).
- Anthropic, effective context engineering: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents (persist decisions, unresolved bugs and implementation details; discard redundant output; over-aggressive pruning loses subtle context).
- Anthropic, long-running agent harnesses: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents (progress file plus git log lets a fresh session resume; end each session with a structured update).