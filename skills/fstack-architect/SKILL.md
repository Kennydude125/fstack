---
name: fstack-architect
description: "Design a financial research method, valuation model or strategy specification before implementation. Ground the question, compare structurally distinct alternatives and record the selected design."
---

Read the [Codex adapter](../../adapters/codex.md) once per session and the [finance contract](../../references/finance-contract.md) before acting. Resolve peer skills by their file paths. Run helper commands from the canonical package root, with the detected Python interpreter.

# Architect

Design the research, model or strategy contract before filling in calculations or code. Open Ground, Sketch, Agree, Implement and Scrap as the phase list.

## A. Ground

Run [how](../fstack-how/SKILL.md) over the relevant business, model and data path. If changing ownership or assumptions, also run [why](../fstack-why/SKILL.md). Read original records and actual artifacts; naming a file is not grounding. Skip only for a genuinely new problem with no surrounding system.

## B. Sketch

Run [arena](../fstack-arena/SKILL.md) with the common grounding and [runner prompt](references/runner-prompt.md). Use `architect runners`. Require two structurally distinct viable alternatives before synthesis. Write the intended caller usage or research question first, then derive inputs, outputs, transformations, assumptions and verification boundaries. A strategy sketch includes the rules, timing, universe, costs and evaluation protocol before returns are computed.

Screen alternatives with [design red flags](references/design-red-flags.md). Prefer the design that hides the actual complexity behind the simpler interface. The synthesis record follows [the rationale template](references/rationale-template.md), including selected base, grafts and rejected choices.

## C. Agree

Proceed to implementation when already authorized. Stop at the design only when the user requests a checkpoint or the host is in planning mode. Material new scope or permissions still follow the host's rules.

## D. Implement

Fill in the chosen sketch. Log departures and determine whether they expose a missed requirement, wrong design or unnecessary implementation. Keep development-data results separate from untouched evaluation.

## E. Scrap

Repeated workarounds, inconsistent units, hidden assumptions, multiple writers or repeated contract deviations are signals to revisit the design. Re-ground, subtract redundant structure and re-run arena. A single ordinary edge case does not justify redesigning everything.

Deliver the usage sketch, model/data contract, selected design, synthesis rationale and actual validation. A model design can be coherent while its economic hypothesis remains uncertain.
