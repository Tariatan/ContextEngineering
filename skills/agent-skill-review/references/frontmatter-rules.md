# Frontmatter rules

Reference for the `agent-skill-review` skill. Open before Step 2 of `SKILL.md`.

Everything needed to judge a skill's frontmatter is here. No external document is required.

---

## Check tables — score every ID

### Blockers

| ID | Check | Fails when |
|---|---|---|
| B1 | File is named exactly `SKILL.md` | any other casing, e.g. `skill.md`, `SKILL.MD` |
| B2 | Frontmatter opens and closes with `---` on their own lines | a delimiter is missing |
| B3 | Frontmatter parses as YAML | unclosed quote, or an unquoted value containing a colon followed by a space |
| B4 | `name` is present, kebab-case, lowercase | spaces, capitals or underscores |
| B5 | `name` matches the folder name | they differ |
| B6 | `name` does not begin with `claude` or `anthropic` | reserved prefix used |
| B7 | `description` is present and under 1024 characters | count it, do not estimate |
| B8 | No angle bracket characters anywhere in the frontmatter | either bracket appears |
| B9 | Top-level keys limited to `name`, `description`, `license`, `allowed-tools`, `metadata` | any other key |
| B10 | No `README.md` inside the skill folder | one exists |
| B12 | No pre-approved tooling, and no act-without-confirmation instruction, for High Risk (Rigor Level II) work | `allowed-tools` is present, or the body directs unattended action, on a skill scoped to High Risk units |

B11 is a body check. It lives in `body-rules.md`.

### Warnings

| ID | Check | Fails when |
|---|---|---|
| W1 | `description` states both WHAT the skill does and WHEN to use it | either half is missing |
| W2 | `description` contains at least two phrases a user would literally type | it only describes capability |
| W3 | `description` names concrete artefacts — repo, tool, or file extension | it is generic |
| W4 | A negative trigger is present | a sibling skill covers adjacent ground and neither excludes the other |
| W5 | `metadata.owner` is a team, not an individual | a person's name is used |
| W6 | `metadata.last-reviewed` is present, is today or earlier, and is no more than one quarter old | empty, dated in the future, or older than one quarter |
| W7 | `allowed-tools` is absent, or its presence is justified in the pull request | present with no justification |
| W8 | `allowed-tools` syntax matches the target harness | see below; no portable form exists |
| W16 | `metadata.source-repository` is present and is a bare `https://` repository URL | empty, not a URL, or carries credentials, a `.git` suffix, a branch or a file path |

W9–W15 are body checks. They live in `body-rules.md`.

---

## Field reference

Only these five top-level keys are permitted. Anything else fails B9.

| Field | Status | Copilot | Claude | Notes |
|---|---|---|---|---|
| `name` | REQUIRED | documented | documented | kebab-case; must match folder name; must not start with `claude` or `anthropic` |
| `description` | REQUIRED | documented | documented | under 1024 chars; must contain *what* **and** *when*; no angle brackets |
| `license` | OPTIONAL | documented | documented | SPDX id, e.g. `MIT`, `Apache-2.0` |
| `allowed-tools` | OPTIONAL | documented | documented | syntax differs per harness — see below |
| `metadata` | OPTIONAL | *not documented* | documented | free-form map, used for org governance — see values below, and the caveat further down |

Governance values inside `metadata`, for W5, W6 and W16:

| Key | Expected | Finding when wrong |
|---|---|---|
| `owner` | a team — the skill must survive its author leaving | W5 |
| `source-repository` | the `https://` URL of the git repository where this skill is maintained | W16 |
| `last-reviewed` | the date the skill was last reviewed — today or earlier, and no more than one quarter old | W6 |
| `risk` | `low` or `high` only — see the binary scale below | W7 neighbourhood; report as a warning |

## `source-repository` — for W16

`metadata.source-repository` records in which repository the skill is committed. It must be a valid URL,
without additional credentials, suffixes or usernames.

```yaml
# PASSES W16 — bare browse URL, no credentials, no suffix
  source-repository: https://dev.azure.com/diaitads/mollab/_git/Tool.ContextEngineering
```

```yaml
# FAILS W16 — embeds a username; also a §9 security-review finding
  source-repository: https://diaitads@dev.azure.com/diaitads/mollab/_git/Tool.ContextEngineering
```

```yaml
# FAILS W16 — not resolvable to a repository
  source-repository: Tool.ContextEngineering
```

Two keys that reviewers commonly see and should reject or question:

| Field | Verdict | Why |
|---|---|---|
| `compatibility` | fails B9 | documented for Claude only; excluded by org decision. The same information belongs in the `Prerequisites:` bullet of the body's `## Scope` section, which both harnesses read as plain Markdown. |
| provenance keys written by `gh skill install` (source repo, ref, tree SHA) | do not flag | added by tooling on install, not by the author. Present only in *installed* copies, never in source. Distinct from `metadata.source-repository`, which the author writes by hand and which W16 requires in the source. If the two disagree, raise it as an advisory — the skill was probably copied from a fork. |

## Hard constraints

These are absolute. A skill violating any of them may fail to load at all.

1. The file must be named exactly `SKILL.md`. Casing is significant.
2. Frontmatter must open and close with `---` on their own lines, and must be the very first
   thing in the file — no comment or blank line above it.
3. **No angle bracket characters anywhere in the frontmatter.** Frontmatter is injected into the
   system prompt, and angle brackets are rejected as an injection vector. This is the single
   most common cause of a skill that silently refuses to load.
4. Any value containing a colon followed by a space must be quoted, or the YAML will not parse.
5. `name` must not begin with `claude` or `anthropic` — reserved prefixes.

## The description field — clinic for W1, W2, W3

The description is the only part of a skill that is always in context. It is a retrieval key,
not a summary. Structure:

