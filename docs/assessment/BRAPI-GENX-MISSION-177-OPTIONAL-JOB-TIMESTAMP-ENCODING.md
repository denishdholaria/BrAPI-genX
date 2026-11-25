# Mission 177 — Optional Job timestamp encoding

**Status:** implementation in progress; hosted verification and merge pending.
**Dependency:** Mission 176, Pull Request #126.
**Scope:** Job acknowledgments and collection evidence; existing synthetic
regressions and conformance documentation.

## Confirmed false-positive risk

`Job.createdAt`, `Job.updatedAt`, and `Job.expiresAt` are optional
strings with OpenAPI `date-time` format. Previously, the live
conformance runner verified the Job lifecycle status and progress
but accepted timestamps without a timezone, invalid calendar dates,
date-only values, nulls, or arbitrary strings.

## Minimal correction

- Retain the existing lifecycle and progress checks.
- When a Job supplies a timestamp, require an ISO 8601 extended
  date-time string with a timezone, including `Z`, `+HH:MM`, and
  `-HHMM` offset forms documented by
  `Specification/GeneralInfo/Date_Time_Encoding.md`.
- Reuse the existing `parse_rfc3339` parser for calendar validity
  after verifying field syntax.
- Apply the validator to existing initial, replay and concurrent
  acceptance responses, warned inference acceptance, complete
  stored-job collections and L-25 first-page responses.
- No inferred chronology or lifecycle transition constraints.
  Timestamp fields remain optional.

## Verification gate

```sh
python Scripts/test_job_replay_single_stored.py
python Scripts/test_concurrent_job_stored_effect.py
python Scripts/test_deprecated_inference_completion.py
python Scripts/test_collection_pagination_arithmetic.py
python Scripts/checkGenXConformance.py
```

Require hosted static conformance, live-reference conformance,
independent-runtime differential and specification generation
before merge.

## Out of scope

Direct expired/terminal Job response assertions can be audited
separately. No official BrAPI (Breeding Application Programming Interface)
version 2.1 source contract, GenX wire schema, scientific maturity,
Job lifecycle policy or embargo policy changes.
