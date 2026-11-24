# Mission 039 — Cache Gradle dependencies for repeatable schema generation

**Date:** 2026-11-24
**Starting `main`:** `4fc34b816424cd6d5ef058240ee51478541d04c2`
**Scope:** only the existing specification-generation GitHub Actions workflow and this assessment.

## Evidence and observed failure

The integrated Mission 037 specification generation [run 45348881251](https://github.com/denishdholaria/BrAPI-genX/actions/runs/45348881251), first attempt, failed in `./gradlew validate` because Maven Central returned **HTTP 429 Too Many Requests** while downloading `org.brapi.brapi-schema-tools:brapi-schema-tools-cli:0.77.0`. A retry of the same commit passed without changing source or contracts. This was an external dependency-resolution failure rather than a schema validation result.

## Narrow correction

The existing `actions/setup-java@v5` step supports `cache: gradle`, which restores and saves Gradle dependency caches keyed by build descriptors. Set that option on the **generator job** to reduce repeated remote downloads on later runs. The old human-readable step said `JDK 21` while the configured `java-version` is `22`; rename the step to reflect the actual runtime.

This is a best-effort caching measure: a cold cache, cache miss, invalidation, or upstream outage can still fail. It is not a change to the dependency version, its checksums, artifact source, contract generator, or release-branch commit policy.

## Verification

The workflow syntax and exact `setup-java@v5` caching input were reviewed against the official action documentation. Hosted workflow success, cache restore/save evidence and a subsequent warm run must be recorded from completed GitHub Actions logs; no hosted pass is claimed by this draft assessment.

No official BrAPI wire contract, GenX schema, registry, scientific governance or generated output was edited.
