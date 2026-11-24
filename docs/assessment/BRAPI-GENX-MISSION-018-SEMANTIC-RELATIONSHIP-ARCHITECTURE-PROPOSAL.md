# Mission 018 — Semantic-Relationship Architecture Decision Package

**Date:** 2026-11-24  
**Baseline `main`:** `ecbfbcb1bd9f06738e7da3a100d9ba7f43b8507b`  
**Status:** **PROPOSAL ONLY — NOT RATIFIED**, no standards or endpoint contract change.

## Problem statement: overloaded "semantic neighbor"

The endpoint registry currently contains `semanticNeighborIds`, sometimes
including operation IDs and sometimes governed labels such as `SEM-*`.
The source GenX OpenAPI documents independently declare
`x-brapi-genx.semanticNeighbors`. The governance ledger records 153
additional, registry-only operation-level references that are not declared
in the corresponding source operations. Historic "neighbor" metadata can
therefore appear in catalogue output even when it is not a verified
scientific relationship.

Current observations: 51 relationships have been triaged as
`requires-decision`; 102 remain `inherited-unreviewed`. Nothing in those
statuses constitutes scientific equivalence or normative acceptance.

**Failure mode:** a client, code generator, or an assistant could interpret
a weak registry neighbor as permission to link records, infer common identity,
deduce derivation, or invoke a write operation. Cross-module examples like
IrrigationAdvice → `genxRegisterGenomicDataset` make this especially unsafe.

## Distinct semantics that must not be conflated

| Concept | Example | Required evidence before claiming the relationship | Safe interim treatment |
|---|---|---|---|
| **Operation navigation** | `genxGetFarm` and `genxListFarms` are discoverable alongside each other | Source operation identity and intent, not resource identity | Editorial discovery hint only; no automatic write, conversion or join |
| **Typed resource reference** | The existing optional `YieldMap.harvestRecordDbId` | Owning service, authority-qualified record ID, target identity, version and direction/cardinality | Preserve the source-schema field, but do not infer missing resolution semantics |
| **Provenance / derivation** | Candidate genomic dataset outputs traced to a pipeline run | Exact input/output identities and versions, execution evidence, timestamps, role and reproducibility | Hypothesis until typed source-to-result evidence exists |
| **Operation contract equivalence** | An officially specified operation and a potential adapter operation | Matched HTTP method, path, request/response schemas, effect, retry/idempotency, errors, permissions, identity and independent conformance | Never infer equivalence from shared names or neighbor tags |
| **Governed semantic overlap** | Existing `SEM-*` and `OVERLAP-*` registry labels | An actual separately governed boundary decision and its scope | Keep distinct from operation-ID navigation |

The underlying wire contracts remain the authoritative statement of what
each operation reads, writes or returns. Registry metadata alone cannot
create a typed foreign-key, provenance fact or scientific equivalence.

## Architectural options (not approvals)

### Option A — Keep one `semanticNeighborIds` field, document it as discovery only

Smallest migration cost. Existing SDK (Software Development Kit) and
catalogue readers can keep their current format, but ambiguity remains and
every consumer must correctly interpret a weak advisory field. Typed
scientific relationships would have to be documented elsewhere, without
machine-readable linkage between the two concepts.

### Option B — Make every neighbor relationship a verified scientific relation

A seemingly simpler model, but unsafe and expensive: all historical,
source-declared, intra-module and governed links would need exact relationship
semantics, identity/cardi­nality and authority validation. It would encourage
premature elimination or semantic upgrading of useful operation-navigation
links. **Not recommended.**

### Option C — Separate navigation from typed relationships (recommended for maintainer review)

Retain existing IDs as historical provenance, but introduce **a separate
proposed metadata model** with explicit `relationKind`. Navigation remains
advisory. Scientific links, directed derivations, and operation-equivalence
mappings require differentiated validation and are not inferred from
navigation. This supports incremental migration and testable consumer
behavior; it adds small governance and reporting overhead.

**Recommendation:** select Option C after an explicit maintainer decision.
Do not change registry field semantics or published catalogues until
compatibility expectations and decision authority are confirmed.

