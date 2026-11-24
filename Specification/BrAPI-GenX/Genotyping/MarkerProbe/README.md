# BrAPI-GenX — Marker Probe (Genomics)

MarkerProbe is a candidate physical-probe metadata register. BrAPI v2.1
already covers Variants and marker positions; `markerDbId` in this candidate
is not proven equivalent to official `variantDbId`, and the optional probe
sequence has not been biologically validated.

- `POST /genx/v1/marker-probes` (`genxRegisterMarkerProbe`) registers one
  `MarkerProbe` (`Schemas/MarkerProbeNewRequest.yaml`). Same
  `markerProbeDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/marker-probes` (`genxListMarkerProbes`) lists probes,
  optionally filtered by marker, platform, or status.
- `GET /genx/v1/marker-probes/{markerProbeDbId}`
  (`genxGetMarkerProbe`) retrieves one probe.

Details and falsifiers: `../../RFCs/RFC-071-Marker-Probe.md`.
