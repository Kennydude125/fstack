# Codex adapter

This layer maps pstack mechanisms to actual host capabilities. It is not a grant of permissions, a sandbox or an additional orchestrator service.

## Load and resolve

Find the canonical fstack package from the skill path supplied by the parent or install shim. Resolve peer skills through relative file links, not generic names or global searches. Helpers run from that package root. Carry private research paths as explicit task inputs; do not move them into the public package.

## Task and role mapping

| Original mechanism | Codex behavior |
| --- | --- |
| Task subagent | Use the actual spawn capability with the role's prompt, original goal, scope, source cutoff, exact input identity, output location and finish predicate |
| poteto-agent | Read agents/fstack-agent.md and the canonical main SKILL.md before ordinary delegated work |
| Workflow-specific roles | Read the named workflow's prompt and applicable leaves; do not force the ordinary wrapper onto a specialist whose contract differs |
| Background fan-out | Dispatch independent workers within actual limits, then gather terminal results; keep dependent work sequential |
| AskQuestion | Use the host's structured question tool if available for real missing preferences, not discoverable facts or already-granted permission |
| Todolist | Use the host task-list facility or a visible phase checklist; preserve matched steps and skip reasons |
| Cloud/local worktree | Use isolated authorized output directories or actual supported worktrees; never claim a cloud environment was used if it was not |
| Cursor transcripts | Use only active task transcripts exposed by this host or an explicit user-supplied record; otherwise disclose an artifact-only audit |
| /loop and automations | Run a bounded in-session loop or explicitly requested host automation; no hidden persistent scheduler |
| .mdc model rule | Use fstack's private role configuration and detected available models; do not alter global settings implicitly |

Where native named agent registration is supported, the host may register narrow roles using its documented local format. Otherwise pass the role prompt directly to the actual spawn API. A role name in prose does not mean an agent ran.

## Models and costs

Read the actual available model set. Real identifiers must be confirmed. `auto` and `inherit-parent` omit model overrides. Use configured role choices with the original large/xhigh budget intent where supported; adjust effort to task difficulty without claiming unavailable settings. Fast modes require actual urgency. Every result records the actual model or honest unavailable identity.

Arena and eval prefer a judge from a different available model family than the coordinator. If unavailable, record the missing gate, inspect the outputs and state what review ran. Same-model workers can supply independent contexts, not cross-family confirmation. Never silently swap rejected identifiers or invent model diversity.

## Permissions, isolation and stops

Subagents inherit host permissions. A read-only role instruction is behavioral guidance, not a separately enforced sandbox. Source access must still be in scope. Give each worker its own outputs and a bounded retry policy; the parent owns canonical journal writes. No worker may trade, send external messages or publish private material from this research brief.

On user stop, cancel child work and only processes this run created, preserve atomic artifacts and write an explicit checkpoint. New tasks use fresh workers; resume a worker only for live state that would be costly or unsafe to move. Inspect outputs and actual checks; missing capabilities, dropout or unavailable sources remain gaps.

## Portability

Use a detected Python 3.11+ interpreter for fstack helpers. Windows also needs the declared tzdata dependency for IANA timezones. Do not assume /bin/sh, Bun, mise, gh, Cursor folders, Java/TLC, cloud tools or any provider subscription exists. Optional original developer resources explicitly identify their unbundled runtime. Do not install missing software or authenticate a new destination merely because an upstream instruction names it; apply the user's scope and host rules.
