# Custom Agent Authoring Guide

How to write a custom agent (`*.agent.md`) so that it is discovered, does one job well, stays inside its boundaries and survives its author leaving.

Companion files:

- [custom-agent-template.md](templates/custom-agent-template.md): copy this to start a new agent file. It encodes the section order and marks every section required, recommended or optional.
- [`custom-agent-review`](../.agents/skills/custom-agent-review/SKILL.md): a skill that scores an agent against this guide with 36 checks and a PASS, PASS WITH WARNINGS or FAIL verdict. Run it before you open the PR.

**Where the rules come from.** A rule follows from how the harnesses load an agent file, from the harnesses' documentation, or from a convention this repository adopts where the documentation leaves the point open.

**Contents.** §1 to §9 are what you need to write an agent. §10 to §15 are what you need to ship and keep one.

1. [What an agent file is, mechanically](#1-what-an-agent-file-is-mechanically)
2. [Decide whether you need an agent at all](#2-decide-whether-you-need-an-agent-at-all)
3. [Plan before you write](#3-plan-before-you-write)
4. [Folder structure and naming](#4-folder-structure-and-naming)
5. [Frontmatter](#5-frontmatter)
6. [The description](#6-the-description)
7. [The body](#7-the-body)
8. [Tools and permissions](#8-tools-and-permissions)
9. [Context, delegation and multi-agent design](#9-context-delegation-and-multi-agent-design)
10. [Governance and maintenance](#10-governance-and-maintenance)
11. [Security review](#11-security-review)
12. [Testing](#12-testing)
13. [Troubleshooting](#13-troubleshooting)
14. [Anti-patterns](#14-anti-patterns)
15. [Pre-merge checklist](#15-pre-merge-checklist)

Appendix: [Agent skeleton](#agent-skeleton) (points to the template)

---

## 1. What an agent file is, mechanically

An agent file is a Markdown file with YAML frontmatter. The frontmatter configures the agent (name, description, tools, model). The body is the agent's system prompt. The file loads only when a person selects the agent or a parent thread delegates to it. The harness then starts a new thread governed by that file, so the cost of its body is paid inside that thread and nowhere else. The `description` is the exception: harnesses load it into the parent context so the agent can be chosen (§5). It answers one question: who does this task, with which tools and limits?

Four consequences shape everything below:

- **The agent starts with a clean context.** In Claude Code a subagent receives its body, basic environment details and the project context files (`CLAUDE.md`, git status), with no conversation history. In every harness, anything the agent must know has to be in the file, reachable from it, or handed over in the delegation message.
- **The file is a system prompt, so it competes for attention.** Models attend less reliably as context grows. A 300-line agent file is paid in full inside its thread, on top of the task and the tool output.
- **The frontmatter is configuration the harness enforces.** The body is advice the model may or may not follow. Limits that matter belong in `tools` (§8), and the body states them as well.
- **Files that steer an LLM are code.** Review, version and test them like code.

---

## 2. Decide whether you need an agent at all

Use the simplest design that reliably works: a direct model call, then one agent with tools, then multiple agents. Add a level only when the lower one measurably fails.

Pick the primitive with this test:

> If it must apply to every task in a repository, it is an instruction.
> If the agent must decide when a procedure applies, it is a skill.
> If a human always starts it by name with the same steps, it is a prompt file.
> If the work needs a different role, a restricted tool set, a different model, or its own clean context, it is an agent.

Write an agent when at least one of these holds:

- **Different tool boundary.** The job needs a narrower or different tool list than the default (a read-only reviewer, an audit agent without write tools).
- **Own context.** The job reads a lot (a repository clone, a batch of work items, logs) and would flood the parent thread. A separate thread returns a summary.
- **Specialist judgment.** The job needs named domain knowledge and anti-patterns that a general agent lacks.
- **A repeatable end-to-end workflow** that a person starts with one input (a PR URL, a repository URL).

Keep one agent and add tools or skills when the two jobs share a context and a tool list. Split an agent when it fails in one of two ways:

- **Complex logic.** The prompt carries many if-then-else branches and templates no longer scale. Give each logical segment its own agent.
- **Tool overload.** The agent picks wrong tools. The cause is overlap between tools more than their count: 15 distinct, well-described tools can work where 10 overlapping ones fail. Clarify names and descriptions first, then split.

Start small: three to five agents, for example an architect, a domain expert for core business logic and a documentation writer. A new agent earns its place by repeated corrections that point at a missing specialization. An agent with no failure history behind it is a guess.

Do not write an agent for a rule that applies to all code in the repository (that is an instruction), or for deterministic work such as formatting, linting or version-ordering (that is a script or a pipeline step, see §8).

---

## 3. Plan before you write

Write down the following before you open an editor. If you cannot fill a line, the agent is not ready to be written.

```text
Job:            Audit one repository's dependency setup and report gaps
Starts from:    A repository URL pasted by the user
Failure today:  A general agent skips the lockfile check and guesses the package manager
Tools needed:   read files, run git, a package-registry MCP server (read only)
Must never:     Change dependency settings, push, or open issues without asking
Hands back:     A table with one row per check and a verdict per row
Done when:      Every check has a verdict, or a named blocker
Human gates:    Before any write to the issue tracker or the repository
```

- **Name the failure it prevents.** The highest-value content in an agent is the thing a general agent gets wrong repeatedly: the unwritten convention, the gotcha, the reason behind a choice. Text that restates what the model already does well costs attention and changes nothing.
- **Derive instructions from what exists.** Rewrite existing procedures, runbooks and policies as short, checkable steps instead of writing the routine from memory. Name the source document in the agent's README so a reviewer can compare the two.
- **Iterate in chat first.** Run the task in a normal session until it succeeds, then extract the winning approach into the file. This gives faster signal than writing the agent up front.
- **Choose the model last.** Prototype on the most capable model to set a quality baseline, then try smaller ones and keep the cheapest that still meets the bar.

---

## 4. Folder structure and naming

**Rule.** Publish whole agent folders, so everything an agent needs travels with it.

```text
.agents/
  <agent-name>/
    <agent-name>.agent.md        the agent (required)
    README.md                    optional: usage notes, source document (see §10)
    references/                  files only this agent reads, opened on a condition
    skills/<skill-name>/SKILL.md skills only this agent uses
  skills/<skill-name>/SKILL.md   skills shared by several agents
```

**Rules for a repository that publishes agents:**
- Agent `name` values are unique across all agent folders, ignoring case.
- Skill folder names are unique across shared and agent-owned skills.
- A folder is an agent only if it holds an `*.agent.md`, and a skill only if it holds a `SKILL.md`.
- Keep one `*.agent.md` per agent folder.
- VS Code finds agent files through `chat.agentFilesLocations`. If the folder is not in a default location, add it there.
- When an agent is added, moved or renamed, update the catalog and the directory tree in `README.md`.

**Rule:** use lowercase kebab-case `domain-object-action` and make the folder name, the file stem and the frontmatter `name` identical (`pr-review/pr-review.agent.md` with `name: pr-review`). Reason: Copilot identifies an agent by its file name and Claude Code by its `name` field. Three different strings for one agent means three different identifiers depending on where it runs. Put the human-readable title in the H1.

**Names say the job.** `repo-audit`, `pr-review`, `documentation-assessment` work. `helper`, `utils`, `assistant` and names that start with `claude` or `anthropic` do not.

Placement by scope:

| Scope | Copilot | Claude Code |
|---|---|---|
| Repository | `.github/agents/` | `.claude/agents/` |
| User | `~/.copilot/agents/` | `~/.claude/agents/` |
| Organization | GitHub organization-level agents | Managed settings |

Never keep a second hand-edited copy in one of these folders. Agent files have no common standard: Copilot uses `.agent.md`, Claude Code a plain `.md`, Codex a `.toml` under `.codex/agents/`. Port by translation from the single source.

---

## 5. Frontmatter

Fields that matter, with what each harness documents:

| Field | Claude Code | Copilot (VS Code and GitHub) | Guidance |
|---|---|---|---|
| `name` | Required, unique, up to 256 characters, no `:` | Optional display name. The file name is the identifier | Required here, equal to the folder name (§4) |
| `description` | Required, drives delegation | Required, drives selection | See §6 |
| `metadata` | Not a documented field, ignored without a message | String pairs, documented for GitHub.com and the CLI, ignored by IDEs | Required here, see §10 |
| `tools` | Allowlist, as a comma-separated string or a YAML list. If omitted, the agent inherits every available tool | Omitted or `["*"]` enables all tools, `[]` disables all | Always set it, never `*`. One comma-separated line that names tools in both vocabularies (§8) |
| `disallowedTools` | Denylist applied before `tools` | Not documented | Use when the allowlist would be long |
| `model` | `sonnet`, `opus`, `haiku`, a full ID, or `inherit` | Model name | Omit unless the job needs a specific model. Names differ per harness |
| `argument-hint` | Not documented | Documented for IDE agents, ignored on GitHub.com | Add for agents a person starts with an input |
| `handoffs`, `user-invocable`, `disable-model-invocation`, `target` | Not documented | Copilot only | Add only when you use the feature, and test in Copilot |
| `permissionMode`, `maxTurns`, `skills`, `mcpServers`, `hooks`, `memory`, `effort`, `isolation` | Claude Code only | Not documented | Add only when you use the feature, and test in Claude Code |

Facts that cause silent failures:

- **Unknown fields are ignored without a message.** Claude Code skips unrecognized fields and reports nothing. A misspelled `disallowedTool` does nothing. Run `claude --debug` and search for `does not recognize or apply` to find them.
- **Invalid files are skipped.** Claude Code silently skips an agent file with no `name`, with the opening `---` not on line 1, or with unparseable YAML. Quote any value that contains `: `.
- **Tool names differ between the harnesses, and one list can serve both.** Claude Code refuses to launch a subagent when no `tools` entry resolves (`would be spawned with zero tools`), and Copilot ignores names it does not know. Each harness skips the entries meant for the other, so a list that names every capability in both vocabularies loads in both. A list written in Copilot names only (`read`, `search`, `execute`, `vscode/askQuestions`, `server/*`) aborts every prompt in Claude Code. The syntax is in §8.
- **Body size.** GitHub limits the Markdown body to 30,000 characters. Claude Code warns when the combined descriptions of all custom subagents pass about 15,000 tokens.

**Common style.** One style for every agent in the repository, so a diff shows only content:

```yaml
---
name: repo-audit
description: "Use when a maintainer needs to audit one repository for dependency hygiene: lockfile present, pinned versions, known advisories. The user pastes a repository URL to start. Do not use to fix findings (use dependency-fixer) or to audit many repositories at once (use org-audit)."
tools: Read, TodoWrite, mcp__github__*, github/*
argument-hint: "Paste a repository URL (e.g. https://github.com/OWNER/REPO)"
metadata:
  owner: platform-team
  source-repository: https://github.com/OWNER/REPO
  version: 0.1.0
  status: draft
  last-reviewed: "2026-10-30"
  risk: low
---
```

- `description` is a double-quoted single-line string.
- `tools` is one comma-separated line in the portable syntax (§8), with no commented-out alternatives. A commented `#tools:` line means the agent inherits every tool, so delete it or fill it.
- No `model` unless justified in the PR description.
- `metadata` with all six keys (§10).
- No angle bracket characters (`<` or `>`) in the values of `description`, `argument-hint` and `metadata`. Square brackets are fine. Write a placeholder as `REPO-URL` or `[repo-url]`.
- No fields from a harness you have not tested.

---

## 6. The description

The description is the retrieval key. It is the text a parent agent or a person reads to decide whether to pick this agent.

Formula:

```text
[What it does] + [When to use it, with the literal words users type] + [When NOT to use it, naming the sibling to use instead]
```

Rules:

- Lead with the trigger. Front-load the words that distinguish this agent from its neighbours. Start with `Use when` or a verb, never with `This agent`.
- Name the artifacts users say: product names, URL shapes, tool names, file names (`GitHub PR URL`, `catalog-info.yaml`, `quality gate`).
- Add a negative trigger as soon as a second agent covers a nearby job, and name that agent.
- State the input when a person starts the agent (`The user pastes a repository URL`).
- Keep it brief. Move detail into the body, which loads only when the agent runs.

```yaml
# GOOD: what, when, literal trigger, negative trigger
description: "Use when auditing one repository for dependency hygiene, started with a repo URL or inside a checked-out repository. Do not use for batch audits (use org-audit)."

# WEAK: no trigger words and no boundary, so it cannot be told apart from a general agent
description: Reviews a pull request acting as a senior developer.

# BAD: describes internals and gives a parent nothing to match
description: Wraps the pipelines and repo MCP tools.
```

Test it: in a fresh session, ask "When would you use the NAME agent?" The gap between the answer and your intent is what to edit. Then run the trigger suite in §12.

---

## 7. The body

The body is the system prompt. Write it as the briefing you would give a capable colleague who has never seen this repository and cannot ask you questions.

### Structure

**Fixed section order.** Start from [custom-agent-template.md](templates/custom-agent-template.md), which already has it. Prohibitions lead, as in [agents-md-authoring-guide.md §3](agents-md-authoring-guide.md#front-load-safety-boundaries), because an agent on a tight context budget may never reach rules that sit at the bottom.

1. **H1 and role.** One to three sentences: who the agent is, what it produces, for whom. Make the expertise specific ("Click CLI design with Rich output") because "expert developer" narrows nothing.
2. **`## Critical`.** The never-do rules and the human gates: what needs confirmation, what is out of bounds, when to stop. Required when `tools` includes a write tool, a shell or a write MCP tool. A read-only agent may omit it.
3. **`## Prerequisites`.** What must exist (an MCP server, a token, a clone). Check it first and stop with a fix when it is missing, so a missing server surfaces at step 0 and not as a tool error in step 6.
4. **`## Inputs`.** What the agent asks for, in one batched question, and what it derives itself.
5. **`## Steps`.** One numbered line per step, with the expected result or gate on that line.
6. **`## Output`.** The exact shape of what the agent hands back.
7. **`## Definition of done`.** The checkable condition that ends the run, including a verification step.
8. **`## Delegation`** (optional). Only for an agent that starts other agents: the brief it gives, its fan-out and its depth (§9).
9. **`## Troubleshooting`** (recommended). One entry per failure you have actually seen.
10. **`## References`.** Pointers to `references/` files and skills, each with the condition for opening it.

### Writing rules

- **Be literal where the answer is checkable.** Commands, formats, gates, ordering that matters and thresholds get an observable condition ("stop if the count is above 10"). "Handle errors properly" is a wish.
- **Describe the goal where judgment is needed.** For current models, state outcomes, constraints and how to verify, and keep numbered scripts for steps where order is fragile. A hand-written script for a judgment task often does worse than the model's own plan. Aim for the right altitude: specific enough to steer, loose enough to let the model apply heuristics.
- **Give the reason.** A rule with its "because" generalizes to cases you did not list. A bare prohibition can anchor the model toward the failure it names, so keep prohibitions for failures that actually reproduce, and write the rest as positive intent.
- **Use emphasis sparingly.** When several lines are marked CRITICAL, MANDATORY or ALWAYS, the markers stop carrying information, and older-model habits such as `THIS STEP IS MANDATORY!` make current models over-apply the rule. Reserve emphasis for the one or two rules a test showed the agent underweighting.
- **Give every step a completion criterion.** "Every check has a verdict or a named blocker" beats "produce a list". Vague bounds invite premature completion, and checkable, exhaustive ones drive thorough work.
- **Gate irreversible actions in the file.** `STOP`, present the plan, wait for approval. Each of these needs the user's confirmation immediately before the action: commit, push, creating a PR, posting a comment, any work item write.
- **Show a few varied examples** for format-sensitive output. One gold example gets copied literally (length, tone, structure), so give two or three that differ, labelled as illustrative.
- **Prune.** Delete a line the model already obeys by default, a line that restates `README.md` or a skill, a line that describes the environment (a lookup the agent can run), and a line that explains a model-version workaround nobody can trace. Keep the unwritten convention, the reason and the gotcha.
- **Do not describe the grader.** State the requirement. "You will be scored on..." pushes effort toward being watched.
- **Point, do not paste.** A pointer names the material and the condition that triggers reading it: "Before writing any query, read `references/mcp-gotchas.md`." "See also references/x.md" fires unreliably.

### Size and splitting

**Rule: 150 lines is the target, 30,000 characters is the platform ceiling.** Both count the body only, that is everything after the closing `---` of the frontmatter. Agent threads pay the body in full, so the AGENTS.md budget of 40 to 50 lines does not apply, and attention still thins as the file grows. Past 150 lines, decide where each block belongs:

| Block                                                                 | Move to                                  |
| --------------------------------------------------------------------- | ---------------------------------------- |
| Reference tables, long lookups, format specs read in only some runs   | `references/` with a conditional pointer |
| A procedure reused by another agent                                   | A shared skill under `.agents/skills/`   |
| A procedure only this agent uses                                      | `skills/` inside the agent folder        |
| A deterministic check (counting, version ordering, schema validation) | A script the agent runs                  |
| Rules for a different job                                             | A second agent                           |

Split sequences carefully: later steps in view tempt the model to rush the step in front of it, and a split across a real context boundary (a delegated child thread) hides them. An inline call does not.

---

## 8. Tools and permissions

Bound every agent on three axes: capability (which tools), knowledge (which context loads) and authority (what needs a human). An agent that can do everything is the "unbounded agent" and its blast radius is the whole repository.

**Tool list syntax.**

- Write `tools` as one comma-separated line (`tools: Read, Grep, Glob`).
- Name built-ins in Claude-style PascalCase: `Read`, `Edit`, `Write`, `Grep`, `Glob`, `Bash`, `TodoWrite`. Copilot accepts them as aliases. Test any other built-in in both harnesses before you use it.
- Name every MCP server in both forms: `mcp__SERVER__*` for Claude Code and `SERVER/*` for Copilot, where SERVER is the server name. When the agent needs only some tools, list them one by one in both forms (`mcp__SERVER__TOOL`, `SERVER/TOOL`). Take SERVER from the MCP configuration and confirm the Claude Code name with `/mcp`, because a name that does not match resolves to nothing.
- Never name a capability in one vocabulary only. Lowercase aliases (`read`, `search`, `execute`, `todo`) and Copilot IDs (`search/listDirectory`, `vscode/askQuestions`) are not Claude Code names, and an `mcp__` name is not a Copilot name. An entry that resolves in only one harness is harmless as an extra. A list in which no entry resolves in a harness makes that harness refuse the launch or leaves the agent without the tool.

```yaml
tools: Read, Grep, Glob, mcp__github__*, github/*
```

**Rules**

- **Set `tools` explicitly on every agent.** An omitted `tools` line inherits everything in Claude Code and enables everything in Copilot. Wildcards (`["*"]`) are the same failure written down.
- **Start from the role, then tighten.** These roles are a good start:

| Role                       | Capability                                       | Authority                                                     |
| -------------------------- | ------------------------------------------------ | ------------------------------------------------------------- |
| Planner, reviewer, auditor | Read, search, read-only commands. No write tools | None needed. The output is commentary or a plan               |
| Code writer                | Edit and run tests inside a named path           | Stop before API signature, schema, auth or dependency changes |
| Test runner                | Run tests, read sources                          | Stop before deleting fixtures or skipping tests               |
| Deployer                   | Deploy scripts only                              | Human approves every environment promotion                    |

- **A tool list and a prose limit say the same thing twice on purpose.** The list is enforced. The prose tells the model why, so it does not keep trying. A prose rule on its own ("never run mutating git commands") is a request, so grant `Bash` only when the job needs a shell. A shell sets `metadata.risk: high` and needs a second reviewer.
- **Prefer a narrow tool to a shell.** A dedicated tool gives the harness a typed hook to gate, log and parallelize. `bash -c "curl -X POST ..."` is an opaque string. Where a shell is unavoidable, restrict the allowed commands in the harness permission rules (in Claude Code, a `Bash(git push *)` entry in `disallowedTools` removes the whole tool, so use a `permissions.deny` rule for specific commands).
- **MCP server wildcards (`mcp__server__*`, `server/*`) need a reason.** Name the tools the job uses. If you take the whole server, record why in the PR description.
- **Add a path boundary in the body** for any agent that can write: the directories it may change and the ones it may not.
- **Consequential effects go on the deterministic side.** The model proposes, a gate disposes. Where a write is irreversible (a push, a published comment, a work item), the agent presents the exact change and waits. Rating each tool low, medium or high (read-only versus write, reversibility, account permissions, financial impact) is a useful way to decide which tools get a gate.
- **Human decision first.** On work touching production or safety-critical systems an agent must not act without confirmation, and pre-approving a shell is functionally unattended execution.

---

## 9. Context, delegation and multi-agent design

### Brief the agent you delegate to

A delegated agent starts clean, so the delegation message is its whole task. Vague briefs ("research the semiconductor shortage") lead to duplicated and missed work. Give every delegated agent four things: an objective, an output format, the tools and sources to use, and task boundaries. Define each agent's slice so no two cover the same ground.

Subagents see no conversation history, so decisions the parent made earlier in the session have to be restated in the delegation message.

### Keep the parent clean

- Return a condensed summary (roughly 1,000 to 2,000 tokens) and write large outputs to a file, returning the path.
- Pass state through files: a plan file, a focused brief. Re-read the plan at decision points in long runs so it sits near the end of context, where attention is strongest.
- Reset after two pasted error traces and carry forward a one-line summary.

### Pick the simplest orchestration

| Pattern | Use it for | Watch out for |
|---|---|---|
| Single agent with tools and skills | Most jobs. The default | Tool overlap, long prompts (§2) |
| Writer, reviewer, tester | Separating production from validation | Give the reviewer the diff and keep the writer's reasoning out |
| Audit, execute, validate | Scope unknown up front | The human decision between audit and execute is the key gate |
| Sequential pipeline | Clear stage dependencies | An early failure propagates. Validate output between stages |
| Concurrent | Independent analyses of one input | Conflicting results need an arbiter. Cost spikes |
| Manager (agents as tools) | One agent owns the conversation and the user | Manager prompt grows with each specialist |
| Handoff (decentralized) | The right specialist emerges during the work | Handoff loops, unpredictable paths |

Rules for any multi-agent design:

- Within one batch of parallel work, no two agents edit the same file ("one file, one agent"). String-matching edits fail silently when a second agent edits the same file.
- Declare the maximum fan-out and the recursion depth at the dispatch site, and exclude the spawning tool in agents that must not delegate further.
- Do not let the orchestrator trust a child's "done". Verify with a deterministic check: run the tests, read `git diff`.
- Specialize by context. Two agents earn their cost when each carries a different context (type definitions and module boundaries versus output conventions and migration examples).
- Count the cost. Each added agent adds a model call, latency and a failure mode. Put explicit effort rules in the lead prompt (one agent and a few tool calls for a simple lookup, more only for a comparison or a research task).
- Where a pr-review style agent needs several checks, bundle them as skills in the agent's folder. That is composition: the agent orchestrates, each skill is small enough to test alone.

---

## 10. Governance and maintenance

**Rule: every agent carries a `metadata` block in its frontmatter.** The block records who owns the agent and when it was last reviewed, so an agent survives its author leaving. `custom-agent-review` reports a missing or invalid block as warnings.

```yaml
metadata:
  owner: platform-team
  source-repository: https://github.com/OWNER/REPO
  version: 0.1.0
  status: draft
  last-reviewed: "2026-10-30"
  risk: low
```

| Key | Value |
|---|---|
| `owner` | A team or a handle that will still exist next year, never a bare personal name |
| `source-repository` | The bare `https://` URL of the repository where the agent is maintained. No credentials, `.git` suffix, branch or file path |
| `version` | Semantic version (see Versioning below) |
| `status` | `draft`, `active` or `deprecated` |
| `last-reviewed` | A quoted ISO 8601 date, `"YYYY-MM-DD"`, today or earlier. The quotes keep YAML parsers from reading it as a date object, since the map holds strings |
| `risk` | `low` or `high` (see §11) |

Copilot on GitHub.com documents `metadata` as a map of string pairs and ignores it in IDEs. Claude Code lists no such field and ignores it without a message. Both mean the block has no effect on how the agent runs, so no instruction in the body may depend on a `metadata` value.

A `README.md` in the agent folder is optional and holds usage notes, an example session and the source document the agent was derived from. Keep instructions for the agent in the `.agent.md`, so the model reads one source.

**Versioning.** Semantic versions in `metadata.version`:

- **major**: changed trigger surface, removed step, changed tool list or output format that others parse
- **minor**: new step, new bundled skill or reference, broadened description
- **patch**: wording, typo, added troubleshooting entry

Consumers hold links or copies, so announce a major directly.

**Fix the primitive.** When an agent repeats a mistake, edit the agent file. Correcting the output and moving on guarantees the same failure next session. Diagnose by cause: agent too generic means add domain knowledge, a skill missing a case means extend the skill, no repeatable process means add a prompt, a context gap means update memory.

**Staleness cap.** Review every agent at least every 90 days, as for instruction files. A rule that names a moved file or a retired tool actively misleads. Prompts written for older models also age: re-test emphasis, step-by-step scripts and workarounds when the model changes.

**Deprecation.** Set `metadata.status: deprecated` and edit the description first, because the description controls selection: `DEPRECATED, use repo-audit instead.` Keep it for one release cycle, then delete.

**Portfolio hygiene.** Every description is read on every delegation decision. Two agents with overlapping descriptions fight for the same triggers, so merge them or add mutual negative triggers. Review the catalogue each quarter.

---

## 11. Security review

An agent file is code that runs with the tools you grant it. Review gate before merge:

- [ ] Read the whole file and every bundled script and reference. Look for instructions that exfiltrate data, escalate privilege or disable checks.
- [ ] `tools` is explicit, narrow and justified. Any shell, MCP server wildcard (`mcp__server__*`, `server/*`) or write tool is explained in the PR description. A shell also means `risk: high` and a named second reviewer.
- [ ] No secret, token, key, connection string or URL with credentials is embedded, and no IP address or hostname of a single machine or build agent. Reference secrets by environment variable name (`MCP_API_TOKEN`) and tell the agent to stop when it is missing. The hostname of a shared service the agent has to recognise or call is fine in a private repository. In a public repository, leave internal hostnames out.
- [ ] External content is data. Steps that read PR descriptions, work items, dependency READMEs or web pages must treat their text as input to analyze and never as instructions. Restrict security-sensitive agents to first-party sources.
- [ ] Every irreversible or outward-facing action sits behind a confirmation step, and the `## Critical` block lists them.
- [ ] Least privilege: the agent is written for the narrowest path, repository and system scope its steps need.
- [ ] No verbatim copyrighted third-party material (vendor docs, licensed standards). Summarize or link.
- [ ] Third-party agents: read the entire folder before copying it in, and re-read the diff before taking an update.
- [ ] Context files get the same branch protection and PR approval as production code in their repository.

**Risk class.** Reuse the binary scale from [the skill guide §9](skill-authoring-guide.md#9-security-review): `low` when the agent only reads or every mutation waits for explicit confirmation, `high` when it has a shell (`Bash`) in `tools` or can take an irreversible action without a human decision. The discriminator is whether a human decides before the irreversible thing happens. Record the class in `metadata.risk`. `high` agents, and every agent with a shell in `tools`, need a named second reviewer and a `## Critical` block that enumerates what they never do unasked. The risk class describes the agent's own blast radius.

Guardrails layer. Stack several specialized guardrails (relevance, safety, rules-based, tool safeguards) and add new ones from real failures. In a repository agent that means the tool allowlist, the `## Critical` block, the confirmation gates and the verification step together. No single one is enough.

---

## 12. Testing

Run the `custom-agent-review` skill first: it covers the static checks, so the layers below can concentrate on behavior. Four layers. Do all four for an agent that is shared widely, and layers 1 and 2 for a repository-specific one.

**Layer 1: selection.** Write the suite in the PR description. In a fresh session each:

```text
SHOULD select the agent:
- "audit this repo: <repository URL>"
- "which of these dependencies are unpinned?"

SHOULD NOT select it:
- "fix the unpinned dependencies in service-a"   -> dependency-fixer
- "what is a lockfile?"                           -> plain answer
```

**Layer 2: functional, including error paths.** Cover a missing MCP server, an invalid or empty input, a source that returns nothing, and a run that is interrupted. State the expected end state, because valid paths vary and only the outcome is checkable.

```text
Test:  Batch with one entry that has no repo link
Given: A list with three entries, one without a repository URL
When:  The agent runs
Then:  - Two repos are checked and one is reported as "missing link"
       - No check is skipped silently
       - No write call was made
```

**Layer 3: baseline comparison.** Run the same task with and without the agent and record turns, tool calls, failed tool calls, tokens and corrections needed. If the "with" column is not clearly better, the agent is a context tax: fix it or delete it.

**Layer 4: regression after every edit.** A wording change that fixes one path can degrade another, and small lead-prompt changes can change delegated behavior unpredictably. Re-run layers 1 and 2 after each change.

How to evaluate:

- Start with about 20 representative tasks drawn from real work. Large effects show up in small samples.
- Judge outcomes. A rubric scored by a model (accuracy, completeness, tool efficiency, pass or fail) beats an exact-match check against one fixed sequence of steps.
- Read transcripts. Many redundant calls point at missing limits. Many invalid-parameter errors point at unclear tool descriptions.
- Check the known failure modes of multi-agent runs: too many agents for a simple task, endless search for sources that do not exist, duplicated or gapped subtasks, continued work after the answer is sufficient, wrong tool choice.
- Never accept the agent's report as the test result. Run the checks yourself.
- Test in every harness the agent targets. The editor's tool picker does not prove which tools the running agent can use, so use the harness diagnostics view.

---

## 13. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| The agent does not appear | Folder outside the harness's agent locations (for VS Code, `chat.agentFilesLocations`), duplicate `name`, first agent file in a new Claude Code `agents` directory | Add the folder to the locations, make names unique, restart the harness |
| Appears in one harness only | Tool names, fields or file format differ between harnesses | Compare against §5, test in each harness |
| Silently ignored by Claude Code | Missing `name` or `description`, `---` not on line 1, bad YAML | `claude --debug`, quote values containing `: ` |
| A setting has no effect | Misspelled or unsupported field | Claude Code ignores unknown fields without a message. Check the field table |
| Claude Code aborts every prompt with `would be spawned with zero tools`, while Copilot works | The list uses Copilot names only (`read`, `search`, `execute`, `server/*`, `vscode/...`) | Use the portable list from §8 |
| MCP tools are missing in one harness | The server is named in one form only, or the server name differs from the configured one | List `mcp__SERVER__*` and `SERVER/*`, and check the name with `/mcp` |
| Never selected automatically | Generic description, no trigger words, or too many agents compete | Rewrite per §6, run the selection suite |
| Selected for the wrong jobs | Description too broad, or an overlapping sibling | Add negative triggers on both agents |
| Ignores a rule that is in the file | File too long, rule buried, rule vague | Cut, move the rule under `## Critical`, make it observable |
| Makes unrequested changes | Unbounded tools or no path boundary | Narrow `tools`, add a path boundary (§8) |
| Behaves differently from run to run | Probabilistic steps that should be deterministic | Move the check into a script, tighten the completion criterion |
| Loops or runs long | No exit condition, no turn or fan-out limit | Add a definition of done and a stop condition, set `maxTurns` where supported |
| Output format drifts | No output section or a single example | Specify the format and give two or three varied examples |
| Delegated agent lacks context | The delegation message did not carry it | Brief with objective, format, tools and boundaries (§9) |
| Quality drops late in a long run | Context exhaustion | Split the task, write a plan file, start a fresh thread |

---

## 14. Anti-patterns

| Anti-pattern | Symptom | Fix |
|---|---|---|
| Monolithic agent | One 300-line file for several jobs. Adding a rule breaks something else | Split by job. Move reference to `references/` and procedures to skills |
| Unbounded agent | `tools` omitted or `*`. Edits files nobody mentioned | Explicit allowlist, path boundary, confirmation gates |
| Persona-only agent | "You are an expert developer" and nothing else | Name the domain, the patterns, the anti-patterns and the output |
| Wish instructions | "Be thorough", "follow best practices" | An observable condition or a concrete prohibition |
| Emphasis inflation | Every line is CRITICAL or MANDATORY | Reserve emphasis for tested, underweighted rules and give the reason |
| Hidden policy | Tool restriction only in a comment, or only in prose | Put it in `tools`, then repeat it in the body |
| README in disguise | The body restates the README or a standards document | Link the source with a conditional pointer |
| Standards as an agent | A rule that applies to every task, packaged as an agent | Move it to `AGENTS.md` |
| Tool soup | Many overlapping tools, vague descriptions | Few targeted tools, distinct names, clear descriptions |
| Single-vocabulary tools | Works in one harness and aborts or loses its MCP tools in the other | The portable list (§8), tested in each harness |
| Solo hero | One agent handles a whole large feature in one thread | Decompose, delegate with clean context, checkpoint after each part |
| Trust fall | The agent says "done" and nobody checks | Verify with tests, `git diff`, a deterministic gate |
| Orphaned copy | A hand-edited copy in another tool folder | One source under `.agents/`, links everywhere else |
| Fossil | Workarounds for a retired model, stale paths | Review dates, consistency check, re-test on model change |
| Unowned agent | No owner or review date | `metadata.owner` (§10). An unowned agent is deleted |

---

## 15. Pre-merge checklist

Check each box with a command or by reading the file, or run the `custom-agent-review` skill, which scores the same items as blockers, warnings and advisories.

**Discovery**

- [ ] Folder, file stem and `name` are identical lowercase kebab-case. The name is unique across `.agents/`.
- [ ] `description` states what, when with literal triggers, and when not with the sibling to use.
- [ ] `description`, `argument-hint` and `metadata` values contain no angle bracket characters.
- [ ] The `README.md` catalog and tree are updated, and the folder is in the harness's agent locations.

**Boundaries**

- [ ] `tools` is explicit, narrow and never `*`. It is one comma-separated line with Claude-style built-in names and every MCP server in both forms (§8). Every shell and server wildcard is justified.
- [ ] `## Critical` is the first section after the role and lists the gates and prohibitions. Required when `tools` includes a write tool, a shell or a write MCP tool.
- [ ] Every irreversible or outward-facing action has a confirmation step.
- [ ] A writing agent states its path boundary.
- [ ] An agent that acts on production or safety-critical systems sets no pre-approving `permissionMode` and never acts without asking.

**Content**

- [ ] Each step has an expected result or gate, and the file defines done.
- [ ] Prerequisites are checked first and stop with a fix.
- [ ] Every pointer carries the condition for opening the target.
- [ ] Nothing restates `README.md`, a skill or the environment. Nothing the model already does by default.
- [ ] Body is at most 150 lines, or the excess has a stated reason. It is under 30,000 characters.

**Governance and quality**

- [ ] `metadata` has all six keys with valid values: `owner` is a team or lasting handle, `source-repository` is a bare https URL, `version` is semver, `status` is draft, active or deprecated, `last-reviewed` is a quoted ISO date, `risk` is low or high.
- [ ] Selection suite (3 should, 3 should not) and at least one error-path functional test are in the PR description.
- [ ] Tested in every harness the agent targets.
- [ ] No secret, credential-bearing URL, machine or IP address, or third-party copyrighted text.

If you fail a boundary item, start there: safety gaps have the highest blast radius and the cheapest fix.

---

## Agent skeleton

Copy [custom-agent-template.md](templates/custom-agent-template.md) to `.agents/<agent-name>/<agent-name>.agent.md`. Its inline markers say which sections are required, recommended or optional, and the HOW TO USE comment lists the steps after copying. Check the result with the [`custom-agent-review`](../.agents/skills/custom-agent-review/SKILL.md) skill.