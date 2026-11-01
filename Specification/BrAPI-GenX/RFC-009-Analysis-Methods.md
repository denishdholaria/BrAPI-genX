# RFC-009 — Analysis Method Registry

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-004 (Model Registry), `CLASSIFICATION.md` (D7).

## 1. Problem

BrAPI v2.1 standardizes breeding data resources but not the analytical methods
applied to them. GenX already registers model artifacts (`Models`) and executes
work (`Jobs`), but there is no record for the method/algorithm, its version,
input/output contracts, and implementation reference. Without this, scientific
results cannot cite the exact method and version used, and methods cannot be
deprecated or revoked independently of models.

## 2. Object

`AnalysisMethod` — one immutable version of a registered analysis method.

## 3. Endpoints

- `GET /genx/v1/analysis-methods` (`genxListAnalysisMethods`)
- `POST /genx/v1/analysis-methods` (`genxRegisterAnalysisMethod`)
- `GET /genx/v1/analysis-methods/{analysisMethodDbId}` (`genxGetAnalysisMethod`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Analysis methods reference input/output contracts by reference; they do not
  duplicate data resources.

## 5. Invariants

- A published `(analysisMethodDbId, methodVersion)` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- `status` is one of `active`, `deprecated`, `revoked`; revoked is terminal.
- A method does not imply scientific validation, approval, or endorsement.
- Corrections are recorded as additional versions linked by `supersededBy`.

## 6. Deferred questions

- D-24: Should `methodType` be a governed enumeration or free string?
  (Current: free string.)
- D-25: Should input/output schema references be required at registration?
  (Current: optional.)
- D-26: Should a revoked method block new jobs only, or also invalidate
  prior results? (Current: blocks new jobs only.)

## 7. Classification

Primary domain: D7 — Scientific Analysis, Models and Derived Evidence.
Cross-cutting: C1, C2, C3 (POST), C6, C9.