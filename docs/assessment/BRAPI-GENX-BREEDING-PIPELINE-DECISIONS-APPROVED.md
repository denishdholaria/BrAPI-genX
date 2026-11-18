# BrAPI-GenX — Breeding Pipeline and Scheme Decision Ratification

**Status:** Maintainer-approved design decisions; recorded 18 November 2026.  
**Workstream:** BGX-P1-06 — Approved candidate contract baseline.  
**Scope:** D-BP-01 through D-BP-13.  
**Normative status:** These decisions authorize preparation of normative specifications; they do not themselves promote an RFC to a released normative contract.

## Approval record

The maintainer explicitly approved the recommendations in the Breeding Pipeline and Scheme Maintainer Decision Package. The approved choices are:

| Decision | Approved choice |
|---|---|
| D-BP-01 | Distinct concepts: BreedingPipeline is the workstream; BreedingScheme is the process blueprint. |
| D-BP-02 | Option C: first-class scheme logical identity and immutable version, initially embedded in PipelineRevision without separate Scheme endpoints. |
| D-BP-03 | Separate stable logical identity and immutable version identity for pipeline and scheme. |
| D-BP-04 | Scheme-local stage IDs and explicit directed transitions; no generic workflow engine. |
| D-BP-05 | Typed purpose-specific target-context collection; no independent MarketSegment, ProductConcept, or TPE endpoint in this initial design. |
| D-BP-06 | Authority-qualified typed BrAPI references containing API generation, resource type, authoritative server/authority, and dbId. |
| D-BP-07 | RFC-154 is the canonical editorial surface; RFC-014 is retained as historical predecessor, preserving its useful stage-gate concepts. |
| D-BP-08 | Defer broad ProgenyRecords; reopen only for a distinct immutable formation/family event not already owned by BrAPI Pedigree. |
| D-BP-09 | Retain CropCycle as a crop-production interval; do not use it as a breeding-cycle identity. |
| D-BP-10 | Retain and refine PopulationAdvancement as an actual material-progression event. |
| D-BP-11 | Defer broad CrossingSchedule; reopen only for scheduling/booking semantics beyond BrAPI PlannedCross and CrossingProject. |
| D-BP-12 | Defer duplicate ResearchProgram; BrAPI Program remains authoritative. |
| D-BP-13 | Retain the initial list/register/retrieve pipeline surface provisionally, make registration version-aware, and specify exact historical revision retrieval before normative promotion. |

## Authority and implementation boundary

The approval authorizes the next specification-development phase. It does not authorize:
- modifying official BrAPI v2.1 source contracts or generated official artifacts;
- treating candidate fixtures as normative production conformance;
- promoting RFC maturity before semantic, schema, fixture, interoperability, and compatibility gates pass;
- silently deleting or renumbering historical RFCs.

RFC-154 is the canonical editorial surface for the approved candidate model. RFC-014 remains preserved as historical evidence. Related RFC dispositions are recorded in RFC-154 and must be reflected consistently in future catalogue and governance materials.

All reversible contract-design work should proceed autonomously within these boundaries. Escalate only a genuinely new consequential decision not covered by D-BP-01 through D-BP-13.
