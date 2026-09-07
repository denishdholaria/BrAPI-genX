# BrAPI GenX — Jobs

One lifecycle for long-running work: submit, poll, retrieve-or-cancel, expire.

- `POST /jobs` submits work (`Schemas/JobNewRequest.yaml`). Returns `202` and
  a `Job`. Resubmitting a byte-identical body under the same `idempotencyKey`
  returns the existing `Job` with zero new effects.
- `GET /jobs/{jobDbId}` reports the current `Job` (`Schemas/Job.yaml`).
- `DELETE /jobs/{jobDbId}` requests cancellation. Terminal states
  (`COMPLETED`, `FAILED`, `CANCELLED`, `EXPIRED`) are immutable.

V2 `/search/*` behavior is unchanged. A server may additionally expose an
async search as a `jobType`, but clients must not assume it.
