# Mission 188 — Combined Job type/status filtering and confidentiality

**Status:** implemented; GitHub-hosted verification required before merge.
**Baseline:** `91d726a542cd0d95b220d3447c10bef50dec8fbb`.
**Dependency:** Mission 187, Pull Request #137.
**Scope:** registered L-25 Job collection conformance and mandatory mutation suites.

## Confirmed coverage gap

Mission 187 verifies that `GET /jobs?status=EXPIRED` returns only
`EXPIRED` rows and withholds their results on every advertised page.
The existing published Jobs route also permits independent `jobType`
filtering. No registered probe verifies that both conditions hold
**together**, or that later pages preserve both filters.

A server can pass the unfiltered and status-only collection probes while
ignoring the `jobType` parameter on combined requests, returning an
unrelated `EXPIRED` job type (or a leaked result) under the wrong filter.

## Bounded correction

- Register one additional mandatory L-25 GET:
  `/jobs?jobType=germplasm_search&status=EXPIRED&page=0&pageSize=2`.
- Reuse the existing status-filtered pagination validator, parameterized
  with the required Job type instead of duplicating its confidentiality
  checks.
- Require every row on the first and all advertised later pages to
  retain both `status: EXPIRED` and `jobType: germplasm_search`.
- Preserve the existing absent-or-null `result` requirement,
  optional-field validation, integer pagination arithmetic,
  cross-page unique identities, complete page slices, and fail-closed
  handling of inaccessible/malformed pages.
- Fetch later pages **with both query filters intact** and the
  advertised page size. A query that drops either filter is not
  acceptable evidence.
- Keep a legitimate empty filtered result valid; it proves query shape
  only, not that a matching expired job exists.
- Protect the new manifest assertion and request shape against
  removal, disabling, misspelling, and dropping/changing a filter.
- Extend the mandatory L-25 synthetic regression suites with wrong
  Job types, statuses, leaked expired results, incomplete pages,
  duplicates, pagination mutations, and valid withheld results.

## Verification

```sh
python Scripts/test_collection_envelope_integrity.py
python Scripts/test_collection_pagination_arithmetic.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/checkGenXConformance.py
```

All required hosted static, live reference, independent-runtime
differential and specification generation jobs must pass before merge.

## Contract and evidence boundaries

No changes to official BrAPI (Breeding Application Programming Interface)
version 2.1, the published GenX Job schema, the proposed lifecycle,
expiration timing or visibility rules. The Python and TypeScript
reference servers already apply the two filters together after Mission
187; no server implementation change is needed.

An empty result cannot prove completeness or presence of matching
records. Offset pagination is not snapshot-based; concurrent writes can
cause a fail-closed scan. L-25 does not assert a new authorization policy.
