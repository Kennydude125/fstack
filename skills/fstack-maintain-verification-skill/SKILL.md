---
name: fstack-maintain-verification-skill
description: "Maintain a financial verification map as data providers, models or strategy rules change. Distinguish stale instructions, missing checks and real defects."
---

Read the [Codex adapter](../../adapters/codex.md) once per session and the [finance contract](../../references/finance-contract.md) before acting. Resolve peer skills by their file paths. Run helper commands from the canonical package root, with the detected Python interpreter.

# Maintain verification

Reconcile the project verification map with current datasets, model interfaces and strategy behavior.

1. Read the current map, manifest, data contracts, commands and code changes. Pin the previous and current identities.
2. Inspect each affected journey. Classify stale instructions, harness gaps, data-provider or schema changes, and genuine calculation defects separately.
3. Run at least one affected real journey and reproduce every claimed defect. Missing credentials or data is a gap, not an excuse to report a pass.
4. Update only the map and checks warranted by actual changes. Do not silently replace the investment hypothesis, alter an evaluation protocol after observing its result or overwrite original forecasts.
5. Re-run the changed instructions and the relevant regression; demonstrate that a deliberately wrong calculation is still rejected. Record receipts for the exact artifacts.
6. Report actual changes, stale receipts, coverage and unsupported cases. Route product/calculation fixes to Bug fix instead of hiding them in documentation maintenance.
