# BrAPI GenX — Jobs

One lifecycle for long-running work: submit, poll, retrieve-or-cancel, expire. List jobs with `GET /brapi/v3/jobs` (`genxListJobs`).

- `POST /brapi/v3/jobs` (`genxSubmitAsyncJob`) submits work (`Schemas/JobNewRequest.yaml`). Returns `202` and
  a `Job`. Resubmitting a byte-identical body under the same `idempotencyKey`
  returns the existing `Job` with zero new effects.
- `GET /brapi/v3/jobs/{jobDbId}` (`genxGetAsyncJobById`) reports the current `Job` (`Schemas/Job.yaml`).
- `DELETE /brapi/v3/jobs/{jobDbId}` (`genxRequestAsyncJobCancellation`) requests cancellation. Terminal states
  (`COMPLETED`, `FAILED`, `CANCELLED`, `EXPIRED`) are immutable.

BrAPI V2.1 `/brapi/v2/search/*` behavior is unchanged. A server may additionally expose an
async search as a `jobType`, but clients must not assume it.
