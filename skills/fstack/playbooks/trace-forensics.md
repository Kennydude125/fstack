# Trace forensics

1. Freeze the supplied dataset, trade log, calculation trace or backtest artifact and record its hash. The deliverable is diagnosis, not an unrequested correction.
2. Reconstruct input-to-output flow with how. Partition independent paths only when useful; preserve the same cutoff and source packet.
3. Reproduce demonstrated data/timing/calculation mechanisms with explicit commands. Separate confirmed defects, economic hypotheses and unknowns.
4. Return causal paths, affected outputs, exact evidence and the next discriminating check. Preserve the original artifact. A requested correction starts Bug fix.

See the [main mode](../SKILL.md) for linked peer skills and the [finance contract](../../../references/finance-contract.md) for shared artifact and authority rules.

Derived from [pstack trace-forensics.md](https://github.com/cursor/plugins/blob/c742dd61706fbacc1b95f1a20b7b988cf096ce6c/pstack/skills/poteto-mode/playbooks/trace-forensics.md).
