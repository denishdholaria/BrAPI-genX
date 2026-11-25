# Mission 176 — Optional Job.progress schema integrity

**Status:** implementation pending hosted verification.
**Baseline:** `995e20fc407bdb628adfbee27926f236a97f0a66`.
**Scope:** existing registered job-acknowledgment and job-collection
paths, mandatory synthetic regressions and conformance documentation.

## Confirmed false-positive risk

The published `Specification/BrAPI-GenX/Core/Jobs/Schemas/Job.yaml`
defines `progress` as an **optional number** with minimum 0 and
maximum 1. Missions 172–175 enforce required Job status and identities,
but the shared checks accepted Job responses with `progress: null`,
boolean, string, negative, above one, or non-finite numbers, despite
the existing schema. Later correct job state can mask an invalid
initial acknowledgment.

## Bounded correction

- Retain the existing six-value required Job status validator.
- Add a single reusable check for Job status **and** optional progress.
  Missing progress is allowed; present progress must be a finite
  JSON-compatible number within the inclusive [0, 1] interval.
  In Python, bool must not be treated as a number for this field.
- Use the check in initial/replay/concurrent Job acknowledgments,
  warned-inference initial acknowledgment, complete Job collections,
  and every visible L-25 first-page Job.
- Extend mandatory replay, concurrent, deprecated-inference and
  first-page pagination test suites with negative cases and positive
  zero, intermediate and full progress.
- Preserve existing job identity, lifecycle status, pagination and
  negative-effect assertions. No phase/progress correlation or new
  transition rule is introduced.

## Verification

```sh
python Scripts/test_job_replay_single_stored.py
python Scripts/test_concurrent_job_stored_effect.py
python Scripts/test_deprecated_inference_completion.py
python Scripts/test_collection_pagination_arithmetic.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/checkGenXConformance.py
```

Require hosted static conformance, live-reference conformance,
independent-runtime differential and specification generation
before merging.

## Boundaries

No official BrAPI (Breeding Application Programming Interface)
version 2.1 contracts, proposed GenX wire schemas, scientific
maturity decisions, Job transition policy or embargo visibility
policy change. Validation of optional Job timestamps is a separate
subsequent audit.
