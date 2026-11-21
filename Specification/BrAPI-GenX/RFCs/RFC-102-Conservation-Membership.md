# RFC-102 — Conservation Membership (Germplasm)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (cross-cutting).

## 1. Problem

BrAPI v2.1 has no place to record conservation memberships. Conservation
memberships are the routine reference for germplasm and genetic resources.
Without a record, memberships arrive as unversioned notes with no stated
member, program, or provenance, so they cannot be audited or reproduced.

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
- Conservation membership records reference BrAPI `Germplasm` by identifier;
  they do not duplicate those resources.
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
