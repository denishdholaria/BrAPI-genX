# BrAPI-GenX specification

BrAPI-GenX is an independently governed set of candidate extensions to BrAPI. These contracts use `/genx/v1/`. The official BrAPI v2.1 specifications are in the sibling [specification directories](../README.md).

## Browse by topic

Each section groups related modules. A module keeps its OpenAPI operations, schemas, and local documentation together.

| Section | Scope |
| --- | --- |
| [Core](./Core/) | Capability discovery, job execution, and reusable provenance |
| [Reference data](./ReferenceData/) | Terminology, units, measurement definitions, and shared identifiers |
| [Germplasm](./Germplasm/) | Accessions, collection, custody, and conservation |
| [Breeding and trials](./Breeding/) | Breeding strategy, selection, genetic improvement, and experimental design |
| [Genotyping and genomics](./Genotyping/) | Assays, genomic data, variant exchange, and molecular analysis |
| [Phenotyping](./Phenotyping/) | Plant measurements, capture workflows, and observation quality |
| [Environment](./Environment/) | Weather, climate, soil, water balance, and environmental accounting |
| [Crop production](./CropProduction/) | Field operations, agronomic advice, harvest, yield forecasts, and seed-lot movements |
| [Plant health](./PlantHealth/) | Disease observations, diagnostics, risk forecasts, and pest management |
| [Geospatial and remote sensing](./Geospatial/) | Geometries, coordinate systems, imagery, and spatial queries |
| [Instrumentation and telemetry](./Instrumentation/) | Devices, calibration, readings, and gateway status |
| [Research](./Research/) | Research organization, methods, reusable models, and evidence workflows |
| [Interoperability and exchange](./Interoperability/) | Mappings, packaging, exchange, and conformance interfaces |

## Design and verification

- [RFC index](./RFCs/README.md) and [maturity register](../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md)
- [Scientific classification](./CLASSIFICATION.md) and [module registry](./Conformance/domain-classification.yaml)
- [GenX endpoint catalogue](./GENX-ENDPOINT-CATALOG.md), [master endpoint registry](../ENDPOINT-REGISTRY.json), and [BijMantra crosswalk](../BIJMANTRA-CROSSWALK.md)
- [Conformance probes and fixtures](./Conformance/) and [legacy endpoint inventory](./Inventory/)
- [Decision register](./DECISIONS.md), [endpoint identity rules](./ENDPOINT-IDENTITY.md), and [adoption guide](./ADOPTION.md)
- [Ambika gap register](./AMBIKA-GAP-REGISTER.md) and [coverage matrix](./AMBIKA-GENX-COVERAGE-MATRIX.md)

## Placing a module

Choose the section by what the resource describes. A weather forecast belongs with weather, a yield forecast with crop production, and a disease-risk forecast with plant health. Reusable execution and evidence contracts can support resources across sections.

Record the module path in the registry and keep its module name and endpoint identifiers stable. Record scientific ownership in the primary domain and facets. A navigation section expresses the module's topic and leaves open classification questions visible. Add a new section when scoped contracts justify it and identify the external standard or authority they connect to.

For a design proposal, add its numbered document to the RFC index and record its review status in the maturity register.
