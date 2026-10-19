# Typed and opaque errors, worked example

Read from the Error Handling section of `SKILL.md` when a finding needs to show how a typed error converts into an opaque one.

```rust
#[derive(Debug, thiserror::Error)]
pub enum SensorError {
    #[error("communication timeout after {timeout_ms} ms")]
    Timeout { timeout_ms: u64 },
    #[error("I/O error")]
    Io(#[from] std::io::Error),
}

fn run() -> anyhow::Result<()> {
    let temperature = read_sensor().context("failed to read temperature sensor")?; // SensorError -> anyhow::Error
    Ok(())
}
```
