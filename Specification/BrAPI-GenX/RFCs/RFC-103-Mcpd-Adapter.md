# RFC-103 — MCPD Adapter (Germplasm)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (cross-cutting).

## 1. Problem

Official BrAPI version 2.1 already provides `GET /brapi/v2/germplasm/{germplasmDbId}/mcpd` and a GermplasmMCPD schema. This candidate adapter record includes only an optional source string and provenance; it does not execute a transform, define a verified data mapping, or replace the official MCPD representation.

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
- No typed link to an official BrAPI Germplasm or other candidate entity is established by the current record. Any externally meaningful resource linkage requires evidence and an explicit decision. D-308 remains open.
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
