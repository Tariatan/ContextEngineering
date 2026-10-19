---
name: review-rust
description: Provides best practices and guidelines for Rust code regarding naming, ownership/borrowing, error handling, Send/Sync and async lock-across-await hazards, Drop/RAII cleanup, dispatch, and unit test conventions. Use when reviewing Rust changes.
---

# Review: Rust

This skill is activated when the reviewer agent encounters Rust code. It refines (but does not contradict) the universal review principles defined in the reviewer agent.

The guidance below is general Rust community practice — the official Rust API Guidelines, the reasoning behind widely-used crates, and idioms enforced by `rustfmt`/`clippy` — not tied to any specific company or codebase. Always follow the repository's own conventions (its `rustfmt.toml`, `clippy.toml`, or a documented style guide) when they specify something different.

## Scope

- Use for: reviewing Rust changes, as the language step of the reviewer agent.
- Not for: other languages; logging (use check-logging); general design review (use check-code-quality).
- Prerequisites: none. The repository's own `rustfmt.toml`, `clippy.toml` and style guide win when they differ.

## Instructions

1. **CONVENTIONS**: Read the repository's `rustfmt.toml`, `clippy.toml` and style guide when present. Expected: the list of rules that override the guidance below.
2. **CHECK**: Walk Naming, Best Practices, Error Handling and Async and Concurrency against the change. For `Drop`, handles or cleanup paths read `references/resource-management.md`; for traits, generics or `dyn` read `references/dispatch-and-structure.md`; when tests are added or edited read `references/unit-tests.md`. Expected: findings with file and location.
3. **REPORT**: Map each finding to the reviewer agent's priorities. Expected: a severity per finding.

## Naming

Follow the [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/naming.html) casing conventions (originally RFC 430):

- `snake_case` for functions, variables, modules, and crate names
- `UpperCamelCase` for types (structs, enums, traits)
- `SCREAMING_SNAKE_CASE` for constants and statics
- `kebab-case` is conventional for the package/directory name on disk, even though the crate name used in `use` statements is `snake_case`

## Best Practices

Prefer:

- ownership and borrowing over cloning
- `Result`/`Option` over panicking
- enums with data over stringly-typed values
- iterators and combinators over manual loops
- derive macros for common traits
- the newtype pattern for type safety
- exhaustive pattern matching (let a new enum variant fail to compile at every match site instead of silently falling through a wildcard arm)

Avoid:

- unnecessary `unwrap()`/`expect()` in library code — prefer propagating a `Result`; reserve `unwrap()`/`expect()` for cases the code has already proven can't fail, and prefer `expect()` with a message explaining why
- unnecessary `clone()` or `Arc` where a borrow would suffice
- `unsafe` without a `// SAFETY:` comment explaining which invariant the caller/implementation is upholding
- overly broad trait bounds (bound on exactly what the function body uses, not "whatever might be convenient later")

## Error Handling

- Use a typed, matchable error (e.g. via the `thiserror` crate) at any boundary where a caller needs to inspect or react differently per failure — a public crate API, or an internal module interface with distinct handling per variant.
- Use an opaque, propagation-only error (e.g. via the `anyhow` crate, with `.context()`/`.with_context()` to attach information as it propagates) for code whose only job is to bubble the error up to a logging/reporting boundary (`main`, a CLI handler, a test helper).
- Never return an opaque/type-erased error from an API callers are expected to `match`/`if let` on — that erases exactly the information they need. Return the typed error instead.
- A typed error that implements `std::error::Error` converts into an opaque error automatically via `?`, so the two compose cleanly: typed at the boundary that must react, opaque above it.

A worked example (a typed `SensorError` converted into `anyhow::Error` through `?`) is in `references/error-handling-example.md`. Read it when a finding needs to explain the typed-versus-opaque split.

## Async and Concurrency

Pay particular attention to:

- `Send`/`Sync` bounds on anything crossing a thread or task boundary
- proper use of async runtime primitives
- deadlocks from holding a lock across an `.await` point
- for synchronous, short-held locks (even inside async code), a non-poisoning lock (e.g. `parking_lot::Mutex`/`RwLock`) is usually a better fit than `std::sync` — a panic while holding a `std::sync` lock poisons it for every future user, which is rarely what you want
- switch to an async-aware lock (e.g. `tokio::sync::Mutex`/`RwLock`) only when the lock genuinely must be held across an `.await`; never call a blocking variant of it (e.g. `blocking_lock()`) from inside an async task — it blocks the executor thread and risks starvation/deadlock
- prefer a read-write lock over a plain mutex when reads significantly outnumber writes
- cancellation safety — what state does a future leave behind if it's dropped mid-`.await`?
- proper error propagation with `?`
