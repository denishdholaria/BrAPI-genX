# RFC-115 — Reference Assembly (Genotyping)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-013 (Genomic Datasets), `../CLASSIFICATION.md` (D3).

## 1. Problem

BrAPI v2.1 has no place to record reference genome assemblies. Reference
assemblies are the routine reference for genotyping and variant calling.
Without a record, assemblies arrive as unversioned files with no stated
accession or provenance, so they cannot be audited or reproduced.

## 2. Object

`ReferenceAssembly` — one immutable reference assembly record, with its
accession, version, and provenance.

## 3. Endpoints

- `GET /genx/v1/reference-assemblies` (`genxListReferenceAssemblies`)
- `POST /genx/v1/reference-assemblies` (`genxRegisterReferenceAssembly`)
- `GET /genx/v1/reference-assemblies/{referenceAssemblyDbId}` (`genxGetReferenceAssembly`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Reference assembly records reference GenX `GenomicDataset` by identifier; they
  do not duplicate those resources.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `referenceAssemblyDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- A record does not imply that the assembly is validated or endorsed.

## 6. Deferred questions

- D-343: Should `assemblyAccession` be required? (Current: optional.)
- D-344: Should `assemblyAccession` be a controlled vocabulary? (Current:
  free-form string.)
- D-345: Should records link to GenX `GenomicDataset`? (Current: no link.)

## 7. Classification

Primary domain: D3 — Genotyping and Molecular Genomics.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
