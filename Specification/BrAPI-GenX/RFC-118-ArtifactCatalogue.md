# RFC-118 — Artifact Catalogue (Cross-cutting S)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (S).

## 1. Problem

BrAPI v2.1 has no place to record dataset/model artefacts. Artefacts arrive as
unversioned files with no stated storage reference, digest, or provenance, so
they cannot be audited or reproduced.

## 2. Object

`ArtifactCatalogue` — one immutable artefact catalogue record, with its name,
type, storage reference, digest, and provenance.

## 3. Endpoints

- `GET /genx/v1/artifact-catalogues` (`genxListArtifactCatalogues`)
- `POST /genx/v1/artifact-catalogues` (`genxRegisterArtifactCatalogue`)
- `GET /genx/v1/artifact-catalogues/{artifactCatalogueDbId}` (`genxGetArtifactCatalogue`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `artifactCatalogueDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.

## 6. Deferred questions

- D-352: Should `digest` be required? (Current: optional.)
- D-353: Should `artefactType` be a controlled vocabulary? (Current: free-form string.)
- D-354: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting S).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
