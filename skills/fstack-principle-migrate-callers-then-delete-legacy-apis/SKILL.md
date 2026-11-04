---
name: fstack-principle-migrate-callers-then-delete-legacy-apis
description: "For fstack financial research: Apply when introducing a new internal API while old callers still exist. Migrate callers and delete the old API in the same wave instead of preserving compatibility layers."
---

Read the [Codex adapter](../../adapters/codex.md) once per session and the [finance contract](../../references/finance-contract.md) before acting. Resolve peer skills by their file paths. Run helper commands from the canonical package root, with the detected Python interpreter.

# Migrate Callers Then Delete Legacy APIs

- Update tests to assert the new contract, and delete tests that only protect pre-refactor implementation details

**When this applies:**
- No external users depend on backward compatibility
- The project can absorb coordinated breaking changes
- The new API is part of a simplification or refactor initiative



## Financial application

This principle applies to development migrations. Preserve historical research inputs, forecasts and published interfaces as required.
