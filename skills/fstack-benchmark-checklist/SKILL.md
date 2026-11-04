---
name: fstack-benchmark-checklist
description: "Audit a reported financial performance result for data provenance, costs, leakage, search history, baseline, sample coverage and whether the reported experiment actually ran."
---

Read the [Codex adapter](../../adapters/codex.md) once per session and the [finance contract](../../references/finance-contract.md) before acting. Resolve peer skills by their file paths. Run helper commands from the canonical package root, with the detected Python interpreter.

# Benchmark checklist

Before reporting or acting on a financial performance number, write the precise claim and read the program that produced it. Keep software runtime benchmarks separate from investment returns.

1. **What is measured?** State metric formula, sample unit, period, universe, benchmark and currency. Show the path from observations to the number.
2. **What information was available?** Check publication and revision dates, historical constituents and delistings. Period end is not announcement time. Label LLM hindsight contamination.
3. **Was the experiment selected?** Preserve candidate/parameter search history, development choices and the frozen evaluation protocol. Reused holdouts are no longer untouched.
4. **Did it error?** Count missing/invalid observations, failed commands, absent trades and rejected orders. Empty data and zero trades cannot establish a strategy edge.
5. **Did the work happen?** Inspect generated signals, execution times, trade/cash records and outputs. A summary saying a backtest ran is not evidence. Same-close execution after a closing signal is invalid unless executable timing is demonstrated.
6. **Are economic costs included?** Check commissions, spreads/slippage, applicable taxes, borrowing, FX, dividends, splits and investable liquidity. Unknown material costs make net-return claims inconclusive.
7. **Does the comparison match?** Use comparable periods, currency, risk and exposure. Separate development, untouched evaluation and prospective simulation. Overlapping bets and correlated samples are not independent trials.
8. **Does it reproduce and matter?** Re-run deterministic calculations from frozen inputs; report relevant sensitivity, regime dependence, drawdowns and uncertainty. Repeating the same historical sample does not create new economic evidence.

Lead with the supported conclusion or inconclusive result. Include units, sample size, assumptions, provenance, costs, search history and missing checks. A favorable historical number is evidence about that specified experiment, not a guarantee or a proved durable advantage.
