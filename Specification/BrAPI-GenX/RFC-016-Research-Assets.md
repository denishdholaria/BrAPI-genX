# RFC-016 — Research Assets (Publication & Knowledge)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-006 (FAIR Packages), `CLASSIFICATION.md` (cross-cutting C5).

## 1. Problem

BrAPI v2.1 has no research asset registry. Research outputs (datasets, models,
protocols, reports, evidence packs) need citable identities, license/access
metadata, embargo, and persistent identifiers. GenX already provides the FAIR
package envelope; a research asset record provides the asset-level identity and
metadata that the envelope wraps.

## 2. Object

`ResearchAsset` — one immutable research asset record.

## 3. Endpoints

- `GET /genx/v1/research-assets` (`genxListResearchAssets`)
- `POST /genx/v1/research-assets` (`genxRegisterResearchAsset`)
- `GET /genx/v1/research-assets/{researchAssetDbId}` (`genxGetResearchAsset`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Research assets reference BrAPI data resources and GenX FAIR packages by
  identifier; they do not duplicate those resources.
- An asset is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `researchAssetDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional assets linked by `supersedes`.
- `accessPolicy` and `license` are recorded, not inferred.
- An asset does not imply scientific validation or approval.

## 6. Deferred questions

- D-45: Should persistent identifier minting be a separate operation?
  (Current: recorded as a field; minting is out of scope.)
- D-46: Should research assets require a FAIR package reference?
  (Current: optional.)
- D-47: Should embargo visibility follow FAIR package rules?
  (Current: recorded as `embargoUntil`; visibility policy is out of scope.)

## 7. Classification

Primary domain: none (cross-cutting).
Cross-cutting: C1, C2, C3 (POST), C5, C6, C9.