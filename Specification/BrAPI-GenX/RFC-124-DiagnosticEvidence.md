# RFC-124 — Diagnostic Evidence (N)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (N).

## 1. Problem

BrAPI v2.1 has no place to record diagnostic evidence. Diagnostic results
circulate without a stated method, result, confidence, or provenance, so they
cannot be used for IPM or disease management decisions.

## 2. Object

`DiagnosticEvidence` — one immutable diagnostic evidence record, with its
evidence type, diagnostic method, result, confidence, and provenance.

## 3. Endpoints

- `GET /genx/v1/diagnostic-evidences` (`genxListDiagnosticEvidences`)
- `POST /genx/v1/diagnostic-evidences` (`genxRegisterDiagnosticEvidence`)
- `GET /genx/v1/diagnostic-evidences/{diagnosticEvidenceDbId}` (`genxGetDiagnosticEvidence`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `diagnosticEvidenceDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.

## 6. Deferred questions

- D-370: Should `confidence` be required? (Current: optional.)
- D-371: Should `diagnosticMethod` be a controlled vocabulary? (Current: free-form string.)
- D-372: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting N).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
