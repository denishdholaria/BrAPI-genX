# Mission 031 — Prevent regression of reviewed GenX group descriptions

**Date:** 2026-11-24; **baseline main:** `c287d734a26955a6260276341cf8458e12dd00fb`.

User-authorized evidence-bounded documentation improvements have
replaced nine of the 156 title-only GenX group-description placeholders.
This mission protects **only the nine documented groups** from
silent regression to a heading-only description, source links that
no longer resolve, absent maturity qualification, or unreferenced
scientific scope claims.

`Scripts/check_genx_group_descriptions.py` counts all group descriptions,
identifies a pinned subset of reviewed paths, checks that each has a
substantial description, an explicit status, direct repository-local
sources, and at least one clear candidate/proposed qualification.
Other groups are counted as deferred and **never automatically
filled or failed** solely for remaining incomplete. Its 10 isolated
mutation tests cover legitimate reviewed content, missing files, empty
reversions, missing maturity/status/citations, dangling and remote
links, and deliberately deferred title-only modules.

**Local verification:** `python -m unittest -v test_genx_group_descriptions.py`
and `python -m py_compile check_genx_group_descriptions.py
test_genx_group_descriptions.py` both passed under
`/mnt/data/genx_group_guard`. **10/10 tests** passed; exact Git
object hashes of tested files: checker
`ef237a0b861700792e22c8ba59f96c30d71e7edf`, tests
`49daf500252e13eeec55a997580df53a8e11d75a`.

The repository's GitHub tree and the nine committed files were
inspected separately: 42 direct module-documentation links were
verified as tracked files; the nine reviewed descriptions all have
source citations and explicit maturity labels.

The checker cannot prove that the prose is scientifically correct;
its source-link and scope checks are regression safeguards, not
independent domain peer review or normative acceptance. The
historical BrAPI version 2.1 sources and GenX wire contracts remain
unchanged, and full-checkout and hosted tests still need execution.
