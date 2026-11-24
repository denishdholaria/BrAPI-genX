# RFC-091 — Calendar (Reference Data)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (cross-cutting).

## 1. Problem

Official BrAPI v2.1 already has a `Season` resource with a required
`seasonDbId` and optional `seasonName`/`year`; it does not constitute a
validated calendar-convention registry. A separate convention catalogue
could clarify time conventions, but this draft requires only `calendarDbId` on
registration. No date system, timezone, Study mapping, or official Season
crosswalk is enforced by the present schema.

## 2. Object

`Calendar` — a proposed immutable calendar or time-convention metadata record.
`name`, free-text `convention` and `provenance` are optional in the current
contract, so the record need not describe a usable calendar convention.

## 3. Endpoints

- `GET /genx/v1/calendars` (`genxListCalendars`)
- `POST /genx/v1/calendars` (`genxRegisterCalendar`)
- `GET /genx/v1/calendars/{calendarDbId}` (`genxGetCalendar`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- There is no `studyDbId` or `seasonDbId` in the current Calendar schema;
  neither an authoritative Study relationship nor a mapping to official
  BrAPI `Season` has been modelled.
- A calendar record is not a BrAPI Study or Season and must not be treated as one.

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
