# Group Calendar

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 091. This is a proposed time-convention metadata record, not an official Breeding Application Programming Interface (BrAPI) version 2.1 Season, Study, or verified temporal calendar.

The registration request requires only `calendarDbId`; the response requires `calendarDbId` and lifecycle `status`. `name`, `convention`, `supersedes`, and `provenance` are optional. `convention` is an unconstrained string (the `ISO-8601` example is **not** a schema-enforced standard). The schema has **no `studyDbId` or `seasonDbId`**, no timezone/locale/calendar-system identifier, no validity interval, and no mapping to study dates or seasons. An identifier and an optional convention label cannot establish correct calendar arithmetic, crop-season boundaries, reproducible time conversion, or scientific comparability.

**Official-contract overlap:** Official BrAPI version 2.1 already has a `Season` resource, with required `seasonDbId` and optional `seasonName` and `year`. Calendar may eventually describe different conventions, but the current contract has neither a defined crosswalk to `Season` nor an authoritative Study linkage. It must not be advertised as filling an entirely missing time/season domain.

**Deferred design decisions:** D-271 asks whether `name` should be required (currently optional); D-272 asks whether `convention` should use a controlled vocabulary (currently free text); D-273 asks whether it should link to GenX `ReusableList` (no such property exists). None is approved by this source-evidence review.

**Sources:** [module overview](./README.md), [response schema](./Schemas/Calendar.yaml), [registration schema](./Schemas/CalendarNewRequest.yaml), [operations](./Calendar_GET_POST.yaml), [RFC](../../RFCs/RFC-091-Calendar.md), [official Season schema](../../../BrAPI-Core/Seasons/Schemas/Season.yaml), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
