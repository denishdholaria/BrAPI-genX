# Mission 124 — Ledger replay retained-state assurance

**Status:** implemented, hosted verification required.  
**Scope:** existing L-10; no new probe identifier and no scientific/wire-schema
changes. **Dependency:** Mission 123.

## Gap

L-10 already checks the replay response's seed-lot and ledger-entry
identifiers, and reads a one-record ledger collection. The recorded source
entry could nonetheless be overwritten during replay while the same identifier
and collection count were returned.

## Change

The L-10 collection GET now requires the same `ledger_original_intact: true`
postcondition added for L-11 in Mission 123. It verifies:

- HTTP 200 and exactly one stored row on a complete, correctly counted page.
- The captured seed-lot and entry identifiers.
- All fields of the original request, including the exact fixed-scale
  quantity string, idempotency key, actor, custodian, movement locations,
  and nested provenance.

The existing `same_ledger: true` response check remains mandatory. Manifest
validation rejects dropping the follow-up readback. The separate
`Scripts/test_ledger_replay_postcondition.py` suite mutates stored values
despite expected replay responses, including missing, duplicate and changed
records, pagination errors, and incorrect replay identifiers.

## Verification

```bash
python Scripts/test_ledger_replay_postcondition.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
```

All required hosted static/live/cross-runtime conformance and generation
workflows remain merge gates.

## Limits

Evidence is limited to a synthetic entry in the project's in-memory
reference server. It does not demonstrate durable append-only storage,
exactly-once transaction semantics, multi-node race safety, scientific data
authority, or third-party conformance. Official BrAPI 2.1 and proposed GenX
wire contracts are unchanged.
