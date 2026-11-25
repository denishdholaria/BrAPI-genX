# Mission 139 — Complete first-page collection pagination checks

**Status:** implemented; hosted checks required before integration.  
**Scope:** existing registered L-25 and negative regression coverage.  
**Dependency:** Mission 138.  
**Wire-schema and scientific maturity changes:** none.

## Confirmed false-positive risk

The previous L-25 accepted any positive totalPages, sufficiently large
pageSize and totalCount at least as large as the number of returned records.
A server could report totalCount=100 and pageSize=100 while returning one
row, or claim two pages for a collection that fits in one, and still pass.

## Correction

For L-25's two unqualified GET collection requests, strengthen the
existing `collection_contains_created` assertion to require:

- HTTP 200, a nonempty result.data array of records, and integer pagination.
- Page size greater than zero and currentPage exactly zero, matching the
  first page requested by the registered probe.
- totalPages = ceil(totalCount/pageSize).
- Exactly min(totalCount, pageSize) rows for the first page.
- Continued presence of the freshly created jobDbId and modelDbId/version.

The registered procedure is protected against missing or swapped collection
steps. The mandatory `Scripts/test_collection_pagination_arithmetic.py`
suite tests counts, page-index, totals, sparse pages, missing fields,
malformed records and omitted created objects. Existing collection envelope
tests remain active.

## Verification

```bash
python Scripts/test_collection_pagination_arithmetic.py
python Scripts/test_collection_envelope_integrity.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
```

Required hosted static, live-reference, independent runtime and
specification-generation checks must pass before merging.

## Evidence boundary

The assertion verifies internal arithmetic of the observed first-page
response, not an independent database count or pagination across all pages.
It does not certify concurrent snapshot isolation, correctness of all
objects in a large collection, or third-party interoperability.
