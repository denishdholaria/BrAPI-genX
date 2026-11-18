# BrAPI-GenX — Selection Decisions (Breeding Verdicts)

SelectionDecision records an actual, immutable selection verdict and its rationale/evidence. It is not a planned selection rule or a scheme TaskDefinition.

- The decision may reference the exact BreedingPipeline logical ID and revision and the exact BreedingScheme logical ID and version that governed it.
- A stage identifier is scheme-version-local. If `stageId` is supplied, `breedingSchemeVersionDbId` is required.
- Where both a pipeline revision and scheme version are supplied, the revision must bind that exact scheme version.
- BrAPI Program, Study, Germplasm and Observation resources remain authoritative; references must preserve their owning BrAPI server context.

The existing list, record, and retrieve operations remain non-normative until the referenced schema and conformance gates pass.

Details: `../RFC-008-Selection-Decisions.md`.
