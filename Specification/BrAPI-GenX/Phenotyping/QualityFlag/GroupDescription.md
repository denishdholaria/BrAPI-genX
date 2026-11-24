# Group QualityFlag

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 111. This record proposal is not an official Breeding Application Programming Interface (BrAPI) version 2.1 Observation contract or verified measurement-quality workflow.

Proposed operations register, list by lifecycle status, and retrieve immutable namespaced metadata. Same-body replay and changed-body conflict remain candidate behavior without independent persistent-service evidence. The candidate requires a namespaced `qualityFlagDbId` and `status`, while `flag`, `supersedes` and provenance are optional. There is no typed BrAPI Observation or GenX PhenotypeCapture reference, no standardized flag vocabulary, and no rule establishing whether a value is valid, suspect, corrected or omitted. D-331–D-333 remain open.

**Boundaries:** BrAPI version 2.1 Observations already carry reported value, timestamp, variable, observation-unit, study and collector context. The draft metadata must not be assumed to mutate these official observations, authenticate collectors, validate a sensor reading, infer scientific missingness, or perform a correction. Advisory neighbor links establish no typed relationship. Further policy and scientific semantics require explicit decisions.

**Sources:** [candidate overview](./README.md), [candidate schema](./Schemas/QualityFlag.yaml), [registration request](./Schemas/QualityFlagNewRequest.yaml), [draft operations](./QualityFlag_GET_POST.yaml), [RFC-111](../../RFCs/RFC-111-Quality-Flag.md), [official BrAPI Observation request](../../../BrAPI-Phenotyping/Observations/Schemas/ObservationNewRequest.yaml), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
