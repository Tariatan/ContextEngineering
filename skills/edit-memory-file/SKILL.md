---
name: edit-memory-file
description: Procedure for creating or editing MEMORY.md and its topic files - index format, one-fact-per-file frontmatter, the 200-line/25KB load limit, what to save or skip, and pruning stale entries. Use when adding, changing, or cleaning up an agent memory file, either the auto-memory index under ~/.claude/projects/<project>/memory/ or a repo-root MEMORY.md of durable project context.
---

# Edit Memory File

Procedure for any write to a memory file. It exists because memory edits drift in predictable ways: the index grows past its load limit, entries duplicate each other, derivable facts pile up, and stale claims survive. The steps below keep each edit small and verifiable.

Two kinds of file share the name `MEMORY.md`. Identify which one you are editing in Step 1, because the structure differs.

## Sources behind these rules

If a vendor doc changes, the vendor doc wins.

- Claude Code memory ([code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory)): `MEMORY.md` is an index, one line per memory, with detail in topic files. Only the first 200 lines or 25KB load at session start; topic files load on demand. Four memory types: `user`, `feedback`, `project`, `reference`. Skip anything derivable from the code or already in CLAUDE.md. Keep instruction files under 200 lines and make entries concrete enough to verify.
- Anthropic memory tool ([platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)): keep the directory current, coherent, and organized; rename or delete obsolete files; create new files only when necessary; cap file sizes; expire files nobody reads; never store sensitive data; record progress as if interruption can happen at any moment.
- Anthropic context engineering ([anthropic.com/engineering/effective-context-engineering-for-ai-agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)): structured notes outside the context window hold decisions, unresolved issues, and progress. Prune redundant material aggressively and keep subtle context whose value may appear later.
- OpenAI AGENTS.md and Codex ([agents.md](https://agents.md), Codex AGENTS.md guide): plain Markdown with no required fields. The nearest file wins, files layer from broad to specific, and Codex stops reading at 32 KiB (`project_doc_max_bytes`). Put specialized rules close to the code they govern.
- Letta memory blocks ([docs.letta.com/guides/agents/memory-blocks](https://docs.letta.com/guides/agents/memory-blocks)): every block has a label, a description, a value, and a size limit. The description is what tells the agent how to read and write the block, so write it for that reader.
- LangGraph memory concepts ([docs.langchain.com/oss/python/concepts/memory](https://docs.langchain.com/oss/python/concepts/memory)): a single growing profile document gets error-prone, while a collection of narrow documents is easier to extend and gives better recall. Collections need deliberate update and delete discipline.

## Step 1 - Identify the file kind

- **Auto-memory index**: `~/.claude/projects/<project>/memory/MEMORY.md`. Loaded into every session. Contains only pointers. Content lives in sibling topic files.
- **Repo-root MEMORY.md**: checked-in durable project context (ownership, incidents, integration facts), the companion of the repo's CLAUDE.md. Contains the facts themselves, grouped under headings. CLAUDE.md holds the rules; MEMORY.md holds what the team learned.

If the user's request fits neither (for example a rule an agent must always follow), put it in CLAUDE.md instead and say so.

## Step 2 - Read before writing

1. Read the whole `MEMORY.md`. For an index, list the directory and read the topic files whose hooks overlap the new fact.
2. Run `wc -l` and `wc -c` on the index. Note how close it is to 200 lines or 25KB.
3. Look for an existing entry that already covers the fact. Update that entry; create a new one only when nothing fits.

## Step 3 - Decide whether the fact belongs

Save when a future session would otherwise repeat a mistake or miss a constraint:

- A correction from the user, or an approach the user confirmed (`feedback`).
- The user's role, expertise, or working preferences (`user`).
- Ongoing work, deadlines, decisions, or incident root causes that git history does not show (`project`).
- A pointer to an external system such as a tracker, dashboard, or wiki page (`reference`).

Skip when:

- The code, the git log, or CLAUDE.md already records it. File paths, architecture, and past fixes belong here only when the non-obvious reason behind them is the point.
- It only matters inside the current conversation.
- It contains a secret, token, password, or personal data.
- It is a guess. Record only what was observed or stated, with the source.

When asked to remember something that fails this test, ask what was non-obvious about it and save that.

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

Use plain headings for the sections that apply and omit the rest. Typical sections: ownership and contacts, integration facts, incidents and decisions, open questions.

- Cite evidence for each non-obvious claim: a file path, PR number, work item ID, or quoted decision.
- State an incident's root cause and how the fix was validated.
- Date-stamp facts that can expire (`as of 2026-10-08`).
- Keep entries as bullets or short paragraphs under a heading. Do not restate what README or CLAUDE.md already say.
- Never silently drop an incident or decision record. Remove it only when it is demonstrably wrong, and say so in the hand-back summary.

## Step 7 - Verify and prune

1. Re-check every file, function, flag, or path named in the entries you touched and confirm it still exists.
2. Delete or correct entries that turned out to be wrong. Leave no tombstone line.
3. Resolve contradictions between entries or with CLAUDE.md. Keep the newer, evidenced one.
4. Re-run `wc -l` and `wc -c` on the index and confirm it is under both limits.
5. Confirm every index line points at an existing file and every topic file has an index line.
6. Preserve the file's original EOF newline style.

## Notes

- A memory is background context for future sessions and reflects what was true when written. Verify before acting on one.
- Do not commit or push memory files that live in a repo without explicit user confirmation.
- Hooks, not memory, enforce behavior that must run on every action.