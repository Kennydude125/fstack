# Shipping research

1. Freeze the artifact and dependency graph. Obtain a verifier who did not author the research program/calculation. The verifier follows real user commands and compares expected and actual outputs, not only test badges.
2. Accept only a receipt covering current data, code, configuration, outputs and actual check scope. Inspect it with `python -m fstack_tools check-receipt RECEIPT.json` from the canonical package root.
3. Finalize dependency order from the root, stopping at the first missing, failed, stale or inconclusive required gate. An artifact above an unverified dependency waits.
4. Recheck identities immediately before finalization. Material changes invalidate dependent verification; do not carry over a prior green status by title or filename.
5. Finalize only the verified research run and report its ceiling, verifier, evidence and next gap. Keep the three conclusions separate: artifact integrity, thesis support and performance evidence.
6. A completed research package does not authorize publication of private data or a financial transaction. Apply separate user authority to any external publication. Leave finalized artifacts immutable and record later revisions separately.

See the [main mode](../SKILL.md) for linked peer skills and the [finance contract](../../../references/finance-contract.md) for shared artifact and authority rules.

Derived from [pstack shipping.md](https://github.com/cursor/plugins/blob/c742dd61706fbacc1b95f1a20b7b988cf096ce6c/pstack/skills/poteto-mode/playbooks/shipping.md).
