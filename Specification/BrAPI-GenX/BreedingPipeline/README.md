# BrAPI-GenX — BreedingPipeline

**Canonical design:** [RFC-154 — Breeding Pipeline](../RFC-154-BreedingPipeline.md)  
**Historical predecessor:** [RFC-014 — Breeding Pipeline (Stage Gates)](../RFC-014-Breeding-Pipeline.md)  
**Maintainer approval:** [D-BP-01 through D-BP-13](../../../docs/assessment/BRAPI-GENX-BREEDING-PIPELINE-DECISIONS-APPROVED.md)

## Resource boundary

A BreedingPipeline is a stable, goal- and target-oriented workstream associated with one authority-qualified BrAPI Program reference. Its changing configuration is represented by immutable BreedingPipelineRevision records.

BreedingScheme has a distinct logical identity and immutable version identity. In the initial API surface its version definition is embedded in the adopting PipelineRevision; separate Scheme endpoints are deferred. Scheme versions contain stage definitions, directed transitions, and design-time task definitions. They do not represent actual execution.

Actual crosses, germplasm and pedigree, trials, studies, and observations remain owned by official BrAPI resources. SelectionDecision and PopulationAdvancement remain separate GenX execution records and may reference the exact pipeline revision, scheme version, and scheme-local stage when applicable.

## Provisional operations

The existing list, register, and retrieve operations remain provisional. Before normative promotion, the contract must define:
- list behavior for logical pipelines versus revisions, including default current-only behavior and an explicit all-revisions mode;
- registration under a stable pipeline ID with a required new immutable version ID for every new revision;
- replay keyed by the immutable version ID;
- exact historical revision retrieval;
- authority-qualified BrAPI reference resolution.

No published revision may be changed in place. A substantive change requires a new version identity.

## Deliberate exclusions

This module does not introduce a pipeline-wide current stage, a generic workflow engine, standalone MarketSegment/ProductConcept/TPE APIs, or duplicate BrAPI Program, Cross, Germplasm, Pedigree, Trial, or Study resources.

All operations remain non-normative until the RFC-154 acceptance gates pass.
