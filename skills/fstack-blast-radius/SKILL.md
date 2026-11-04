---
name: fstack-blast-radius
description: "Trace the effects of a changed financial assumption, dataset, model rule or exposure through dependent calculations and portfolio scenarios."
---

Read the [Codex adapter](../../adapters/codex.md) once per session and the [finance contract](../../references/finance-contract.md) before acting. Resolve peer skills by their file paths. Run helper commands from the canonical package root, with the detected Python interpreter.

# Blast radius

Trace how a changed assumption, data correction, model rule or exposure affects dependent financial artifacts.

1. Pin the before/after change and its source. Use how to trace actual dependencies, units, timestamps and consumers.
2. Partition uncertain effects through swarm only where independent analysis adds coverage. Keep a matrix of affected models, scenarios, instruments and reports.
3. Recalculate affected outputs from the same frozen inputs except for the named change. Separate directly measured effects from hypothetical scenarios and unknown dependencies.
4. Invalidate receipts whose material inputs changed. Check portfolio concentration, common risk factors, currency and liquidity where relevant.
5. Report the smallest supported scope, each verified effect, scenario assumptions, untouched or unexamined boundaries, and the next check. Do not infer maximum loss from one chosen stress scenario.
