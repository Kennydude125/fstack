---
name: fstack-interrogate
description: "Challenge a financial thesis, model, dataset or backtest. Reproduce technical defects and separately report sourced economic objections and unresolved uncertainty."
---

Read the [Codex adapter](../../adapters/codex.md) once per session and the [finance contract](../../references/finance-contract.md) before acting. Resolve peer skills by their file paths. Run helper commands from the canonical package root, with the detected Python interpreter.

# Interrogate

Adversaries try to break a thesis, model, dataset or strategy result. Report findings without silently applying fixes. Open Frame, Fan out, Verify and Report.

## Frame

Restate the user's intent with [in your own words](../fstack-in-your-own-words/SKILL.md). Pin exact artifacts, source cutoff, rules, assumptions and requested scope. Ask only when a consequential intent choice cannot be inferred.

## Fan out

Use arena's runner selection and isolated-output steps with the `interrogate reviewers` roster. Give reviewers the same scope and intent, not a favored conclusion. Each must distinguish two channels.

1. **Technical defects.** Reproduce an actual data, timing, calculation, implementation or evaluation error. Return the exact command, actual output, required output and affected artifact. Assertions without a run are not verified defects.
2. **Economic objections and unknowns.** State the disputed assumption, contrary evidence or plausible alternative mechanism, economic effect and discriminating future observation. These remain objections or uncertainties; do not require a deterministic repro of an uncertain future.

## Verify

Re-run each technical reproduction on the pinned artifact. Keep it only when the observed failure contradicts intent. Reopen sources for material economic objections, preserve their evidence tier, and flag missing evidence. Merge shared root causes. Do not select a winning reviewer or graft their reports as arena does.

## Report

Give intent, verified technical findings with commands, sourced economic objections, unresolved questions, and dropped findings with reasons. No verified technical findings is valid and does not erase economic uncertainty. Prioritize issues by their effect on the user's research decision.
