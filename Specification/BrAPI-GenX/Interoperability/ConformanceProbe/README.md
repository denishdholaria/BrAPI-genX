# BrAPI-GenX — ConformanceProbe

ConformanceProbe records describe ConformanceProbe entries.
BrAPI v2.1 has no ConformanceProbe record.

- `POST /genx/v1/conformance-probes` (`genxRegisterConformanceProbe`) registers one
  `ConformanceProbe` (`Schemas/ConformanceProbeNewRequest.yaml`). Same
  `conformanceProbeDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/conformance-probes` (`genxListConformanceProbes`) lists records,
  optionally filtered by status.
- `GET /genx/v1/conformance-probes/{conformanceProbeDbId}`
  (`genxGetConformanceProbe`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-155-ConformanceProbe.md`.
