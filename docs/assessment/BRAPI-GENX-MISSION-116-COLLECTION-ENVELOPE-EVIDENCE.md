# Mission 116 — Verify collection envelopes contain created resources

**Date:** 2026-11-25. **Source parent:** Mission 115 review commit `fee6c9782ea48505e4392908149cc600e0712805`. **Dependency:** integrate Mission 115 before retargeting to `main`.

## Confirmed false-positive risk

Registered live probe **L-25** promises paginated `result.data` arrays for jobs and models after each resource is created. Its two GET assertions previously checked only HTTP 200. A server could respond with an empty list, omit pagination or fail to return the just-created record and still satisfy the executable test.

## Bounded correction

- Require `collection_contains_created: jobs` or `models` in the existing two L-25 GET assertions, retaining `status: 200`.
- Verify a nonempty `result.data` array of records, `metadata.pagination` with integer `totalCount`, `pageSize`, `totalPages`, `currentPage`, coherent count/page relations and inclusion of the captured job identifier or model identifier/version.
- Restrict assertion selector values to the two supported collections to prevent silent typos.
- Add twelve regression tests covering the registered fixture, valid collections, unknown selector, missing data/pagination, contradictory counts, out-of-range pages, missing created records, malformed rows and bad HTTP status. Protect execution in the hosted static job.

## Falsifiers

```sh
python Scripts/test_collection_envelope_integrity.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py --server http://127.0.0.1:18080/genx/v1 --only L-25
```

The last command needs a separately started Python reference server. Require all hosted static, live, TypeScript differential/legacy fallback and specification-generation checks on the exact pull-request head before integrating; independently verify `main` after merging.

**Evidence boundary:** This checks the current project-owned in-memory reference server, not exhaustive pagination contracts, durable storage, tenant authorization, real scientific data provenance or vendor conformance. No official Breeding Application Programming Interface (BrAPI) version 2.1 sources, proposed GenX wire schemas, endpoint registry, Request for Comments (RFC) maturity or deferred geospatial decisions change.
