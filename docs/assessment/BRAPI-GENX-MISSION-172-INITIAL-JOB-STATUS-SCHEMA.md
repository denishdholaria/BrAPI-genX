# Mission 172 — Initial Job acceptance status schema integrity

**Status:** implemented; verify hosted checks before merge.
**Baseline:** `830728db34ea6b05c8bd74bc501ef3565880f2e9`.
**Scope:** the shared `capture_job` path and specialized L-27
deprecated inference initial acknowledgment, required positive
synthetic fixtures and conformance documentation.

## Confirmed gap

`Specification/BrAPI-GenX/Core/Jobs/Schemas/Job.yaml` marks
`jobDbId`, `jobType`, and `status` as required, and enumerates
six permitted Job status values. The conformance runner's initial
acceptance paths verified the submitted job type, idempotency key,
and identifier but not the presence or enum membership of
`status`. A malformed acceptance could therefore pass when later
readback was correct.

## Bounded change

- Declare `JOB_LIFECYCLE_STATES` from the existing terminal states
  plus `SUBMITTED` and `RUNNING`; add a safe shared validator
  accepting only string-typed enum values.
- Enforce that validator on shared first Job acceptance and the
  specialized L-27 warned inference acknowledgment, before replay
  or polling.
- Extend the existing mandatory L-01 and L-27 regression suites with
  missing, unsupported and nonstring status mutations, early-failure
  assertions, valid RUNNING controls, and an enum/schema parity test.
- Repair previously abbreviated positive synthetic Job acknowledgments
  so tests continue to exercise their intended scenarios.
- Do not require SUBMITTED exclusively or change protocol schemas.

## Verification

```sh
python Scripts/test_job_replay_single_stored.py
python Scripts/test_deprecated_inference_completion.py
python Scripts/test_deprecated_inference_result_binding.py
python Scripts/test_collection_pagination_arithmetic.py
python Scripts/test_collection_envelope_integrity.py
python Scripts/test_terminal_cancel_retained_state.py
python Scripts/test_inference_result_identity_digest.py
python Scripts/checkGenXConformance.py
```

Require hosted static conformance, live-reference conformance,
independent-runtime differential and specification generation
before merging. Inspect main-branch post-merge checks separately.

## Out of scope

The identical replay and eight-way concurrent acknowledgment
status checks remain separate potential follow-ups. No official
BrAPI (Breeding Application Programming Interface) version 2.1
source contract, proposed GenX wire schema, lifecycle transition
policy, scientific maturity or embargo policy changes.
