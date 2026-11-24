#!/usr/bin/env python3
"""Mutation tests for historical-versus-new neighbor provenance classification."""
from __future__ import annotations

import unittest

from semantic_neighbor_lineage import noncurrent_lineage_errors, terminal_publication_errors

HIST = 'original.source -> target'
BASELINE = frozenset({HIST})
PAIR = ('original.source', 'target')


def entry(**overrides):
    row = {'id': HIST, 'sourceCatalogId': PAIR[0], 'targetOperationId': PAIR[1],
           'reviewStatus': 'requires-decision', 'provenance': 'inherited-registry-only',
           'rationale': 'Missing link contract'}
    row.update(overrides)
    return row


class LineageTests(unittest.TestCase):
    def test_original_inherited_link_passes(self):
        self.assertEqual([], noncurrent_lineage_errors(entry(), {PAIR}, BASELINE))

    def test_historical_rejection_after_registry_removal_passes(self):
        row = entry(reviewStatus='rejected')
        self.assertEqual([], noncurrent_lineage_errors(row, set(), BASELINE))

    def test_historical_supersession_after_registry_removal_passes(self):
        row = entry(reviewStatus='superseded')
        self.assertEqual([], noncurrent_lineage_errors(row, set(), BASELINE))

    def test_historical_unreviewed_removal_fails(self):
        row = entry(reviewStatus='inherited-unreviewed')
        self.assertTrue(any('authorized terminal disposition' in x
                            for x in noncurrent_lineage_errors(row, set(), BASELINE)))

    def test_historical_requires_decision_removal_fails(self):
        self.assertTrue(noncurrent_lineage_errors(entry(), set(), BASELINE))

    def test_historical_proposal_removal_fails(self):
        row = entry(reviewStatus='evidence-backed-proposed')
        self.assertTrue(noncurrent_lineage_errors(row, set(), BASELINE))

    def test_new_link_cannot_inherit_provenance(self):
        row = entry(id='new.source -> target', sourceCatalogId='new.source',
                    reviewStatus='requires-decision')
        self.assertTrue(any('beyond inherited-registry-only' in x
                            for x in noncurrent_lineage_errors(row, set(), BASELINE)))

    def test_new_link_cannot_be_unreviewed(self):
        row = entry(id='new.source -> target', sourceCatalogId='new.source',
                    reviewStatus='inherited-unreviewed', provenance='manual-review')
        self.assertTrue(any("cannot be 'inherited-unreviewed'" in x
                            for x in noncurrent_lineage_errors(row, set(), BASELINE)))

    def test_new_link_needs_rationale(self):
        row = entry(id='new.source -> target', sourceCatalogId='new.source',
                    provenance='manual-review', rationale=' ')
        self.assertTrue(any('non-empty rationale' in x
                            for x in noncurrent_lineage_errors(row, set(), BASELINE)))

    def test_new_documented_link_passes_provenance_classification(self):
        row = entry(id='new.source -> target', sourceCatalogId='new.source',
                    provenance='documented-mapping', rationale='Typed evidence established')
        self.assertEqual([], noncurrent_lineage_errors(row, set(), BASELINE))

    def test_new_link_with_invalid_rationale_type_fails(self):
        row = entry(id='new.source -> target', sourceCatalogId='new.source',
                    provenance='manual-review', rationale=['untrusted'])
        self.assertTrue(noncurrent_lineage_errors(row, set(), BASELINE))


class TerminalPublicationTests(unittest.TestCase):
    def test_rejected_link_still_active_fails(self):
        row = entry(reviewStatus='rejected')
        self.assertTrue(any('remains published' in msg
                            for msg in terminal_publication_errors(row, {PAIR})))

    def test_superseded_link_still_active_fails(self):
        row = entry(reviewStatus='superseded')
        self.assertTrue(any('remains published' in msg
                            for msg in terminal_publication_errors(row, {PAIR})))

    def test_terminal_registry_removal_passes(self):
        for status in ('rejected', 'superseded'):
            self.assertEqual([], terminal_publication_errors(
                entry(reviewStatus=status), set()))

    def test_nonterminal_link_can_be_active(self):
        for status in ('inherited-unreviewed', 'requires-decision',
                       'evidence-backed-proposed'):
            self.assertEqual([], terminal_publication_errors(
                entry(reviewStatus=status), {PAIR}))

    def test_different_source_is_not_the_same_link(self):
        self.assertEqual([], terminal_publication_errors(
            entry(reviewStatus='rejected'), {('another.source', 'target')}))

    def test_publication_guard_does_not_claim_approval(self):
        # Authorization is separately required by the canonical validator.
        self.assertEqual([], terminal_publication_errors(
            entry(reviewStatus='rejected'), set()))


if __name__ == '__main__':
    unittest.main()
