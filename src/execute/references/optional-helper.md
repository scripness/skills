# Optional Helper

`scripts/loop.py` is an optional local convenience wrapper for plan-driven
work. It is not workflow truth and it does not replace the `execute` or
`verify` skill contracts.

Use it only when you already have:

- one explicit `plans/*.md` path
- one explicit non-interactive external runner

The runner contract is:

```text
<runner> execute <plan-path>
<runner> verify <plan-path>
```

The helper expects that runner to:

- keep durable state in repo files plus the plan file
- persist plan-driven verification findings back into that same plan file
- map `verify` outcomes to exit codes the helper can judge:
  - `0` = pass
  - `10` = pass with risks
  - `20` = fail

When `--continue-after-fail` is used, the helper may continue after a
repairable `verify=fail` only when the updated plan is not blocked and still
shows remaining work. In that opt-in mode, the `verify <plan>` pass that runs
against a now-complete plan becomes the strict final review and succeeds only
on `verify=pass`. If the plan is already complete before the next `execute`
pass would start, the helper runs one strict completion review before exiting.

`--allow-pass-with-risks` applies only to slice-level verify passes. Strict
final review still requires `pass`. If final review finds a cross-cutting issue
that does not map cleanly to an existing milestone, `verify` should append one
new bounded follow-up milestone rather than hide the failure inside unrelated
history.

The shipped skill contracts remain the workflow source of truth. Any helper
script in this repo may only add invocation mechanics, machine-readable event
transport, exit-code mapping, or presentation on top of those contracts.

This source repo may also ship provider-specific convenience wrappers above the
generic helper, such as `scripts/providers/codex_loop.py`, plus presentation
wrappers such as `scripts/providers/codex_loop_dashboard.py`. Those wrappers
are local accelerators only and must delegate back to the generic
`scripts/loop.py` contract rather than redefining it.
