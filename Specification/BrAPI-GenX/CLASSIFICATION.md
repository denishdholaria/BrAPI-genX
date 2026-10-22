## BrAPI-Den Scientific Domain Classification

Proposes seven scientific/operational domain classes: D1 Germplasm and Biological Resources; D2 Breeding Programs and Experimental Design; D3 Genotyping and Molecular Genomics; D4 Phenotyping and Plant Observations; D5 Environment, Agroecology and Field Context; D6 Crop Production and Material Operations; D7 Scientific Analysis, Models and Derived Evidence. Separates these from cross-cutting capabilities for identity/versioning, provenance, execution/idempotency, terminology, exchange/access, artifact integrity, telemetry, conformance, and security/authority/tenancy.

Rule: every domain resource has one primary semantic owner, with secondary facets permitted. Classify by the scientific phenomenon/resource meaning—not the HTTP verb, instrument, technology, team, or UI. Telemetry must be classified by what it measures: environmental readings as D5 and plant phenotype readings as D4.

Maps current GenX objects: VariantMatrix→D3; LotLedgerEntry→D6; ModelArtifact→D7; VariableTerm→cross-cutting terminology governance; ProvenanceEnvelope→cross-cutting provenance; Job→cross-cutting execution; ServerInfoV3→cross-cutting discovery; FAIRPackage→cross-cutting exchange/access; TelemetryPoint→context-dependent D4/D5; Conformance→cross-cutting contract governance.

BrAPI V2.1 classes and contracts remain unchanged. This is a BrAPI-Den proposal, not official BrAPI community ratification. No paths, schemas or operationIds are renamed; no folders are moved solely to match taxonomy. Classification does not assert wire equivalence. In particular, D-20 remains unresolved: GenX LotLedgerEntry is not automatically equivalent to V2.1 SeedLotTransaction.

Further rationale and adoption guardrails are maintained in this classification policy in the same directory.