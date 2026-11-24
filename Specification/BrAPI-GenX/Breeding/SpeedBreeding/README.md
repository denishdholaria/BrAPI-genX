# BrAPI-GenX — Speed Breeding (Breeding)

This **STRUCTURAL_DRAFT** records a proposed speed-breeding protocol description, not an applied light/temperature schedule, measured generation acceleration or validated reproducibility. Official BrAPI version 2.1 Study already represents environmental parameters, growth facility and cultural practices.

- `POST /genx/v1/speed-breeding-protocols` (`genxRegisterSpeedBreedingProtocol`) registers `SpeedBreedingProtocol` (`Schemas/SpeedBreedingProtocolNewRequest.yaml`), requiring only candidate ID, Program string and `protocolName`. Light/temperature regime, photoperiod, generation time and provenance remain optional.
- `GET /genx/v1/speed-breeding-protocols` (`genxListSpeedBreedingProtocols`) lists by optional Program/status.
- `GET /genx/v1/speed-breeding-protocols/{speedBreedingProtocolDbId}` (`genxGetSpeedBreedingProtocol`) retrieves a record.

Identical-body replay and `409` conflict are candidate service behavior. There is no typed BreedingPipeline relationship or measured generation result. See [evidence](./GroupDescription.md), [RFC-022](../../RFCs/RFC-022-Speed-Breeding.md); D-63–D-65 remain open.
