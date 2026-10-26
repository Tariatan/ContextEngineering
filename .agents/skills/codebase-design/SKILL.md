---
name: codebase-design
description: Shared vocabulary and principles for designing deep modules - a lot of behaviour behind a small interface, placed at a clean seam. Use when the user says "design this module's interface", "find deepening opportunities", "where should the seam go", "make this more testable", "is this module too shallow", or when another skill needs the deep-module vocabulary. Do not use for per-class responsibility review (use check-srp) or for reviewing a whole change (use check-code-quality).
metadata:
  version: 1.0.0
  status: active
  last-reviewed: 2026-10-26
  risk: low
  adapted-from: https://github.com/mattpocock/skills (skills/engineering/codebase-design, MIT, Copyright (c) 2026 Matt Pocock)
---

# Codebase Design

Design **deep modules**: a lot of behaviour behind a small interface, placed at a clean seam, testable through that interface. Use this language and these principles wherever code is being designed or restructured. The aim is leverage for callers, locality for maintainers, and testability for everyone.

## Scope

- Use for: designing or restructuring a module's interface; deciding where a seam goes; making code more testable; supplying the vocabulary to another skill.
- Not for: per-class responsibility review (use check-srp); reviewing a whole change (use check-code-quality).
- Prerequisites: none.

## Instructions

1. **FRAME**: Name the module, its callers and its seam in the Glossary terms below. Expected: module, interface, seam and adapter each named for the code at hand.
2. **JUDGE**: Apply the Principles and read `references/deep-vs-shallow.md` for the shape questions. Expected: the module called deep or shallow, with the interface facts that decide it.
3. **BRANCH**: To make code testable, read `references/testability.md`. To deepen a cluster given its dependencies, read `references/deepening.md`. To explore alternative interfaces for a chosen candidate, read `references/design-it-twice.md`. Expected: the matching procedure followed, or none needed.

## Glossary

Use these terms exactly: don't substitute "component," "service," "API," or "boundary." Consistent language is the whole point.

**Module**: anything with an interface and an implementation. Deliberately scale-agnostic: a function, class, package, or tier-spanning slice. _Avoid_: unit, component, service.

**Interface**: everything a caller must know to use the module correctly: the type signature, but also invariants, ordering constraints, error modes, required configuration, and performance characteristics. _Avoid_: API, signature (too narrow, they refer only to the type-level surface).

**Implementation**: what's inside a module, its body of code. Distinct from **Adapter**: a thing can be a small adapter with a large implementation (a Postgres repo) or a large adapter with a small implementation (an in-memory fake). Reach for "adapter" when the seam is the topic; "implementation" otherwise.

**Depth**: leverage at the interface. The amount of behaviour a caller (or test) can exercise per unit of interface they have to learn. A module is **deep** when a large amount of behaviour sits behind a small interface, **shallow** when the interface is nearly as complex as the implementation.

**Seam** _(Michael Feathers)_: a place where you can alter behaviour without editing in that place; the *location* at which a module's interface lives. Where to put the seam is its own design decision, distinct from what goes behind it. _Avoid_: boundary (overloaded with DDD's bounded context).

**Adapter**: a concrete thing that satisfies an interface at a seam. Describes *role* (what slot it fills).

**Leverage**: what callers get from depth. More capability per unit of interface they learn. One implementation pays back across N call sites and M tests.

**Locality**: what maintainers get from depth. Change, bugs, knowledge, and verification concentrate in one place rather than spreading across callers. Fix once, fixed everywhere.

## Principles

- **Depth is a property of the interface, not the implementation.** A deep module can be internally composed of small, mockable, swappable parts; they just aren't part of the interface. A module can have **internal seams** (private to its implementation, used by its own tests) as well as the **external seam** at its interface.
- **The deletion test.** Imagine deleting the module. If complexity vanishes, it was a pass-through. If complexity reappears across N callers, it was earning its keep.
- **The interface is the test surface.** Callers and tests cross the same seam. If you want to test *past* the interface, the module is probably the wrong shape.
- **One adapter means a hypothetical seam. Two adapters means a real one.** Don't introduce a seam unless something actually varies across it.

## Relationships

- A **Module** has exactly one **Interface**; **Depth** is measured against it.
- A **Seam** is where a **Module**'s **Interface** lives; an **Adapter** sits there and satisfies it.
- **Depth** produces **Leverage** for callers and **Locality** for maintainers.

## Rejected framings

- **Depth as ratio of implementation-lines to interface-lines** (Ousterhout): rewards padding the implementation. We use depth-as-leverage instead.
- **"Interface" as the TypeScript `interface` keyword or a class's public methods**: too narrow: interface here includes every fact a caller must know.
- **"Boundary"**: overloaded with DDD's bounded context. Say **seam** or **interface**.
