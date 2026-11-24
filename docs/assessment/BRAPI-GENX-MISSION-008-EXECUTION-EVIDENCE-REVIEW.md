# Mission 008 — Execution, Design and Scientific Data Relationship Review

**Review date:** 2026-11-24  
**Inspected `main`:** `423e7f2f0b174c8dc4d9b06d356da2697ed53944`  
**Scope:** six source–target operation groups, 18 inherited links; explicitly non-normative. This is a schema-level review, not evidence of deployment behavior or consensus acceptance.

## Why this batch matters

Not all inherited semantic neighbors are obviously unrelated. Six pairings have scientific associations or overlapping identifiers that could tempt an implementation to *treat operations as interchangeable*. Such a shortcut would conflate **design versus execution**, **source versus derived data**, **observed versus planned activity**, or **controlled terms versus data-quality assessments**. This report checks the actual source contracts and preserves the valid distinctions.

## Source-contract audit

| Source module → target module | Existing evidence | Missing contract or hazard | Question |
|---|---|---|---|
| AssayExecution → AssayDesign | Execution has `assayDbId`; design uses `assayDesignDbId` with platform and marker count | IDs are not explicitly bound; executed design revision and authority unknown; execution GET/LIST/POST ≠ design POST | M008-Q1 |
| VcfExport → VcfImport | Export `format`; import `sourceFile`, `sourceFormat`, `importedAt`, `genomicDatasetDbId` | Export and import are different events; no shared immutable artifact ID or digest in the inspected source | M008-Q2 |
| FieldBook → FieldScouting | Both expose opaque `fieldDbId`; field book stores definition, scouting stores observations/notes | No typed field-book/version reference in scouting, and common field ID does not imply execution of that protocol | M008-Q3 |
| YieldMap → HarvestRecords | YieldMap **already contains optional `harvestRecordDbId`** describing derivation; HarvestRecord has harvest time/quantity/units/area | Real source reference exists, but lacks explicit authoritative server/immutable revision and spatial-temporal/quantity reconciliation; map GET/LIST/POST ≠ harvest POST | M008-Q4 |
| QualityFlag → VariableTerms | Flag stores `flag`; versioned VariableTerm stores trait/method/scale references | Quality label ≠ ontology/variable publication, no typed observed-value linkage | M008-Q5 |
| ReferenceAssembly → GenomicDatasets | Assembly has accession/version/organism; dataset has required text `referenceAssembly` | Candidate scientific reference, but text alone cannot ensure identity, authority or exact immutable revision | M008-Q6 |

Each group includes **three inherited operation-level neighbors** (source get/list/register or record → target write). The same endpoint triple does not imply an actual scientific relationship of any kind.

## Traceable source evidence

- AssayExecution: `Specification/BrAPI-GenX/Genotyping/AssayExecution/Schemas/AssayExecution.yaml`
- AssayDesign: `Specification/BrAPI-GenX/Genotyping/AssayDesign/Schemas/AssayDesign.yaml`
- VcfExport: `Specification/BrAPI-GenX/Genotyping/VcfExport/Schemas/VcfExport.yaml`
- VcfImport: `Specification/BrAPI-GenX/Genotyping/VcfImport/Schemas/VcfImport.yaml`
- FieldBook: `Specification/BrAPI-GenX/Breeding/FieldBook/Schemas/FieldBook.yaml`
- FieldScouting: `Specification/BrAPI-GenX/PlantHealth/FieldScouting/Schemas/FieldScouting.yaml`
- YieldMap: `Specification/BrAPI-GenX/Geospatial/YieldMap/Schemas/YieldMap.yaml`
- HarvestRecords: `Specification/BrAPI-GenX/CropProduction/HarvestRecords/Schemas/HarvestRecord.yaml`
- QualityFlag: `Specification/BrAPI-GenX/Phenotyping/QualityFlag/Schemas/QualityFlag.yaml`
- VariableTerms: `Specification/BrAPI-GenX/ReferenceData/VariableTerms/Schemas/VariableTerm.yaml`
- ReferenceAssembly: `Specification/BrAPI-GenX/Genotyping/ReferenceAssembly/Schemas/ReferenceAssembly.yaml`
- GenomicDatasets: `Specification/BrAPI-GenX/Genotyping/GenomicDatasets/Schemas/GenomicDataset.yaml`

## Questions for future policy decisions — not ratifications

**M008-Q1** — Does `AssayExecution.assayDbId` identify a particular authority-qualified, versioned `AssayDesign.assayDesignDbId`? What are the execution-to-design cardinality and version rules?

**M008-Q2** — Should VCF import/export exchange use an immutable artifact identity and content digest with explicit producer/receiver, transport access, provenance, checksum mismatch handling and replay semantics?

**M008-Q3** — Is a `FieldBook` definition used as an input protocol for `FieldScouting` records, or do they merely share a field/study context? What exact version and observation evidence must be preserved?

**M008-Q4** — What precisely does **the existing** optional `YieldMap.harvestRecordDbId` mean, including source authority, exact source revision, multi-source derivations, harvest amount/unit versus spatial map values and access permissions? Do not erase the already specified field.

**M008-Q5** — Should quality flags attach to specific observations and immutable variable term versions, or does a governed quality-flag vocabulary suffice? Avoid confusing quality assessments with term publication.

**M008-Q6** — Should a genomic dataset reference an immutable reference-assembly record rather than relying only on free-form assembly text, and how can existing field values continue to interoperate?

## Quality gates before any actual mapping

1. Demonstrate a real scientific exchange with source/target ownership, versioned identities, direction and cardinality.
2. Name the authoritative server for each existing reference, including links to official BrAPI (Breeding API) operations where they own the data.
3. Distinguish design definitions from actual execution, immutable source data from derivations, and narrative labels from controlled vocabularies.
4. Include units, timestamps, spatial support and quality/uncertainty wherever interpretation depends on them.
5. Define authorization, provenance, denial behavior and independent interpretations; add both valid and negative fixture scenarios.
6. Reject inference that GET or LIST of the source is equivalent to POST to the target, absent an explicit and falsifiable operation-level discovery contract.

## Changes and evidence boundary

This review transitions **18 original ledger entries** from `inherited-unreviewed` to `requires-decision` with their specific source schema, target schema, rationale and open question. It does not remove registry references or make a terminal rejection. All 153 stable ledger IDs are retained; the resulting status totals are **36 requires-decision**, **117 inherited-unreviewed**.

The source analysis is based on the checked-in GenX schemas. Upstream acceptance, second implementations, deployment conformance and future scientific use cases were *not* established here. The separate semantic-neighbor issue and decision register retain scientific-policy authority.
