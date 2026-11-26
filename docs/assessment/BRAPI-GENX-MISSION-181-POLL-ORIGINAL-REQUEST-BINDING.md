# Mission 181 — Polling original Job request binding integrity

**Status:** implemented; hosted checks required before merge.
**Dependency:** Mission 180, Pull Request #130.
**Scope:** shared `wait_terminal` and its two registered callers,
mandatory terminal cancellation and deprecated-inference regression
suites, registered expectations and conformance documentation.

## Confirmed false-positive risk

After Mission 179, each terminal polling GET validates the published
Job schema and exact accepted jobDbId. The shared helper still did
not bind each intermediate Job's jobType or idempotencyKey to the
original request. An intermediate RUNNING record could report a
different scientific job kind or altered original client request key
and be overwritten by a correct terminal record, producing a false
conformance pass. L-03 and L-27 already require these values in their
initial acknowledgments and terminal evidence.

## Bounded correction

- Retain the existing HTTP, requested Job ID, and Job schema checks
  on each terminal polling GET.
- Let `wait_terminal` accept optional expected jobType and
  idempotencyKey values. Both registered callers (L-03 and L-27)
  now supply the verified original submitted values.
- Fail closed if any intermediate or terminal Job reports a
  different type, missing key, or changed key.
- Keep default expectations optional for the existing lower-level
  polling unit tests, preserving compatibility and permitting
  unrelated client usages without an asserted submitted key.
- Extend the mandatory L-03 unit tests with terminal and
  intermediate mutations and a valid multi-poll positive control.
  Extend L-03/L-27 existing synthetic stubs to verify these
  expected values reach the helper.
- Do not change lifecycle state transition rules or add wire fields.

## Verification

```sh
python Scripts/test_terminal_cancel_retained_state.py
python Scripts/test_deprecated_inference_completion.py
python Scripts/test_deprecated_inference_result_binding.py
python Scripts/test_provenance_roundtrip_integrity.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/checkGenXConformance.py
```

Require hosted static, live-reference, independent-runtime
differential and specification-generation success before merge.
Observe post-merge main workflows separately.

## Boundaries

No official BrAPI (Breeding Application Programming Interface)
version 2.1 source contract, GenX wire schema, expiry timing,
scientific maturity or embargo policy changes. Only already-required
binding of submitted original type and echoed key is enforced
at every polling readback.
