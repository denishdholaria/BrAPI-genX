# RFC-091 — Calendar (Reference Data)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (cross-cutting).

## 1. Problem

BrAPI v2.1 has no place to record calendars and time conventions. Calendars
are the routine reference for research organization. Without a record,
calendars arrive as unversioned notes with no stated convention or provenance,
so they cannot be audited or reproduced.

## 2. Object

`Calendar` — one immutable calendar or time convention record, with its name,
convention, and provenance.

## 3. Endpoints

- `GET /genx/v1/calendars` (`genxListCalendars`)
- `POST /genx/v1/calendars` (`genxRegisterCalendar`)
- `GET /genx/v1/calendars/{calendarDbId}` (`genxGetCalendar`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Calendar records reference BrAPI `Study` by identifier; they do not duplicate
  those resources.
- A calendar record is not a BrAPI Study and must not be treated as one.

## 5. Invariants

- A published `calendarDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- A record does not imply that the calendar is validated or endorsed.

## 6. Deferred questions

- D-271: Should `name` be required? (Current: optional.)
- D-272: Should `convention` be a controlled vocabulary? (Current: free-form
  string.)
- D-273: Should calendar records link to GenX `ReusableList`? (Current: no
  link.)

## 7. Classification

Primary domain: (none, cross-cutting).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
