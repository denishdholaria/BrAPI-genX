# BrAPI GenX — Jobs

One lifecycle for long-running work: submit, poll, retrieve-or-cancel, expire. List jobs with `GET /genx/v1/jobs` (`genxListJobs`).

- `POST /genx/v1/jobs` (`genxSubmitAsyncJob`) submits work (`Schemas/JobNewRequest.yaml`). Returns `202` and
  a `Job`. Resubmitting a byte-identical body under the same `idempotencyKey`
  returns the existing `Job` with zero new effects.
- `GET /genx/v1/jobs/{jobDbId}` (`genxGetAsyncJobById`) reports the current `Job` (`Schemas/Job.yaml`).
- `DELETE /genx/v1/jobs/{jobDbId}` (`genxRequestAsyncJobCancellation`) requests cancellation. Terminal states
  (`COMPLETED`, `FAILED`, `CANCELLED`, `EXPIRED`) are immutable.

BrAPI V2.1 `/brapi/v2/search/*` behavior is unchanged. A server may additionally expose an
async search as a `jobType`, but clients must not assume it.
