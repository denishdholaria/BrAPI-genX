# Mission 156 — Fail closed on unsuccessful terminal polling GET

**Status:** implemented; required hosted verification pending.
**Dependency:** Mission 155, pull request #105.
**Scope:** shared conformance-runner terminal polling and the existing
mandatory regression suite.

## Confirmed false-positive risk

The shared `wait_terminal` helper polled `GET /jobs/{jobDbId}` but
returned the received response payload unchanged for every non-200
HTTP status. An unsuccessful lookup returning a terminal-looking JSON
body could be treated by downstream assertions as successful completion
because the helper discarded the HTTP error status.

## Correction

- Raise `ValueError` immediately if a terminal GET returns a status other
  than 200. The existing live-probe exception handler reports FAIL.
- Retain the existing terminal-state polling and deadline behavior for
  successful status-200 responses.
- Extend `Scripts/test_terminal_cancel_retained_state.py` with direct
  helper tests that reject 404, 503, and 302 even when the body reports
  a completed job; retain successful 200 control.
- No assertion vocabulary, wire schema, registered probe structure or
  workflow command change.

## Verification

```sh
python Scripts/test_terminal_cancel_retained_state.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/checkGenXConformance.py
```

Require static and live-reference conformance, independent-runtime
differential and specification generation to pass before merge.

## Boundaries

This establishes a transport-integrity prerequisite for terminal polling.
It does not change retry semantics for transient server failure,
job durability, or expiry rules, and does not modify official Breeding
Application Programming Interface (BrAPI) 2.1 contracts, GenX wire
schemas, scientific maturity or embargo visibility policy.
