# Mission 184 — Expired Job collection result confidentiality

**Status:** implemented; hosted verification required before merge.
**Dependency:** Mission 183, Pull Request #133.
**Scope:** the complete and first-page `GET /jobs` conformance
validators, existing mandatory suites and registered probe text.

## Confirmed false-positive

The Job contract defines a full Job resource in
`GET /genx/v1/jobs` collection rows. Expiry must withhold its
result, and L-05 already asserts absent/null expired output on
an individual GET. Mission 183 closes this exposure for terminal
polling and cancellation readbacks.

Before this mission, `immutable_job_snapshot` and L-25 validated
the lifecycle status, original identities, optional progress and
timestamps, but did not prevent an `EXPIRED` Job row in a
collection from containing `result` data. A server could deny
individual expired results yet disclose them through the list.

## Bounded correction

- Reuse `expired_job_result_withheld` for every row with
  `status: EXPIRED` in the shared **complete** Job collection.
  It is used by L-01, L-02, L-04, L-15 and L-24.
- Apply the same rule to **every visible** L-25 first-page Job,
  without implying that later pages were read.
- Accept absent or explicit-null expired result and preserve
  caller-visible expired metadata, valid current state and
  original job identities.
- Reject even non-null empty objects, arrays and falsy values.
- Extend mandatory L-01 replay, L-24 concurrent and L-25 first-page
  suites with expired created/unrelated leak tests and positive
  withholding controls.
- Preserve pagination and all preexisting request-binding,
  uniqueness, science and status assertions.

## Verification

```sh
python Scripts/test_job_replay_single_stored.py
python Scripts/test_concurrent_job_stored_effect.py
python Scripts/test_collection_pagination_arithmetic.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/checkGenXConformance.py
```

Require successful hosted static conformance, live-reference
conformance, independent-runtime differential and specification
generation on the exact pull-request head before merge.
Post-merge main workflows are checked separately.

## Out of scope

No official BrAPI (Breeding Application Programming Interface)
version 2.1 contract, new GenX schema, lifecycle policy, expiry
timing, embargo visibility or scientific maturity decision changes.
This makes existing confidentiality requirements consistent
across an additional endpoint shape.
