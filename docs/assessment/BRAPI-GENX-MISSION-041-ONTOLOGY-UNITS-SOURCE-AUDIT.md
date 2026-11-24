# Mission 041 — Source-truth audit of ontology and quantity relationships

**Date:** 2026-11-24
**Starting `main`:** `8253388a7d682a4e2b2531d294fd9279882f2211`
**Scope:** 3 candidate group descriptions, 3 editorial RFC compatibility corrections, pinned guard and 2 regression tests.

## Discrepancy proven against existing schemas

RFC-082 (§4), RFC-085 (§4), and RFC-086 (§4) had indicated that their draft resources **reference** GenX VariableTerm/OntologyTerm by identifier. However the respective OpenAPI record and request schemas define no typed reference property to those resources, and the same proposals defer exactly such links under D-246, D-255 and D-258.

These are not settled relationships. The misleading compatibility bullets were corrected to acknowledge the missing links and open decisions; no scientific mapping was invented, accepted or rejected.

## Three source-bound descriptions

- **UnitsAndQuantity:** optional unit/quantity/definition strings are not a controlled unit system, conversion engine, or measurement validity proof. Official BrAPI Scale remains authoritative for official scale exchange.
- **OntologyTerm:** optional text/synonyms/ontology name do not imply a versioned external concept identifier, synonym equivalence or a typed VariableTerm link.
- **OntologyMapping:** optional source and target name vocabulary systems; the free-form mapping object does not imply a typed OntologyTerm relationship, exactMatch, or an executable crosswalk.

All three remain `STRUCTURAL_DRAFT` under RFC-082/085/086. The reviewed group guard rises from 17 to **20** of the unchanged 156; **136 stay deferred**. Two regression tests protect pinned identities and the still-unratified typed links.

## Verification limits

All direct description evidence links were checked against the inspected repository tree; schema presence/optionality and the conflicting old prose were reviewed. Hosted tests must run on this integrated commit before reporting full success.

**No changes to official BrAPI contracts, GenX OpenAPI schemas, operations, semantic-neighbor ledger, maturity register, route generation or scientific approval decisions.**