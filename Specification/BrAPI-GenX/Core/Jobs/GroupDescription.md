# Group Jobs

One lifecycle for long-running work: submit, poll, retrieve-or-cancel, expire. Jobs model general asynchronous work; resubmitting a byte-identical body under the same idempotency key returns the existing job with zero new effects. Terminal states are immutable. BrAPI v2.1 search behavior is unchanged.
