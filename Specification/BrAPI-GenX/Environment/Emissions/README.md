# BrAPI-GenX — Emissions (Environment)

`Emissions` proposes an immutable reporting **metadata** record, not a certified emissions estimate. Only `emissionsDbId` is required at registration: site, period, greenhouse-gas category, numeric quantity, unit and provenance are optional. `CO2e` (carbon dioxide equivalent) is an example of a reporting equivalence category, not a greenhouse-gas species; the schema does not fix a global-warming-potential methodology, accounting scope or comparable unit.

The current record contains **no `carbonStockDbId`**, so it does not implement the CarbonStock relationship previously claimed by its Request for Comments (RFC). `siteDbId` is an optional string, not a verified official BrAPI (Breeding Application Programming Interface) Location join. D-226–D-228 remain deferred.

- `POST /genx/v1/emissions` (`genxRegisterEmissions`) registers one `Emissions` (`Schemas/EmissionsNewRequest.yaml`); replay and conflict behavior are candidate invariants.
- `GET /genx/v1/emissions` (`genxListEmissions`) lists records, optionally filtered by site or status.
- `GET /genx/v1/emissions/{emissionsDbId}` (`genxGetEmissions`) retrieves a record.

See [source-backed group description](./GroupDescription.md) and [RFC-076](../../RFCs/RFC-076-Emissions.md).
