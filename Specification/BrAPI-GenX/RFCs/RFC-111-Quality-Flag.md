# RFC-111 — Quality Flag (Phenotyping)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (D4).

## 1. Problem

BrAPI version 2.1 already represents individual Observations with values, variables, timestamps, units of observation and collectors. A separate quality-flag history may be useful, but the candidate is only an optional string flag and lifecycle metadata. It does not define an observation linkage, controlled quality taxonomy or validated quality assessment.

## 2. Object

`QualityFlag` — one immutable quality flag record, with its flag value and
provenance.

## 3. Endpoints

- `GET /genx/v1/quality-flags` (`genxListQualityFlags`)
- `POST /genx/v1/quality-flags` (`genxRegisterQualityFlag`)
- `GET /genx/v1/quality-flags/{qualityFlagDbId}` (`genxGetQualityFlag`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- No typed link to an official BrAPI Observation or GenX PhenotypeCapture record is present in this candidate schema; D-333 remains unresolved. Matching labels or navigation links do not create scientific identity.
- A record is not a BrAPI Observation and must not be treated as one.

## 5. Invariants

- A published `qualityFlagDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- A record does not imply that the flag is validated or endorsed.

## 6. Deferred questions

- D-331: Should `flag` be required? (Current: optional.)
- D-332: Should `flag` be a controlled vocabulary? (Current: free-form
  string.)
- D-333: Should records link to GenX `PhenotypeCapture`? (Current: no link.)

## 7. Classification

Primary domain: D4 — Phenotyping and Plant Measurements.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
