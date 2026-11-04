---
name: fstack-reflect
description: "Review the current research process through judgment, tooling and divergent lenses, then synthesize evidence-backed improvements to existing skills or structural checks."
---

Read the [Codex adapter](../../adapters/codex.md) once per session and the [finance contract](../../references/finance-contract.md) before acting. Resolve peer skills by their file paths. Run helper commands from the canonical package root, with the detected Python interpreter.

# Reflect

Improve the research process from observed repeated failures. Investment outcome review belongs to the review playbook; a recent profitable trade alone does not justify changing the process.

## 1. Locate the current record

Use this task's authorized transcript, decision journal and artifact receipts. If a transcript is unavailable, provide a bounded session digest and name the gap. Never read unrelated projects or global chat stores. Skip trivial or already addressed one-offs.

## 2. Three reviewers

Spawn three independent lenses within concurrency limits, using the configured roles and the corresponding prompt files.

| Lens | Role | Prompt |
| --- | --- | --- |
| Judgment | reflect judgment | [judgment](references/judgment-reviewer.md) |
| Tooling | reflect tooling | [tooling](references/tooling-reviewer.md) |
| Divergent | reflect divergent | [divergent](references/divergent-reviewer.md) |

Each finds repeated, evidence-backed process problems and routes a concrete improvement to an existing skill or structural control. They return actual evidence, accepted limitations and alternative explanations.

## 3. Separate synthesis

After the three reports, spawn `reflect synthesizer` with all outputs and [the synthesizer prompt](references/synthesizer.md). Spot-check citations. Return Accepted, Rejected and Structural backlog, explaining each choice. Do not turn agreement between same-model agents into cross-model validation.

## 4. Structural enforcement

Move proposals better enforced by a parser, type, test, metadata field or runtime gate to the structural backlog. Favor an existing canonical rule over duplicated instructions. Preserve the original experiment history.

## 5. Apply within scope

Present concrete destinations and edits before persistence. Apply already authorized local changes under the host's rules; obtain any additional authorization those rules actually require. Do not edit plugin caches, automatically file tickets or send messages. For substantial skill edits use the host skill creator and validate the result. Future-run global configuration changes require explicit scope.

## 6. Report

List edits applied, concrete structural backlog, rejected items and why, verification performed and remaining gaps. Only claim changes or backlog writes that actually occurred.
