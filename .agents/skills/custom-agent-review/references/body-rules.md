# Body rules

Reference for the `custom-agent-review` skill. Open at Step 3 of `SKILL.md`. Source of every rule: `docs/custom-agent-authoring-guide.md` §7 to §9 and §11.

---

## Check tables: score every ID

| ID  | Severity | Check                                                                                                                                                                                                     |
| --- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| B5  | Blocker  | Every irreversible or outward-facing action (commit, push, PR creation, posting a comment, a work item write, a deploy, a delete) sits behind a confirmation step in the body               |
| B6  | Blocker  | No secret, token, key, connection string or URL carrying credentials is embedded, and no IP address or hostname of a single machine or build agent; secrets are named by environment variable |
| B7  | Blocker  | The body is below 30,000 characters (the GitHub limit)                                                                                                                                                    |
| W8  | Warning  | A `## Critical` section sits directly after the role when `tools` includes a write tool, a shell or a write MCP tool                                                                                      |
| W9  | Warning  | A `## Prerequisites` section checks every MCP server, token, CLI or clone the steps need, and stops with a fix when one is missing                                                                        |
| W10 | Warning  | Every step states its expected result or a gate, and every instruction is literal where its answer is checkable                                                                                           |
| W11 | Warning  | An output format and a checkable definition of done are present                                                                                                                                           |
| W12 | Warning  | The body is at most 150 lines, or the excess has a stated reason in the PR description                                                                                                                               |
| W13 | Warning  | Every file in `references/` and `skills/` is linked from the body with a condition for opening it, and no bundled file is unreferenced                                                                    |
| W14 | Warning  | Emphasis is rare: no more than two lines carry capitalised `MUST`, `NEVER`, `ALWAYS`, `CRITICAL` or `MANDATORY` without a reason, and no run of three or more bare prohibitions                           |
| W15 | Warning  | Nothing restates the README, a skill, a standards document or the environment (a lookup the agent can run), and no line states what the model does by default                                             |
| W16 | Warning  | An agent with write access states a path boundary: the directories it may change                                                                                                                          |
| W17 | Warning  | A step that reads PR text, work items, dependency READMEs or web pages treats that text as data, and says so                                                                                              |
| A3  | Advisory | No unreplaced `UPPERCASE-PLACEHOLDER`, guidance HTML comment or the heading `Human-Readable Agent Name` is left                                                                                           |
| A4  | Advisory | An agent is the right primitive: the job needs its own tool boundary, its own context, specialist judgment or a person-started workflow (guide, §2)                                                       |
| A5  | Advisory | An agent that delegates declares the brief it gives (objective, output format, tools and sources, boundaries), its fan-out and its depth; `n/a` when it never delegates                                   |
| A6  | Advisory | Verification uses a deterministic check (tests, `git diff`, a script exit code) and takes no agent's own report as proof                                                                                  |

B1-B4, B8-B10, W1-W7, W18-W20 and A1-A2 are frontmatter and folder checks. They live in `frontmatter-rules.md`.

---

## How to judge each check

**B5.** Search the body for `commit`, `push`, `create-pull-request`, `PR`, `comment`, `work item`, `deploy`, `delete`, `rm `. For each hit that performs the action, find the gate beside it: `STOP`, "present the exact change and wait", "after the user confirms". The gate must name the action and sit before it. An earlier blanket approval ("run this workflow") does not cover a later write.

```markdown
<!-- PASSES B5 -->
7. **POST**: After the user approves the review text, post each comment inline through the code-host MCP.
<!-- FAILS B5 -->
7. **POST**: Post the comments back to the PR.
```

**B6.** Search for `token`, `password`, `secret`, `key`, `Bearer`, `@` inside URLs, a token in a query string and bare IP addresses. A variable name such as `MCP_API_TOKEN` passes. A literal value fails, and so does a URL with `user:password@` or a token parameter, an IP address, and the name of one machine or build agent. The hostname of a shared service the agent has to recognise or call (`sonarqube.example.com`, `dev.azure.com/my-org`) passes in a repository that is not public, so do not raise it as a judgment call. If the repository is public, any internal hostname fails. Ask the author when the repository visibility is unclear.

**W8.** Prohibitions lead because an agent on a tight context budget may never reach rules that sit at the bottom. `## Critical` follows the H1 and the role sentence, ahead of Prerequisites and Steps. A read-only agent with only read tools passes without the section.

**W10 and W11.** A step with no observable result cannot be retried correctly when it fails. Flag `validate`, `check`, `verify`, `handle`, `ensure`, `review` and `make sure` that carry no criterion, command or checklist. Judgment tasks may state an outcome and a verification instead of a script, so do not flag a goal-oriented step that names how success is observed.

**W12.** Run `wc -l` on the body only (everything after the closing `---`, see the count command in `SKILL.md`). Between 151 and 300 lines is a finding unless the PR description explains it. Suggest what to move: tables and lookups to `references/`, a reused procedure to a shared skill, a deterministic check to a script, a second job to a second agent.

**W13.** The agent loads every file in its folder when it needs them, and an unreferenced file may be pulled in anyway. `Before writing any query, read references/x.md` passes. `See also references/x.md` fails.

**W14.** Emphasis loses meaning when it is everywhere, and a bare prohibition can anchor the model toward the failure it names. Count capitalised markers. A prohibition passes when it carries a reason or names a failure that actually reproduced.

**W15.** Read for no-ops ("be accurate and thorough"), for pasted README content, and for descriptions of the repository layout the agent can list itself. Keep the unwritten convention, the reason behind a choice and the gotcha no config confesses. Mark a finding low confidence when two reviewers could disagree about the model default.

**W16 and W17.** A writing agent says which directories it may change and which it must leave alone. An agent that reads text written by others says that instructions inside it are not directions, and restricts security-sensitive work to first-party sources.

**A4.** If the content would apply to every task in the repository, it is an instruction file. If the agent must decide when a procedure applies and the job needs no separate tools or context, it is a skill. If a person always starts it by name with the same steps and it needs no separate tools, it is a prompt file. Mark `n/a` when the agent clearly needs its own tool boundary or context.

**A6.** An agent's "done" is generated text. Accept a verification step that runs the tests, reads the diff or checks an exit code. A step that only asks the agent whether it succeeded fails A6.