---
name: domain-modeling
description: Builds and sharpens a project's domain model as the user designs - challenges terms against GLOSSARY.md, sharpens fuzzy language, stress-tests with edge-case scenarios, and records resolved terms in GLOSSARY.md and hard-to-reverse decisions as ADRs. Use when the user says "what do we call this", "update the glossary", "write an ADR", "record this decision", or debates what a domain term means. Do not use for merely reading GLOSSARY.md for vocabulary, or for deciding a module's shape (use codebase-design).
metadata:
  version: 1.0.0
  status: active
  last-reviewed: 2026-10-26
  risk: low
  adapted-from: https://github.com/mattpocock/skills (skills/engineering/domain-modeling, MIT, Copyright (c) 2026 Matt Pocock)
---

# Domain Modeling

Actively build and sharpen the project's domain model as you design. This is the *active* discipline: challenging terms, inventing edge-case scenarios, and writing the glossary and decisions down the moment they crystallise. (Merely *reading* `GLOSSARY.md` for vocabulary is not this skill: that's a one-line habit any skill can do. This skill is for when you're changing the model, not just consuming it.)

## Critical

- Create `GLOSSARY.md` and `docs/adr/` lazily: only when you have something to write.
- Offer an ADR and write it only after the user agrees.

## Scope

- Use for: changing the domain model during a design or grilling session; writing or editing `GLOSSARY.md`, `GLOSSARY-MAP.md` or an ADR.
- Not for: reading `GLOSSARY.md` for vocabulary; module shape and seams (use codebase-design).
- Prerequisites: none. A missing `GLOSSARY.md` is created when the first term resolves.

## Instructions

1. **LOCATE**: Read `references/file-structure.md`, then find the context the topic belongs to (`GLOSSARY-MAP.md` if present, else the root `GLOSSARY.md`). Expected: the glossary file and ADR directory named, or none yet; ask the user when the context is unclear.
2. **APPLY**: Run the practices under During the session as the conversation unfolds. Expected: each resolved term in `GLOSSARY.md` the moment it resolves, and each qualifying decision offered as an ADR.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `GLOSSARY.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y. Which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account': do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible. Which is right?"

### Update GLOSSARY.md inline

When a term is resolved, update `GLOSSARY.md` right there. Capture terms as they happen. Before writing, read `references/glossary-format.md`.

`GLOSSARY.md` stays free of implementation details: it is a glossary and nothing else.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse**: the cost of changing your mind later is meaningful
2. **Surprising without context**: a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Before writing one, read `references/adr-format.md`.
