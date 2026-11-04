---
name: fstack-arena
description: "Compare independent financial research or model designs on the same fixed task, choose a base, graft useful parts and verify the result. Keep evaluation data out of strategy selection."
---

Read the [Codex adapter](../../adapters/codex.md) once per session and the [finance contract](../../references/finance-contract.md) before acting. Resolve peer skills by their file paths. Run helper commands from the canonical package root, with the detected Python interpreter.

# Arena

Generate independent solutions to the same research or model-design task, choose a base, and integrate only useful parts. Open the phase list before launching workers.

## A. Frame

Define the artifact and freeze the common evidence packet, information cutoff and constraints. Write 3–6 concrete criteria for judging this task. Candidates receive the task, not the rubric. Pick `arena runners` from confirmed available models. Preserve at least two candidates for a design comparison; disclose any unavailable seat or repeated model. Give each candidate a separate output location. No shared writes.

## B. Fan out

Give all candidates the same task and evidence. Each produces its artifact and a short rationale naming alternatives considered and rejected. Run independent candidates concurrently within host limits. If a candidate produces no artifact, record the dropout rather than inventing a result.

## C. Cross-judge

After candidates finish writing, select one available judge from `arena cross-judge pool` whose model family differs from the coordinator's. Give it the hidden rubric and outputs under neutral labels, not author model names. It scores each criterion and recommends a base with reasons. Run it alongside the coordinator's reading. If no eligible family exists, skip this judge, record the gap and make no cross-family claim.

## D. Pick

Read every candidate end to end. Score each criterion and compare to the judge. Resolve disagreement by inspecting artifacts and the rubric. Choose the coherent design the next researcher can extend without breaking assumptions. Ties favor the simpler interface and stronger evidence boundary.

## E. Graft

Revisit each losing candidate once. Integrate only the few elements that strengthen the chosen design. Record their origin, what was rejected and why. Preserve one coherent model. If the proposals diverge because the task was underspecified, reframe rather than average incompatible designs.

## F. Verify

Verify the actual synthesized artifact. Report the chosen base, judge verdict or missing judge, grafts, rejected alternatives, dropouts and verification outcome.

For strategies, candidate selection and grafting use development data only. Do not reveal or optimize against the reserved evaluation data. Record all attempted variants. Reading a holdout for selection changes its status; re-running it cannot restore untouched status. Arena chooses a research artifact, not a guarantee of future profitability.