```text
[What it does] + [When to use it, with literal trigger phrases] + [When NOT to use it]
```

Use these examples to justify a W1–W3 finding concretely, rather than telling the author their
description is "too vague".

```yaml
# PASSES W1, W2, W3 — what, when, literal phrases, negative trigger
description: Triages failing Azure DevOps pipeline runs for a pull request using the
  Azure DevOps MCP server. Use when the user says "the build is red", "why did CI fail",
  "the pipeline broke on my PR", or pastes an Azure DevOps build URL. Do not use for
  local build errors that never reached a pipeline.
```

```yaml
# PASSES W3 — names concrete artefacts the user would actually say
description: Plans and executes a version bump for a shared NuGet library, including
  downstream consumer impact analysis. Use when the user asks to "release
  Library.Messaging.Interface", "bump the shared package", or "who consumes this library".
  Do not use for application repos that only consume packages.
```

```yaml
# FAILS W1 (no WHEN), W2 (no user phrasing), W3 (no artefacts)
description: Helps with builds.
```

```yaml
# FAILS W1 — capability only, no trigger condition
description: Implements a comprehensive Azure DevOps pipeline analysis subsystem.
```

```yaml
# FAILS W2, W3 — describes internals; uses no word a user would ever type
description: Wraps pipelines_build and pipelines_build_log MCP tool invocations.
```

Additional signals worth raising:

- A description opening with "This skill…" wastes always-loaded tokens. Advisory.
- Technical nouns are strong retrieval keys. `PackageReference`, `.csproj`,
  `azure-pipelines.yml` retrieve far better than "build configuration".
- A missing negative trigger only matters once a sibling skill covers adjacent ground. If no
  sibling exists, mark W4 as `n/a` rather than failing it.

## `allowed-tools` — divergence and security, for W7 and W8

**The two harnesses document different syntax for the same key. No portable form exists.**

```yaml
# GitHub Copilot documentation
allowed-tools: shell
```

```yaml
# Claude documentation
allowed-tools: "Bash(python:*) Bash(npm:*) WebFetch"
```

How to review it:

- **Absent is the correct default.** Without the key, the agent asks for confirmation before
  running a tool. That is the safe behaviour. Mark W7 and W8 `n/a` and move on.
- If present, the author must state which harness the skill targets. A Copilot-syntax value in
  a skill intended for both harnesses is a W8 finding.
- If present with no justification recorded in the pull request, that is a W7 finding.

**Security.** Pre-approving `shell` or `bash` removes the human confirmation step entirely. A
prompt injection reaching that skill then executes arbitrary commands in the user's environment.
Per the `## Critical` rules in `SKILL.md`, such a skill can never be PASS on a single review;
the report must name a required second reviewer, and the skill's own `metadata.risk` should
read `high`. If it reads `low`, raise that as a separate warning.

**The HITL mandate — for B12.** Roadmap §10.2 permits **HITL only** for software classified High
Risk (Rigor Level II), with no exception pathway. Pre-approving `shell` is functionally HOOTL,
and HOOTL is available only for tasks explicitly whitelisted by the A&T Discipline, on Low Risk
(Rigor Level I) units (roadmap §5.1, §5.4).

So B12 fails when either of these is true of a skill whose steps touch High Risk units:

- `allowed-tools` is present at all, or
- the body instructs the agent to proceed, push, deploy or delete without asking.

A skill that genuinely needs unattended execution must name the whitelisted task it implements.
If it names none, fail B12. B12 is a Blocker, however well the rest of the skill is written.

**`metadata.risk` is binary, and it is not a safety class.** Permitted values are `low` and
`high` only — the scale mirrors the chapter's binary software classification, which dropped its
middle tier because that tier proved endlessly interpretable (roadmap §3.4). Reject `medium`.

| Value | Correct when |
|---|---|
| `low` | read-only, or every mutation sits behind an explicit confirmation step; no `allowed-tools` |
| `high` | pre-approves `shell`/`bash`, or can push, tag, deploy or delete without confirmation |

The discriminator is whether a human decides before the irreversible thing happens. A skill that
releases software is still `low` if it cannot release without asking. And a skill's `risk` says
nothing about the IEC 62304 class of the code it touches — flag any skill whose body conflates
the two.

## Caveat: `metadata` is unverified in the Copilot harness

`metadata:` is documented for the Claude harness. The GitHub Copilot documentation does not list
it, and **no available source states whether Copilot ignores or rejects undocumented keys.**

Consequences for review:

- Do **not** fail a skill for carrying `metadata`. It is org-sanctioned.
- **Do** raise an advisory if any *instruction in the body depends on a `metadata` value.*
  Governance metadata must be human- and CI-facing only. If the harness drops the key, an
  instruction that reads it breaks silently.
- If a team reports that a `metadata`-carrying skill fails to load in Copilot, the fix is to
  move those fields into a `## Ownership` body section or a sibling `OWNERS.yml` outside the
  skill folder.

## Unverified behaviour register

State these as unknown when they come up in review. Do not assert either way.

| Question | Status |
|---|---|
| Does Copilot accept a `metadata:` block? | Unverified. See caveat above. |
| Is there a portable `allowed-tools` syntax? | No portable form is documented. |
| Does `compatibility:` work in Copilot? | Unverified, and excluded by org decision regardless. |

One question that used to sit here is settled: **the Claude harness does not discover
`.agents/skills/` natively** (roadmap §6.6). The remedy is a symlink `.claude/skills/` →
`.agents/skills/`, or an explicit reference from `CLAUDE.md`. Do not fail a skill for living in
`.agents/skills/`; check instead that the bridge exists in the consuming repository.

In every case the fallback is the same: move the information out of frontmatter and into the
body, where both harnesses treat it as plain Markdown.
