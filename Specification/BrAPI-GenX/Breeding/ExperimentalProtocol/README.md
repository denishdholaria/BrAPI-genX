# BrAPI-GenX — ExperimentalProtocol

This **STRUCTURAL_DRAFT** registers descriptive protocol metadata, not an executable or validated procedure. Official BrAPI version 2.1 Study design metadata, Observation Unit treatment factors and Events already represent related but distinct facts. GenX ProtocolLibrary is another draft without a typed relationship here.

- `POST /genx/v1/experimental-protocols` (`genxRegisterExperimentalProtocol`) registers one `ExperimentalProtocol` (`Schemas/ExperimentalProtocolNewRequest.yaml`). Only `experimentalProtocolDbId` is required; `protocolName`, version, counts and provenance are optional. Replay and `409` are proposed semantics.
- `GET /genx/v1/experimental-protocols` (`genxListExperimentalProtocols`) lists by optional status.
- `GET /genx/v1/experimental-protocols/{experimentalProtocolDbId}` (`genxGetExperimentalProtocol`) retrieves a record.

No typed Study, ExperimentalDesign, ProtocolLibrary or GenomicDataset link exists. Details: [evidence review](./GroupDescription.md), [RFC-117](../../RFCs/RFC-117-ExperimentalProtocol.md); D-349–D-351 remain open.
