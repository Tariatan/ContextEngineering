---
name: teach
description: Teaches the user a new skill or concept over multiple sessions, using the current directory as a stateful teaching workspace (MISSION.md, lessons, reference sheets, learning records). Use when the user types "/teach", or says "teach me X", "I want to learn X over several sessions", "build me a course on X". Do not use for a one-off explanation or for explaining code in the current repository.
metadata:
  version: 1.0.0
  status: active
  last-reviewed: 2026-10-26
  risk: low
  adapted-from: https://github.com/mattpocock/skills (skills/productivity/teach, MIT, Copyright (c) 2026 Matt Pocock)
---

# Teach

The user has asked you to teach them something. This is a stateful request: they intend to learn the topic over multiple sessions.

## Critical

- Unless the user typed `/teach`, confirm the current directory is the intended teaching workspace before writing anything into it.
- Confirm with the user before changing `MISSION.md`.

## Scope

- Use for: a multi-session learning request, where lessons, reference sheets and learning records accumulate in the current directory.
- Not for: a one-off explanation; explaining code in the current repository.
- Prerequisites: a writable current directory and a topic. If no topic was given, ask "What would you like to learn about?".

## Instructions

1. **ORIENT**: Read the workspace files listed below. Expected: the topic known, and which workspace files exist.
2. **GROUND**: Make sure `MISSION.md` is populated (see The Mission), then pick the next thing to teach (see Zone Of Proximal Development). Expected: a one-line lesson target tied to the mission.
3. **DESIGN**: Read `references/pedagogy.md` and gather knowledge from the sources in `RESOURCES.md`. Expected: a lesson plan holding only the knowledge its skill needs.
4. **WRITE**: Author the lesson per Lessons and Assets. Expected: `./lessons/NNNN-<dash-case-name>.html`, opened for the user by a CLI command.
5. **RECORD**: Read `references/reference-documents.md`, then add the reference documents, learning records and notes the lesson earned. Expected: each lesson has its reference sheet, and every qualifying learning record is written.

## Teaching Workspace

Treat the current directory as a teaching workspace. Workspace paths (`./lessons/` and the rest) resolve from the directory `/teach` was run in; only the `references/*-format.md` files resolve from this skill's folder. The state of their learning is captured in this directory in several files:

- `MISSION.md`: A document capturing the _reason_ the user is interested in the topic. This should be used to ground all teaching. Before writing it, read `references/mission-format.md`.
- `./reference/*.html`: A directory of reference materials. These are the compressed learnings from the lessons - cheat sheets, reference algorithms, syntax, yoga poses, glossaries. They are the raw units of learning. They should be beautiful documents which print out well, and are designed for quick reference.
- `RESOURCES.md`: A list of resources which can be explored to ground your teaching in contextual knowledge, or to acquire knowledge and wisdom. Before writing it, read `references/resources-format.md`.
- `./learning-records/*.md`: A directory of learning records, which capture what the user has learned. These are loosely equivalent to architectural decision records in software development - they capture non-obvious lessons and key insights that may need to be revised later, or drive future sessions. These should be used to calculate the zone of proximal development. They are titled `0001-<dash-case-name>.md`, where the number increments each time. Before writing one, read `references/learning-record-format.md`.
- `./lessons/*.html`: A directory of lessons. A **lesson** is a single, self-contained HTML output that teaches one tightly-scoped thing tied to the mission. This is the primary unit of teaching in this workspace.
- `./assets/*`: Reusable **components** shared across lessons. See Assets.
- `NOTES.md`: A scratchpad for you to jot down user preferences, or working notes.

## Lessons

A lesson is the main thing you produce: the unit in which knowledge and skills reach the user. Each lesson is one self-contained HTML file, saved to `./lessons/` and titled `0001-<dash-case-name>.html` where the number increments each time.

A lesson should be **beautiful**, with clean, readable typography and layout, since the user will return to these later to review. Think Tufte.

The lesson should be short, and completable very quickly. Learners' working memory is very small, and we need to stay within it. But each lesson should give the user a single tangible win that they can build on. It should be directly tied to the mission, and should be in the user's zone of proximal development.

If possible, open the lesson file for the user by running a CLI command.

Each lesson should link via HTML anchors to other lessons and reference documents.

Each lesson should recommend a primary source for the user to read or watch. This should be the most high-quality, high-trust resource you found on the topic.

Each lesson should contain a reminder to ask followup questions to the agent. The agent is their teacher, and can assist with anything that's unclear.

## Assets

Lessons are built from reusable **components**, stored in `./assets/`: stylesheets, quiz widgets, simulators, diagram helpers, and anything else a second lesson could reuse.

Reuse is the default. Before authoring a lesson, read `./assets/` and build from the components already there. When a lesson needs something new and reusable, write it as a component in `./assets/` and link to it; never inline code a future lesson would duplicate.

A shared stylesheet is the first component every workspace earns: every lesson links it, so the lessons look like one consistent course. As the workspace grows, so should the component library.

## The Mission

Every lesson should be tied into the mission - the reason that the user is interested in learning about the topic.

If the user is unclear about the mission, or the `MISSION.md` is not populated, your first job should be to question the user on why they want to learn this.

Failing to understand the mission will mean knowledge acquisition is not grounded in real-world goals. Lessons will feel too abstract. You will have no way of judging what the user should do next.

Missions may change as the user develops more skills and knowledge. This is normal - make sure to update the `MISSION.md` and add a learning record to capture the change. Confirm with the user before changing the mission.

## Zone Of Proximal Development

Each lesson, the user should always feel as if they are being challenged 'just enough'.

The user may specify an exact thing they want to learn. If they don't, figure out their zone of proximal development by:

- Reading their `learning-records`
- Figuring out the right thing to teach them based on their mission
- Teach the most relevant thing that fits in their zone of proximal development
