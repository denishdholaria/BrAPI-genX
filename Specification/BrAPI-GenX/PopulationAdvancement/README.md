# BrAPI-GenX — Population Advancement (Breeding)

PopulationAdvancement records an actual, immutable movement/progression event for a population or family. It is an execution record, not a definition of a permitted scheme transition.

- The event may reference the exact BreedingPipeline logical ID and revision and the exact BreedingScheme logical ID and version that governed it.
- `schemeContext` is optional. When supplied, it contains both `breedingSchemeDbId` and exact `breedingSchemeVersionDbId`. Any `fromStageId` or `toStageId` must be nested inside this context and resolve within the embedded scheme version.
- `pipelineContext` is optional and contains both the stable pipeline ID and exact immutable pipeline revision. When both contexts are supplied, that pipeline revision must embed the exact referenced scheme version.
- Either context may be omitted when no registered pipeline or scheme governed the event; a stage identifier must never be invented without its scheme context.
- BrAPI Program and material identities remain authoritative and are represented as authority-qualified references.

The existing list, register, and retrieve operations remain non-normative until the referenced schema and conformance gates pass.

Details: `../RFC-035-Population-Advancement.md`.
