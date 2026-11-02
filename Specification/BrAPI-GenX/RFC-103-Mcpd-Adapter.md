# RFC-103 — MCPD Adapter (Germplasm)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (cross-cutting).

## 1. Problem

BrAPI v2.1 has no place to record MCPD adapters. MCPD adapters are the routine
reference for germplasm and genetic resources. Without a record, adapters arrive
as unversioned notes with no stated source or provenance, so they cannot be
audited or reproduced.

## 2. Object

`McpdAdapter` — one immutable MCPD adapter record, with its source system and
provenance.

## 3. Endpoints

- `GET /genx/v1/mcpd-adapters` (`genxListMcpdAdapters`)
- `POST /genx/v1/mcpd-adapters` (`genxRegisterMcpdAdapter`)
- `GET /genx/v1/mcpd-adapters/{mcpdAdapterDbId}` (`genxGetMcpdAdapter`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- MCPD adapter records reference BrAPI `Germplasm` by identifier; they do not
  duplicate those resources.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `mcpdAdapterDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- A record does not imply that the adapter is validated or endorsed.

## 6. Deferred questions

- D-307: Should `source` be required? (Current: optional.)
- D-308: Should adapter records link to BrAPI `Germplasm`? (Current: no
  link.)
- D-309: Should adapter records link to GenX `Crosswalk`? (Current: no link.)

## 7. Classification

Primary domain: (none, cross-cutting).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
