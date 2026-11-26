# Mission 179 — Terminal polling Job wire integrity

**Status:** implemented; hosted verification required before merge.
**Baseline:** `9a2190acad97c97bbf6ef183fe35317a8472c64b`.
**Scope:** shared `wait_terminal` helper, existing mandatory
terminal-cancellation regression suite, registered L-03 expectation and
conformance guidance. The helper is also called by L-27 warned inference.

## Confirmed false-positive risk

After Missions 172–178, initial, replay, concurrent, collection and
expired-record Job responses are schema-checked, but the shared
`wait_terminal` function only required HTTP 200 and a matching
`jobDbId`. An intermediate Job could report an unknown status
(or malformed optional progress), then be overwritten by a valid
terminal result and pass the probe. A direct completed response
could omit required `jobType` or report malformed optional fields.

## Bounded correction

- Preserve the existing HTTP 200 and exact requested Job identity checks.
- On **every successful GET**, require nonempty string `jobType`,
  existing required lifecycle enum, valid optional bounded progress,
  valid optional timezone-bearing timestamps and a string-valued
  optional idempotency key.
- Fail immediately on any invalid intermediate or terminal response.
- Preserve valid multi-poll progressions including `RUNNING` to
  `COMPLETED`; introduce no new transition order, monotonic-progress
  policy, or additional required wire fields.
- Extend the existing mandatory terminal-cancel synthetic suite with
  missing/invalid type and status, optional-field mutation tests,
  early-rejection before another request, and multi-poll positive controls.
- Keep terminal-cancel result-retention evidence untouched.

## Verification

```sh
python Scripts/test_terminal_cancel_retained_state.py
python Scripts/test_deprecated_inference_completion.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/checkGenXConformance.py
```

Require hosted static conformance, live-reference conformance,
independent-runtime differential and specification-generation success
before merge. Inspect post-merge main workflows separately.

## Out of scope

Original submitted jobType/key **binding** during polling is a
distinct deeper assertion; this mission only enforces the published
Job field schema and requested identity. No official BrAPI (Breeding
Application Programming Interface) version 2.1 contract, proposed
GenX wire schema, scientific maturity, embargo visibility, or Job
state-transition policy changes.
