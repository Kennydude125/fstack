---
name: fstack-how
description: "Explain how a business, ETF, portfolio, valuation model or trading strategy works. For complex questions, use source explorers and a separate explainer. Use fstack-why for reasons and competing explanations."
---

Read the [Codex adapter](../../adapters/codex.md) once per session and the [finance contract](../../references/finance-contract.md) before acting. Resolve peer skills by their file paths. Run helper commands from the canonical package root, with the detected Python interpreter.

# How

Explain the mechanism of the named company, ETF, portfolio, financial model or strategy. Build a working mental model from source material, not a generic description.

## 1. Assess complexity

State the interpretation and explore if scope is ambiguous. A simple single-model or narrow question uses one explainer that investigates and explains in one pass. Give it [the explainer prompt](references/explainer-prompt.md) without explorer findings, then go to presentation.

For a subsystem spanning several business drivers, model components or data transformations, use the complex path. When in doubt, keep the path simple.

## 2. Explore, complex only

Partition the question into 2–4 distinct angles. Spawn explorers using [the explorer prompt](references/explorer-prompt.md), the user's goal, exact evidence cutoff and assigned angle. Give each a separate result location. Use the `how explorer` role. Batch the fan-out within actual concurrency limits.

Each explorer reports components, actual flow, boundaries, files/sources read, surprising behavior and unresolved questions. An unsearched source is a gap, not a negative finding.

## 3. Synthesize, complex only

After all explorers return, spawn a separate `how explainer` with their complete findings and the original question using [the explainer prompt](references/explainer-prompt.md). It reconciles contradictions by reopening sources rather than averaging conflicting claims.

## 4. Present

Present the explanation with light edits only. Preserve uncertainty and evidence. Use Overview, Key concepts, How it works, Where things live and Gotchas where applicable. A diagram is useful when it clarifies several interacting drivers or transformations. Missing data remains visible.
