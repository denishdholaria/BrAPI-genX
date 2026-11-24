# BrAPI-GenX — Calendar (Reference Data)

`Calendar` proposes **draft time-convention metadata**, not a validated calendar, an official BrAPI (Breeding Application Programming Interface) version 2.1 `Study`, or a replacement for the official `Season` resource. Official BrAPI `Season` already carries `seasonDbId`, optional `seasonName`, and `year`.

The current GenX registration request requires only `calendarDbId`; `name`, free-text `convention`, and provenance are optional. There is **no `studyDbId` or `seasonDbId` link**, timezone, validity interval, or verified mapping to dates or seasons. An `ISO-8601` example does not enforce a time standard.

- `POST /genx/v1/calendars` (`genxRegisterCalendar`) registers one `Calendar` (`Schemas/CalendarNewRequest.yaml`). Same `calendarDbId` + identical body replays; different body is described as rejected with `409`.
- `GET /genx/v1/calendars` (`genxListCalendars`) lists records, optionally filtered by status.
- `GET /genx/v1/calendars/{calendarDbId}` (`genxGetCalendar`) retrieves a record.

Source-contract limits and open decisions: [group description](./GroupDescription.md), [RFC-091](../../RFCs/RFC-091-Calendar.md).
