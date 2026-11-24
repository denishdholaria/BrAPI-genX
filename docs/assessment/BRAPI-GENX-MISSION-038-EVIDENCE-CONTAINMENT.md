# Mission 038 — Repository-local evidence containment

**Date:** 2026-11-24
**Starting `main`:** `d4c4cbcf55d6f64ca2b93924cb14350c95eba0dc`
**Status:** implementation prepared; validation must execute on the final committed branch before any hosted success claim.

## Problem

The group-description evidence guard rejected URLs and verified that relative source paths existed, but it could accept a relative traversal into a real file **outside** the checked-out repository. A tracked path that was a symlink to an external file had the same problem. Such a reference is not valid portable source evidence.

## Bounded correction

Before checking existence, canonicalize each referenced source path with `Path.resolve()` and require `target.is_relative_to(root.resolve())`. Reject escaped and symlink-escaped paths with a specific `source link escapes repository` diagnostic. Keep legitimate local `../` references to tracked project decisions and Request for Comments documents working.

Three new isolated tests cover in-repository parent-relative evidence, traversal to an existing external file, and a repository symlink pointing to a file outside its root.

## Verification and scope boundaries

The canonical path-containment rule was separately exercised with a disposable local filesystem demonstration: a legitimate two-level parent link was accepted, while a relative escape and symlink escape were both rejected. The revised full checker and regression suite are subject to hosted execution. No public source contract, scientific mapping, RFC maturity, registry or catalogue changed. This guard enforces link containment, not the scientific correctness of the linked document.
