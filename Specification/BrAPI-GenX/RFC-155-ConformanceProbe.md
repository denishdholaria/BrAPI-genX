# RFC-155 — Conformance Probe (T/W/A)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (T/W/A).

## 1. Problem

BrAPI-GenX has no place to record conformance probe records. Conformance probes
circulate without a stated probe type, target endpoint, or provenance, so they
cannot be used for automated conformance testing.

## 2. Object

`ConformanceProbe` — one immutable conformance probe record, with its probe type,
target endpoint, expected response, actual response, and provenance.

## 3. Endpoints

- `GET /genx/v1/conformance-probes` (`genxListConformanceProbes`)
- `POST /genx/v1/conformance-probes` (`genxRegisterConformanceProbe`)
- `GET /genx/v1/conformance-probes/{conformanceProbeDbId}` (`genxGetConformanceProbe`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `conformanceProbeDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.

## 6. Deferred questions

- D-460: Should `expectedResponse` be required? (Current: optional.)
- D-461: Should `probeType` be a controlled vocabulary? (Current: free-form string.)
- D-462: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting T/W/A).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
