<!--
HOW TO USE:
- Copy to [root-of-project]/AGENTS.md, or to [sub-directory]/AGENTS.md for a directory-level instruction file.
- Replace the [UNIT/REPOSITORY/DOMAIN NAME] placeholder.
- Delete every section or line marked OPTIONAL that you don't need; follow the rule stated next to anything marked REQUIRED or RECOMMENDED instead of deleting it outright.
- Delete every HTML comment, including this one.
- Keep the finished file under 40 to 50 lines (blank lines count).
- Keep this file scoped to one clear domain or file pattern.
- Keep the sections in the order below.
- For more info see ../agents-md-authoring-guide.md.
-->

# [UNIT/REPOSITORY/DOMAIN NAME] Development Instructions

<!-- The next line is REQUIRED for directory-level files that should extend their parent (see §4.3); delete the line entirely for root-level files or ones that intentionally replace the parent. -->
> Before making any change here, read [`AGENTS.md`](../AGENTS.md) and follow its rules together with the ones below; this file does not replace it.

## Core Principles & Safety Boundaries <!-- RECOMMENDED: this is where prohibitions belong, what the agent MUST NOT do; omit only if this repo has none to state. -->

## Architecture & Design Patterns <!-- REQUIRED if you need to specify the links below for root-level files; OPTIONAL for directory-level files that already extend the root via the blockquote above, or if there's nothing to state. -->
- Architectural decisions and development practices: see [architecture docs](docs/architecture/index.md).
- Coding guidelines and design decision records: see [coding guidelines](docs/coding-guidelines.md).

## Coding & Error Handling Standards <!-- OPTIONAL: mandatory exception classes, logging wrappers, serialization rules; omit if this repo has none to state. -->

## Development & Workflow Conventions <!-- OPTIONAL: workspace CLI shortcuts, git commit styles, PR title formatting; omit if none of these are worth stating. -->

## Testing & Quality Gates <!-- OPTIONAL: coverage thresholds, fixture base classes, the commands to run before submitting a pull request; omit if none apply. -->

## Context & Memory References <!-- REQUIRED if you need to specify the links below for root-level files; OPTIONAL for directory-level files that already extend the root via the blockquote above, or if there's nothing to state. -->
- Active decisions & trade-off history: see [.agents/memory.md](.agents/memory.md).
- Shared skills: see [.agents/skills/](.agents/skills/).