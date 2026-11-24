# Mission 007 — Cross-Module Genomic Dataset Relationship Review

**Review date:** 2026-11-24  
**Starting main commit:** `d22f80f22c81e4f0285c46c6f7fe890ac2ef0b4e`  
**Scope:** 15 inherited, registry-only operation-neighbor links: five source modules × three source operations, all targeting `genxRegisterGenomicDataset`.  
**Status:** source-contract evidence and nonterminal triage; non-normative.

## Scope and standard of evidence

All five source modules and GenomicDatasets have independent record authority. An
operation-level discovery neighbor is not, without an explicit contract, a
foreign-key relationship, dataset-derivation fact, shared identity, compatible
request/response type, or authorization grant. The reviewed links are in
`Specification/ENDPOINT-REGISTRY.json` but are not declared as equivalent
relationships in their source OpenAPI (Open Application Programming Interface)
contracts. This assessment does **not** evaluate whether those resources should
exist in an eventual accepted standard; it evaluates only these inherited links.

## Source-schema comparison and disposition

| Source module | Reviewed schema properties | Distinction from GenomicDataset | Evidence classification | Outstanding question |
|---|---|---|---|---|
| CapabilityNegotiation | `counterparty`, `negotiationType`, `lastSeen` | Protocol capability exchange is not molecular dataset registration | No demonstrated typed relationship | M007-Q1 |
| ConformanceProbe | `targetEndpoint`, `expectedResponse`, `actualResponse` | Generic test of any operation is not semantic equivalence to the tested operation | Possible operation-testing *relationship*, not dataset relationship | M007-Q2 |
| IrrigationAdvice | `cropType`, `regionOrZone`, `recommendedAmount`, `recommendedFrequency` | Agronomic advice cannot be inferred as a prepared molecular dataset | No demonstrated typed relationship | M007-Q3 |
| ArtifactCatalogue | `storageReference`, `digest`, `artefactType`, `version` | File-artifact metadata and biological dataset metadata have different ownership and identifier scope | Possible optional file-membership relationship, not proven | M007-Q4 |
| PipelineProvenance | `pipelineName`, `pipelineVersion`, free-string `inputs`/`outputs` | Pipeline-run lineage may contextualize genomic data, but there is no typed run-to-dataset reference | Possible explicit provenance relationship, not proven | M007-Q5 |

**Common target evidence:** `GenomicDataset.yaml` defines
`genomicDatasetDbId`, `datasetType`, `referenceAssembly`, pipeline metadata,
digests, `sampleCount`, `variantCount`, access policy and release status.
It lacks typed references to the five reviewed source resource identifiers.

### Five scientific questions (unratified)

- **M007-Q1 — CapabilityNegotiation:** Is there a falsifiable capability-to-operation discovery relation, or are these dataset-registration neighbors an inherited classification error?
- **M007-Q2 — ConformanceProbe:** Should testing an arbitrary operation be represented as a generic `probe-tests-operation` relationship, instead of three special links to `genxRegisterGenomicDataset`?
- **M007-Q3 — IrrigationAdvice:** Can any observed agricultural exchange justify a typed data-provenance relation to a molecular dataset? An imagined use case alone is insufficient.
- **M007-Q4 — ArtifactCatalogue:** Does an independent consumer require a typed dataset-to-artifact reference with cardinality, authority, byte-digest meaning, file lifecycle and access enforcement?
- **M007-Q5 — PipelineProvenance:** Should a prepared dataset reference an actual versioned pipeline-run record rather than merely repeating pipeline name/version? How are inputs, outputs, authorization and run provenance represented?

These are **local review questions**, not newly accepted global decision IDs.
The correct next step is evidence capture and maintainer review. No automatic
rejection of potentially legitimate artifact/provenance links is warranted.

## Scientific constraints and falsifiers

1. **Authority:** identify which service issues each source record identifier and how a target consumer resolves it; an opaque string example is insufficient.
2. **Version and provenance:** distinguish design instructions, executed processing, catalogued bytes and prepared scientific data. Preserve exact source versions and transformation evidence where applicable.
3. **Cardinality and direction:** if an artifact belongs to several datasets, or one dataset has multiple artifacts, do not silently impose one-to-one identity. A link must state directionality and cardinality explicitly.
4. **Units and quantities:** IrrigationAdvice currently illustrates `recommendedAmount: "25mm"` as one string. This is not a typed numerical quantity-and-unit contract and must not be silently conflated with molecular measurement or generic dataset fields.
5. **Security:** endpoint discovery, probes, artifact storage and processing logs can be restricted. A neighbor ID must not imply cross-resource access or automatic creation.
6. **Independent implementability:** require typed request/response examples, valid and invalid fixtures, provenance/identity edge cases, and cross-implementation interpretation before an evidence-backed mapping can be proposed.
7. **Falsification:** absence of a typed link in the *present* contracts does not prove that no future scientific relationship could exist; it only prevents declaring this registry-only mapping valid now.

## Ledger update and preservation

- Fifteen entries transitioned **`inherited-unreviewed` → `requires-decision`**, retaining the original source-target IDs, registry records and original `provenance: inherited-registry-only`.
- Each entry now includes the specific source schema, the target schema, this assessment, a module-specific rationale and an open decision question.
- Combined with the earlier ExperimentalProtocol triad: **18 requires-decision**, **135 inherited-unreviewed**, **153 total**, **0 approved or rejected by Mission 007**.
- The concentration of 120 links on one target is a structural review signal only. Following this batch, 34 source groups targeting that operation remain inherited-unreviewed (102 individual links).
- No official Breeding API (BrAPI) version 2.1 files, GenX operation identifiers, route paths, response schemas or released contracts were changed.

## Next independently verifiable slice

Enforce existence of source/target schema evidence and a tracked assessment for reviewed entries; add negative tests for missing paths and unauthorized path traversal. Continue small-batch evidence reviews before any terminal status transition. Hosted GitHub Actions checks remain blocked by the maintainer-reported monthly minutes budget until its expected 2026-12-01 reset; local tests do not substitute for independent conformance.
