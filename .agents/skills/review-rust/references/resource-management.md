# Rust resource management review

Read from the Instructions section of `SKILL.md` when the change touches `Drop`, file handles, connections or cleanup paths.

Check:

- `Drop` implementations — correct, and never panicking inside `drop()`
- RAII patterns used for guaranteed cleanup instead of "remember to call `close()`"
- proper cleanup in error paths (not just the happy path)
- file handle and connection lifetime, and that it's obvious from the type who owns them
