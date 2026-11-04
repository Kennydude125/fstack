---
name: fstack-setup
description: "Detect fstack model and tool capabilities, configure per-role model choices and reasoning budget, and report unavailable diversity without inventing models."
---

Read the [Codex adapter](../../adapters/codex.md) once per session and the [finance contract](../../references/finance-contract.md) before acting. Resolve peer skills by their file paths. Run helper commands from the canonical package root, with the detected Python interpreter.

# Setup fstack

Configure roles using actual host capabilities. This is an instruction-driven coordinator, not a separate scheduling service.

1. **Detect.** Enumerate models accepted by the current spawn interface and actual tool capabilities. Never persist an unconfirmed model identifier. `auto` and `inherit-parent` mean omit the explicit model. Detect the canonical package root and usable Python interpreter.
2. **Load.** Read the private workspace role configuration if one exists. Keep it outside tracked source. Compare it with [the role roster](../../agents/README.md); remove retired roles with an explanation.
3. **Budget.** Preserve the original choices unlimited/max, large/xhigh, medium/high and small/medium. Default intent is large/xhigh. Use supported effort values; reduce routine work and reserve highest supported reasoning for difficult work. Fast modes are for genuine urgency, not an assumed blanket preference.
4. **Map.** Assign available models per role. Arena/architect runners and interrogate reviewers are lists; list length determines seats. The cross-judge pool is ordered and produces one eligible judge from another family. An inherited model never creates diversity by itself.
5. **Review.** Show roles, effective effort, model family, unsupported choices and missing tools. Ask only for real preference decisions or unavailable identifiers. Existing session authorization can cover writing the presented local configuration.
6. **Validate and save.** Save schema_version, budget, roles and detected capabilities in the user's private fstack configuration. Re-running converges to the same configuration. Do not rewrite global Codex settings or install providers implicitly.
7. **Confirm.** Report what was actually saved, where, active limitations and whether a new session is required by the host. Offer a project-specific verification skill when an actual project lacks one; do not create schedules without a request.

When only the inherited model is usable, all needed roles can still run as separate agents. State that cross-family judgment did not run. Respect actual concurrency and permission inheritance.
