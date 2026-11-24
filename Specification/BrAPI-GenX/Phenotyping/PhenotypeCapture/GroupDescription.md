# Group PhenotypeCapture

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 012. This is neither an official Breeding Application Programming Interface (BrAPI) version 2.1 Observation nor independently validated capture/correction workflow.

The candidate requires a namespaced `phenotypeCaptureDbId`, `studyDbId`, `observationUnitDbId`, `capturedAt`, and an `entries` array. Each entry requires a string `variableDbId`, while `value` is an optional nullable *number*, and `qualityFlag`, `missingReason`, `correctedFrom` and `unit` are optional. Image references, status, revision links and provenance are optional metadata. Registration replay and conflict semantics remain candidate behavior.

**Boundaries:** Official BrAPI Observation `value` is nullable string content capable of representing more than numerical values. The proposed numeric-only capture entry does not automatically cover categorical scales. The RFC proposes a missingReason for missing-quality entries, but its schema does not conditionally require it. No independent test proves reference resolution, capture provenance, correction history, authorization or scientific validity. D-33–D-35 remain unresolved, including cardinality of entries and time-series relationships.

**Sources:** [candidate overview](./README.md), [candidate schema](./Schemas/PhenotypeCapture.yaml), [registration schema](./Schemas/PhenotypeCaptureNewRequest.yaml), [draft operation](./PhenotypeCapture_GET_POST.yaml), [RFC-012](../../RFCs/RFC-012-Phenotype-Capture.md), [official Observation request](../../../BrAPI-Phenotyping/Observations/Schemas/ObservationNewRequest.yaml), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
