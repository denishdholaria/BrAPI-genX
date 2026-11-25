# Mission 123 — Ledger conflict retained-state integrity

**Status:** implemented; hosted verification required.  
**Scope:** existing live L-11 and its conformance regression suite.  
**Dependency:** Mission 122; no modification to official BrAPI or proposed
GenX wire schemas.

## False-positive risk

L-11 already returned HTTP 409 for a conflicting ledger append and then
required a collection length of one. A server could overwrite the original
quantity, actor, location, or provenance while returning the expected error
and row count.

## Postcondition

After the rejected append, L-11 checks all of the following against its
original submitted entry:

- The collection response is HTTP 200 and contains one structured entry.
- Pagination reports exactly one total entry on a complete single page.
- `seedLotDbId` equals the original lot and `entryDbId` equals the
  identifier captured from the first successful append.
- All originally submitted values, including the fixed-scale quantity
  string, idempotency key, actor, movement locations, and nested provenance
  are unchanged. Optional extra server-managed attributes may be present.

The manifest validator requires the GET assertion **after** the conflict
submission and rejects removal, disabling or relocation. The
`Scripts/test_ledger_conflict_postcondition.py` suite models successful
preservation and mutations of quantities, provenance, identities, field
presence, pagination and response statuses.

## Verification commands

```bash
python Scripts/test_ledger_conflict_postcondition.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
```

All required hosted conformance and generation jobs must pass before merge.

## Boundaries

This confirms retained in-memory records in the project-owned Python
reference server for the synthetic fixture; it does not prove durable
append-only storage, transaction isolation, crash recovery, authorization,
external-vendor interoperability, or scientific traceability of the source.
The ledger's normative contract and scientific maturity are unchanged.
