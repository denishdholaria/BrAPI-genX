# RFC-089 — Project (Reference Data)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (cross-cutting).

## 1. Problem

BrAPI v2.1 has no place to record project and funding references. Projects are
the routine reference for research organization. Without a record, projects
arrive as unversioned notes with no stated title, funding, or provenance, so
they cannot be audited or reproduced.

## 2. Object

`Project` — one immutable project and funding reference record, with its title,
funding, and provenance.

## 3. Endpoints

- `GET /genx/v1/projects` (`genxListProjects`)
- `POST /genx/v1/projects` (`genxRegisterProject`)
- `GET /genx/v1/projects/{projectDbId}` (`genxGetProject`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- The current candidate `Project` schema contains no typed BrAPI
  `Study` reference. A project title or funding string cannot establish
  a Study-to-Project relationship or authoritative grant linkage.
- A project record is not a BrAPI Study and must not be treated as one.

## 5. Invariants

- A published `projectDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- A record does not imply that the project is validated or endorsed.

## 6. Deferred questions

- D-265: Should `title` be required? (Current: optional.)
- D-266: Should `funding` be a structured object? (Current: free-form
  string.)
- D-267: Should project records link to GenX `ResearchAsset`? (Current: no
  link.)

## 7. Classification

Primary domain: (none, cross-cutting).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
