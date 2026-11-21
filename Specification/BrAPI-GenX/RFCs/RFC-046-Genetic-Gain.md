# RFC-046 — Genetic Gain (Scientific Compute)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (D7).

## 1. Problem

BrAPI v2.1 has no genetic gain record. Estimated genetic improvement for a
trait over a period is essential for breeding progress reporting. Without
this record, genetic gain cannot be audited or linked to programs with
provenance.

## 2. Object

`GeneticGainRecord` — one immutable genetic gain record.

## 3. Endpoints

- `GET /genx/v1/genetic-gains` (`genxListGeneticGains`)
- `POST /genx/v1/genetic-gains` (`genxRecordGeneticGain`)
- `GET /genx/v1/genetic-gains/{geneticGainRecordDbId}` (`genxGetGeneticGain`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Genetic gain records reference BrAPI Program and Trait by identifier; they
  do not duplicate those resources.
- A record is not a BrAPI Program and must not be treated as one.

## 5. Invariants

- A published `geneticGainRecordDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- `gainValue` and `traitDbId` are required.
- A record does not imply scientific validation or approval.

## 6. Deferred questions

- D-136: Should `gainValue` be required? (Current: required.)
- D-137: Should genetic gain link to GenX `AnalysisMethod`? (Current:
  optional, not required.)
- D-138: Should gain be a structured quantity? (Current: number + unit
  string.)

## 7. Classification

Primary domain: D7 — Scientific Analysis, Models and Derived Evidence.
Cross-cutting: C1, C2, C3 (POST), C6, C9.