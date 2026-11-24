# BrAPI-GenX — BiodiversityExport

`BiodiversityExport` is an **experimental metadata record**, not evidence that an occurrence/specimen dataset has been exported, delivered, accepted or published. Its registration request requires only `biodiversityExportDbId`; occurrence ID, collection date, location, taxon, specimen type and provenance are optional and not structurally validated. In particular, `status: active` is a record lifecycle status, **not an export-delivery receipt**.

The current candidate does **not** define a Darwin Core Archive, required occurrence terms, coordinate validation, publisher/license metadata, destination, payload URI/digest, delivery state or authoritative Germplasm/ResearchAsset mapping. Official BrAPI (Breeding Application Programming Interface) Germplasm passport metadata and GenX FAIRPackage remain separate; no interoperability crosswalk is approved here.

- `POST /genx/v1/biodiversity-exports` (`genxRegisterBiodiversityExport`) registers one `BiodiversityExport` (`Schemas/BiodiversityExportNewRequest.yaml`). Candidate replay and changed-body conflict (`409`) do not guarantee external publication.
- `GET /genx/v1/biodiversity-exports` (`genxListBiodiversityExports`) lists records, optionally filtered by lifecycle status.
- `GET /genx/v1/biodiversity-exports/{biodiversityExportDbId}` (`genxGetBiodiversityExport`) retrieves a record.

Source boundaries and deferred decisions: [group description](./GroupDescription.md), [RFC-121](../../RFCs/RFC-121-BiodiversityExport.md).
