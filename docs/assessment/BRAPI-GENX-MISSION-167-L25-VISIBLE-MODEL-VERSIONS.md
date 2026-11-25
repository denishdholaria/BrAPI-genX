# Mission 167 — L-25 visible model-version identity integrity

**Status:** implementation proposed for hosted verification.
**Dependency:** Mission 166 (L-25 job page identities).
**Scope:** L-25 model first-page readback, its mandatory synthetic
regressions, and conformance documentation.

## Confirmed false-positive risk

L-25 verified that its newly submitted model version survived unchanged
and that first-page pagination arithmetic was correct. It did not
reject unrelated model records with missing, blank, or nonstring
`modelDbId` or `modelVersion`, or duplicated unrelated
`(modelDbId, modelVersion)` pairs. A corrupted collection could
therefore pass while the originally created version was correct.

## Bounded correction

- Validate the two published model-version identity fields on **every
  visible row** and reject duplicate pairs.
- Keep `modelVersion` opaque; distinct models may share version tokens,
  and one model may have multiple distinct versions.
- Continue allowing valid additional pages. L-25 tests first-page
  evidence rather than complete-collection immutability.
- Retain original model source-field and nested-provenance checks.
- Add mandatory negative and positive tests for unrelated model
  identities, duplicated pairs, and legitimate multi-page envelopes.

## Verification

```sh
python Scripts/test_collection_pagination_arithmetic.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/checkGenXConformance.py
```

Require GitHub-hosted static conformance, live-reference conformance,
independent-runtime differential and specification generation before
merging.

## Boundaries

No BrAPI (Breeding Application Programming Interface) v2.1 source
contracts, GenX schemas, model-version semantics, scientific maturity,
or unresolved embargo policies change.
