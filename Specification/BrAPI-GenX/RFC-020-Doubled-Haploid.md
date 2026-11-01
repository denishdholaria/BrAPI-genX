# RFC-020 — Doubled Haploid Programs (Breeding)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (D2).

## 1. Problem

BrAPI v2.1 has no record for doubled haploid programs: haploid induction
method, donor, and counts. Without this record, DH program outcomes cannot be
audited or reproduced.

## 2. Object

`DoubledHaploidProgram` — one immutable doubled haploid program record.

## 3. Endpoints

- `GET /genx/v1/doubled-haploid-programs` (`genxListDoubledHaploidPrograms`)
- `POST /genx/v1/doubled-haploid-programs` (`genxRegisterDoubledHaploidProgram`)
- `GET /genx/v1/doubled-haploid-programs/{doubledHaploidProgramDbId}` (`genxGetDoubledHaploidProgram`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Doubled haploid programs reference BrAPI Program and Germplasm by
  identifier; they do not duplicate those resources.
- A program record is not a BrAPI Program and must not be treated as one.

## 5. Invariants

- A published `doubledHaploidProgramDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- `method`, `haploidCount`, and `doubledCount` are recorded, not inferred.
- A record does not imply an approved breeding plan or release.

## 6. Deferred questions

- D-57: Should DH programs require a BrAPI Program reference? (Current: required.)
- D-58: Should chromosome doubling method be a separate field?
  (Current: included in `method`.)
- D-59: Should counts be required for completed programs?
  (Current: optional.)

## 7. Classification

Primary domain: D2 — Breeding Programs and Experimental Design.
Cross-cutting: C1, C2, C3 (POST), C6, C9.