# Pause safely

1. Honor the user's stop immediately and propagate it to child agents. Stop only processes owned by the run; do not kill unrelated tools.
2. Finish or roll back only the smallest already-running atomic write needed to preserve consistency. Do not start new analysis.
3. Preserve original inputs, results, rejected attempts and journal. Write a paused or cancelled checkpoint using the actual runtime command and a concrete next action.
4. Return the saved state, work still incomplete and how to resume. A checkpoint is not a completed verification.

See the [main mode](../SKILL.md) for linked peer skills and the [finance contract](../../../references/finance-contract.md) for shared artifact and authority rules.

Derived from [pstack pause-safely.md](https://github.com/cursor/plugins/blob/c742dd61706fbacc1b95f1a20b7b988cf096ce6c/pstack/skills/poteto-mode/playbooks/pause-safely.md).
