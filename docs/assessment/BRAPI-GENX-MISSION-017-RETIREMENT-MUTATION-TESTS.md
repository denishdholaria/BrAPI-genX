# Mission 017 — Repository-Level Semantic-Neighbor Retirement Regression Fixtures

**Date:** 2026-11-24  
**Baseline main:** `bc2104416e120653d9d997da34eaea3f42e856ba`  
**Scope:** integrate terminal-retirement consistency checks with the existing canonical governance test suite.

## Why the integration tests matter

Mission 016 delivered a pure, isolated 17-test guard. It is useful to
exercise the same rule across the actual registry, governance ledger and
validator audit path. Three additional tests were added to
`Scripts/test_semantic_neighbor_governance.py`. Each works on a copied
repository and compares the mutated ledger with an explicit prior ledger:

1. A synthetic terminal `rejected` disposition while the source still
   publishes the target must fail with `remains published`.
2. A structurally consistent terminal disposition with the active registry
   reference withdrawn should pass the canonical checks, while retaining
   its original ledger ID.
3. Removing the registry reference without the corresponding terminal
   disposition must fail with `authorized terminal disposition`.

The fixtures use `RFC-002` as a *syntactic, followable test token* for
`authorizationReference`. Such a token **does not constitute real
maintainer authorization**. The current validator verifies followability
and legal status transitions; independently verifying approval signatures
or a ratified decision record is a separate design concern.

## Verification boundary

The added integration tests were inspected and committed for the existing
workflow that executes `python Scripts/test_semantic_neighbor_governance.py`.
They were **not executed locally** because a complete repository checkout
including its large endpoint registry and historical source files was not
available in the isolated Python runtime. The separate Mission 016 unit
test suite has 17 passing tests with exact Git blob verification.

After the maintainer-reported GitHub Actions budget reset, execute the full
governance test suite, check the baseline drift gate, and inspect failure
details before considering the retirement workflow production-capable.
No endpoint registry relation or real decision was modified.

## Additional unresolved governance policy

The validator's current `_is_followable_reference` checks a reference's
shape, not the maintainer's authorization of the particular scientific
disposition. Define a verifiable authorized-decision record and its
relationship to `authorizationReference` before actually retiring a
scientific link. This concern should be assessed in issue #17 rather than
quietly inventing an approval mechanism.
