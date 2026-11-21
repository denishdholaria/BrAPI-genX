# BrAPI-GenX — Selection Decisions (Breeding Verdicts)

SelectionDecision records an actual, immutable selection verdict and its rationale/evidence. It is not a planned selection rule or a scheme TaskDefinition.

- The decision may reference an exact BreedingPipeline revision and exact BreedingScheme version when those definitions governed the decision.
- `schemeContext` is optional and contains both `breedingSchemeDbId` and `breedingSchemeVersionDbId`. Any `stageId` must be nested inside this context and resolve within that exact scheme version.
- `pipelineContext` is optional and contains both the stable pipeline ID and exact immutable pipeline revision. When both contexts are supplied, that pipeline revision must embed the referenced scheme version.
- A decision made outside a registered pipeline or scheme may omit both contexts.
- BrAPI Program, Study, Germplasm and Observation resources remain authoritative; references preserve their owning BrAPI server context.

The list filters require authority pairs: `programDbId` with `programServer`, `studyDbId` with `studyServer`, and `candidateGermplasmDbId` with `candidateGermplasmServer`. These are the authoritative BrAPI v2.1 server base URIs that issued the identifiers.

The existing list, record, and retrieve operations remain non-normative until the referenced schema and conformance gates pass.

Details: `../../RFCs/RFC-008-Selection-Decisions.md`.
