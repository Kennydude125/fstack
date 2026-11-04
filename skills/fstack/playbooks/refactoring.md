# Refactoring

1. Pin current inputs, formulas, rules, outputs and meaningful invariants before restructuring. Distinguish structural equivalence from changed investment assumptions.
2. Use how to trace consumers and architect when changing boundaries. Choose the smallest coherent structure and one owner per artifact.
3. Refactor in independently verifiable units. Keep numerical tolerances explicit; do not silently alter cost, adjustment, timing or evaluation conventions.
4. Re-run before/after behavior and regression checks. Independently review material changes and regenerate stale receipts.
5. Finalize through Shipping with equivalence evidence and any actual semantic change called out separately.

See the [main mode](../SKILL.md) for linked peer skills and the [finance contract](../../../references/finance-contract.md) for shared artifact and authority rules.

Derived from [pstack refactoring.md](https://github.com/cursor/plugins/blob/c742dd61706fbacc1b95f1a20b7b988cf096ce6c/pstack/skills/poteto-mode/playbooks/refactoring.md).
