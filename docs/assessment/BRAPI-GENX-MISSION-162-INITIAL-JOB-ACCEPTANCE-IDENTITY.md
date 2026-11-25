# Mission 162 — Bind initial job acceptance to submitted job identity

**Status:** implemented; hosted verification required.
**Baseline:** `main` at `c2033b0b5a476bfc17ae5cc2ccbd0c6626188a86`.
**Scope:** the existing shared `capture_job` path in the live conformance
runner, mandatory synthetic consumers and conformance documentation.

## Confirmed false-positive risk

The shared `capture_job` code only checked for a 200 or 202 response
and extracted `result.jobDbId`. An initial response with the right
identifier but a changed or absent `jobType` or `idempotencyKey`
could pass if the later replay, terminal GET or collection readback
returned the expected original state. A malformed result body also
risked an attribute exception instead of an explicit fail-closed check.

The existing proposed Job schema requires the job type and declares
that a supplied idempotency key is echoed. Both fields are present
in the reference server's accepted job response.

## Bounded correction

- For every `capture_job` step, verify accepted status 200 or 202,
  object-shaped response result, a nonempty string `jobDbId`,
  the exact original submitted `jobType`, and echoed
  `idempotencyKey` before recording the identifier.
- Preserve existing downstream polling, stored collection, conflict,
  replay, inference and provenance checks; do not require that
  analytical result data echo the initial job parameters.
- Permit additional server-managed fields and leave the existing
  status allowance unchanged; this is not a new normative wire rule.
- Correct the existing synthetic fixtures in the terminal cancellation,
  provenance, inference and paginated collection suites to provide
  schema-consistent accepted Job acknowledgments.
- Extend the already-mandatory
  `Scripts/test_job_replay_single_stored.py` synthetic suite with
  negative mutations for changed/missing type, key and identifier,
  malformed result bodies and failed status, plus a positive
  extra-server-metadata case.

## Verification

```sh
python Scripts/test_job_replay_single_stored.py
python Scripts/test_terminal_cancel_retained_state.py
python Scripts/test_provenance_roundtrip_integrity.py
python Scripts/test_inference_result_identity_digest.py
python Scripts/test_collection_envelope_integrity.py
python Scripts/test_collection_pagination_arithmetic.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/checkGenXConformance.py
```

Require successful hosted static, live-reference and independent runtime
conformance plus specification generation before merging.

## Boundaries

This improves the reference live conformance tests, not job durability
or the semantics of output derivation. It does not change official BrAPI
(Breeding Application Programming Interface) version 2.1 contracts,
GenX wire schemas, scientific maturity or unresolved embargo policy.
