# Skill Authoring Guide

How to write an agent skill so that it triggers when it should, stays quiet when it is not needed, and stays maintainable over time.

Companion files:

- [skill-template.md](templates/skill-template.md) - copy this to start a new skill.
- [`agent-skill-review`](../skills/agent-skill-review/SKILL.md) - a real skill in this repository, used as the worked example (§12) and as the checker for the skills you write.

**Contents.** §1-§6 are what you need to write a skill; §7-§11 are what you need to ship one.

1. [What a skill is, mechanically](#1-what-a-skill-is-mechanically)
2. [Decide whether you need a skill at all](#2-decide-whether-you-need-a-skill-at-all)
3. [Plan before you write](#3-plan-before-you-write)
4. [The description field](#4-the-description-field)
5. [Writing the instructions](#5-writing-the-instructions)
6. [Optional sections and optional bundled files](#6-optional-sections-and-optional-bundled-files)
7. [Where skills live, and how they get there](#7-where-skills-live-and-how-they-get-there)
8. [Ownership and maintenance](#8-ownership-and-maintenance)
9. [Security review](#9-security-review)
10. [Testing](#10-testing)
11. [Troubleshooting](#11-troubleshooting)
12. [Worked example](#12-worked-example)
13. [Counter-example: this should not be a skill](#13-counter-example-this-should-not-be-a-skill)

---

## 1. What a skill is, mechanically

A skill is a folder with a `SKILL.md` in it. It loads in three stages, and every design decision in this guide follows from that:

| Stage | What loads | Cost | Implication |
|---|---|---|---|
| 1 | YAML frontmatter only | Paid on **every** request, for **every** installed skill | The `description` is the whole product. Get it right or nothing else matters. |
| 2 | `SKILL.md` body | Paid only when the agent decides the skill is relevant | Keep it to 80 lines or fewer. Front-load the critical parts. |
| 3 | Files in the skill folder | Paid only when the agent opens them | Push rare detail into `references/`. Push determinism into `scripts/`. |

Two consequences people miss:

- **Frontmatter is a shared, always-on budget.** Fifty installed skills means fifty descriptions in the system prompt on every turn, whether or not any of them is used.
- **Skills are composable and non-exclusive.** Several may load at once. Write yours so it does not assume it is the only thing steering the agent.

The format follows [this open specification](https://agentskills.io/specification).

---

## 2. Decide whether you need a skill at all

Most "I should make a skill for this" ideas are better served by something cheaper.

> If it must apply to every task, it is an instruction.
> If the human always asks for it by name, it is a prompt file.
> If the agent must *decide* when it applies, it is a skill.

A skill is one of several context primitives and it is not the default. Pick the one that matches the knowledge:

| Use | When | Why |
|---|---|---|
| **Instruction file** (`AGENTS.md`, `.github/copilot-instructions.md`, `CLAUDE.md`) | Knowledge about how to work *inside* a repository: code style, build command, branch naming, threading rules | Always loaded for the matching scope. No triggering risk. No maintenance surface. |
| **Skill** | How an *external consumer* uses a shared library, or a detailed conditional procedure the agent should load *only when relevant* | Cross-cutting; activates when the agent meets the library or pattern in use. Progressive disclosure earns its keep. |
| **Agent configuration** | The work needs specialist judgement, a different persona, model or tool allow-list | Skills cannot change the agent's identity |
| **Prompt file / slash command** | A repeatable multi-step process the human invokes by name every time | No triggering logic needed at all |
| **Memory file** | Decisions, trade-offs and history that explain *why* the code is the way it is | Dated background context, a fact and no rule |
| **Orchestration spec** | A specification of *what to build*: components, contracts, acceptance criteria | Carries the traceability metadata a skill cannot |
| **Hook** | An automated reaction to a development event | Event-driven; needs no agent invocation |
| **MCP server** | The agent needs *access* to a system it cannot reach | Skills add knowledge and no connectivity |

Then apply a design test. It is a skill only if **all three** hold:

- [ ] The knowledge applies across multiple files.
- [ ] It takes more than a few rules to express.
- [ ] It is triggered by a detectable code pattern.

If the knowledge applies to a single directory, it is an instruction. If it is a general disposition, it is an agent configuration.

Skills and MCP are complements. MCP is the kitchen; the skill is the recipe. An MCP server without skills produces questions that read "I connected it, now what?"

---

## 3. Plan before you write

Write 2-3 concrete use cases before opening an editor. Anything fewer and the skill is probably an instruction; anything more and it is probably two skills.

```text
Use case: Triage a failing PR build
Trigger:  "why did the build fail", "the pipeline is red", "fix CI on this PR"
Steps:    1. Resolve the pipeline + branch for the PR
          2. Get failing step name and error text without downloading full logs
          3. Rule out agent/environment failure before blaming the code
          4. Fetch only the log that matters
          5. Reproduce locally, fix, verify
Result:   Named root cause + a verified fix, without a 60k-token log dump
```

Ask, per use case:

- What does the agent get *wrong* today, repeatedly? That is the highest-value content.
- What does the user actually want at the end?
- Which tools are needed: built-in, MCP, or a bundled script?
- What domain knowledge do you have that the agent demonstrably lacks?

That first question is the one that matters. A skill that restates what the model already does well is pure context tax. A skill that encodes a non-obvious gotcha, one you learned the hard way, pays for itself on the first run.

**Pro tip:** iterate on one hard task in a normal chat until the agent succeeds, *then* extract the winning transcript into a skill. Far faster signal than writing a skill up front and testing it broadly.

---

## 4. The description field

This is the only part of your skill that is always in context. It is a retrieval key and a summary only secondarily:

```text
[What it does] + [When to use it, with literal trigger phrases] + [When NOT to use it]
```

Rules:

- Under 1024 characters. No `<` or `>`.
- Include the literal nouns your users say: product names, repo names, file extensions, tool names. Technical terms are strong retrieval keys: `PackageReference`, `.csproj`, `azure-pipelines.yml` are worth more than "build configuration".
- Include at least one negative trigger once you have a second skill in the same domain.
- Do **not** start it with "This skill...". Wasted tokens on the always-loaded line.

```yaml
# GOOD - what, when, literal phrases, negative trigger
description: Triages failing Azure DevOps pipeline runs for a pull request using the
  Azure DevOps MCP server. Use when the user says "the build is red", "why did CI fail",
  "the pipeline broke on my PR", or pastes an Azure DevOps build URL. Do not use for
  local build errors that never reached a pipeline.

# GOOD - mentions the concrete artefact names a user would say
description: Plans and executes a version bump for a shared NuGet library, including
  downstream consumer impact analysis. Use when the user asks to "release Acme.Messaging",
  "bump the shared package", or "who consumes this library". Do not use for application
  repos that only consume packages.

# BAD - too vague, will never trigger reliably and will also trigger on nothing
description: Helps with builds.

# BAD - no trigger conditions at all, only capability
description: Implements a comprehensive Azure DevOps pipeline analysis subsystem.

# BAD - describes internals, uses no word a user would ever type
description: Wraps pipelines_build and pipelines_build_log MCP tool invocations.
```

**Debugging a description.** Ask the agent, in a fresh session: *"When would you use the SKILL-NAME skill?"* It will paraphrase the description back. The gap between its answer and your intent is exactly what to edit.

---

## 5. Writing the instructions

**Be literal.** Every step needs a command or an observable condition. "Check the impact properly" is a wish and gives the agent nothing to execute.

```markdown
<!-- GOOD -->
Run `pwsh ./scripts/check-consumers.ps1 -Package Acme.Messaging`.
Expected output: a table of consuming repos and a total count.
If the count is above 10, stop and ask the user to confirm before proceeding.

<!-- BAD -->
Check the impact before proceeding.
```

**Front-load anything critical.** Instructions get diluted the further down the file they sit. Destructive or irreversible rules belong in a `## Critical` block immediately after the H1, and a Notes section at the bottom is too late.

**Prefer code to prose for anything with a right answer.** Language interpretation is probabilistic; a script is deterministic. If a validation has a definite correct answer (schema conformance, version ordering, "does this file exist"), bundle a script and tell the agent to run it. Reserve prose for judgement.

**Put the dependency in the step.** Steps are one numbered line each, `N. **STEP NAME**: WHAT-HAPPENS`, so the dependency, the expected output and the gate all sit on that line. Explicit ordering and explicit gates are the difference between a workflow and a suggestion.

```markdown
3. **CREATE SUBSCRIPTION**: Using `customerId` from Step 1, POST to `/subscriptions`. Do not
   continue until Step 2 has reported a verified payment method. Expected: HTTP 201 and an id.
```

**Keep it small.** 80 lines or fewer, the same cap the template carries. Past that, you have either two skills or a `references/` folder.

### The shared-library variant

One skill type deserves a fixed shape: the skill that documents a shared library for the people who consume it. An instruction file teaches an agent how to work *inside* a repository, and this skill teaches every other project how to *consume* the library. Ship it in the library's own repository.

Its contract is five items, which go in the template's `## Scope` and `## Usage` sections:

1. Purpose and scope.
2. Correct usage patterns, including a code example of the golden path.
3. Common misuse patterns.
4. Message contracts, where the library emits or consumes messages.
5. Threading and lifecycle constraints.

A shared-library skill that cannot fit those five in 80 lines has become documentation; link out to it instead.

---

## 6. Optional sections and optional bundled files

Which sections and directories exist, and whether each is REQUIRED, RECOMMENDED or OPTIONAL, is marked inline in [skill-template.md](templates/skill-template.md). What the template cannot decide for you is when the optional ones are worth their cost:

**`## Scope`** - required, and deliberately one section. It folds `When to use`, `When NOT to use` and `Prerequisites` into three bullets, because three headings cannot fit in the 80-line cap. Write `none` for a bullet that does not apply and keep the bullet.

**The `Not for:` bullet** - fill it the moment a second skill exists in the same domain. It is the cheapest possible fix for over-triggering and costs one line of always-loaded context if you also mirror it in the description.

**The `Prerequisites:` bullet** - fill it when the skill will fail confusingly instead of obviously. "MCP server not connected" surfaces as a tool error deep in Step 4; a prerequisite check surfaces it at Step 0 with a fix.

**`## Usage`** - required for a shared-library skill, because it carries four of the five contract items from §5. Delete it for every other skill type.

**`scripts/`** - the agent discovers every file in the skill folder when the skill loads, so a script is available without any registration step. Reference it by path relative to the skill's base directory. Read §9 before pre-approving `shell` via `allowed-tools`.

**`references/`** - link, and never inline. Give the agent a *condition* for opening it:

```markdown
GOOD: Before writing any query, read `references/ado-mcp-gotchas.md` for parameter formats.
BAD:  See also references/ado-mcp-gotchas.md.
```

**`assets/`** - templates the skill fills in. Keep them free of instructions; instructions belong in `SKILL.md`.

---

## 7. Where skills live, and how they get there

| Scope | Directory | Read by |
|---|---|---|
| Project, cross-harness | `.agents/skills/` | Read natively by Cursor, Windsurf, OpenCode and Codex. **Copilot and Claude Code both need a bridge, see below.** |
| Project, Copilot-specific | `.github/skills/` | Copilot. Also the directory Copilot **code review** picks up automatically. |
| Project, Claude-specific | `.claude/skills/` | Claude harness |
| User-wide, Claude | `~/.claude/skills/` | Claude harness, in every project |

Three carve-outs:

- The Copilot **code review** harness does not read `.agents/skills/`. Publish skill folder links under `.github/skills/`.
- For Copilot **code review** the skill folder has to be named something descriptive (e.g. `code-review`) so that it can be distinguished from other skills.
- Claude Code does not discover `.agents/skills/` natively. Bridge it: symlink `.claude/skills/` to `.agents/skills/`, or reference the skill explicitly from `CLAUDE.md`.

Never hand-maintain a second copy for any of these. Duplicated content across tool directories drifts, so link it or reference it. A skill is portable content, so write it **once** under `.agents/skills/` and treat everything else in the tree as thin bridging:

```text
my-repo/
├── AGENTS.md                      <- instructions; read natively by most harnesses
├── .agents/
│   └── skills/
│       └── measurement-uncertainty/
│           └── SKILL.md           <- the skill, written once, here
├── CLAUDE.md                      <- imports @AGENTS.md; references the skill explicitly
├── .claude/
│   └── skills/                    <- link to ../.agents/skills
├── .github/
│   └── skills/
│       └── measurement-uncertainty/ <- link to ../../.agents/skills/measurement-uncertainty
└── src/
```

This repository is a source library of skills and agents, so it keeps them at the top level (`skills/`, `*.agent.md`) and has no bridging of its own. Consuming repositories copy or link them into the layout above.

### Getting a skill into a repository

There is no package manager for skills. Distribution is a copy, so keep one source of truth and copy from it instead of authoring the same skill twice.

1. Take the source folder from the repository that maintains it. The copy carries `metadata.source-repository`, which identifies where it came from.
2. Copy the **whole skill folder**, with all of `references/`, `scripts/` and `assets/`, into `.agents/skills/<name>/` in the consuming repository.
3. Add whatever tool bridging that repository needs, then commit.

For Claude.ai, zip the skill folder and upload it under Settings, Capabilities, Skills.

Because every copy is manual, copies drift. Comparing the `metadata.version` and `metadata.source-repository` keys of two copies shows which one is stale.

Run `agent-skill-review` on a skill before it merges, and again when a copy is updated. A malformed skill that reaches a consuming repo is expensive to recall, because recalling it is also a copy.

---

## 8. Ownership and maintenance

**Ownership.** Every skill carries `metadata.owner`. Name a team or a handle that will still exist next year, and the skill survives its author losing interest. An unowned skill is deleted and nobody adopts it. See the `metadata` caveat in the template: if a harness turns out to reject the key, move these fields to a body section or a sibling `OWNERS.yml`.

**Provenance.** Every skill also carries `metadata.source-repository`: the bare `https://` URL of the git repository where it is maintained.

```yaml
  source-repository: https://github.com/OWNER/REPO
```

It names the repository and leaves the folder out, because the folder is already `name` and a path goes stale the moment the skill moves. Write it even when the source is the repository you are sitting in, because the consumer who needs it will be somewhere else. The reviewer skill scores this as W16.

**Maintenance is a feedback loop.** When an agent repeats a mistake this skill should have prevented, fix the skill and the output together. Correcting the generated code and moving on guarantees the same failure next session, with the next agent, on the next task. Two consequences:

- A recurring failure traced to this skill is a defect in this skill, and lands as a change to it with a version bump.
- After changing a skill, re-run the functional tests in §10 before publishing. A wording change that improves one path can quietly degrade another.

**Versioning.** Semver on `metadata.version`:

- **major**: changed trigger surface, removed step, changed script arguments
- **minor**: new step, new optional bundled file, broadened description
- **patch**: wording, typo, added troubleshooting entry

Consumers hold copies, so `metadata.source-repository` and `metadata.version` together are the only way they can tell a stale copy from a current one: the first finds the source, the second dates the copy. Announce majors loudly and directly, since nothing prompts a consumer automatically.

**Naming.** Kebab-case, `domain-object-action`: `ado-build-failure-triage`, `shared-library-release`. Avoid `helper`, `utils` and `misc`. The name is a retrieval key too. Never begin a name with `claude` or `anthropic`, which are reserved.

**Deprecation.** Set `metadata.status: deprecated`, and edit the **description** first, because that is what controls triggering:

```yaml
description: DEPRECATED, use shared-library-release instead. Previously handled NuGet
  version bumps.
```

Leave it deprecated for one release cycle, then delete. Deleting without a deprecation window strands every repo holding a copy, with no signal that the source is gone.

**Portfolio hygiene.** Frontmatter is an always-on shared budget. Review the whole catalogue quarterly:

- `metadata.last-reviewed` records when the skill was last reviewed.
- Two skills whose descriptions overlap will fight for the same triggers. Merge them or add mutual negative triggers.
- Past roughly 20-50 simultaneously enabled skills, expect measurable degradation. Ship role-scoped packs and skip "install everything".

---

## 9. Security review

Skills are executable instructions injected into an agent's context. Treat them as code.

Review gate before merging a skill into a shared skills repository:

- [ ] Read `SKILL.md` in full. Look for instructions that exfiltrate, escalate or disable checks.
- [ ] Read **every** bundled script line by line.
- [ ] Confirm no secret, token, connection string or internal hostname is embedded. This includes `metadata.source-repository`, which is a bare browse URL.
- [ ] Confirm `allowed-tools` is absent, or justified in the PR description.
- [ ] If `allowed-tools` includes `shell` or `bash`: second reviewer required, `risk: high`.
- [ ] **Least privilege**: the skill asks for the narrowest file, tool and system scope its steps actually need. A skill that touches three files should not be written to assume repository-wide write access.
- [ ] **Input copyright**: no third-party copyrighted material (vendor SDK docs, licensed technical references, purchased standards) is copied verbatim into `SKILL.md` or `references/`. Summarise it in your own words, or link to the licensed source.
- [ ] **External content**: steps that read dependency READMEs, vendor pages or other third-party content are restricted to first-party sources for security-sensitive work. Adversarial content in a dependency README is a live injection path.
- [ ] **Context files are code**: the skill folder is covered by the same branch protection and PR approval rules as production code in its home repository.
- [ ] For any third-party skill: read the entire folder before copying it in, and re-read the diff before taking any update. Nobody verifies third-party skills for you.

Set `metadata.risk`. The scale is **binary**, because a middle tier proves endlessly interpretable:

| Risk | Meaning |
|---|---|
| `low` | Read-only, or every mutation sits behind an explicit confirmation step. No `allowed-tools`. |
| `high` | Pre-approves `shell`/`bash`, or can take an irreversible action (push, tag, deploy, delete) without a confirmation step. |

The discriminator: **does a human decide before the irreversible thing happens?** A skill that pushes tags is still `low` if it cannot push without asking. Skills that reach `high` need a `## Critical` block enumerating exactly what they will never do without asking.

`metadata.risk` describes the skill's own blast radius and says nothing about how critical the code it touches is. A skill should never pre-approve tools, or instruct the agent to act without confirmation, on work where a wrong action is costly to undo. Pre-approving `shell` means unattended execution, so a skill that needs it must say which task it automates and why no confirmation step is needed. If it cannot say, it does not get `allowed-tools`.

---

## 10. Testing

Three layers. Do all three for any skill shared across repositories; layer 1 alone is acceptable for a repository-specific skill.

**Layer 1: triggering.** Write the suite in the PR description. Target: triggers on ~90% of the should-trigger set without the user naming the skill. Run each in a **fresh session**, because a warm session biases the result.

```text
SHOULD trigger:
- "The build failed on my PR, can you look?"
- "Why is CI red on my-service?"
- "https://dev.azure.com/my-org/my-project/_build/results?buildId=12345 what went wrong"

SHOULD NOT trigger:
- "My local dotnet build is failing"          -> plain agent behaviour
- "Add a new stage to azure-pipelines.yml"    -> pipeline authoring, not triage
- "What's the weather in Basel?"
```

**Layer 2: functional.** Cover the error paths too: MCP disconnected, build still running, no build for the branch.

```text
Test:  Triage a build that failed in the restore step
Given: A PR with a known NuGet restore failure
When:  The skill runs
Then:  - Failing step is named correctly    - Root cause is restore, not test
       - No full log download occurred      - Zero failed MCP calls
```

**Layer 3: baseline comparison.** Run the same request with and without the skill and record the table below. If the "with" column is not clearly better, the skill is context tax: delete it or fix it. This is the single most-skipped step and the reason most skill catalogues rot.

| Metric | Without | With |
|---|---|---|
| Turns to resolution | | |
| Tool calls | | |
| Failed tool calls | | |
| Tokens consumed | | |
| User corrections needed | | |

---

## 11. Troubleshooting

### Skill will not load

| Symptom | Cause | Fix |
|---|---|---|
| "Could not find SKILL.md" | Wrong filename case | Rename to exactly `SKILL.md` |
| "Invalid frontmatter" | Missing `---`, unclosed quote, unescaped `:` | Re-check both delimiters; quote values containing `: ` |
| "Invalid skill name" | Spaces or capitals in `name` | kebab-case only |
| Rejected without explanation | `<` or `>` in frontmatter | Remove them (security restriction) |

### Skill never triggers

The description is wrong. In order: is it generic? ("Helps with builds" retrieves nothing.) Does it contain phrases users literally type? Does it name the concrete artefacts: repo names, file extensions, tool names? Then run the fresh-session check in §4.

### Skill triggers too often

1. Add negative triggers to the description.
2. Narrow the scope: "processes documents" becomes "processes Azure DevOps build logs".
3. Check for a sibling skill competing for the same words.

### Skill loads but the agent ignores the instructions

| Cause | Fix |
|---|---|
| Too verbose | Cut. Move detail to `references/`. |
| Buried | Move critical rules directly under the H1, under `## Critical`. |
| Ambiguous | Replace "validate properly" with an explicit checklist or a script call. |
| Skipping steps | Add explicit validation gates between steps. Encouragement text ("be thorough") works better in the user prompt than in `SKILL.md`. |

### MCP calls fail although the skill loaded

Test the MCP server directly, without the skill. If that fails, the skill is the wrong place to look. Otherwise check tool names: they are case-sensitive and drift between server versions.

### Everything is slow and answers got worse

Too much always-on context. Audit the installed catalogue and disable what the current work does not need.

---

## 12. Worked example

Read [`agent-skill-review`](../skills/agent-skill-review/SKILL.md), a real skill that lives in this repository, instead of a fabricated sample. Being a review skill, it is also the fastest way to see this guide's rules applied to a skill by a skill.

| Guide section | What to look for |
|---|---|
| §4 | A `description` that states what it does, carries four phrases a user would literally type, and closes with two negative triggers |
| §5 | `## Critical` sits directly under the H1, so the never-do rules come before the procedure |
| §5 | One numbered line per step, each naming its expected output, e.g. Step 1's "Expected: a file tree" |
| §5 | A hard gate in Step 1: no `SKILL.md` at the folder root means stop and report |
| §6 | A `## Scope` section whose `Not for:` and `Prerequisites:` bullets both earn their place |
| §6 | A `references/` folder in which every file is linked *with the condition for opening it* |
| §8 | A filled-in `metadata` block: owner, `source-repository`, semver, `status`, `last-reviewed` |
| §9 | `risk: low`: it reads and reports, and is explicitly forbidden from rewriting what it reviews |

It deliberately has no `scripts/` directory and no `allowed-tools` field. Most skills need neither. See §5 for when a bundled script is the right answer, and §9 before you reach for `allowed-tools`.

---

## 13. Counter-example: this should not be a skill

```yaml
# Do not do this
name: csharp-coding-standards
description: Our C# coding standards, nullable enabled, file-scoped namespaces,
  no regions, xUnit with FluentAssertions.
```

Why it fails: it applies to *every* C# task in the repo, so it must never be conditionally loaded. As a skill it will sometimes not trigger, and the agent will silently write non-conforming code. There is no signal that it failed.

Correct home: repository custom instructions (`.github/copilot-instructions.md` / `AGENTS.md` / `CLAUDE.md`), which are always loaded.

The rule again: **always-applicable means instructions. Conditionally-applicable means skill.**
