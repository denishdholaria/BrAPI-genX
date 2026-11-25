# Mission 130 — FAIR package conflict whole-record verification

**Status:** implemented; required hosted checks pending.  
**Scope:** existing registered L-19 and supporting regression tests.  
**Dependency:** Mission 129. No official BrAPI 2.1 or GenX wire changes.

## Confirmed false-positive

L-19 rejects a conflicting package license update with HTTP 409 and rereads
the published package. Before this mission, the test compared only packageDbId
and license. A server could tamper with originally published access rights,
creators, evidence links/digests, or nested provenance while still passing.

## Change

The existing `unchanged_package_license: true` assertion now compares every
originally submitted field with the readback record, reusing the
`published_record_problem` runner-local helper introduced in Mission 129.
The helper validates HTTP status, original identity, complete stored mapping,
and original field equality, allowing additional server-managed fields.

Manifest validation requires the L-19 publish → rejected conflicting POST
→ original GET sequence. Dedicated
`Scripts/test_package_conflict_whole_record.py` regressions include
positive preservation and failures for changed license, access rights,
identifiers, title, evidence digests, provenance, missing fields, malformed
responses and incorrect conflict status. Existing publication-conflict
regressions remain active.

## Verification

```bash
python Scripts/test_package_conflict_whole_record.py
python Scripts/test_publication_conflict_postconditions.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
```

Required full hosted static/live conformance, independent cross-runtime
checks and specification generation remain merge gates.

## Limits

This is synthetic, observable reference-server retained-state evidence, not
cryptographic verification of external source content, scientific authority,
durable database storage, distributed transactions, authorization or
third-party interoperability. No specification or maturity promotion is made.
