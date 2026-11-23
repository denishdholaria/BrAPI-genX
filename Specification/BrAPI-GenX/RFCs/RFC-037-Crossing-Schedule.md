# RFC-037 — Crossing Schedule (Breeding)

- Status: deferred; retained as historical proposal.
- Supersedes: none.
- Decision: D-BP-11 — the broad CrossingSchedule surface is deferred; reopen only for scheduling/booking semantics beyond BrAPI PlannedCross and CrossingProject.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (D2).

## 1. Historical problem statement (not an accepted gap)

> The proposed planned-cross information overlaps BrAPI v2.1 PlannedCross and CrossingProject. D-BP-11 deferred this candidate pending proof of distinct resource scheduling semantics. The text below is historical, not a current gap assertion.

BrAPI v2.1 standardizes crosses and crossing projects but not crossing
schedules: planned crosses with parents and dates. Without this record,
crossing plans cannot be audited or linked to programs with provenance.

## 2. Object

`CrossingSchedule` — one immutable crossing schedule record.

## 3. Endpoints

- `GET /genx/v1/crossing-schedules` (`genxListCrossingSchedules`)
- `POST /genx/v1/crossing-schedules` (`genxRegisterCrossingSchedule`)
- `GET /genx/v1/crossing-schedules/{crossingScheduleDbId}` (`genxGetCrossingSchedule`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Crossing schedules reference BrAPI Program and Germplasm by identifier;
  they do not duplicate those resources.
- A schedule is not a BrAPI Cross or CrossingProject and must not be treated
  as one.

## 5. Invariants

- A published `crossingScheduleDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional schedules linked by `supersedes`.
- `parents` and `scheduledDate` are required.
- A schedule does not imply an approved breeding plan or release.

## 6. Deferred questions

- D-109: Should `parents` require at least two entries? (Current: required
  array, may have one.)
- D-110: Should crossing schedules link to GenX `BreedingPipeline`?
  (Current: optional, not required.)
- D-111: Should mating design be a governed vocabulary? (Current: free
  string.)

## 7. Classification

Primary domain: D2 — Breeding Programs and Experimental Design.
Cross-cutting: C1, C2, C3 (POST), C6, C9.