---
name: check-technical-design-description
description: Deterministic check that new messages, handlers, and architectural elements introduced by a change are reflected in the repo's Technical Design Description (prose and PlantUML) and respect its documented design decisions. Use when the user says "check the TDD", "is the design document up to date", "does this change match the technical design", or when the reviewer agent runs a review. Do not use for changelog or version checks (use check-changelog-versioning) or for judging architecture in general (use check-code-quality).
metadata:
  version: 1.0.0
  status: draft
  last-reviewed: 2026-10-22
  risk: low
---

# Check: Technical Design Description (TDD)

## Critical

- This check is mandatory for every review, regardless of language. Never skip it.
- A repo without a TDD is reported in the summary table as "no TDD found". Never omit the row.
- If the TDD cannot be fetched at a ref, name the exact failure (for example "TDD fetch failed on base ref"). Never write "could not verify".

## Scope

- Use for: every review, to confirm that documentation-relevant additions appear in the TDD and that no changed line contradicts it.
- Not for: changelog and version checks (use check-changelog-versioning), general architecture judgment (use check-code-quality).
- Prerequisites: the diff, and read access to the TDD at the base and current refs.

## Instructions

1. **LOCATE**: Look for `Documentation/Technical_Design_Description.md`, then `Docs/Technical_Design_Description.md`, then any `**/Technical_Design_Description.md`. Expected: a path, or "no TDD found" and a stop here.
2. **REFS**: Pick the two refs by review mode. Hosted pull request: target branch and source branch. Local diff: `<base>` and `HEAD`. Uncommitted changes: `HEAD` and the working tree. Expected: a base ref and a current ref.
3. **COLLECT**: List documentation-relevant additions or renames in the diff: process managers, repositories, aggregates, services, value objects, a call into a unit not referenced before, a renamed or restructured message contract, and any code the TDD's Unit Design Notes, Decisions or Scope sections make an explicit claim about. Expected: a list of symbols, possibly empty.
4. **DOCUMENT**: For each symbol check three places. Prose: it appears in a relevant section, typically MESSAGES or Execution. Diagram: it appears in a `plantuml` fenced block with a matching stereotype (`<<command>>`, `<<event>>`, `<<handler>>`, `<<process manager>>`). Context Map: a new external-unit dependency appears in the Context Map diagram. Expected: prose and diagram verdicts per symbol.
5. **CONTRADICT**: Compare the diff against Unit Design Notes, Decisions and Scope. Example: the TDD says "ID only, no path passing" and the diff passes a path across the boundary. Expected: each contradiction with the quoted TDD text and the code line.
6. **HISTORY**: If the TDD itself changed in this diff, confirm the Modification History table at the top gained a row describing the change. Expected: a pass or a named gap.

## Reporting

- A new message, handler or process manager missing from both prose and diagram, or a violated design decision: **Major**. Quote the TDD text or name the section the symbol belongs in, and give the code line.
- A symbol present in prose but missing from the diagram (or the reverse), or a TDD change without a Modification History row: **Minor**.
- Summary table: ✅ no findings, ❌ any Major finding, ⚠️ only Minor findings, "no TDD found" when step 1 stopped.
