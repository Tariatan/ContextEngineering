# C# design review

Read from the Instructions section of `SKILL.md` when the change adds types or public APIs.

- Avoid cyclic dependencies between types, namespaces, and assemblies — even an indirect cycle (A → B → C → A) is a design smell worth flagging, not just a direct one.
- Use documentation comments (`///`) on public types and members; keep `<inheritdoc/>` for interface implementations and overrides rather than re-stating the same summary.
