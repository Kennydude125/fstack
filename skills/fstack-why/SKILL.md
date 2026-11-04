---
name: fstack-why
description: "Investigate the reasons behind financial results, market narratives, assumptions or investment decisions using source-specific investigators, competing hypotheses and explicit evidence gaps."
---

Read the [Codex adapter](../../adapters/codex.md) once per session and the [finance contract](../../references/finance-contract.md) before acting. Resolve peer skills by their file paths. Run helper commands from the canonical package root, with the detected Python interpreter.

# Why

Investigate financial drivers, economic explanations and reasons for an investment assumption or decision. [How](../fstack-how/SKILL.md) owns mechanics. This skill owns evidence for reasons.

## 1. Anchor the question

Identify the target, observation, period, publication time and competing explanations. Preserve the user's hypothesis as one candidate, not the answer. Establish a seed packet with instrument identity, dated source excerpts, metrics, original decision records and applicable model version. Give the same packet to every investigator.

Read [epistemics](references/epistemics.md). Every material claim is Direct, Supported, Inferred, Speculative or Unknown. Direct records what a source actually states; management's explanation remains management's statement, not independently established causality.

## 2. Discover evidence and cover the categories

Default to a full source coverage map. Discover actual connectors and public browsing capabilities. A connector being available does not authorize reading unrelated private records. Consult [the source playbook](references/source-playbook.md).

| Category | Best evidence |
| --- | --- |
| Issuer and regulatory disclosures | Original filings, exchange announcements, shareholder reports and fund documents |
| Market and instrument data | Identified price/volume/action series with dates, basis and source |
| Expectations | Dated analyst consensus, separately labeled issuer guidance, or model-derived price assumptions |
| Official economic data | Central bank, government and statistical releases with release/revision dates |
| Industry and independent reporting | Relevant primary industry material and reporting whose original source can be checked |
| Authorized research and portfolio records | The user's named research, original forecasts and provided holdings or trade records |
| Models and experiment history | Actual model code, rules, manifests, decisions, failures and verification receipts |

For each category record searched, empty, unavailable or not applicable, with searches and reasons. Missing consensus must remain unknown. Deduplicate syndicated reports. Do not manufacture a source investigation merely to fill a category.

## 3. Parallel investigators

Spawn one investigator per relevant available source category, each owning a specific source or connector, using [the investigator prompt](references/investigator-prompt.md). Multiple sources in a category can have separate workers when necessary. Use `why investigators`; keep source reads behaviorally read-only and outputs isolated. Explicitly justify skipped or unavailable categories. Exhaustive coverage is about relevant sources, not accessing every connected service.

## 4. Separate synthesis

After terminal reports, spawn `why synthesizer` with every finding, negative search and skip reason, the original packet, [epistemics](references/epistemics.md) and [the synthesizer prompt](references/synthesizer-prompt.md). It spot-checks citations and competing explanations. Never convert incomplete evidence into certainty.

## 5. Present

Keep The question, The observation, What we found, What we can reasonably infer, Competing hypotheses, What we do not know, Sources consulted and Confidence summary as appropriate. Keep one source-coverage line per investigation, including empty results. Preserve the synthesizer's confidence language. If planning a change, finish with Preserve / Change / Avoid / Risk constraints.
