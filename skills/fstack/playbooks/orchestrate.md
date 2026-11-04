# Orchestrate

1. Use this only for a standing multi-project research program that outlives one ordinary task. Define program outcomes, dependencies, scope, budgets and completion conditions first.
2. The coordinator owns durable task state, decisions, worker roster and final synthesis. Assign one owner and a distinct verifier to each artifact. Workers receive exact input identities and isolated outputs.
3. Dispatch independent ready work within host limits. Advance dependencies only from actual checked artifacts. Replace completed workers with fresh agents for new tasks, preserving live state only when necessary.
4. Record blockers, stale inputs, unavailable models and bounded retry outcomes. Replan from evidence without erasing original forecasts or failed experiments.
5. On stop, cancel child work and preserve each atomic result and next action. Resume by validating checkpoint and artifact identities. Use host task/event capabilities if available; report missing capabilities rather than pretending a background service exists.
6. Finalize verified dependency runs through Shipping. Program completion is a research outcome, not a profitability target or trading authority.

See the [main mode](../SKILL.md) for linked peer skills and the [finance contract](../../../references/finance-contract.md) for shared artifact and authority rules.

Derived from [pstack orchestrate.md](https://github.com/cursor/plugins/blob/c742dd61706fbacc1b95f1a20b7b988cf096ce6c/pstack/skills/poteto-mode/playbooks/orchestrate.md).
