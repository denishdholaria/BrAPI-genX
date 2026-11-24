# BrAPI-GenX — CarbonStock (Environment and Climate)

`CarbonStock` proposes an immutable carbon-stock **metadata** record. In the present schema, only `carbonStockDbId` is mandatory for registration; even `pool`, numeric `stockMgPerHa` (megagrams per hectare), `depthCm`, timestamp, location, study and provenance are optional. The record cannot by itself establish sampled or modelled carbon, depth comparability, scientific provenance, sequestration, emissions offsets or accreditation.

The proposal is not an official BrAPI (Breeding Application Programming Interface) version 2.1 Observation, and optional context identifiers are not verified database joins. Deferred D-199–D-201 remain unresolved.

- `POST /genx/v1/carbon-stocks` (`genxRecordCarbonStock`) registers one `CarbonStock` (`Schemas/CarbonStockNewRequest.yaml`). The source describes same-identity/same-body replay and changed-body conflict (`409`).
- `GET /genx/v1/carbon-stocks` (`genxListCarbonStocks`) lists records, optionally filtered by study, location, pool or status.
- `GET /genx/v1/carbon-stocks/{carbonStockDbId}` (`genxGetCarbonStock`) retrieves a record.

See [source-backed group description](./GroupDescription.md) and [RFC-067](../../RFCs/RFC-067-Carbon-Stock.md).
