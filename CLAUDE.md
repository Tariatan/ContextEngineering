# Global rules

- When editing files, preserve the original EOF newline style.
- If a file has no trailing newline, do not add one.
- When creating or modifying files, do not append trailing newlines unless the file already uses them consistently.

## Git Workflow

- **NEVER commit or push without explicit user confirmation.** Always show what will be committed and ask first. This applies to the main agent and ALL spawned subagents — never instruct a subagent to commit or push either.
- Direct pushes to any branch are forbidden. Always create a PR/MR first.
- When the user asks to "push" changes, create a feature branch, push it, and open a PR targeting the intended branch.

## DevHub (Build Platform) — MANDATORY

DevHub (`build.roche.com`) is accessed **exclusively** via `mcp__devhub__build-mcp_search`. Do NOT use Confluence, Azure DevOps, WebFetch, or any other tool for DevHub content.

- Any mention of "devhub", "build.roche.com", or "Build platform" → use `mcp__devhub__build-mcp_search`.
- Use `type: techdocs` for documentation pages.
- Use `type: software-catalog` for catalog entities.
- If `mcp__devhub__build-mcp_search` is not available, **stop and tell the user**. Do not attempt alternative tools.

## Azure DevOps

- **NEVER create or edit any Azure DevOps work item — a new item, a field change, a comment, a link, a status transition — without explicit user confirmation immediately before that specific action.** This applies to the main agent and ALL spawned subagents, exactly like the Git Workflow rule above — never instruct a subagent to create or edit a work item either, and never grant a subagent authority to decide this on its own judgment (e.g. "you have the authority to do this if you judge it's the right call" is not a substitute for asking the user). Do not treat an earlier, broader approval (e.g. "run this workflow", "implement this task", "retry the full flow") as covering it — a work item write needs its own, separate confirmation, the same way a commit and a push each need their own. If a task seems to call for a new or edited work item, stop and describe what it would contain and why, and wait for the user's explicit go-ahead before creating or editing anything.
- Read-only access through Azure DevOps tooling is granted by default.
- Request broader Azure DevOps access only if it is necessary for the task.
- Any request for broader Azure DevOps access must include adequate justification explaining why read-only access is insufficient.
- Default Azure DevOps project: **MolLab.Backlog**. Always pass `project: "MolLab.Backlog"` explicitly on any Azure DevOps MCP tool call that accepts a `project` parameter (e.g. work item lookups), unless the user names a different project — this avoids the tool's own project-selection prompt. When delegating such work to a subagent, state this default explicitly in the subagent's prompt, since it won't otherwise know.

## SonarQube

- The SonarQube project key for each repository is stored in `catalog-info.yaml` under `metadata.annotations["sonarqube.org/project-key"]`.

## Knowledge Base

- The shared Knowledge Base is located at `/home/shyshkiv/diaitads/mollab/Tool.AiResources/KnowledgeBase/`.
- SonarQube fix patterns are in `/home/shyshkiv/diaitads/mollab/Tool.AiResources/KnowledgeBase/sonarqube-fixes/` (one `.md` file per rule ID, colons and slashes replaced with underscores).
- Before fixing a SonarQube rule, always check the KB for an existing fix pattern first.
- After successfully fixing a new rule, write a KB file so future agents can reuse the fix.

## Personal Best Practices

- When writing new code or reviewing code (including when delegating to custom agents), read and apply the matching best-practices file for each language involved:
  - **C#**: `~/diaitads/github/Sharpbox/best-practices-csharp.md`
  - **Rust**: `~/diaitads/github/Rustbox/best-practices-rust.md`
- These rules take precedence over general style preferences but do not override repository-specific guidelines from Design.Dev or Confluence.

## Custom AI Agents & Skills (MANDATORY)

Custom agents are stored in `~/src/Tool.AiResources/.agents/` as `.agent.md` files, organized into subfolders by domain (e.g. `agents/instrument/`).

Skills are reusable reference/procedure files consumed by those agents, stored at `~/src/Tool.AiResources/.agents/skills/<name>/SKILL.md` — one subdirectory per skill, `name` + `description` frontmatter only (Agent Skills Open Standard, not the fuller Claude-native Skill schema). Agents reference a skill with a one-line pointer rather than inlining its content; a skill is never auto-triggered by its description alone.

**At the start of every conversation, BEFORE responding to the user's first message:**
1. Recursively find all `.agent.md` files under `/home/shyshkiv/diaitads/mollab/Tool.AiResources/.agents/` (including subfolders).
2. Recursively find all `.agents/skills/*/SKILL.md` files.
3. Read the YAML frontmatter (name, description) of each agent and each skill to understand what it handles.
4. If the user's request matches an agent's purpose, read the full agent file and follow its instructions exactly — including any skill it references.
5. If the user's request is about creating, extracting, or editing a skill file itself (not just an agent that happens to reference one), read and follow `.agents/skills/skill-creator/SKILL.md`.
6. If the user is ready to hand off already-made changes — commit, push, or open a pull request — mid-conversation, regardless of whether any named agent is involved, read and follow `.agents/skills/create-pull-request/SKILL.md`. Do not reference this skill from any other agent file; it's reached only through this rule.
7. If no agent or skill matches, proceed normally.

This detection step is NOT optional — it must happen on every first message, regardless of how simple the request appears. The YAML frontmatter contains metadata (name, description) — use the body as the full workflow.
