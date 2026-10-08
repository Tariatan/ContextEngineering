---
name: edit-memory-file
description: Create or tidy MEMORY.md and its topic files, retaining useful counterintuitive findings, decisions with alternatives, preserved workarounds, and unfinished tasks. Use for memory edits and pruning; exclude release history and facts already available in code or maintained documentation.
---

# Edit Memory File

Procedure for any write to a memory file. It exists because memory edits drift in predictable ways: the index grows past its load limit, entries duplicate each other, derivable facts pile up, and stale claims survive. The steps below keep each edit small and verifiable.

Two kinds of file share the name `MEMORY.md`. Identify which one you are editing in Step 1, because the structure differs.

## Sources behind these rules

The user's memory criteria take precedence over these background references. Vendor documentation informs storage mechanics; it does not require retaining content that fails the admission criteria below.

- Claude Code memory ([code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory)): `MEMORY.md` is an index, one line per memory, with detail in topic files. Only the first 200 lines or 25KB load at session start; topic files load on demand. Four memory types: `user`, `feedback`, `project`, `reference`. Skip anything derivable from the code or already in CLAUDE.md. Keep instruction files under 200 lines and make entries concrete enough to verify.
- Anthropic memory tool ([platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)): keep the directory current, coherent, and organized; rename or delete obsolete files; create new files only when necessary; cap file sizes; expire files nobody reads; never store sensitive data; record progress as if interruption can happen at any moment.
- Anthropic context engineering ([anthropic.com/engineering/effective-context-engineering-for-ai-agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)): structured notes outside the context window hold decisions, unresolved issues, and progress. Prune redundant material aggressively and keep subtle context whose value may appear later.
- OpenAI AGENTS.md and Codex ([agents.md](https://agents.md), Codex AGENTS.md guide): plain Markdown with no required fields. The nearest file wins, files layer from broad to specific, and Codex stops reading at 32 KiB (`project_doc_max_bytes`). Put specialized rules close to the code they govern.
- Letta memory blocks ([docs.letta.com/guides/agents/memory-blocks](https://docs.letta.com/guides/agents/memory-blocks)): every block has a label, a description, a value, and a size limit. The description is what tells the agent how to read and write the block, so write it for that reader.
- LangGraph memory concepts ([docs.langchain.com/oss/python/concepts/memory](https://docs.langchain.com/oss/python/concepts/memory)): a single growing profile document gets error-prone, while a collection of narrow documents is easier to extend and gives better recall. Collections need deliberate update and delete discipline.

## Step 1 - Identify the file kind

- **Auto-memory index**: `~/.claude/projects/<project>/memory/MEMORY.md`. Loaded into every session. Contains only pointers. Content lives in sibling topic files.
- **Repo-root MEMORY.md**: durable project lessons and unfinished work, alongside the repo's instruction files. Contains the facts themselves, grouped under headings. CLAUDE.md holds the rules; MEMORY.md holds what the team learned.

If the user's request fits neither (for example a rule an agent must always follow), put it in CLAUDE.md instead and say so.

## Step 2 - Read before writing

1. Read the whole `MEMORY.md`. For an index, list the directory and read the topic files whose hooks overlap the new fact.
2. Run `wc -l` and `wc -c` on the index. Note how close it is to 200 lines or 25KB.
3. Look for an existing entry that already covers the fact. Update that entry; create a new one only when nothing fits.

## Step 3 - Decide whether the fact belongs

Save only information whose non-obvious value would otherwise be lost, within these four categories:

- **Useful counterintuitive findings:** an approach or result proved useful despite being controversial, apparently contradictory, or contrary to the expected rule. Record the evidence and the conditions under which it worked.
- **Decisions over alternatives:** a choice was made over a concrete counterpart. Record the chosen option, the rejected alternative, and the reason or tradeoff that is not already explained elsewhere.
- **Preserved workarounds:** an unresolved limitation requires a workaround future sessions must retain. Record the trigger, the workaround, why it is still needed, and its removal condition when known.
- **Unfinished tasks:** work was left for a future session. Record the unresolved part, blocker or constraint, and next concrete step. Do not duplicate a maintained plan or issue tracker.

For every candidate, ask: would this entry change a future session's decision, preserve a necessary workaround, or enable unfinished work to resume? If it only recounts what happened, omit it.

Skip:

- Release narratives, completed-task reports, test-count histories, benchmark logs, and routine fixes already recorded in CHANGELOG.md or git history.
- Facts visible in code, architecture descriptions, path inventories, setup instructions, or rules already maintained in README, AGENTS.md, CLAUDE.md, a design document, or a plan.
- Generic user profiles, preferences, and reference links that do not support one of the four categories above.
- Transcripts, temporary conversation context, guesses, secrets, credentials, or personal data.

A code or changelog reference can support a qualifying entry; it does not justify copying that source into memory. Save the non-obvious lesson or rationale, not the implementation summary. If no entry qualifies, leave memory small or empty rather than inventing content.

When tidying, delete redundant or obsolete material directly. Do not relocate it to linked history files, archives, or topic files merely to preserve volume. Do not recreate memory folders the user deliberately removed. Preserve a qualifying lesson when its useful rationale is absent from maintained sources; briefly report material pruning in the hand-back.

## Step 4 - Write one fact per topic file (auto-memory index)

File name: short snake_case or kebab-case slug, prefixed by type when helpful (`feedback_testing.md`).

```markdown
---
name: <short-kebab-case-slug>
description: <one line used to decide relevance during recall>
metadata:
  type: user | feedback | project | reference
---

<the fact>

**Why:** <the reason or incident behind it>
**How to apply:** <when and where this changes behavior>
```

- `Why` and `How to apply` are required for `feedback` and `project`; optional for `user` and `reference`.
- Convert relative dates ("next Thursday") to absolute dates.
- Link related memories with `[[other-name]]` using that file's `name:` slug.
- Write the `description` for a reader deciding whether to open the file, in the way Letta treats a block description.
- Keep each file short. Split a file once it covers two independent facts.

## Step 5 - Update the index

Add or edit exactly one line per memory:

```markdown
- [Title](file.md) - one-line hook
```

- No frontmatter and no memory content in `MEMORY.md`.
- Keep each line under about 150 characters. The hook should tell a future session whether to open the file.
- Group related lines under short headings once the index passes roughly 40 lines.
- Stay under 200 lines and 25KB. Beyond that point the tail silently stops loading. Near the limit, merge overlapping entries and delete stale ones before adding.
- When a file is renamed or deleted, fix its index line and every `[[link]]` pointing at it in the same edit.

## Step 6 - Repo-root MEMORY.md structure

Use plain headings for the sections that apply and omit the rest. Suitable sections: counterintuitive findings, decisions and alternatives, preserved workarounds, unfinished tasks. Create only sections with qualifying entries.

- Cite evidence for each non-obvious claim: a file path, PR number, work item ID, or quoted decision.
- Include incident evidence only when it explains a qualifying lesson or a workaround that still matters. Routine completed fixes belong in the changelog.
- Date-stamp facts that can expire (`as of 2026-10-08`).
- Keep entries as bullets or short paragraphs under a heading. Do not restate what README or CLAUDE.md already say.
- Prune entries that no longer meet the admission criteria, even when historically correct. Do not preserve redundant incident or decision records in archives.

## Step 7 - Verify and prune

1. Re-check every file, function, flag, or path named in the entries you touched and confirm it still exists.
2. Delete or correct wrong, redundant, superseded, or no-longer-useful entries. Remove completed tasks unless they yielded a qualifying lesson or preserved workaround. Leave no tombstone line.
3. Resolve contradictions between entries or with CLAUDE.md. Keep the newer, evidenced one.
4. Re-run `wc -l` and `wc -c` on the index and confirm it is under both limits.
5. Confirm every index line points at an existing file and every topic file has an index line.
6. Preserve the file's original EOF newline style.

## Notes

- A memory is background context for future sessions and reflects what was true when written. Verify before acting on one.
- Do not commit or push memory files that live in a repo without explicit user confirmation.
- Hooks, not memory, enforce behavior that must run on every action.