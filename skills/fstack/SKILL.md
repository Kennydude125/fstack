---
name: fstack
description: "Coordinate investing and finance research through pstack-style playbooks, specialist agents, evidence review, reproducible calculations, and recorded decisions. Use for fstack, company or ETF research, valuation, portfolio risk, strategy research, and research reviews."
---

Read the [Codex adapter](../../adapters/codex.md) once per session and the [finance contract](../../references/finance-contract.md) before acting. Resolve peer skills by their file paths. Run helper commands from the canonical package root, with the detected Python interpreter.

# Fstack mode

You own the user's research question, its playbook, every delegation and the final answer. Ordinary delegates read this file and applicable principle leaves; specialized workflow roles read their own prompts. Give each delegate this file's absolute canonical path. Do not delegate ownership of the same whole task to a nested coordinator.

## Start and route

1. State the user's goal and the decision the research should inform. Establish instrument identity, venue, currency, information cutoff, horizon and the requested artifact. Infer only routine working defaults and label them.
2. Read the principle index below. Read each principle's leaf before applying it. Cite only principles actually read, and explain the choice they changed when it helps the user.
3. Select the matched playbook, read it in full, and present a task list whose first items are its steps in order. A skipped step remains visible with a specific reason. Add task-specific steps after the playbook sequence.
4. Use the configured role and available capabilities. Keep candidates and worker results isolated. One owner writes each artifact; the coordinator owns the canonical journal. Batch independent work within host concurrency limits and keep dependent work sequential.
5. Inspect real evidence and actual artifacts before synthesis. Worker self-reports are not verification. Distinguish artifact integrity, thesis support and performance evidence in the final answer.

## Triggers

- Nontrivial investigation or placement question: [how](../fstack-how/SKILL.md). Reasons or competing explanations also use [why](../fstack-why/SKILL.md).
- A new model or research method with consequential structural choices: [architect](../fstack-architect/SKILL.md), which invokes [arena](../fstack-arena/SKILL.md).
- Independent coverage, partitions or declared races: [swarm](../fstack-swarm/SKILL.md). Alternative whole designs: arena. Keep those contracts distinct.
- A contested thesis or review-ready financial artifact: [interrogate](../fstack-interrogate/SKILL.md).
- Any reported performance number: [benchmark checklist](../fstack-benchmark-checklist/SKILL.md).
- Long, autonomous or multi-phase work: [decision trail](../fstack-show-me-your-work/SKILL.md).
- No fitting playbook, or one ambitious cross-cutting run: [figure it out](../fstack-figure-it-out/SKILL.md). A genuinely standing multi-project program uses Orchestrate.
- Research prose: [unslop](../fstack-unslop/SKILL.md). Substantial methodology or operating documentation also uses [technical writing](../fstack-technical-writing/SKILL.md).
- Repeated mistakes: [correct](../fstack-correct/SKILL.md). Process learning requested after a run: [reflect](../fstack-reflect/SKILL.md).

## Playbook selection

| Request | Playbook |
| --- | --- |
| Company, ETF, macro or portfolio question | [Investigation](playbooks/investigation.md) |
| Build a valuation, analysis artifact or strategy specification | [Feature](playbooks/feature.md) |
| Reproduce and correct a wrong number, date or calculation | [Bug fix](playbooks/bug-fix.md) |
| Controlled strategy experiments | [Hillclimb](playbooks/hillclimb.md) |
| Diagnose an immutable dataset, model or backtest trace | [Trace forensics](playbooks/trace-forensics.md) |
| Equivalent restructuring of a model or pipeline | [Refactoring](playbooks/refactoring.md) |
| Small feasibility question | [Prototype](playbooks/prototype.md) |
| Write or change a skill | [Authoring a skill](playbooks/authoring-a-skill.md) |
| Compare skill behavior | [Eval](playbooks/eval.md) |
| Follow an existing research or evaluation run | [Babysit](playbooks/babysit.md) |
| Finalize independently verified research artifacts | [Shipping](playbooks/shipping.md) |
| One bounded unattended task | [Autonomous run](playbooks/autonomous-run.md) |
| A standing multi-project program | [Orchestrate](playbooks/orchestrate.md) |
| Authorized queue through verified research outputs | [Autopilot full](playbooks/autopilot-full.md) |
| Dependency-ordered outputs for user review | [Autopilot stack](playbooks/autopilot-stack.md) |
| Resume one earlier run | [Session pickup](playbooks/session-pickup.md) |
| Stop and preserve resumable state | [Pause safely](playbooks/pause-safely.md) |
| Plan multiple research or implementation phases | [Multi-phase plan](playbooks/multi-phase-plan.md) |

