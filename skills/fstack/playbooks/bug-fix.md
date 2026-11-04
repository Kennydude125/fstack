# Bug fix

1. Pin the defect and reproduce it against the actual dataset, financial model, import or strategy code. Capture a failing command with its actual and intended result before editing.
2. Trace the first wrong input, timestamp, unit, transformation or assumption. Inspect all affected callers and downstream artifacts through how; use why when rationale matters.
3. Make the smallest root-cause correction. Keep a meaningful regression that fails on the original defect. Distinguish a software error from a losing investment outcome.
4. Re-run the reproduction, relevant checks and dependent calculations. Invalidate receipts bound to changed artifacts and obtain fresh independent verification where required.
5. Finalize through Shipping with before/after evidence, corrected scope and remaining uncertainties. Preserve original research records and add the correction as a new version.

See the [main mode](../SKILL.md) for linked peer skills and the [finance contract](../../../references/finance-contract.md) for shared artifact and authority rules.

Derived from [pstack bug-fix.md](https://github.com/cursor/plugins/blob/c742dd61706fbacc1b95f1a20b7b988cf096ce6c/pstack/skills/poteto-mode/playbooks/bug-fix.md).
