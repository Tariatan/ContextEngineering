# Auto-memory format

For an agent's auto-memory directory. Other agents can adapt the layout. The index holds pointers; each topic file holds one fact.

## Topic file

File name: short kebab-case slug, optionally prefixed by type (`feedback-testing.md`).

```markdown
---
name: short-kebab-case-slug
description: one line a reader uses to decide whether to open the file
metadata:
  type: user | feedback | project | reference
---

The fact.

**Why:** the reason or incident behind it.
**How to apply:** when and where it changes behavior.
```

- `Why` and `How to apply` are required for `feedback` and `project`, optional for `user` and `reference`.
- Convert relative dates to absolute dates.
- Link related memories with `[[other-name]]`, using that file's `name:` slug.
- Split a file once it covers two independent facts.

## Index line

```markdown
- [Title](file.md) - one-line hook
```

- No frontmatter and no memory content in `MEMORY.md`.
- Keep each line under 150 characters; the hook says whether to open the file.
- Add short headings once the index passes 40 lines.
- Stay under 200 lines and 25KB; the tail stops loading past that.
- When a file is renamed or deleted, fix its index line and every `[[link]]` to it in the same edit.