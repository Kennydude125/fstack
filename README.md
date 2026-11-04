# fstack

Investing and finance research workflows adapted from [pstack](https://github.com/cursor/plugins/tree/c742dd61706fbacc1b95f1a20b7b988cf096ce6c/pstack), with a Codex adapter and reproducible local checks.

[繁體中文使用指南](docs/README.zh-Hant.md) · [Architecture](docs/architecture.md) · [Upstream adaptation map](docs/upstream-map.md) · [Validation record](docs/validation.md)

Fstack keeps pstack's single coordinator, task-specific playbooks, progressively loaded principles, independent workers, adversarial review, verification, and decision trail. Its first finance scope is US and Hong Kong equities, ETFs, portfolio analysis, and daily-or-longer strategy research. Sources are public documents and user-supplied files.

## Install in a research project

Use Python 3.11 or newer. From this package's root:

```sh
python -m pip install -e .
python scripts/check_package.py
python scripts/install.py /absolute/path/to/your-project
python scripts/install.py /absolute/path/to/your-project --apply
```

The project installer defaults to a dry run. The `--apply` command copies a canonical payload into the project's `.agents/fstack/` folder and creates discovery shims under `.agents/skills/`. All cross-skill references resolve in the canonical payload. Windows does not need symlink privileges. Identical reruns make no changes. A different existing destination file stops the install before it writes anything; unrelated skills are preserved. This installer deliberately does not overwrite an older or edited installation.

Open that project in Codex. Invoke `$fstack`, or select its skill. If the client has not refreshed its skill catalog, restart it. Installation does not change global models, account permissions, or credentials.

## Research with the original workflow mechanisms

Examples:

```text
$fstack I think this company's margin recovery is underappreciated. Investigate the evidence and what would disprove it.
$fstack Build a reproducible daily strategy study from these files. Freeze the evaluation protocol before running it.
$fstack-interrogate Challenge this investment memo and reproduce any calculation or data defects.
$fstack Review my original forecast against the new results without rewriting the original record.
```

The coordinator selects the relevant playbook and owns the final answer. Complex understanding uses separate explorers and an explainer. Source investigations retain missing and contradictory evidence. Design comparisons use separate candidates and a hidden rubric. Reviewers check actual artifacts rather than accepting author self-reports. Role-specific model choices must be available in the current environment; missing model diversity is disclosed.

Use `$fstack-setup` to inspect available tools and models and configure role assignments. The port keeps pstack's task-driven collaboration and role budget intent. It does not fabricate a Claude/Grok reviewer when the host only exposes another model family.

## Reproduce the synthetic example

Run these commands from the package root:

```sh
python -m fstack_tools check-data examples/daily_research/us.csv examples/daily_research/us.metadata.json
python -m fstack_tools check-data examples/daily_research/hk.csv examples/daily_research/hk.metadata.json
python -m fstack_tools verify examples/daily_research/manifest.json examples/daily_research/.fstack/receipt.json --verifier reviewer
python -m fstack_tools check-receipt examples/daily_research/.fstack/receipt.json
```

The sample prices, symbols, sessions and strategy are fictional fixtures. They demonstrate data handling and reproducibility. They are not a live data feed or a performance claim.

Verification executes the manifest's explicit commands, so inspect a manifest before running one from another source. A receipt records checks actually run and fingerprints the manifest, declared inputs and outputs. Existing outputs cannot serve as fresh evidence, and the receipt is immutable. For another run, use a fresh research directory with new output paths. A material input change makes the old receipt stale. A verifier name is an operator assertion, not authenticated proof of identity or independence.

## Read the three conclusions separately

| Conclusion | What it establishes |
| --- | --- |
| Integrity | Whether the specified data and calculation checks ran and passed. |
| Thesis support | Whether available evidence supports, contradicts, mixes, or leaves the economic thesis unknown. |
| Performance evidence | Whether results come from development data, untouched evaluation data, or prospective simulation, with their limitations. |

An integrity pass does not establish a durable trading edge. A model's agreement is not an independent data source. Historical model knowledge can contaminate reconstructed forecasts. Original assumptions and rejected experiments remain in the decision trail.

Calendar inputs declare actual trading sessions and timezone-aware times. Windows installs `tzdata` through the package dependency. Corporate actions and costs must be explicit. Missing calendar, source or adjustment semantics remain a failure or an inconclusive result rather than guessed data. Research and simulation do not authorize broker orders or transfers.

## Checks and private inputs

```sh
python scripts/check_package.py
python -m unittest discover -s tests -v
python scripts/check_secrets.py --staged
python scripts/check_secrets.py --history
```

Install the official Gitleaks binary and make it available on `PATH`, or set `GITLEAKS_BIN` to its absolute path. Secret-check output is redacted. The CI checks package structure, tests and secrets. A passing package check validates references and declared upstream coverage; it is separate from behavioral evaluation and investment evidence.

Keep real keys, portfolios, raw imports and research runs in ignored local locations. Use `.env.example` only for empty or clearly fake placeholders. Gitignore rules do not remove secrets already committed to history. The project publishes code, documentation and synthetic fixtures, not private research records.

## Provenance

The pinned upstream is pstack v0.15.36 at commit `c742dd61706fbacc1b95f1a20b7b988cf096ce6c`. The lock inventories all 573 upstream files. The adaptation map accounts for all 58 top-level skills, 24 principles and 23 playbooks. Development-only and omitted components have explicit reasons. Fstack is an independent adaptation, not an official pstack or OpenAI product. Original pstack copyright and MIT permission notices are retained in the distribution.
