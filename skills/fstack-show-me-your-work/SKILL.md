---
name: fstack-show-me-your-work
description: "Maintain an append-only, retry-safe investment research decision trail with evidence pointers, experiment identity, checkpoints and an audit against actual work."
---

Read the [Codex adapter](../../adapters/codex.md) once per session and the [finance contract](../../references/finance-contract.md) before acting. Resolve peer skills by their file paths. Run helper commands from the canonical package root, with the detected Python interpreter.

# Show me your work

Keep one canonical append-only decision journal in the private research workspace. The coordinator owns its writes; workers provide separate result artifacts. Public examples use synthetic content only.

## Record decisions

For each consequential choice, checkpoint, experiment, rejection, correction or blocker, create an event with a stable event_id, run_id, phase, decision, reason and evidence strings. An optional result field records the observed outcome. Use the actual runtime event contract and [event template](../../templates/event.json). Start a new run with a start event identifying the previous range and any inherited work. On return, read recent events before writing.

From the canonical package root run:

```text
python -m fstack_tools log PATH_TO_PRIVATE_JOURNAL.jsonl PATH_TO_EVENT.json
```

The helper owns timestamping, duplicate-event handling and validation. Do not implement a second ad hoc journal writer. Evidence is a pointer to a source, command output, receipt or versioned artifact, not a confident narrative. Prefer rerunnable checks to one-time observations.

Wrong decisions receive a new superseding event. Never rewrite the original forecast, delete losing experiments or edit history. If a run retries, use the same event ID for the same event. A conflicting payload is an error, not a new version of history.

## Audit against actual work

Before handing back, compare this run's journal with its actual tool activity and artifacts. Read only the active authorized transcript if the host exposes one. Otherwise label the audit as artifact-based and name the missing transcript. Do not search global chat storage.

Check every claimed action occurred, evidence resolves, meaningful abandoned approaches are present, and verification claims match command outputs. Add corrections as new events, preserving wrong original entries. Review inherited claims only insofar as the current work actually verifies them.

## Independent review

Use an independent reviewer, preferably from a different available model family, to flag weak evidence, skipped verification and risky choices. If the required family is unavailable, disclose that gap and report what review actually ran. End the trail report with reviewer identity, flags linked to events, or an evidence-backed no-flags result. Keep private journals out of the public repository.
