# RFC-102 — Conservation Membership (Germplasm)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (cross-cutting).

## 1. Problem

Official BrAPI Germplasm and MCPD records already describe accession and institute context. A conservation-program membership may be a distinct workflow, but this draft currently stores only optional `memberDbId` and free-form `program` strings, without typed identity, consent, custody, or a verified conservation obligation.

## 2. Object

`ConservationMembership` — one immutable conservation membership record, with
its member reference, program, and provenance.

## 3. Endpoints

- `GET /genx/v1/conservation-memberships` (`genxListConservationMemberships`)
- `POST /genx/v1/conservation-memberships` (`genxRegisterConservationMembership`)
- `GET /genx/v1/conservation-memberships/{conservationMembershipDbId}` (`genxGetConservationMembership`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- No typed link to an official BrAPI Germplasm or other candidate entity is established by the current record. An optional `memberDbId` is an unconstrained string, and the GenX CollectingMission relationship remains unratified. D-306 remains open.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `conservationMembershipDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- A record does not imply that the membership is validated or endorsed.

## 6. Deferred questions

- D-304: Should `memberDbId` be required? (Current: optional.)
- D-305: Should `program` be required? (Current: optional.)
- D-306: Should records link to GenX `CollectingMission`? (Current: no link.)

## 7. Classification

Primary domain: (none, cross-cutting).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
