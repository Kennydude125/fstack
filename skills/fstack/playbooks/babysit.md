# Babysit research

1. Declare whether this request is a one-time status check or authorized ongoing monitoring. Identify the existing run, exact manifest, completion predicate and deadline before polling.
2. Read current checkpoints, terminal worker reports, outputs and receipts. Validate identity and freshness; finished processes alone do not establish correctness.
3. Triage blockers as fix within existing scope, unsupported external dependency, or material user decision. Retry a failed worker at most once with consolidated scope; record persistent gaps.
4. Produce a current review-ready research package or an honest blocked/inconclusive result. Do not start unrelated work or convert monitoring into trading.
5. For an explicitly requested schedule use the host automation tools and preserve meaningful-change-only notifications unless periodic updates were requested. No automatic schedule follows from this playbook alone.

See the [main mode](../SKILL.md) for linked peer skills and the [finance contract](../../../references/finance-contract.md) for shared artifact and authority rules.

Derived from [pstack babysit.md](https://github.com/cursor/plugins/blob/c742dd61706fbacc1b95f1a20b7b988cf096ce6c/pstack/skills/poteto-mode/playbooks/babysit.md).
