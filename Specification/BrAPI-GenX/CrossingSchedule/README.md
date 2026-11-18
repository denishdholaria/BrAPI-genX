# BrAPI-GenX — Crossing Schedule (Deferred)

**Status:** Deferred by maintainer decision D-BP-11.

BrAPI PlannedCross and CrossingProject remain authoritative for mating intent, parent associations, cross type, project context, and planned-cross status. The current broad CrossingSchedule record must not duplicate that intent.

Do not implement or promote the current CrossingSchedule endpoint surface. Reopen only for a distinct operational scheduling/booking requirement, such as resource/time-slot reservation and conflict semantics, with an explicit link to the BrAPI PlannedCross/CrossingProject identity. Calendar booking is not implied by a breeding scheme task.

Historical RFC: `../RFC-037-Crossing-Schedule.md`.