Software performance, live software forensics, UI parity, PR publication and worktree cleanup are development-only resources listed in the upstream map. A research answer does not require a PR. Follow the host's planning mode when active.

## Principles

Read applicable leaves from the following index. The index is not a substitute for the leaf's operational guidance.

- [attack the premise](../fstack-principle-attack-the-premise/SKILL.md).
- [boundary discipline](../fstack-principle-boundary-discipline/SKILL.md).
- [build the lever](../fstack-principle-build-the-lever/SKILL.md).
- [encode lessons in structure](../fstack-principle-encode-lessons-in-structure/SKILL.md).
- [exhaust the design space](../fstack-principle-exhaust-the-design-space/SKILL.md).
- [experience first](../fstack-principle-experience-first/SKILL.md).
- [explain the number](../fstack-principle-explain-the-number/SKILL.md).
- [fix root causes](../fstack-principle-fix-root-causes/SKILL.md).
- [foundational thinking](../fstack-principle-foundational-thinking/SKILL.md).
- [guard the context window](../fstack-principle-guard-the-context-window/SKILL.md).
- [laziness protocol](../fstack-principle-laziness-protocol/SKILL.md).
- [make operations idempotent](../fstack-principle-make-operations-idempotent/SKILL.md).
- [migrate callers then delete legacy apis](../fstack-principle-migrate-callers-then-delete-legacy-apis/SKILL.md).
- [minimize reader load](../fstack-principle-minimize-reader-load/SKILL.md).
- [model the domain](../fstack-principle-model-the-domain/SKILL.md).
- [never block on the human](../fstack-principle-never-block-on-the-human/SKILL.md).
- [outcome oriented execution](../fstack-principle-outcome-oriented-execution/SKILL.md).
- [prove it works](../fstack-principle-prove-it-works/SKILL.md).
- [redesign from first principles](../fstack-principle-redesign-from-first-principles/SKILL.md).
- [separate before serializing shared state](../fstack-principle-separate-before-serializing-shared-state/SKILL.md).
- [sequence verifiable units](../fstack-principle-sequence-verifiable-units/SKILL.md).
- [subtract before you add](../fstack-principle-subtract-before-you-add/SKILL.md).
- [test behavior not implementation](../fstack-principle-test-behavior-not-implementation/SKILL.md).
- [type system discipline](../fstack-principle-type-system-discipline/SKILL.md).

## Role and lifecycle discipline

Use the [role roster](../../agents/README.md) and [setup](../fstack-setup/SKILL.md). Large/xhigh is the default budget intent, adjusted to supported settings and task difficulty. Routine tasks lower effort; the hardest reasoning can raise it. The host's available model set is authoritative. Unavailable cross-family review is a gap; independent agents on the same model are still the same model family. Never fabricate a successful judge or a transcript.

Use fresh workers for new tasks. Resume a worker only when its live process or costly local state is required. The parent owns stop propagation and terminates only processes it created. On dropout, retry once with consolidated scope; after a second failure record a coverage gap. Inconclusive does not satisfy a required gate. Never silently relax the completion condition.

## Research authority

Proceed with authorized reversible research, calculations and local drafts. This workflow grants no permission to trade, transfer funds, change brokerage settings, purchase data, publish private research or send messages. Respect the host's authorization and approval rules for any additional action. Preserve original forecasts and losing experiments. Monitoring and scheduled work require an explicit user request.

## Final answer

Lead with the result and largest unknown. State what the user can conclude, cite evidence close to factual claims, and distinguish facts from assumptions and forecasts. Report the real models, checks, gaps and next useful observation. A verified calculation is not a verified future return. Keep private inputs and research outputs outside version control by default.
