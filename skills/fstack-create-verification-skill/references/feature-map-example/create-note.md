# Data and calculation journey

## Sub-features

Nonempty source data, time/identity/unit conventions, a known calculation result, and rejection of an intentionally wrong variant.

## How to get to it (user POV)

Use the project's actual dataset, metadata and manifest. The generated map records their exact paths and information cutoff.

## Driving it with the harness

Run the actual check-data and independent verify commands from the canonical package root. Record expected numeric values and compare real outputs. This example supplies no invented project commands.

## Gotchas

A check must assert meaningful values, not file existence alone. Missing data, wrong units, source cutoff leaks and unsupported price bases cannot be passes. Clean up only run-owned scratch resources; preserve evidence.
