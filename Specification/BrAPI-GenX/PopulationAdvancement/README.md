# BrAPI-GenX — Population Advancement (Breeding)

PopulationAdvancement records an actual, immutable movement/progression event for a population or family. It is an execution record, not a definition of a permitted scheme transition.

- The event may reference the exact BreedingPipeline logical ID and revision and the exact BreedingScheme logical ID and version that governed it.
- A stage identifier is scheme-version-local. If `fromStageId` or `toStageId` is supplied, `breedingSchemeVersionDbId` is required and the stage ID must resolve within that version.
- Where both a pipeline revision and scheme version are supplied, the revision must bind that exact scheme version.
- If no registered scheme governed the activity, pipeline/scheme references may be absent; do not invent stage IDs.
- BrAPI Program and material identities remain authoritative and must be authority-qualified.

The existing list, register, and retrieve operations remain non-normative until the referenced schema and conformance gates pass.

Details: `../RFC-035-Population-Advancement.md`.
