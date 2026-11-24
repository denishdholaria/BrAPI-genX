# Mission 060 — Fertilizer, tillage, forecasting and irrigation advisory boundaries

**Prepared parent:** `a19db4fd8e9889cd94feb7d749a79b2f12647900`.

Four proposed resource groups are source reviewed and protected. Fertilizer and tillage operation records lack independently validated evidence of agronomic delivery and typed field referential integrity. YieldForecast uses an optional unstructured forecastValue without horizon/uncertainty/model context; IrrigationAdvice includes free-text recommended amounts but no verified weather/water-balance source or link to an applied irrigation event. These remain candidate metadata objects, not validated efficacy, operational compliance or actual field action.

## Confirmed RFC route/operation correction

RFC-131 incorrectly specified `/genx/v1/irrigation-advice` and `genxListIrrigationAdvice`, while actual source operations and module README use `/genx/v1/irrigation-advices` and `genxListIrrigationAdvices`. Corrected only RFC prose to agree with actual source, not the OpenAPI contracts, route registry or operation identities. Added a regression test for this consistency.

Decisions D-75–77, D-112–114, D-400–402 and D-391–393 remain open. All four resources are `STRUCTURAL_DRAFT`; no scientific mapping or maturity decision has been made. Local evidence links checked against the parent repository tree. Hosted conformance must pass after integration.
