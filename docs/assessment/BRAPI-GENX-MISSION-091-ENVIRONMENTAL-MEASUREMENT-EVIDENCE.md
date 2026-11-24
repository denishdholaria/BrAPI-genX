# Mission 091 — Carbon, emissions and environmental-treatment evidence boundaries

**Parent:** integrated `main` at `263630ba920ec977389fd87dd290c5a209a65086` after Mission 090. This is source-backed documentary scientific review, not normative standardization.

## Verified facts and corrected claims

**CarbonStock — RFC-067, D-199–D-201:** The registration contract requires *only* `carbonStockDbId`, while `pool`, numeric `stockMgPerHa`, depth, measurement timestamp, site/Study context and provenance are optional. Even the soil-pool depth is not required conditionally; no bulk density, sampling design, uncertainty, measurement-vs-model flag or validated carbon sequestration is modelled. A megagram-per-hectare label does not establish comparability or a carbon credit. The RFC's description as a required named-pool observation was qualified.

**Emissions — RFC-076, D-226–D-228:** Registration requires *only* `emissionsDbId`; quantity, unit, site, period, greenhouse-gas description and provenance are optional. The period has no time-interval format validation; `CO2e` (carbon dioxide equivalent) is a computed equivalence category, not a gas species. The RFC previously claimed a GenX CarbonStock relationship, but **no `carbonStockDbId` field exists**. No global-warming-potential factors, inventory boundary, accounting scope or certified emissions claim is specified.

**EnvironmentalTreatment — RFC-078, D-232–D-234:** Registration requires *only* `environmentalTreatmentDbId`; treatment type, site and exposure are all optional free text. No controlled experimental conditions, duration, comparator, observation unit, Study or measured response is enforced. The prior RFC claimed a GenX ExtremeWeather relationship, but **no `extremeWeatherEventDbId` field exists**.

All three response schemas additionally require lifecycle `status`. Optional namespaced/local identifiers are not verified cross-authority foreign keys. Official Breeding Application Programming Interface (BrAPI) version 2.1 Observation values can represent scientific recordings, but these three proposals are not official Observation records or guaranteed scientific measurements.

## Implemented documentation and safeguards

- Replaced three title-only GroupDescriptions with source-linked **STRUCTURAL_DRAFT** evidence, carefully separated from scientific validity, climate claims, carbon credit accounting and treatment outcomes.
- Qualified the three module overviews and RFCs, correcting the two non-existent relationship claims.
- Proposed protected evidence-reviewed descriptions **143 of 156**, leaving **13 deferred** after hosted verification. No maturity-state upgrade or decision ratification.
- Added schema-derived regression assertions for identity-only registration, optional scientific fields, absent relationships, existing enumerations and official Observation value type.

## Acceptance and non-goals

No official BrAPI v2.1 contract, GenX wire schema, endpoint/operation ID, registry, governance acceptance, scientific term or response semantics are modified. No emissions factors, units, carbon estimation procedures, controlled treatment standards, tenant-authority joins or validation policies are invented.

Required hosted gates:
```sh
python Scripts/check_genx_group_descriptions.py
python Scripts/test_genx_group_descriptions.py
python Scripts/report_genx_evidence_coverage.py --check
python Scripts/checkGenXConformance.py
python Scripts/checkEndpointRegistry.py
python Scripts/auditEndpointRegistrySourceConsistency.py --strict
python Scripts/generateEndpointArtifacts.py --check
```

Run hosted static + live reference conformance and specification generation on the final branch head. **Draft until verified; source inspection alone does not establish test success.**
