# Mission 186 — Expired Job result confidentiality across collection pages

**Status:** implemented; hosted verification required before merge.
**Dependency:** Mission 185, Pull Request #135.
**Scope:** L-25 live Job collection traversal and focused Python regressions.

## Confirmed false-positive

Prior to Mission 186, L-25 checked every row in the visible first
`GET /jobs` page, including withholding expired results, but did not
request any advertised later pages. An otherwise conformant-looking
first page could conceal a non-null `result` in an `EXPIRED` Job on
page 1 or beyond. Initial acceptance, polling, cancellation,
complete-collection probes and the visible first page were already
hardened by Missions 183–185.

## Bounded correction

- Preserve the original L-25 first-page binding to the newly submitted
  Job, status, identity, and idempotency key, and the existing
  first-page model checks.
- When the first Job page advertises `totalPages > 1`, request **every**
  subsequent page using the advertised `pageSize`.
- Require each requested page to return HTTP 200 and a full, correctly
  indexed slice with unchanged `totalCount`, `pageSize`, and
  `totalPages`, and reconstruct the announced Job identity count.
- Validate required Job lifecycle state, optional progress/timestamps,
  non-empty type and identity, and optional idempotency-key type on
  every later row; reject duplicated IDs across any pages or a
  repeated original submission key.
- Reject every non-null result of an `EXPIRED` Job on **any**
  later page, including `{}`, `[]`, `false`, and `0`.
  Accept result omission or explicit `null`; metadata remains visible.
- Fail closed on missing, malformed, contradictory, inaccessible or
  truncated later pages. Avoid claiming full-collection evidence when
  a tail page was not actually retrieved.

This follows the server-advertised pagination without changing the
published Job schema, expiry policy, or model collection behavior.
A concurrent change to the unversioned Job collection may cause this
strict cross-page scan to fail rather than be reported as complete
evidence; the API does not currently provide a snapshot cursor.

## Regression coverage

```sh
python Scripts/test_collection_pagination_arithmetic.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/checkGenXConformance.py
```

The new L-25 tests exercise a three-page collection with a properly
withheld expired historical Job, then mutate either tail page to
leak results, omit a page, change pagination counters or lifecycle
fields, duplicate identities, or repeat the created key.
They verify that the probe sends actual later-page GET requests.

## Out of scope

- Full model collection traversal or stronger snapshot-isolation semantics
- A new probe identifier or a new published wire contract
- Changes to official BrAPI (Breeding Application Programming Interface) 2.1
- Expiry timing, embargos, inferred visibility rules, or persisted state
