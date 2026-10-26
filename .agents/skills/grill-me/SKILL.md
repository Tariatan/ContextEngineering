---
name: grill-me
description: Starts a relentless interview to sharpen a plan or design by delegating to the grilling skill. Use when the user types "/grill-me" or says "grill me". Do not use for other stress-test requests or for an interview inside another skill (use grilling directly).
metadata:
  version: 1.0.0
  status: active
  last-reviewed: 2026-10-26
  risk: low
  adapted-from: https://github.com/mattpocock/skills (skills/productivity/grill-me, MIT, Copyright (c) 2026 Matt Pocock)
---

# Grill Me

Named entry point for a grilling session. The interview itself lives in the `grilling` skill.

## Scope

- Use for: the user asking by name to be grilled on a plan or design.
- Not for: an interview inside another skill (use grilling directly).
- Prerequisites: the `grilling` skill installed in the same skills folder; verify it appears in the skill list. If absent, stop and tell the user to install it.

## Instructions

1. **DELEGATE**: Call the Skill tool with "grilling". Expected: the first round of numbered questions with recommended answers.

## Troubleshooting

- **Nothing happens, or the agent improvises its own interview** - cause: `grilling` is missing or was not loaded. Fix: install `grilling` next to this skill and call the Skill tool with "grilling" again.
