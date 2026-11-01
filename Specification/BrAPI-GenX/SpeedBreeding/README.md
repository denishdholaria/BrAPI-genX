# BrAPI-GenX — Speed Breeding (Breeding)

Speed breeding protocols record the environmental conditions and generation
time used to accelerate plant development. BrAPI v2.1 has no speed breeding
record.

- `POST /genx/v1/speed-breeding-protocols` (`genxRegisterSpeedBreedingProtocol`) registers one
  `SpeedBreedingProtocol` (`Schemas/SpeedBreedingProtocolNewRequest.yaml`). Same
  `speedBreedingProtocolDbId` + identical body replays; different body is
  rejected with `409`.
- `GET /genx/v1/speed-breeding-protocols` (`genxListSpeedBreedingProtocols`) lists protocols,
  optionally filtered by program or status.
- `GET /genx/v1/speed-breeding-protocols/{speedBreedingProtocolDbId}`
  (`genxGetSpeedBreedingProtocol`) retrieves one protocol.

Details and falsifiers: `../RFC-022-Speed-Breeding.md`.