# Mission 166 — L-25 visible job-identity integrity

**Status:** implementation proposed for hosted verification.
**Baseline:** `d6587e53cdc3443ae4b9ab26e36575b6609aa02e` (Mission 165).
**Scope:** the L-25 jobs first-page readback, its mandatory synthetic
regression suite and conformance documentation.

## Confirmed false-positive risk

L-25 checked the accepted job against its original submission and
verified pagination arithmetic. It did not reject *unrelated* first-page
job rows with duplicated or missing `jobDbId`, missing or blank
`jobType`, or nonstring optional `idempotencyKey`. Such malformed
response evidence could pass despite the created job being correct.

## Bounded correction

- Preserve first-page pagination: unlike L-01, L-15 and L-24, L-25
  does not require an exhaustive jobs collection.
- Check every visible jobs row has a unique, nonempty string
  `jobDbId`, a nonempty string `jobType`, and a string
  `idempotencyKey` if that optional field is present.
- Retain the original created-job identifier/type/key checks, model
  collection checks, and support for unrelated valid jobs.
- Add regression cases for duplicate unrelated identifiers, missing
  or blank unrelated job identities, missing or blank types, nonstring
  optional keys, legitimate unrelated rows, and a valid multi-page
  first-page response.

## Verification

```sh
python Scripts/test_collection_pagination_arithmetic.py
python Scripts/test_job_replay_single_stored.py
python Scripts/test_concurrent_job_stored_effect.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/checkGenXConformance.py
```

Require GitHub-hosted static conformance, live reference conformance,
independent-runtime differential and specification generation before
merging.

## Boundaries

No official BrAPI (Breeding Application Programming Interface) v2.1
contracts, GenX wire schemas, scientific maturity, idempotency semantics,
or unresolved embargo-visibility policies are modified.
