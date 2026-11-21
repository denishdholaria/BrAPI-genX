# RFC-131 — Irrigation Advice (O)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (O).

## 1. Problem

BrAPI v2.1 has no place to record irrigation advice. Irrigation advisories
circulate without a stated advice type, amount, frequency, or provenance, so
they cannot be used for water management decisions.

## 2. Object

`IrrigationAdvice` — one immutable irrigation advice record, with its advice
type, recommended amount/frequency, region/zone, crop type, and provenance.

## 3. Endpoints

- `GET /genx/v1/irrigation-advice` (`genxListIrrigationAdvice`)
- `POST /genx/v1/irrigation-advice` (`genxRegisterIrrigationAdvice`)
- `GET /genx/v1/irrigation-advice/{irrigationAdviceDbId}` (`genxGetIrrigationAdvice`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `irrigationAdviceDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.

## 6. Deferred questions

- D-391: Should `recommendedFrequency` be required? (Current: optional.)
- D-392: Should `adviceType` be a controlled vocabulary? (Current: free-form string.)
- D-393: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting O).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
