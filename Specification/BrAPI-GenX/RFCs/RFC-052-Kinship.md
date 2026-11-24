# RFC-052 — Kinship (Scientific Compute)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-009 (Analysis Methods), `../CLASSIFICATION.md` (D7).

## 1. Problem

GenX proposes a separately identified kinship-matrix metadata record alongside
official BrAPI version 2.1 resources. Scientifically useful kinship estimates
require a defined population, sample ordering, estimator, matrix semantics,
storage integrity and method/version evidence. The present candidate does not
require those inputs; registration cannot by itself establish a reproducible
or scientifically comparable matrix.

## 2. Object

`KinshipMatrix` — one immutable kinship matrix record.

## 3. Endpoints

- `GET /genx/v1/kinship-matrices` (`genxListKinshipMatrices`)
- `POST /genx/v1/kinship-matrices` (`genxRegisterKinshipMatrix`)
- `GET /genx/v1/kinship-matrices/{kinshipMatrixDbId}` (`genxGetKinshipMatrix`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- `analysisMethodDbId` is a required string, not an enforced exact
  `methodVersion` join or independently verified method execution.
- A matrix is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `kinshipMatrixDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional matrices linked by `supersedes`.
- `analysisMethodDbId` is required but `matrixRef`, `matrixDigest`,
  `jobDbId`, `studyDbId` and provenance are optional.
- Neither matrix dimensions nor ordering, population composition, storage
  reachability or digest verification are required.
- A matrix record does not imply validated kinship, equivalence to a
  GenomicRelationship record, scientific approval or reproducible computation.

## 6. Deferred questions

- D-154: Should `matrixRef` be required? (Current: optional.)
- D-155: Should kinship matrices link to GenX `GenomicDataset`? (Current:
  no `genomicDatasetDbId` field is modelled.)
- D-156: Should matrix digest be required? (Current: optional.)

## 7. Classification

Primary domain: D7 — Scientific Analysis, Models and Derived Evidence.
Cross-cutting: C1, C2, C3 (POST), C5, C6, C9.