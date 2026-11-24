# RFC-113 — Assay Execution (Genotyping)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-061 (Assay Design), `../CLASSIFICATION.md` (D3).

## 1. Problem

BrAPI v2.1 provides Samples, CallSets and genotype results; it does not
define this proposed standalone assay-execution register. Such a register
could describe a laboratory workflow, but its utility and cross-system
mapping require separate evidence. A stored record is not proof of a
completed assay or reproducible results.

## 2. Object

`AssayExecution` — one immutable assay execution record, with its assay design
reference and provenance.

## 3. Endpoints

- `GET /genx/v1/assay-executions` (`genxListAssayExecutions`)
- `POST /genx/v1/assay-executions` (`genxRegisterAssayExecution`)
- `GET /genx/v1/assay-executions/{assayExecutionDbId}` (`genxGetAssayExecution`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- `assayDbId` is optional in the current schema and is not named
  `assayDesignDbId`; no typed or validated mapping to GenX AssayDesign
  has been established. The record has no sample, result or dataset field.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `assayExecutionDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- A record does not imply that the execution is validated or endorsed.

## 6. Deferred questions

- D-337: Should `assayDbId` be required? (Current: optional.)
- D-338: Should records link to GenX `GenomicDataset`? (Current: no link.)
- D-339: Should records link to GenX `VendorOrder`? (Current: no link.)

## 7. Classification

Primary domain: D3 — Genotyping and Molecular Genomics.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
