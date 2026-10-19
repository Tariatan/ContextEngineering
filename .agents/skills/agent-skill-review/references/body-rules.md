# Body rules

Reference for the `agent-skill-review` skill. Open before Step 3 of `SKILL.md`.

---

## Check tables — score every ID

| ID | Severity | Check |
|---|---|---|
| B11 | Blocker | An H1 title, `## Scope`, and `## Instructions` are all present |
| W9 | Warning | `## Critical` is present if the skill can delete, push, deploy or spend money |
| W10 | Warning | Every step states its expected output or a validation gate |
| W11 | Warning | Every instruction is literal and runnable — flag vague verbs such as "validate", "check", "handle" with no defined criterion |
| W12 | Warning | Every file in `scripts/`, `references/` and `assets/` is referenced from `SKILL.md` with an explicit condition for opening it |
| W13 | Warning | Body is 80 lines or fewer |
| W14 | Warning | Deterministic checks are delegated to a bundled script rather than described in prose |
| W15 | Warning | A skill that documents a shared library carries the roadmap §9.1 content contract |
| A1 | Advisory | `## Examples` and `## Troubleshooting` are present |
| A2 | Advisory | Critical rules sit near the top, not buried below the instructions |
| A3 | Advisory | No `DELETE-IF-UNUSED` marker or unreplaced UPPERCASE placeholder is left over |
| A4 | Advisory | A skill is the right primitive at all, rather than one of the other six the roadmap defines — instruction file, agent configuration, prompt, memory, orchestration spec, hook |

B1–B10, B12, W1–W8 and W16 are frontmatter checks. They live in `frontmatter-rules.md`. A4 is scored
only when `scope-test.md` applies; otherwise mark it `n/a`.

---

## Section reference

Judge B11, W9 and A1 against this table. Order matters: critical content goes near the top,
because agents follow front-loaded instructions more reliably than buried ones.

| Section | Status | Required when |
|---|---|---|
| `# Title` | REQUIRED | always |
| `## Critical` | RECOMMENDED | the skill can delete, push, deploy, or spend money |
| `## Scope` | REQUIRED | always — carries `Use for:`, `Not for:` and `Prerequisites:` as three bullets |
| `## Instructions` | REQUIRED | always |
| `## Definition of done` | OPTIONAL | "finished" is not obvious from the last step |
| `## Usage` | REQUIRED for a shared-library skill | see W15 below; OPTIONAL for every other skill type |
| `## Examples` | RECOMMENDED | always, unless the skill is a single command |
| `## Troubleshooting` | RECOMMENDED | you have observed at least one real failure |
| `## References` | OPTIONAL | the skill bundles `references/`, `scripts/` or `assets/` |

Only the three REQUIRED rows are blockers (B11). A `## Scope` bullet that is genuinely not
applicable is written as `none`, not dropped — a missing bullet is a W10 finding, not a B11.
RECOMMENDED rows missing without cause are advisories (A1). OPTIONAL rows are never findings on
their own — but a skill that bundles files and has no `## References` section fails W12.

## Instruction quality — for W10 and W11

An instruction the agent cannot act on deterministically is not an instruction. Steps are one
numbered line each, so the expected output sits on the same line as the action.

```markdown
<!-- PASSES -->
1. **CHECK CONSUMERS**: Run `pwsh ./scripts/check-consumers.ps1 -Package Library.Messaging.Interface`.
   Expected: a table of consuming repos and a total count. Above 10, stop and ask the user to confirm.
```

```markdown
<!-- FAILS W10 (no expected output) and W11 (vague verb, no criterion) -->
1. **IMPACT**: Check the impact before proceeding.
```

Flag as W11 any of `validate`, `check`, `verify`, `handle`, `ensure`, `review`, `make sure`
that is not followed by an explicit criterion, command, or checklist. "Validate properly" is a
wish, not a step.

Flag as W10 any step that neither states an expected output nor defines a validation gate.
A step whose success cannot be observed cannot be retried correctly when it fails.

## Bundled files — for W12 and W14

Every file in `scripts/`, `references/` or `assets/` must be referenced from `SKILL.md` with an
explicit *condition for opening it*. The agent discovers all files in the skill folder when the
skill loads; an unreferenced file is dead weight it may pull in anyway.

```markdown
<!-- PASSES W12 — states when to open it -->
Before writing any query, read `references/api-patterns.md` for rate limiting and pagination.
```

```markdown
<!-- FAILS W12 — no condition -->
See also references/api-patterns.md.
```

W14 is the inverse test. If a check in the skill has one objectively correct answer — schema
conformance, a character count, version ordering, file existence — it belongs in a bundled
script, not in prose. Code is deterministic; language interpretation is not. Raise W14 when
prose is doing a job a script should do.

When to expect each directory:

| Directory | Justified when | Not justified when |
|---|---|---|
| `scripts/` | a check must be deterministic | the step is judgement-based |
| `references/` | the body would exceed 80 lines, or detail is needed in fewer than 1 run in 10 | the content is needed every run — it should be inline |
| `assets/` | the skill emits a file that must follow a fixed layout | the output is free-form |

## Size — for W13

Keep the body at **80 lines or fewer**, matching the template. Past that, the skill is either two
skills or is missing a `references/` directory. Count the lines, including blank ones, and do not
estimate. In PowerShell, `(Get-Content .\SKILL.md).Count` — note that
`Measure-Object -Line` silently skips blank lines and will under-report.

Line count is not the only signal. Also raise W13 when:

- The same rule is restated in three or more places.
- Detail needed by one run in ten is inline rather than in `references/`.

## Shared-library skills — for W15

The roadmap (§9.1) makes a `SKILL.md` mandatory for **every shared library consumed by more than
one team**, and fixes what it must contain. This is the most common skill type in the chapter and
it has a tighter contract than a general skill.

Score W15 only when the reviewed skill documents a shared library. Otherwise mark it `n/a`.

| Required content | W15 fails when |
|---|---|
| Purpose and scope | absent, or describes the library's internals rather than a consumer's use of it |
| Correct usage patterns, with a code example of the golden path | no runnable example |
| Common misuse patterns | absent — this is the highest-value half of the file |
| Message contracts, where the library emits or consumes messages | the library has a `.Messages` companion repository and the skill never references it |
| Threading and lifecycle constraints | absent |

In the template, the first row lands in `## Scope` and the other four in `## Usage`.

## Leftover template artefacts — for A3

Raise A3 on any of:

- A `DELETE-IF-UNUSED` marker.
- An unreplaced `UPPERCASE-PLACEHOLDER`, e.g. `CONCRETE-TASK-1`, `TEAM-NAME`, `YYYY-MM-DD`.
- The literal heading `# Human-Readable Skill Name`.
- Guidance HTML comments such as `RECOMMENDED — omit only if…` left in place.
- A `README.md` inside the skill folder — this one is a blocker, B10, not an advisory.
