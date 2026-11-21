# RFC-116 — Pipeline Provenance (Genotyping)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-013 (Genomic Datasets), `../CLASSIFICATION.md` (D3).

## 1. Problem

BrAPI v2.1 has no place to record reference genome assemblies. Reference
assemblies are the routine reference for genotyping and variant calling.
Without a record, assemblies arrive as unversioned files with no stated
accession or provenance, so they cannot be audited or reproduced.

## 2. Object

`PipelineProvenance` — one immutable pipeline provenance record, with its
accession, version, and provenance.

## 3. Endpoints

- `GET /genx/v1/pipeline-provenances` (`genxListPipelineProvenances`)
- `POST /genx/v1/pipeline-provenances` (`genxRegisterPipelineProvenance`)
- `GET /genx/v1/pipeline-provenances/{pipelineProvenanceDbId}` (`genxGetPipelineProvenance`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Reference assembly records reference GenX `GenomicDataset` by identifier; they
  do not duplicate those resources.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `pipelineProvenanceDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- A record does not imply that the assembly is validated or endorsed.

## 6. Deferred questions

- D-346: Should `parameters` be required? (Current: optional.)
- D-347: Should `pipelineVersion` be a controlled vocabulary? (Current:
  free-form string.)
- D-348: Should records link to GenX `GenomicDataset`? (Current: no link.)

## 7. Classification

Primary domain: D3 — Genotyping and Molecular Genomics.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
