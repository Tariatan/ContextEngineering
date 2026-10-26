---
name: improve-codebase-architecture
description: Scans a codebase for deepening opportunities (shallow modules worth turning into deep ones), presents them as a visual HTML report, then runs a grilling session on the candidate the user picks. Use when the user says "/improve-codebase-architecture", "find refactoring opportunities", "where is this codebase shallow", "make this codebase easier for agents to navigate". Do not use for designing a module you already chose (use codebase-design) or for reviewing a change (use check-code-quality).
metadata:
  version: 1.0.0
  status: active
  last-reviewed: 2026-10-26
  risk: low
  adapted-from: https://github.com/mattpocock/skills (skills/engineering/improve-codebase-architecture, MIT, Copyright (c) 2026 Matt Pocock)
---

# Improve Codebase Architecture

Surface architectural friction and propose **deepening opportunities**: refactors that turn shallow modules into deep ones. The aim is testability and AI-navigability.

This command is _informed_ by the project's domain model and built on a shared design vocabulary:

- Call the Skill tool with "codebase-design" for the architecture vocabulary (**module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, **locality**) and its principles (the deletion test, "the interface is the test surface", "one adapter = hypothetical seam, two = real"). Use these terms exactly in every suggestion, and don't drift into "component," "service," "API," or "boundary."
- The domain language in `GLOSSARY.md` gives names to good seams; ADRs in `docs/adr/` record decisions this command should not re-litigate.

## Critical

- Write the report to the OS temp directory only, so no file lands in the repo.
- Do NOT propose interfaces before the user picks a candidate: the grilling loop shapes them.

## Scope

- Use for: finding deepening candidates across a codebase or a named area, then exploring one by interview.
- Not for: designing one module you already chose (use codebase-design); reviewing a change (use check-code-quality).
- Prerequisites: the `codebase-design`, `grilling` and `domain-modeling` skills installed in the same skills folder; verify each appears in the skill list. If one is absent, stop and tell the user.

## Instructions

1. **EXPLORE**: Scope the scan, read `GLOSSARY.md` and the ADRs in the area, then spawn a sub-agent to walk the codebase, as in Explore. Expected: friction points listed, each tested with the deletion test.
2. **REPORT**: Read `references/html-report.md`, then write and open the report as in Present candidates. Expected: `<tmpdir>/architecture-review-<timestamp>.html` with one card per candidate and a Top recommendation, its absolute path given to the user, and the question "Which of these would you like to explore?".
3. **GRILL**: When the user picks a candidate, run the Grilling loop. Expected: constraints, dependencies, the deepened module's shape, the seam and surviving tests settled, with the domain model current.

## Explore

**Scope before you scan: YAGNI.** Deepening a module pays off by making future changes to it easier, so put extra weight on the parts of the codebase that have recently changed. Decide *where* to look before you look:

- If the user named a direction (a module, a subsystem, a pain point), take it, and skip the inference below.
- Otherwise, walk back a good stretch of the commit history (`git log --oneline`) to find the codebase's hot spots, the files and areas that keep coming up, and let those paths pull your attention first. If the changes are scattered with no clear hot spot, widen the net.

Read the project's domain glossary (`GLOSSARY.md`) and any ADRs in the area you're touching first.

Then spawn a sub-agent to walk the codebase. Explore organically and note where you experience friction:

- Where does understanding one concept require bouncing between many small modules?
- Where are modules **shallow**, with an interface nearly as complex as the implementation?
- Where have pure functions been extracted just for testability, but the real bugs hide in how they're called (no **locality**)?
- Where do tightly-coupled modules leak across their seams?
- Which parts of the codebase are untested, or hard to test through their current interface?

Apply the **deletion test** to anything you suspect is shallow: would deleting it concentrate complexity, or move it? A "yes, concentrates" is the signal you want.

## Present candidates

Write a self-contained HTML file to the OS temp directory. Resolve the temp dir from `$TMPDIR`, falling back to `/tmp` (or `%TEMP%` on Windows), and write to `<tmpdir>/architecture-review-<timestamp>.html` so each run gets a fresh file. Open it for the user (`xdg-open <path>` on Linux, `open <path>` on macOS, `start <path>` on Windows) and tell them the absolute path.

The report uses **Tailwind via CDN** for layout and styling, and **Mermaid via CDN** for diagrams where a graph/flow/sequence reliably communicates the structure. Mix Mermaid with hand-crafted CSS/SVG visuals: use Mermaid when relationships are graph-shaped (call graphs, dependencies, sequences), and hand-built divs/SVG when you want something more editorial (mass diagrams, cross-sections, collapse animations). Each candidate gets a **before/after visualisation**. Be visual.

For each candidate, render a card with: **Files** involved; **Problem** (why the current architecture causes friction); **Solution** (plain English, what would change); **Benefits** (in terms of locality and leverage, and how tests would improve); a side-by-side custom-drawn **Before / After diagram**; and a **Recommendation strength** badge, one of `Strong`, `Worth exploring`, `Speculative`. End with a **Top recommendation** section: which candidate you'd tackle first and why.

**Use GLOSSARY.md vocabulary for the domain, and the `codebase-design` vocabulary for the architecture.** If `GLOSSARY.md` defines "Order," talk about "the Order intake module."

**ADR conflicts**: if a candidate contradicts an existing ADR, surface it only when the friction is real enough to warrant revisiting the ADR, and mark it in the card (e.g. a warning callout: _"contradicts ADR-0007, but worth reopening because…"_).

## Grilling loop

Once the user picks a candidate, call the Skill tool with "grilling" to walk the decision tree with them: constraints, dependencies, the shape of the deepened module, what sits behind the seam, what tests survive.

Side effects happen inline as decisions crystallize; call the Skill tool with "domain-modeling" to keep the domain model current as you go:

- **Naming a deepened module after a concept not in `GLOSSARY.md`?** Add the term to `GLOSSARY.md`. Create the file lazily if it doesn't exist.
- **Sharpening a fuzzy term during the conversation?** Update `GLOSSARY.md` right there.
- **User rejects the candidate with a load-bearing reason?** Offer an ADR, framed as: _"Want me to record this as an ADR so future architecture reviews don't re-suggest it?"_ Only offer when a future explorer would need the reason to avoid re-suggesting the same thing; skip ephemeral reasons ("not worth it right now") and self-evident ones.
- **Want to explore alternative interfaces for the deepened module?** Call the Skill tool with "codebase-design" and use its design-it-twice parallel sub-agent pattern.
