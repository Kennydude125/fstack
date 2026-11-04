---
name: fstack-create-verification-skill
description: "Create a project-specific financial research or strategy verification skill, grounded in actual inputs and commands, and execute its instructions before delivery."
---

Read the [Codex adapter](../../adapters/codex.md) once per session and the [finance contract](../../references/finance-contract.md) before acting. Resolve peer skills by their file paths. Run helper commands from the canonical package root, with the detected Python interpreter.

# Create a verification skill

Generate project-specific verification instructions another agent can execute cold. The generated skill is a draft until its own steps have been run.

## 1. Interview the artifacts

Inspect actual datasets, metadata, model/rules, environment, run manifests and existing checks. Establish input identities, publication cutoff, commands, expected outputs, observable invariants and isolation requirements. Ask only what cannot be learned from the project. A broken base is a blocker to claiming a working procedure.

## 2. Generate

Use the host skill creator to create a project-local verify skill with name and discriminating description. Ground every command and expectation in the project. Include Launch/environment, Doctor, Drive/check commands, Evidence and Cleanup. Do not invent a source/provider, expected number or interface. Define the limits of each check and the author/verifier boundary.

Use the actual runtime from the canonical package root:

```text
python -m fstack_tools check-data DATA.csv METADATA.json
python -m fstack_tools verify MANIFEST.json RECEIPT.json --verifier VERIFIER_ID
python -m fstack_tools check-receipt RECEIPT.json
```

The manifest lists actual inputs, outputs and argv-based checks. Check expected values, not only file existence. Verification evidence identifies data, code, configuration and outputs. A check cannot prove future profitability.

## 3. Seed the verification map

Create one index and a small set of user-facing journeys covering source/data validation, the main calculation or strategy path, failure handling and final report. For each record prerequisites, exact invocation, expected observable result, artifacts and gotchas. Preserve unavailable prerequisites as failures or gaps; do not weaken a journey to pass.

## 4. Prove the instructions

Run the generated launch, doctor and at least one whole mapped journey in isolation, capture its real outputs, then clean up only resources created by the run. Verify evidence survives cleanup. Include an intentionally wrong variant for a critical calculation or invariant so the check demonstrably fails. Fix instructions and rerun failures; report any stand-in environment limits.

## 5. Maintain

Link [maintain verification](../fstack-maintain-verification-skill/SKILL.md). Offer cadence only if asked. Do not label an unexecuted verification guide complete.
