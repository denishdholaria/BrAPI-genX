# RFC-122 — Evidence Pack (Cross-cutting S)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (S).

## 1. Problem

BrAPI v2.1 has no place to record evidence packs. Evidence bundles used for
reproducibility, audit, and review circulate without a stated pack type,
contents, or provenance, so they cannot be traced or verified.

## 2. Object

`EvidencePack` — one immutable evidence pack record, with its name, type,
contents, and provenance.

## 3. Endpoints

- `GET /genx/v1/evidence-packs` (`genxListEvidencePacks`)
- `POST /genx/v1/evidence-packs` (`genxRegisterEvidencePack`)
- `GET /genx/v1/evidence-packs/{evidencePackDbId}` (`genxGetEvidencePack`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `evidencePackDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.

## 6. Deferred questions

- D-364: Should `contents` be required? (Current: optional.)
- D-365: Should `packType` be a controlled vocabulary? (Current: free-form string.)
- D-366: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting S).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
