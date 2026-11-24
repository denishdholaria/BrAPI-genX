# Mission 033 — Python-aware semantic-neighbor consumer audit

**Date:** 2026-11-24. **Starting `main`:** `e51bb3c14105f7cc36391901dd230bc6ce67fa21`.

## Why this is needed

The executable semantic-neighbor inventory introduced in Mission 022
previously scanned raw source text, including Python comments and
syntactically recognized documentation strings. After GitHub Actions
was restored, this produced a false-positive failure against a
proposal validator that merely *mentioned* a navigation field in
its introductory docstring.

## Bounded correction

A new pure helper, `Scripts/semantic_neighbor_python_scan.py`,
masks Python comment tokens and genuine module/class/function docstrings
using the standard-library abstract syntax tree and tokenizer before
scanning remaining references. It preserves line numbers and executable
mapping/string keys. When parsing fails, it falls back to the original
source rather than silently allowing unknown tokens.

The existing inventory still scans other-language source lexically,
still requires explicit review for new consumer paths, and still
fails closed for missing or stale reviewed files. It is **not** a
complete static-data-flow or runtime capability audit.

## Verification

The new isolated helper passed **10 of 10** local positive/mutation
tests in `/mnt/data/genx_mission033`. The tests cover multiple
docstring placements, comments, runtime dictionary keys,
error-message strings, same-line mixed documentation/code,
multiline content and parser fallback. Exact Git blobs expected:

- `Scripts/semantic_neighbor_python_scan.py`:
  `76c4f93c3a17b895131697b3d8a685143864fbd5`
- `Scripts/test_semantic_neighbor_python_scan.py`:
  `596edf06777f1188c55369e7d956563efcec9a43`

Three additional integration tests in the existing consumer-audit
test suite verify that the scanner actually suppresses docstring
false positives without hiding runtime data access. Those integration
tests and full repository inventory require GitHub Actions verification
after the commit.

No original registry records, source OpenAPI contracts, relationship
statuses, scientific mapping or external application were changed.
