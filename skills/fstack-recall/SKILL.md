---
name: fstack-recall
description: "Reconstruct topic-scoped financial research context from authorized records, then check current inputs, original forecasts, pending questions and the next action."
---

Read the [Codex adapter](../../adapters/codex.md) once per session and the [finance contract](../../references/finance-contract.md) before acting. Resolve peer skills by their file paths. Run helper commands from the canonical package root, with the detected Python interpreter.

# Recall

Rebuild topic-scoped research context before acting. Resuming one specific prior run uses the Session pickup playbook. If the user already provides a sufficient state capsule, use it rather than mining history again.

1. Lock topic, workspace and date range; recent defaults to the last seven days. Read only authorized research records and chats within that scope.
2. For a large record, partition history across explorers. Each returns original goal, dated forecasts, decisions, open questions, corrections and artifact pointers. One or two records can be read directly.
3. Sweep relevant shared evidence through why in parallel when the topic names a company, model or strategy. Use financial source categories; preserve unavailable and empty results. Do not browse unrelated private connectors.
4. Verify current artifact hashes and stale time-sensitive inputs. Preserve original forecasts and completed valid work; a current quote must not overwrite the quote used in an earlier decision.
5. Present a short capsule, research-thread statuses, recurring problems and one concrete next action. Statuses distinguish planned, in progress, blocked, checked, stale and complete. Cite actual records and sanitize any public output.

If the host cannot expose the requested transcript or source, report the gap. Never fabricate a recalled decision from the current market outcome.
