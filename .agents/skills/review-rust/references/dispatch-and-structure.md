# Rust dispatch and structure review

Read from the Instructions section of `SKILL.md` when the change adds traits, generics or `dyn` types, or touches lint configuration.

- Prefer static dispatch (generics/`impl Trait`) on hot paths, where monomorphization and inlining matter; reach for dynamic dispatch (`dyn Trait`) when you genuinely need a heterogeneous collection or a plugin-style boundary, and accept the small indirection cost there.
- Keep a type's inherent `impl` block(s) near its definition; group trait implementations logically rather than scattering them across the file.
- Run `cargo fmt` and `cargo clippy` (ideally `-D warnings` in CI) as a baseline — don't spend review time on things a formatter/linter would already catch; instead flag `#[allow(clippy::...)]` that lacks a comment explaining why the lint doesn't apply.
