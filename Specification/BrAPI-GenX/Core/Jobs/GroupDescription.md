# Group Jobs

**Status:** BrAPI-GenX candidate contract; not part of official BrAPI version 2.1. The asynchronous-job lifecycle and idempotency architecture have reviewed internal design rules, but durable multi-instance behavior and independent authorization tests remain unverified.

This group defines a common `Job` resource for submitting explicitly advertised asynchronous work, listing caller-visible jobs, inspecting progress or results, and requesting cancellation. `POST /genx/v1/jobs` returns a job for polling rather than guaranteeing synchronous completion. The schema distinguishes `SUBMITTED`, `RUNNING`, `COMPLETED`, `FAILED`, `CANCELLED`, and `EXPIRED` states. Cancellation is a request, not a promise that work has stopped.

**Boundaries:** Jobs do not replace existing official BrAPI search resources, and clients must not submit job types absent from the server's advertised capability set. Accepted project decisions D-24 and D-25 distinguish idempotency namespace, replay fingerprint, fresh authorization, durable duplicate suppression and retention; the historical operation-level replay descriptions still require conformance verification against those decisions.

**Sources:** [Local module contract](./README.md), [job schema](./Schemas/Job.yaml), [proposed operations](./Jobs_GET_POST.yaml), and [project decisions D-24/D-25](../../DECISIONS.md).
