# Body shapes

Four recurring shapes for the `## Instructions` part of a skill in this repo. Skim an existing skill of the same shape first, so the new one reads like it belongs next to them. Pick the shape that matches the content. A checklist forced into numbered steps, or a mechanical procedure loosened into a checklist, both fail.

## A. Checklist skill

The calling agent still exercises judgment against a defined checklist.

- Title: `# Review: <Name>` or `# Check: <Name>`, mirroring the `review-*` / `check-*` prefix of `name:`. Use a plain descriptive title otherwise.
- One paragraph: what invokes it and how it relates to the calling agent(s).
- Authoritative source(s): link the external document the checklist derives from. The source wins if the two disagree.
- The checklist as bullets under thematic headings.
- `## Reporting` only when severity varies by impact. Skip it when severity is inherited from the calling agent's own categories.

## B. Deterministic procedure skill

The check is mechanical enough to specify as exact steps, so it cannot be paraphrased away.

- Title: `# Check: <Name>`.
- One paragraph: which narrative instruction it replaces, and why it is steps.
- A mode-resolution note when the calling agent has several run modes (for example PR, local diff, uncommitted changes) that the skill must treat the same way.
- One numbered line per step, each naming what to look at and the result it produces.
- `## Reporting`: a single failure usually collapses to one severity regardless of which step tripped it.

## C. Reference/lookup skill

A table or procedure the calling agent looks up.

- Title: plain, no prefix.
- One paragraph on who shares it and why it exists (for example platform variance).
- The table or command reference.
- `## Notes` with gotchas found the hard way.

## D. Action/handoff procedure skill

A procedure for doing something (landing changes, running a migration), with no audit of existing code.

- Title: plain, no `Check:` / `Review:` prefix.
- One paragraph on what it does end to end. Add a note that values the calling agent already fixed (branch name, commit message) override derivation.
- One numbered line per decision or action point.
- No `## Reporting`. Confirmation gates (never commit or push without asking) sit inline in the relevant step.
