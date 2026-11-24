# RFC-046 — Genetic Gain (Scientific Compute)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (D7).

## 1. Problem

GenX proposes a separately identified genetic-gain estimate associated with
official BrAPI version 2.1 Program and Trait identifiers. Scientific
interpretation requires a known baseline, period, improvement metric, units
and estimation methodology. The current candidate does not mandate these
context fields or independently verify them, so registration does not by
itself prove auditable genetic progress.

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
- `programDbId` and `traitDbId` are mandatory plain string identifiers; the
  schema does not validate authority, existence, trait harmonization, or
  program ownership and does not duplicate the official resources.
- A record is not a BrAPI Program and must not be treated as one.

## 5. Invariants

- A published `geneticGainRecordDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- `geneticGainRecordDbId`, `programDbId`, `traitDbId`, and `gainValue`
  are required for registration.
- `unit`, `period`, `method`, and provenance remain optional. The numeric
  `gainValue` has no required unit or temporal denominator.
- A record does not imply validated improvement, a reproducible estimator,
  statistical uncertainty, scientific approval or cross-program comparability.

## 6. Deferred questions

- D-136: Should `gainValue` be required? (Current: required.)
- D-137: Should genetic gain link to GenX `AnalysisMethod`? (Current:
  no `analysisMethodDbId` reference is modelled; an optional free-text
  `method` property exists.)
- D-138: Should gain be a structured quantity? (Current: number + unit
  string.)

## 7. Classification

Primary domain: D7 — Scientific Analysis, Models and Derived Evidence.
Cross-cutting: C1, C2, C3 (POST), C6, C9.