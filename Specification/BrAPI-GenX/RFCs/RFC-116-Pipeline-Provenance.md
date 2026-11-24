# RFC-116 — Pipeline Provenance (Genotyping)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-013 (Genomic Datasets), `../CLASSIFICATION.md` (D3).

## 1. Problem

Bioinformatics processing provenance may require pipeline versions, parameters, input/output identities, execution environment and traceable computation. This candidate records only optional pipelineName, pipelineVersion, parameters, inputs and outputs as metadata: it does not prove execution, stable software environments, reproducible results, or a valid genomic dataset linkage.

## 2. Object

`PipelineProvenance` — one candidate immutable bioinformatics pipeline metadata record with optional version, parameters, free-form inputs and outputs, and provenance. It is not a reference genome assembly.

## 3. Endpoints

- `GET /genx/v1/pipeline-provenances` (`genxListPipelineProvenances`)
- `POST /genx/v1/pipeline-provenances` (`genxRegisterPipelineProvenance`)
- `GET /genx/v1/pipeline-provenances/{pipelineProvenanceDbId}` (`genxGetPipelineProvenance`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- The candidate records optional string `inputs` and `outputs`, which have no typed GenX `GenomicDataset` references. D-348 remains open; a dataset-like string does not prove actual lineage.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `pipelineProvenanceDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- A record does not prove that the pipeline executed, produced the stated outputs, or can be reproduced.

## 6. Deferred questions

- D-346: Should `parameters` be required? (Current: optional.)
- D-347: Should `pipelineVersion` be a controlled vocabulary? (Current:
  free-form string.)
- D-348: Should records link to GenX `GenomicDataset`? (Current: no link.)

## 7. Classification

Primary domain: D3 — Genotyping and Molecular Genomics.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
