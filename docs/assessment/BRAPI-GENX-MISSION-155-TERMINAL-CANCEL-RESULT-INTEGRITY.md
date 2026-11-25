# Mission 155 — Terminal cancellation original result integrity

**Status:** implemented; required hosted checks pending.
**Baseline:** `main` at `2ade21658f2493f7c80de440bae3489de45dd289`.
**Scope:** registered L-03 terminal cancellation assertion, its mandatory
synthetic regression suite, and conformance documentation.

## Confirmed false-positive risk

L-03 captured a terminal job via the existing `wait_terminal` path, then
rejected a DELETE and re-read that job. The executable
`terminal_state_unchanged` assertion checked only the job identifier and
terminal state. A server could respond with unchanged identifiers/status
while silently changing the original `jobType`, `idempotencyKey` or
completed `result`, including nested evidence, and still pass.

## Bounded correction

- Tie both the terminal baseline and post-DELETE readback to the actual
  submitted `jobType` and `idempotencyKey`, not solely each other.
- Require the accepted terminal job identifier and terminal status to
  survive as before.
- Require presence and full nested value of any original terminal `result`
  to be unchanged, preventing dropped, added or rewritten results.
- Do not require unrelated server-managed metadata to be identical;
  polling timestamps and other non-scientific fields are outside this claim.
- Extend the already-mandatory
  `Scripts/test_terminal_cancel_retained_state.py` suite with positive
  and negative cases for changed type/key, missing fields, altered nested
  completed results, unexpected results on failed jobs, and extra benign
  server metadata.
- Keep the existing exact L-03 POST/wait, rejected DELETE and GET manifest
  guard. No new assertion vocabulary or workflow command required.

## Required verification

```sh
python Scripts/test_terminal_cancel_retained_state.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
```

Require hosted static, Python live-reference and independent-runtime
conformance, plus specification generation, to pass before merging.

## Boundary

This verifies the stable identity and terminal outcome of a rejected
cancellation. It does not prove job durability or universal immutability of
all server-managed metadata. No official Breeding Application Programming
Interface (BrAPI) version 2.1 contracts, GenX wire schema, scientific
maturity or unresolved embargo metadata-visibility policy changes.
