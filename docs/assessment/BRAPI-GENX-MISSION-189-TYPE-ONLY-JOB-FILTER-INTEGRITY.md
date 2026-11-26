# Mission 189 — Job-type-only collection integrity and expired confidentiality

**Status:** implemented; hosted verification required before integration.
**Baseline:** `3cb90ca9f7f8743efdecc56c3693b50f3d4f1ff0`.
**Dependency:** Mission 188, Pull Request #138.
**Scope:** L-25 live conformance, registered assertion/manifest integrity, and mandatory collection regression suites.

## Confirmed false-positive

The published `GET /jobs` endpoint advertises independent `jobType`
and `status` filters. Registered L-25 previously verified unfiltered
collections, `status=EXPIRED`, and combined `jobType=germplasm_search`
plus `status=EXPIRED`, but never verified a type-only collection.

A server could return an unrelated job type or an `EXPIRED` row
with an exposed `result` when only `jobType` is supplied, yet
pass all existing registered filter checks. Later pages were likewise
never inspected for the type-only route.

## Bounded correction

- Register a mandatory seventh L-25 readback:
  `/jobs?jobType=germplasm_search&page=0&pageSize=2`.
- Generalize the existing filtered-page validator to accept independently
  requested type and status while preserving the previously registered
  expired-only and combined-filter behavior.
- Permit normal mixed Job lifecycle statuses when no status filter is
  requested. Validate each returned Job's required status, optional
  progress/timestamps, nonempty identity and type, and optional key type.
- Every Job must have `jobType: germplasm_search`. Every `EXPIRED`
  row, regardless of requested filter, must omit `result` or return
  `null`; nonexpired Jobs may retain allowed results.
- Verify every advertised later page using the same type filter and
  page size. Fail closed on missing pages, truncated slices,
  inconsistent integer pagination metadata, duplicate identifiers,
  wrong types, malformed fields and expired result disclosure.
- Accept empty type-filtered lists as shape evidence, while explicitly
  noting they cannot demonstrate record presence.
- Preserve the registered manifest check against removing, disabling,
  misspelling or changing the type-only evidence.
- Extend mandatory pagination and envelope suites with mixed-state
  controls, wrong-type cases, expired leaks on first and later pages,
  valid absent/null expired results, corrupt counters and missing pages.

## Verification commands

```sh
python Scripts/test_collection_envelope_integrity.py
python Scripts/test_collection_pagination_arithmetic.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/checkGenXConformance.py
```

All required hosted static, live-reference, independent-runtime and
specification-generation workflows must succeed before merging.

## Constraints and limitations

No published Job wire schema, lifecycle semantics, authorization policy,
official BrAPI (Breeding Application Programming Interface) version 2.1
contract, or reference-server behavior is changed. Reference servers
already honor type-only filtering from Mission 187. Empty filtered
results supply shape evidence only; offset-paginated scans may
conservatively fail when the collection mutates concurrently.
