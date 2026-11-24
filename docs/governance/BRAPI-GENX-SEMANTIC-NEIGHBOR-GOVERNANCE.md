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

## First priority triage — 2026-11-23

Three cross-domain ExperimentalProtocol operation neighbors to
`genxRegisterGenomicDataset` advanced to `requires-decision`, based
on documented source-schema absence of a typed linkage. All original 153
relationships remain inventoried; 150 retain `inherited-unreviewed`.
No terminal rejection or scientific mapping has been approved. See
`docs/assessment/BRAPI-GENX-EXPERIMENTAL-PROTOCOL-GENOMIC-DATASET-REVIEW.md`.

## Reviewed-entry evidence integrity

`Scripts/check_semantic_neighbor_evidence.py` validates repository-local
documentary paths for entries at `requires-decision` or
`evidence-backed-proposed`. Each must cite an existing source-module schema,
an existing target-module schema, and a recorded assessment document; an
unresolved decision also needs a rationale and question. This is deliberately
stricter than the historic `inherited-unreviewed` population and complements,
not replaces, the canonical ledger status-transition validator. A file's
existence is **not** proof of scientific correctness or acceptance.

`Scripts/test_semantic_neighbor_evidence.py` exercises positive fixtures and
mutations for missing schemas, missing assessments, invalid paths, duplicates,
and missing questions. GitHub workflow steps run after the existing PyYAML
dependency installation; monthly hosted usage budget remains unavailable
until the maintainer-reported reset.

## Mission 007 — additional five-group triage (2026-11-24)

Fifteen operation-level links from CapabilityNegotiation, ConformanceProbe,
IrrigationAdvice, ArtifactCatalogue and PipelineProvenance to
`genxRegisterGenomicDataset` moved to `requires-decision` after source-schema
review. None was approved, rejected, or deleted. The statuses now are
**18 requires-decision** and **135 inherited-unreviewed** out of **153 retained**.
The review distinguishes clearly unrelated use cases from potentially legitimate
artifact/provenance relationships without inferring operation equivalence.
See `docs/assessment/BRAPI-GENX-MISSION-007-CROSS-MODULE-RELATIONSHIP-REVIEW.md` for the module-specific evidence, alternatives,
and missing independent conformance criteria. The original grouped queue remains
a pinned historical snapshot, not a live status counter.

## Mission 008 — plausible scientific links (2026-11-24)

Six source/target groups (18 inherited links) were reviewed specifically because
they involve scientific design/execution, derived-data or controlled-term
relationships. In one case, `YieldMap` already has an optional
`harvestRecordDbId`; this must be preserved, not silently relabelled as
missing. Source schemas and unresolved questions are recorded in
`docs/assessment/BRAPI-GENX-MISSION-008-EXECUTION-EVIDENCE-REVIEW.md`. The ledger now contains **36 requires-decision** and
**117 inherited-unreviewed** entries (153 original identities retained).
No operation equivalence or normative mapping was approved.

## Mission 009 — source-field drift regression guard (2026-11-24)

`Scripts/check_scientific_contract_boundaries.py` pins the **specific field
presence, requiredness and known field absences** underlying the six
Mission 008 source-contract assessments. For example, it protects the
existing optional `YieldMap.harvestRecordDbId` from accidental removal,
preserves required `HarvestRecord.quantity` and `HarvestRecord.unit`,
and detects additions to fields previously documented as absent.
It also verifies that each reviewed three-operation group remains traceable
in the ledger and continues to cite its assessment. The dedicated
`Scripts/test_scientific_contract_boundaries.py` has 12 mutation tests.

These checks do **not** prohibit intentional schema evolution: failures
signal that an engineer must update the evidence, tests and relevant contracts
together. They are not scientific proof or normative maturity promotion.
The complete hosted suite remains pending monthly Actions minutes reset.

## Mission 012 — field-experiment relationship triage (2026-11-24)

Fifteen inherited neighbors from Farm, Plot, TrialNetwork,
TreatmentAssignment, and CaptureWorkflow have been assessed as
`requires-decision`, without deletion, endorsement, or route changes.
See `docs/assessment/BRAPI-GENX-MISSION-012-FIELD-EXPERIMENT-NEIGHBOR-REVIEW.md` for the five distinct scientific questions,
source-schema evidence and mapping falsifiers. The ledger retains all 153
original identities: 51 require decisions; 102 await review.

## Non-goals

This framework does not modify official BrAPI v2.1 specifications, GenX routes,
operation identifiers, or resource schemas; does not delete the 153
relationships; and does not declare scientific equivalence.

## Retention and baseline selection

The original 153 relationship identities are retained against the trusted
ledger-bearing baseline commit `3125fbc35dd32abbf8166b990c5597f1aea6e61f`.
The validator compares the current ledger to that baseline and fails if any
original identity is missing.

- First ledger-bearing PR: the comparison revision is the baseline commit
  itself (or absent ledger), so retention is enforced and status transitions
  are not yet constrained beyond the allowed graph.
- Subsequent revisions: the comparison revision is the base branch version of
  the ledger (for example `origin/main`), selected via `--comparison-ref`
  or `--comparison-ledger`. This enforces documented status transitions
  against the previously reviewed state.

## Canonical identity and terminal decisions

- Each entry `id` must equal `"<sourceCatalogId> -> <targetOperationId>"`.
- `evidence-backed-proposed` requires `rationale`, `evidence`,
  `reviewedBy`, and `reviewedAt`.
- `rejected` and `superseded` require `authorizationReference` (maintainer
  authority).
- `superseded` requires `supersededBy` resolving to a known ledger entry,
  governed relationship, or operation.

Allowed transitions are enforced against the trusted comparison revision.

## Comparison selection and bootstrap

The validator no longer accepts `--baseline-ref`; retention uses the embedded
original 153-ID set. Comparison selection is:

1. Explicit `--comparison-ref <git-sha>` or `--comparison-ledger <path>`:
   the comparison must load successfully; a missing, unreadable, or malformed
   comparison fails with a diagnostic.
2. No explicit comparison: use the committed `HEAD` ledger when present.
3. If `HEAD` has no ledger, bootstrap is permitted only when the base is a
   verified pre-ledger revision (an ancestor of the first ledger-bearing commit
   `3125fbc35dd32abbf8166b990c5597f1aea6e61f`). Otherwise the run fails.

Workflow selection:
- Pull requests: `github.event.pull_request.base.sha`
- Pushes: `github.event.before` (zero SHA triggers bootstrap verification)
- Manual dispatch: no comparison by default (bootstrap path, subject to
  verification).
