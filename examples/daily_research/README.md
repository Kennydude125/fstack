# Reproduce the synthetic daily research case

These are invented five-session US and HK equity fixtures. `SYNTH-US` and `SYNTH-HK` are not real securities. The prices, signals and results are not evidence of an investment advantage.

From the repository root, use the detected Python 3.11+ interpreter:

```sh
python -m fstack_tools check-data examples/daily_research/us.csv examples/daily_research/us.metadata.json
python -m fstack_tools check-data examples/daily_research/hk.csv examples/daily_research/hk.metadata.json
python -m fstack_tools verify examples/daily_research/manifest.json examples/daily_research/.fstack/receipt.json --verifier reviewer
python -m fstack_tools check-receipt examples/daily_research/.fstack/receipt.json
```

Windows needs the IANA timezone database, provided by the declared `tzdata` dependency. A missing timezone database produces `INCONCLUSIVE`, not a skipped successful timezone check.

The example buys at the next declared session open after the first completed daily bar, pays 10 basis points of entry cost, applies a 2-for-1 split to existing shares and credits an explicit cash dividend. It holds through the last close without a terminal sale. Fractional shares are allowed. Taxes, foreign exchange, liquidity and actual market costs are outside this fixture.

Each market starts with 10,000 units of its own currency and finishes with approximately 10,969.4227341286. The scripts assert the golden split/dividend/cost result before writing an output. Identical numeric values in different currencies do not imply equal economic value.

## Fresh outputs and independent verification

The verifier executes the manifest's explicit Python commands without a shell. Only run manifests and code you have reviewed and authorized. This is not a sandbox for untrusted programs. Commands retain the caller's filesystem permissions.

Outputs must not already exist, and receipts cannot be overwritten. For a repeat run, copy the source files into a new research directory or choose new output and receipt paths in a copied manifest. Keep each run's artifacts. Changing data, a script, configuration, output or verifier implementation invalidates the old receipt.

`--verifier` must differ from the manifest author. These identities are operator-attested. A name does not authenticate an independent person or model. The coordinator must actually assign a separate verifier and inspect the run evidence. Hashes identify artifact contents; an editable JSON receipt is not a cryptographic signature.

## Manifest contract, version 1

`manifest.json` is a complete example of the contract:

- `schema_version`, `run_id`, `author` and `as_of` identify the research snapshot. All timestamps include a UTC offset.
- `inputs` lists every data, metadata, source-code, configuration and attempt-log file that influences the result. Paths remain inside the manifest directory.
- `outputs` lists fresh result paths. Exactly one check owns each output.
- `datasets` pairs CSV files and metadata files already listed in `inputs`.
- Each `checks` entry has `name`, `argv`, `code_inputs`, `expected_outputs` and optional `timeout_seconds`, capped at 300. Version 1 supports `{python}` followed by a fingerprinted script, or explicit inline `-c` code. Module entrypoints and arbitrary external executables are unsupported. Every script entrypoint and imported local dependency must be listed in `inputs` and `code_inputs`; dependency discovery is not automatic. Inline source is fingerprinted as part of the manifest.
- `thesis_support` is `unknown`, `supported`, `contradicted` or `mixed`. The calculation verifier records this assessment; it does not establish its economic truth.
- `performance_evidence` is `none`, `development`, `untouched_evaluation` or `prospective_simulation`. Any performance classification requires an `evaluation` protocol and a nonempty attempt-log array. An attempt with `evaluation_used_for_tuning` true or unknown prevents an untouched-evaluation claim. Prospective protocols must have been frozen before their declared evaluation start.

Data metadata declares `market`, `venue`, `symbol`, `currency`, IANA `timezone`, `as_of`, `price_basis`, `price_unit`, `corporate_actions`, `cost_bps` and explicit session objects with `date`, `open_at` and `close_at`. Version 1 supports raw daily prices in `currency_per_share` units and explicit split/cash-dividend fields. Total-return-adjusted data or other units are inconclusive until an appropriate treatment is implemented. The checker validates consistency with the supplied session calendar; it does not certify the calendar's external authenticity or fill missing market history.

CSV columns are `session,symbol,currency,open,close,split_ratio,dividend,available_at`. Optional `signal_at,execute_at` must appear together and execute at the first declared session open after the signal, with the signal no earlier than the information availability. Prices and split ratios must be finite and positive; dividends finite and nonnegative. Every declared session needs one bar. Missing conventions, unknown markets and unsupported price bases cannot pass.

CLI exit codes are 0 for the declared checks passing, 1 for failed validation and 2 for an inconclusive check. Outputs report data/calculation integrity separately from thesis support and performance evidence.

## Decision journal and checkpoints

```sh
python -m fstack_tools log .fstack/journal.jsonl event.json
python -m fstack_tools checkpoint .fstack/state.json --run-id research-1 --status running --next "Check the filing"
python -m fstack_tools checkpoint .fstack/state.json --run-id research-1 --status paused --next "Await a publication"
```

Journal events require nonempty `event_id`, `run_id`, `phase`, `decision`, `reason` and `evidence` strings. Repeating identical `(run_id,event_id)` content is a no-op. Reusing that identity with different content fails. The coordinator owns the canonical journal. A lock conflict or partial JSON line stops further writes for inspection; a stale lock after a hard crash needs manual recovery after confirming no writer remains.

Checkpoints atomically record `running`, `paused`, `cancelled` or `complete`. Paused work can resume; cancelled and completed runs are terminal. The helper records state only. The coordinator must stop workers on cancellation and verify artifacts before declaring completion.
