# Mission 185 — Expired Job acknowledgment result confidentiality

**Status:** implemented; hosted verification required before merge.
**Dependency:** Mission 184, Pull Request #134.
**Scope:** existing initial, replay, concurrent and deprecated-inference
Job acknowledgments and mandatory synthetic regressions.

## Confirmed false-positive

The GenX Job contract requires an expired Job to withhold its
result. Missions 183 and 184 cover terminal polling, direct
readbacks and `GET /jobs` collection rows. A server could still
return an otherwise schema-valid `EXPIRED` Job with non-null
`result` contents on an initial POST, identical replay, an
individual concurrent submit reply, or deprecated inference
acceptance. Existing conformance checked identity, echoed
idempotency key, required lifecycle state and optional fields,
but not result confidentiality in these acknowledgment shapes.

## Bounded correction

- Reuse `expired_job_result_withheld` for any returned Job with
  `status: EXPIRED` in:
  - initial job capture;
  - identical replay capture;
  - each independent concurrent POST acknowledgment;
  - warned deprecated-inference POST acknowledgment.
- Reject any non-null expired result before subsequent readback
  or polling evidence can conceal it, including empty objects,
  arrays, false or zero values.
- Preserve valid responses with no `result` or explicit null,
  and do not change the allowed lifecycle state set, timing,
  response codes, identity or original request binding checks.
- Add negative/positive tests in the mandatory replay,
  concurrent and deprecated-inference suites.
- Update registered probe expectations and guide.

## Verification

```sh
python Scripts/test_job_replay_single_stored.py
python Scripts/test_concurrent_job_stored_effect.py
python Scripts/test_deprecated_inference_completion.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/checkGenXConformance.py
```

Require successful hosted static conformance, live-reference
conformance, independent-runtime differential and
specification-generation workflows on the exact pull-request
head before merge. Inspect post-merge main separately.

## Boundaries

No official BrAPI (Breeding Application Programming Interface)
version 2.1 contracts, proposed GenX wire schema, additional
state-transition or expiry-timing rule, scientific maturity or
embargo metadata visibility decision changes.
