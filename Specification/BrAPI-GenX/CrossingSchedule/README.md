# BrAPI-GenX — Crossing Schedule (Breeding)

Crossing schedules record planned crosses with parents and scheduled dates.
BrAPI v2.1 has crosses and crossing projects but no schedule record.

- `POST /genx/v1/crossing-schedules` (`genxRegisterCrossingSchedule`) registers one
  `CrossingSchedule` (`Schemas/CrossingScheduleNewRequest.yaml`). Same
  `crossingScheduleDbId` + identical body replays; different body is
  rejected with `409`.
- `GET /genx/v1/crossing-schedules` (`genxListCrossingSchedules`) lists schedules,
  optionally filtered by program or status.
- `GET /genx/v1/crossing-schedules/{crossingScheduleDbId}`
  (`genxGetCrossingSchedule`) retrieves one schedule.

Details and falsifiers: `../RFC-037-Crossing-Schedule.md`.