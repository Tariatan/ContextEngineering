---
name: check-test-coverage
description: Checklist for judging whether a change has adequate test coverage: new or changed behavior exercised, edge cases and error paths covered, existing tests updated and kept strong. Use when the user says "do I have enough tests", "what tests should I add", "review the test coverage", or when the reviewer agent runs a review. Do not use for logging checks (use check-logging) or for judging production code design (use check-code-quality).
metadata:
  version: 1.0.0
  status: draft
  last-reviewed: 2026-10-22
  risk: low
---

# Check: Test Coverage

## Critical

- NEVER treat a weakened, skipped or deleted existing test as unrelated cleanup. Treat it as seriously as missing coverage.
- NEVER count a test that passes identically before and after the change as coverage for it.

## Scope

- Use for: deciding what tests to add while implementing a change, and judging the tests of someone else's diff.
- Not for: logging (use check-logging), production code design (use check-code-quality), language test idioms (use review-csharp or review-rust).
- Prerequisites: the change or diff, including its test files.

## Instructions

1. **MODE**: Decide the role. An implementing agent runs this on its own diff before declaring the task done and closes every gap itself. A reviewing agent runs it on someone else's diff and reports gaps with a severity. Expected: one role.
2. **CHANGE**: Every new or changed piece of logic has a test that fails if the change is reverted. A bug fix has a regression test that reproduces the original failure on the old code path. Assertions exercise the changed behavior; "no exception was thrown" alone does not count. Expected: a verdict per changed behavior.
3. **EDGES**: Check boundary conditions relevant to the change (empty, null, absent, zero, negative, maximum, first and last element), the error and exception paths the change introduces or touches, and cancellation, timeout, retry and concurrency behavior where the code has those concerns. Expected: covered or a named gap.
4. **PLACEMENT**: The test sits at the right level. A cheap unit test where a unit test can verify the behavior; an end-to-end test only where needed; no unit test that mocks away the integration point the change is about. External dependencies (message broker, HTTP, database, filesystem) follow the conventional pattern for that dependency type. Expected: a verdict per new test.
5. **EXISTING**: No existing assertion was loosened, and no existing test was deleted, skipped, or wrapped in a broad try/catch that ignores failures, without a stated reason. A weakened test hides a regression in code nobody meant to touch. Expected: a list of weakened tests, possibly empty.
6. **REPORT**: Apply Reporting for the chosen role. Expected: gaps closed (implementing) or findings with severity (reviewing).

## Reporting

- Implementing agent: every failed item is a to-do to fix now. No severity applies.
- Reviewing agent, usually **Major**: a bug fix without a regression test, new behavior on a critical path with no coverage, or any weakened or deleted existing test. A regression can reappear silently or has already lost its safety net.
- Reviewing agent, usually **Minor**: a missing edge-case test where the happy path is covered, or a test at the wrong level without a correctness problem.