## Illustrative shadow proposal record — not a current standard

```yaml
candidateRelationshipId: draft-0001  # placeholder, not assigned
relationKind: typed-resource-reference
source:
  module: YieldMap
  property: harvestRecordDbId
target:
  module: HarvestRecords
  identityProperty: harvestRecordDbId
direction: source-references-target
targetAuthority: requires-decision
versionBinding: requires-decision
cardinality: requires-decision
scientificEvidence: []
status: design-proposal
authorizationReference: null
```

The example intentionally leaves authority, version and cardinality
unsettled. It is **not** a new normative field, and it must not be emitted
into `Specification/ENDPOINT-REGISTRY.json` or generated wire schemas.

## Migration and conformance plan (conditional on approval)

1. **Preserve lineage.** Freeze the original 153 ledger identities; keep
   repository-baseline comparison and prevent new uncontrolled registry-only
   links. A rejected historical link remains recorded even after active
   publication ceases.
2. **Classify consumers before changing fields.** Audit endpoint catalogues,
   crosswalks, generated clients, machine-learning agent instructions, and
   any use of `semanticNeighborIds` as navigation, scientific fact or
   action permission. Record unverified consumers explicitly.
3. **Add a separate candidate proposal store first.** Define independent
   schema validation, `relationKind` enumeration, uniqueness, cross-version
   references, authority and source provenance. It must not silently rewrite
   existing operation source contracts or endpoint registry values.
4. **Require concrete scientific evidence per type.** Resource references need
   authority and cardinality; provenance requires input/output facts;
   operation-equivalence requires full identity and behavior, including
   negative and authorization scenarios.
5. **Publish only reviewed relationships.** Make it unambiguous in generated
   catalogues which items are mere related-operation navigation and which
   typed relationships have actually passed the chosen governance gate.
6. **Perform bounded, reversible migrations.** Any registry removal is atomic
   with a documented, maintainer-authorized `rejected` or `superseded`
   ledger transition. Keep original IDs and diff fixtures for independent
   review. No implicit automatic deletion of all 102 unreviewed links.
7. **Verify compatibility.** Run the full checked-out registry audit,
   canonical governance mutations, endpoint artefact regeneration
   (`Scripts/generateEndpointArtifacts.py --check`), negative source
   fixtures and at least one independent consumer interpretation.

The project's
`docs/governance/BRAPI-GENX-SPECIFICATION-QUALITY-STANDARD.md`
(especially E1, E2, E6, E7, E8 and E12) and
`docs/governance/BRAPI-GENX-PROJECT-DECISION-AUTHORITY.md` govern
evidence sufficiency and maintainer authority.

## Specific pending maintainer choices

- **SEM-D1:** Which primary interpretation of `semanticNeighborIds` is
  authoritative for catalogue consumers: editorial navigation or actual
  scientific relationships? **Prefer editorial navigation** for legacy
  metadata, with an explicit warning that it cannot grant side effects.
- **SEM-D2:** Should typed scientific relationships occupy a distinct
  machine-readable store, never be inferred from a list of operation IDs?
  **Prefer yes (Option C)**.
- **SEM-D3:** What constitutes a provably authorized terminal decision?
  The existing validator's `_is_followable_reference` only checks that a
  token is followable or shaped like a reference. It cannot prove that the
  maintainer approved a specific `sourceCatalogId → targetOperationId`
  retirement. **Prefer a repository-controlled exact decision record
  linked to the intended relationship and decision action**.
- **SEM-D4:** What is the minimal reversible compatibility migration for
  catalogue consumers? **Prefer shadow records and opt-in consumers first.**

These questions are tracked in [issue #17](https://github.com/denishdholaria/BrAPI-genX/issues/17)
and [issue #20](https://github.com/denishdholaria/BrAPI-genX/issues/20).

## Delivery boundary

This document is an **architectural decision package**, not an accepted
new BrAPI-GenX API (Application Programming Interface), data model or
normative mapping. No source operation, registry neighbor, scientific
relationship status, generated artifact or official BrAPI version 2.1
contract was modified as part of Mission 018. Its purpose is to make
the next irreversible decision explicit, evidence-backed and testable.
