# BrAPI-GenX Semantic-Neighbor Governance

Status: proposed, non-normative. BrAPI v2.1 contracts remain unchanged.

## Purpose

This document governs the review inventory for operation-level semantic-neighbor
references that exist in `Specification/ENDPOINT-REGISTRY.json` but are absent
from the corresponding source OpenAPI `x-brapi-genx.semanticNeighbors`. These
are reported as `registryOnlyNeighbors` by
`Scripts/auditEndpointRegistrySourceConsistency.py`.

The drift-regression gate (`Scripts/check_registry_drift_regression.py`) already
prevents *new* unreviewed registry-only references. This governance framework
makes the *existing* 153 references individually traceable, reviewable, and
classified by evidence and scientific meaning. It does not declare them
scientifically valid.

## Ledger location

- `Specification/BrAPI-GenX/Conformance/semantic-neighbor-review.yaml`

## Ownership

- Specification engineering: ledger schema, validator, and deterministic
  inventory generation.
- Principal Architect: scope, review, and evidence sufficiency.
- Maintainer: final authority for scientific policy, normative specifications,
  and compatibility decisions.
- Domain/scientific reviewers: module-specific semantic assessment.

## Identity

Each ledger entry has a stable source-target identity:

`"<sourceCatalogId> -> <targetOperationId>"`

This identity is derived from the registry and must not be silently changed.
Entries are never deleted merely because their scientific rationale is
incomplete; they transition to `rejected` or `superseded` only when
independently authorized.

## Allowed statuses

1. `inherited-unreviewed`: inherited registry-only reference awaiting semantic
   review. Not approved, not rejected.
2. `evidence-backed-proposed`: a safe mapping or relationship is proposed with
   traceable evidence. Still requires maintainer/architect review before
   acceptance.
3. `requires-decision`: requires an explicit architectural or scientific
   decision before progress.
4. `rejected`: independently authorized rejection. Requires rationale.
5. `superseded`: superseded by another governed relationship or decision.
   Requires rationale and successor reference.

## Allowed transitions

- `inherited-unreviewed` -> `evidence-backed-proposed`, `requires-decision`,
  `rejected`, `superseded`
- `evidence-backed-proposed` -> `requires-decision`, `rejected`, `superseded`
- `requires-decision` -> `evidence-backed-proposed`, `rejected`, `superseded`
- `rejected` -> `superseded`
- `superseded` -> (none)

## Decision authority

Scientific equivalence, units, identity, versioning, data ownership,
provenance, lifecycle, and authorization decisions follow
`docs/governance/BRAPI-GENX-PROJECT-DECISION-AUTHORITY.md` and the decision
log `Specification/BrAPI-GenX/DECISIONS.md`. Deferred decisions (including D-04
and D-20) are preserved and are not ratified by this framework.

## Validation

- `Scripts/check_semantic_neighbor_governance.py`
- `Scripts/test_semantic_neighbor_governance.py`

The validator ensures every current registry-only relationship is accounted
for, references resolve, duplicates and invalid statuses fail, evidence-backed
claims carry required evidence, and grandfathered entries remain explicitly
unresolved rather than approved.

## Non-goals

This framework does not modify official BrAPI v2.1 specifications, GenX routes,
operation identifiers, or resource schemas; does not delete the 153
relationships; and does not declare scientific equivalence.
