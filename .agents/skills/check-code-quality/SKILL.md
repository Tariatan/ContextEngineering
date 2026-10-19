---
name: check-code-quality
description: Checklist for correctness, architecture, and design-complexity concerns — edge cases and error handling, responsibility separation and dependency direction, change amplification, deep modules, and information hiding. Use when implementing a change, to apply these while writing code, and when reviewing one, to judge them against someone else's diff. Do not use for per-class single-responsibility analysis (use check-srp) or for logging checks (use check-logging).
---

# Check: Code Quality

Shared checklist for the core judgment calls that apply equally to writing code and to reviewing it, used two ways: an implementing agent applies it while designing its own change; a reviewing agent (e.g. the `reviewer` agent) applies the same checklist to someone else's diff. Logging has its own dedicated skill (`check-logging`) and this one doesn't repeat it.

## Scope

- Use for: applying the checklist while writing a change, and judging someone else's diff against it.
- Not for: single-class responsibility analysis (use check-srp), logging (use check-logging), language idioms (use review-csharp or review-rust).
- Prerequisites: the change or diff to judge.

## Instructions

1. **MODE**: Decide whether you are writing the change or reviewing one. Expected: one mode.
2. **WALK**: Go through Correctness, Security, Architecture, Dependency Hygiene and Design Complexity against the change. Expected: each item resolved as fine, a design decision made, or a finding with file and location.
3. **REPORT**: Apply Reporting for the chosen mode. Expected: a severity per finding when reviewing, decisions recorded in the change when writing.

## Correctness

- Edge cases: empty/null/absent input, boundary values, first/last element.
- Error propagation and error handling: does a failure surface where it can be acted on, or get swallowed?
- Cancellation, retries, and idempotency: repeating or interrupting the operation doesn't corrupt state or duplicate effects.
- Concurrency and async correctness: race conditions, ordering guarantees, thread safety, lifecycle issues (something used after it's disposed/shut down).
- Resource cleanup and disposal: everything acquired is released on every exit path, including error paths.
- State transitions: every reachable state is accounted for, not just the ones the happy path exercises.
- Whether an error condition could be **defined out of existence** — a different API shape, a sentinel default, restructuring so the case can't occur — instead of being defended against everywhere it might arise.

## Security

- Injection: user- or external-controlled input reaching a query, command, path, or deserializer without validation/parameterization.
- Secrets: credentials, tokens, or connection strings in source, config committed to the repo, or logged in plaintext.
- Auth: an endpoint or handler that should check identity/authorization but doesn't, or checks it in a way that's bypassable.

## Architecture

- Responsibilities are well separated between types/modules.
- Abstractions are appropriate for what they hide — not too thin (leaks the detail anyway) or too thick (hides something a caller actually needs).
- Dependencies point in the correct direction; no cyclic dependencies.
- The implementation matches the intended concept, not a nearby-but-different one.
- The resulting API is usable from a caller's perspective, not just correct from the implementer's.

## Dependency Hygiene

- A new package dependency is justified — not a small utility that could be a few lines of local code.
- A version bump doesn't silently downgrade a transitive dependency or reintroduce a previously-fixed vulnerability.
- Two dependencies in the diff don't pull in conflicting versions of the same transitive package.

## Design Complexity

Complexity compounds over the life of a system — a change is a chance to catch it early instead of letting it in.

- **Change amplification** — does a simple-sounding change touch many unrelated files or classes? That usually means a missing abstraction, not an unlucky diff.
- **Cognitive load** — to understand or extend this change, how much context does a reader have to hold at once? Prefer designs where a caller only needs the interface, not the implementation.
- **Unknown unknowns** — is it obvious, from the code alone, what else would need to change if this area is touched again? If not, that's a design smell even when the code is otherwise correct.
- **Deep modules** — a simple interface hiding real functionality is worth more than a simple implementation with a complicated interface. Watch for classes/functions whose interface is large or leaky relative to what they actually do.
- **Information hiding** — who needs to know this detail, and when? Watch for places where an implementation detail leaks across a boundary that should hide it.
- **Sensible defaults** — prefer designs where the common case works automatically over ones that require every caller to remember an extra step.
- **Pass-through method** (red flag): a method whose body does little more than forward its arguments to another method with the same shape. Usually signals responsibilities aren't cleanly divided between the two — worth addressing rather than treating as harmless boilerplate.

## Reporting

When an implementing agent applies this to its own change, treat every item as a design decision to get right now, not a graded finding.

When a reviewing agent applies this to someone else's diff, map findings to its own severity categories: correctness issues that risk incorrect behavior, data loss, or a race/deadlock are usually **Critical**; security issues (injection, exposed secrets, missing/bypassable auth) are always **Critical**; architecture, dependency-hygiene, and design-complexity issues are usually **Major**, unless they're small enough to be a **Minor** readability/naming-level nit.