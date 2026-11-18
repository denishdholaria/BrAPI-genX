# RFC-014 — Breeding Pipeline (Historical Stage-Gate Proposal)

- Status: historical predecessor; superseded for canonical design by RFC-154, pending final normative promotion.
- Superseded by: RFC-154 (canonical BreedingPipeline design).
- Related: RFC-001 (GenX skeleton), RFC-008 (Selection Decisions), and D2 (Breeding Programs and Experimental Design).

## 1. Historical purpose

RFC-014 proposed a BreedingPipeline record to describe breeding stages, entry/exit criteria, and advancement rules connecting breeding work. Its stage-gate requirements remain useful historical design evidence.

The later domain assessment established that a flat ordered stage list or one pipeline-wide stage cannot represent recurrent processes, branches, parallel generations, and overlapping cohorts. The canonical design therefore separates the durable pipeline workstream from the versioned breeding-scheme process blueprint.

## 2. Historical endpoint proposal

The original proposal described:
- GET /genx/v1/breeding-pipelines (genxListBreedingPipelines)
- POST /genx/v1/breeding-pipelines (genxRegisterBreedingPipeline)
- GET /genx/v1/breeding-pipelines/{breedingPipelineDbId} (genxGetBreedingPipeline)

These operations are retained as historical evidence, not an independent second contract.

## 3. Retained design contributions

The following ideas remain relevant under the canonical RFC-154 boundary:
- explicit stage definitions;
- entry and exit criteria as bounded design-time information;
- stage-local task and decision context;
- evidence requirements;
- no implication of regulatory release or approval.

## 4. Supersession boundary

RFC-014 does not define a separate API resource and must not be used as an alternative schema or endpoint source. The file and RFC number are preserved; no history is deleted. RFC-154 is the single canonical editorial surface for the approved pipeline/scheme model.

Normative release still requires the RFC-154 acceptance gates and generated-contract validation.
