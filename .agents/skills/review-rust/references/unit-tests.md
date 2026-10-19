# Rust unit test review

Read from the Instructions section of `SKILL.md` when the change adds or edits tests.

Verify:

- unit tests live in a `#[cfg(test)] mod tests` block next to the code they test (`src/`); tests that exercise the crate's public API end-to-end belong in the separate `tests/` integration-test directory — don't blur the two.
- `#[cfg(test)]` (or a dedicated Cargo feature for more advanced mock/integration setups) is the default way to swap a real dependency for a test double — it's zero-cost (the test-only code doesn't exist in the release build) and doesn't require a runtime DI container. Reach for trait-object dependency injection only when the code genuinely needs to swap the implementation at runtime, not just in tests.
- meaningful assertions
- proper use of `#[should_panic]` vs. a `Result`-returning test (prefer the latter — a `Result`-returning test still reports *why* it failed)
- naming convention consistent with the codebase
