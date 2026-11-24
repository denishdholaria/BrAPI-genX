# Mission 012 — Field Experiment and Capture-Workflow Semantic Review

**Date:** 2026-11-24  
**Baseline `main`:** `5a84edd83b6c4feae53ae2a04bba889aef00feef`  
**Scope:** 5 inherited source–target groups, 15 operation-neighbor entries.
**Status:** advisory source-schema review, not normative or acceptance evidence.

## Scientific distinction

A query or registration endpoint for a farm, experimental plot, trial network,
assigned treatment, or phenotyping capture workflow must not be inferred to
be equivalent to creating a crop-cycle event, a field-scouting observation,
or publishing a versioned scientific variable term. Such inference would blur
the boundaries between **place**, **planned activity**, **actual observation**,
**source provenance**, and **scientific term definitions**.

## Source evidence and open questions

| Source → target | Existing properties observed | Missing or ambiguous relationship | Review question |
|---|---|---|---|
| Farm → CropCycle | Farm: `farmDbId`, `locationDbIds`, `totalAreaHa`; CropCycle: `locationDbId`, `studyDbId`, `plantingDate`, `harvestDate` | No typed farm reference in cycle; same Location string does not establish farm membership or authority | M012-Q1 |
| Plot → FieldScouting | Plot: `plotDbId`, `fieldDbId`; FieldScouting: `fieldDbId`, `scoutingType`, `observations` | No `plotDbId` in scouting; a plot may also be represented as an official BrAPI ObservationUnit | M012-Q2 |
| TrialNetwork → FieldScouting | TrialNetwork: `trialNetworkDbId`, `name`; FieldScouting: `fieldDbId`, `observations` | No network, official Trial, or Study relationship in inspected schemas | M012-Q3 |
| TreatmentAssignment → FieldScouting | TreatmentAssignment: `fieldDbId`, `treatment`; FieldScouting: `fieldDbId`, `scoutingType`, `observations` | No treatment-assignment reference, actual-application event, exposure time/dose or attribution rule | M012-Q4 |
| CaptureWorkflow → VariableTerms | CaptureWorkflow: `workflowType`; VariableTerm: `variableDbId`, `version`, trait/method/scale references | No workflow-to-term version binding; workflow execution is not variable-term publication | M012-Q5 |

### Source-of-truth schema paths

- **Farm → CropCycle**: `Specification/BrAPI-GenX/CropProduction/Farm/Schemas/Farm.yaml` and `Specification/BrAPI-GenX/CropProduction/CropCycle/Schemas/CropCycle.yaml`.
- **Plot → FieldScouting**: `Specification/BrAPI-GenX/Breeding/Plot/Schemas/Plot.yaml` and `Specification/BrAPI-GenX/PlantHealth/FieldScouting/Schemas/FieldScouting.yaml`.
- **TrialNetwork → FieldScouting**: `Specification/BrAPI-GenX/Breeding/TrialNetwork/Schemas/TrialNetwork.yaml` and `Specification/BrAPI-GenX/PlantHealth/FieldScouting/Schemas/FieldScouting.yaml`.
- **TreatmentAssignment → FieldScouting**: `Specification/BrAPI-GenX/Breeding/TreatmentAssignment/Schemas/TreatmentAssignment.yaml` and `Specification/BrAPI-GenX/PlantHealth/FieldScouting/Schemas/FieldScouting.yaml`.
- **CaptureWorkflow → VariableTerms**: `Specification/BrAPI-GenX/Phenotyping/CaptureWorkflow/Schemas/CaptureWorkflow.yaml` and `Specification/BrAPI-GenX/ReferenceData/VariableTerms/Schemas/VariableTerm.yaml`.

## Five unresolved questions

- **M012-Q1:** Should a CropCycle resolve Farm membership through authoritative
  BrAPI Location references, or is a separate farm reference needed? Define
  location memberships, time-valid scope, and authority before proposing a link.
- **M012-Q2:** Is scouting plot-specific or field-level? Where a plot is
  an experimental unit, examine official BrAPI ObservationUnit/Study identities
  before defining an additional GenX Plot reference.
- **M012-Q3:** Should a TrialNetwork be a navigational container for official
  Trial/Study/Location records, and how would site scouting be linked without
  duplicating their authoritative scientific facts?
- **M012-Q4:** A treatment **assignment** is not necessarily an actual applied
  intervention. Require exposure/application evidence, timing, units and plot
  specificity before correlating a scouting observation to a treatment.
- **M012-Q5:** An observation-variable **definition** and a data-capture
  **workflow** have different lifecycles. If a workflow prescribes term
  versions, record stable authority-qualified version identifiers without
  creating or replacing a scientific term on execution.

## Falsifiers, implementation gates and non-goals

All five source contracts are structural GenX proposals. A real
cross-implementation exchange may justify a typed optional relationship,
but this review does **not** establish one. For a future mapping, independently
demonstrate stable identifiers and authorities; exact record/term versions;
direction and cardinality; time, spatial and quantity scope; actor and
authorization requirements; provenance; and both positive and negative tests.
Do not equate a GET/LIST/POST operation triple to any derived scientific fact.

The original 153 ledger entries remain unchanged in identity and count.
This batch advances 15 entries from `inherited-unreviewed` to
`requires-decision`, retaining `inherited-registry-only` provenance, and
adds actual source and target schemas plus a distinct open question per module.
The aggregate status after Mission 012 is **51 requires-decision** and
**102 inherited-unreviewed**, with zero approved/rejected by this mission.

No official BrAPI version 2.1 source, GenX endpoint/route/identifier,
maturity register or normative contract is modified. These are review
findings, not a production-ready mapping or decision ratification.
