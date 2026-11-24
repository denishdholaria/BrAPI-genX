# Mission 082 — Extreme-weather, soil chemistry and remote-sensing evidence boundaries

**Parent:** `86b52ce4f1e927db5a9137ffc8e3525e95962c6c` (Mission 081), 2026-11-24.  
**Scope:** source-backed scientific and geospatial interpretation limits. No official Breeding Application Programming Interface (BrAPI) version 2.1 changes, GenX wire schema or endpoint changes, registry identities or semantic relationships, scientific ratification or maturity promotion.

## Findings

1. **ExtremeWeatherEvent** (Request for Comments (RFC) 042, D-124–D-126): the registration request requires event identity, `locationDbId`, `occurredAt` and free-text `eventType`; response also requires `status`. `severity` is optional and selected from four broad labels, without an enforced observed magnitude, meteorological threshold, climatological baseline or weather source. The required Location string is not a validated authority-matched join. D-125 described an optional WeatherObservation link, but no `weatherObservationDbId` property exists.
2. **SoilChemistry** (RFC-077, D-229–D-231): only identity is required for registration. Optional `siteDbId` is a plain string, chemistry is an unconstrained object without a unit, analyte definition or test method, and `moistureDepthCm` is sampling depth, not a moisture value. The RFC previously asserted BrAPI Location and GenX SoilProfile references, but no typed `soilProfileDbId` or authority-matched Location join exists. No site/depth/time/provenance is mandatory, despite the former description.
3. **RemoteSensingMetadata** (RFC-145, D-433–D-435): only record identity is required. Platform, sensor, acquisition date, coordinate reference system, spatial resolution and provenance are optional. No date format, trusted spatial coordinate reference, source raster, spectral bands, footprint, cloud mask or calibration is required. A source catalogue entry cannot establish usable imagery or a scientifically comparable derived vegetation index.

## Assurance and preservation

- Source-linked draft group descriptions and qualified READMEs/RFCs for all three groups.
- Reviewed-description guard and schema-driven tests for exact required/optional fields and absence of assumed measurement or data-ownership links.
- Cumulative stacked documentation coverage: **135/156**, leaving **21 deferred** groups.
- Existing strict source-registry gates, conformance contracts, scientific decision status, and official BrAPI files unchanged.

## Verification

Documentation links and actual schema fields should be independently checked. Full modified Python test execution, registry/source audit, generator reproducibility and live conformance must pass before merge. These source-level claims do not constitute certified weather, soil laboratory quality, spatial metadata validity, or operational data provenance.
