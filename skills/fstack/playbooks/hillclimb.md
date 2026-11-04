# Controlled strategy experiments

1. Define a falsifiable hypothesis and freeze rules, universe, information cutoff, development/evaluation boundaries, costs, benchmark and completion criteria before running candidates.
2. Audit the baseline measurement with benchmark-checklist. Establish data validity and a meaningful wrong-variant check before evaluating hypotheses.
3. Create an append-only experiment log containing every variant and parameter search. Compare alternatives only on development data; predeclare the number or budget of attempts and stopping condition.
4. For each bounded iteration state the hypothesis, make the smallest change, run the fixed development protocol, inspect actual signals/executions/cash and retain or reject with evidence. Do not set a target historical return as the completion condition.
5. Freeze the selected specification before using untouched evaluation data. Once an evaluation result informs selection or tuning, label that data reused and record the changed evidence status. Re-running cannot restore untouched status.
6. Independently verify implementation, data lineage, timing, costs and report labels. Deliver the completed protocol and results, including failures and inconclusive outcomes. Future data or prospective simulation supplies new evidence; historical profitability is not a build property.

See the [main mode](../SKILL.md) for linked peer skills and the [finance contract](../../../references/finance-contract.md) for shared artifact and authority rules.

Derived from [pstack hillclimb.md](https://github.com/cursor/plugins/blob/c742dd61706fbacc1b95f1a20b7b988cf096ce6c/pstack/skills/poteto-mode/playbooks/hillclimb.md).
