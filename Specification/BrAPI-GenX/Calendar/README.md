# BrAPI-GenX — Calendar (Reference Data)

Calendar and time convention records describe time conventions for research.
BrAPI v2.1 has no calendar record.

- `POST /genx/v1/calendars` (`genxRegisterCalendar`) registers one
  `Calendar` (`Schemas/CalendarNewRequest.yaml`). Same
  `calendarDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/calendars` (`genxListCalendars`) lists records,
  optionally filtered by status.
- `GET /genx/v1/calendars/{calendarDbId}`
  (`genxGetCalendar`) retrieves one record.

Details and falsifiers: `../RFC-091-Calendar.md`.
