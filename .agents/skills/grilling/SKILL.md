---
name: grilling
description: Interviews the user relentlessly, a round of numbered questions at a time with a recommended answer each, until every branch of a plan's design tree is resolved. Use when the user says "stress-test this plan", "poke holes in this design", "interview me about this", "challenge my thinking", or when another skill needs an interview. Do not use for a single clarifying question, or for facts the agent can look up itself.
metadata:
  version: 1.0.0
  status: active
  last-reviewed: 2026-10-26
  risk: low
  adapted-from: https://github.com/mattpocock/skills (skills/productivity/grilling, MIT, Copyright (c) 2026 Matt Pocock)
---

# Grilling

Interview the user relentlessly until you reach a shared understanding of a plan, decision or idea.

## Critical

- Do not act on the outcome until the user confirms you have reached a shared understanding.

## Scope

- Use for: stress-testing a plan, decision or idea by interview; the interview step inside another skill.
- Not for: a single clarifying question; looking up facts (do that yourself, see Step 4).
- Prerequisites: none.

## Instructions

1. **MAP**: Map the subject as a **design tree**: every decision branches into the decisions that hang off it. Expected: the root decisions named.
2. **ASK**: Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question, give your recommended answer, and word it so "yes" accepts that answer. Then wait for the user's answers. Expected: one message in the format below, then silence.
3. **RECOMPUTE**: Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round. Expected: the next frontier, asked as in Step 2.
4. **LOOK UP FACTS**: Finding _facts_ is your job. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent to find it, and put to the user only what the environment cannot answer. A running exploration is an unsettled prerequisite: only the questions downstream of it wait for the sub-agent to report, so ask the rest of the frontier now. The _decisions_ are the user's: put each to them and wait. Expected: no question asks the user for something you could look up.
5. **CLOSE**: The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Expected: the user is asked to confirm the shared understanding.

## Round format

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

## Examples

- "Grill this migration plan" → Step 1 (tree), Step 2 (first frontier as numbered questions). Result: one round of questions, each with a recommendation.
- A caller skill says "resolve this ticket by interview" → Steps 1-5 run inside the caller. Result: settled decisions handed back to it.

## Troubleshooting

- **The agent asks the user for something it could have read from the repo** - cause: Step 4 skipped. Fix: dispatch the sub-agent and ask only the decisions.
