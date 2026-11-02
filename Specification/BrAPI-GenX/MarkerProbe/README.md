# BrAPI-GenX — Marker Probe (Genomics)

Marker probe records describe a probe (oligo/vendor probe) targeting a BrAPI
Marker on a genotyping platform. BrAPI v2.1 has no marker probe registry.

- `POST /genx/v1/marker-probes` (`genxRegisterMarkerProbe`) registers one
  `MarkerProbe` (`Schemas/MarkerProbeNewRequest.yaml`). Same
  `markerProbeDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/marker-probes` (`genxListMarkerProbes`) lists probes,
  optionally filtered by marker, platform, or status.
- `GET /genx/v1/marker-probes/{markerProbeDbId}`
  (`genxGetMarkerProbe`) retrieves one probe.

Details and falsifiers: `../RFC-071-Marker-Probe.md`.
