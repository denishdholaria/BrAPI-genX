# BrAPI-GenX — Consistency Register

**Date:** 2026-11-03
**Baseline commit:** `6c09dff4c8f68fc89df541fc1fdcb09abc95e30c`
**Branch:** `assessment/phase-0-consolidation`

Each issue has a stable identifier `CON-NNN`. Severity uses the Phase 0 priority
model (P0 critical, P1 high, P2 medium, P3 low). Historical information is
preserved; corrections are traceable.

| ID | Severity | Issue | Affected files | Correction | Verification |
|---|---|---|---|---|---|
| CON-001 | P0 | Documentation claimed "Official BrAPI v3" is a released community major version. | `docs/project/PROJECT_IDENTITY.md`, `README.md` | Reworded to state v2.1 is latest stable release; "BrAPI v3" is not released. | Manual review |
| CON-002 | P0 | OpenAPI metadata version `3.0-draft` conflated GenX with official BrAPI major version. | `Specification/BrAPI-GenX/swaggerMetaData.yaml` | Changed to `0.1-draft` (proposal series). | `grep` |
| CON-003 | P0 | OpenAPI server URL pointed at unauthorised official test server. | `Specification/BrAPI-GenX/swaggerMetaData.yaml` | Changed to local reference server with description. | Manual review |
| CON-004 | P0 | `DECISIONS.md` central register ended at D-25 while RFCs used D-001…D-462; D-460/461/462 reused between RFC-153 and RFC-155. | `Specification/BrAPI-GenX/RFC-153-*.md`, `RFC-155-*.md` | Renamed colliding RFC-local questions to `RFC-153-Q1..Q3` and `RFC-155-Q1..Q3`. Policy documented in decision governance register. | `grep` (no remaining D-460/461/462) |
| CON-005 | P1 | `Specification/BrAPI-GenX/README.md` reported 21 GenX operations vs 462 in registry. | `Specification/BrAPI-GenX/README.md` | Corrected to 462 with note. | Manual review |
| CON-006 | P1 | `Inventory/README.md` stated D1/D2/D4/D5 had no GenX specs despite newer RFCs. | `Specification/BrAPI-GenX/Inventory/README.md` | Reworded to "specs exist but maturity uneven"; added caveat. | Manual review |
| CON-007 | P1 | Conformance README/RESULTS reference S-22 guardrail not registered in `probes.yaml`. | `Specification/BrAPI-GenX/Conformance/README.md` | Added clarifying note; tracked for resolution. | Manual review |
| CON-008 | P1 | `DEVELOPMENT_WORKSHEET.md` stale (old repo name, branch, RFC range, AI-as-maintainer). | `DEVELOPMENT_WORKSHEET.md` | To be updated in Phase 0 (Deliverable 7). | Manual review |
| CON-009 | P2 | `checkNullableConsistency.py` reports 24 mismatches in V2.1 schemas (pre-existing). | BrAPI V2.1 schemas | Out of GenX scope; documented as known limitation, not fixed. | Script output |
| CON-010 | P2 | 158 resource dirs vs 157 classified (Inventory dir unclassified). | `Conformance/domain-classification.yaml` | Inventory is a generated inventory, not a spec module; documented. | Script |
| CON-011 | P2 | Historical conformance RESULTS.md records older runs; must not be read as current. | `Conformance/RESULTS.md` | Preserved as history; new baseline record to be appended. | Manual review |
| CON-012 | P3 | `CONFORMANCE` README tier table says S-01…S-21 while probe index mentions S-22. | `Conformance/README.md` | Clarified via CON-007 note. | Manual review |

## Counting-rule reconciliation

- **201 BrAPI v2.1 operations** = official released BrAPI v2.1 operations in the
  master endpoint registry (`ENDPOINT-REGISTRY.json`, `apiGeneration=brapi-v2.1`).
- **462 proposed GenX operations** = GenX operations in the same registry
  (`apiGeneration=genx-v1`).
- **249 BrAPI v2.1 routes** = legacy Bijmantra backend routes counted by the
  inventory generator (implementation evidence, different scope).
- These figures are not interchangeable; the registry is authoritative for
  specification operations.