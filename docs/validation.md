# Validation record

Date: 2026-11-04. Implementation baseline: `ee0c88bd6d829b80c79fa513acb8e48110ee4416`.

## Executable checks

- All 28 unit/regression tests pass locally and in the [Windows and Linux CI run](https://github.com/Kennydude125/fstack/actions/runs/41810989957).
- The package checker passes all 50 active skills, local references, namespace rules and the complete 58-skill, 24-principle, 23-playbook disposition registry.
- All 50 active skills also passed the host's official skill frontmatter validator locally.
- The real project installer was applied to an isolated project twice. The first run installed the payload and discovery shims; the second wrote no new files. The installed canonical payload passed the package checker.
- Both synthetic daily datasets passed the actual CLI. Their manifest ran the two independent calculation checks and produced an integrity receipt of VERIFIED, thesis support unknown and performance evidence development. The receipt passed a separate current-artifact check.
- An independent code reviewer reproduced two defects before correction: private filename exclusions differed between Git and installer, and a newline-truncated journal could be corrupted by append. Both fixes were independently rechecked and have regressions.
- Gitleaks 8.30.1 found no leaks in the staged content, working directory or complete history before the first push. Its Linux CI job also passed. The release download was checked against its official checksum. No custom secret allowlist was used.

Run from the repository root:

```sh
python scripts/check_package.py
python -m unittest discover -s tests -v
python scripts/check_secrets.py --staged
python scripts/check_secrets.py --history
```

## Research behavior comparison

Two fresh research contexts received the same [fictional thesis request and source packet](../examples/thesis_research/README.md). One used the earlier four-reference Finstack baseline; one used this fstack implementation. Neither was told it was participating in a comparison. A separate reviewer saw neutral A/B labels and the same sources, without the variant or model identities.

| Shared criterion | Earlier baseline | fstack |
| --- | --- | --- |
| Reported 40%, prior reported 35%, known-rebate-adjusted 33.3333% | PASS | PASS |
| Missing market expectations remain unknown | PASS | PASS |
| USD 12 and 20% are conditional price outputs, not promised returns | PASS | PASS |
| Syndicated stories are one underlying source | PASS | PASS |
| Source/cutoff accuracy and assumption labels | PASS | PASS |
| Concrete next evidence without transactions | PASS | PASS |

No material financial-analysis defect was identified in either final report. This single case supports no statistical accuracy, general superiority or investment-return claim.

The fstack run also executed the instruction graph. Two source investigators returned separate artifacts, which a fresh why synthesizer reconciled. A separate how explainer read the original sources and explained the mechanism through the simple-question path. An independent calculation verifier reran exact-fraction assertions and the real manifest; a separate adversary reproduced calculations and reviewed the report. The coordinator read the artifacts, checked the receipt, accepted an original-cutoff expectations refinement, appended the decision journal and completed a checkpoint. The parent independently checked the final calculation receipt as VERIFIED with no stale-artifact issues. This activity audit is distinct from the blinded report-quality assessment.

## Limits

The behavioral run used independent contexts with inherited available models. It did not establish cross-family model review; precise inherited model identifiers were not exposed to the research workers. No complete exportable host transcript was available, so workflow evidence used actual child activity, commands and artifacts.

An early event-schema mismatch was observed while implementation files were still being finalized. The frozen template and documentation were reopened and the actual journal command passed. It is not an unresolved defect in the published baseline.

The installed file layout and instruction-driven workflow were exercised. Native client skill-picker refresh was not independently automated. Not every playbook has been executed end to end. External data-provider authenticity, live market integrations, optional original developer runtimes and real investment performance were not validated. Verifier identity is operator-attested, and running a manifest executes its explicit commands with caller permissions.
