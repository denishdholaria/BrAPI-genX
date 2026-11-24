# Group PhenotypeAnnotation

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 044, not a scientifically validated annotation ontology, official BrAPI Observation, or guaranteed human review event.

The proposed immutable record requires namespaced `phenotypeAnnotationDbId`, `studyDbId`, `observationUnitDbId`, `variableDbId`, string `annotation`, and lifecycle `status`. Annotator, timestamp, notes, `supersedes`, and provenance are optional. The identifiers provide explicit study/unit/variable context in the candidate, not independently checked referential integrity.

**Boundaries:** Official Breeding Application Programming Interface (BrAPI) version 2.1 already models observation values for a unit/variable. A free-text annotation cannot establish equivalent scoring, an accepted label vocabulary (D-130), authenticated annotator authority, or resolved Observation identity. No typed link to GenX `PhenotypeCapture` exists (D-131), despite earlier proposal prose suggesting optional availability; `annotatedAt` requiredness remains D-132. Same-ID replay and conflict are unverified candidate behaviors.

**Sources:** [candidate overview](./README.md), [candidate schema](./Schemas/PhenotypeAnnotation.yaml), [registration schema](./Schemas/PhenotypeAnnotationNewRequest.yaml), [draft operation](./PhenotypeAnnotation_GET_POST.yaml), [RFC-044](../../RFCs/RFC-044-Phenotype-Annotation.md), [official Observation request](../../../BrAPI-Phenotyping/Observations/Schemas/ObservationNewRequest.yaml), and [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
