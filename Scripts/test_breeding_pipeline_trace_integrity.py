#!/usr/bin/env python3
"""Adversarial snapshot tests for CAS observation integrity checks."""
from __future__ import annotations

import unittest

from breeding_pipeline_trace_integrity import snapshot_integrity_errors


def state(current='V3', publication='published', effects=None):
    return {'currentVersionId': current,
            'revisions': {'V3': {'fingerprint': 'digest3', 'publicationState': publication}},
            'effects': {'event3': 'V3'} if effects is None else effects}


class SnapshotIntegrityTests(unittest.TestCase):
    def test_published_current_valid(self):
        self.assertEqual([], snapshot_integrity_errors('after', state()))

    def test_null_pointer_with_historical_draft_valid(self):
        self.assertEqual([], snapshot_integrity_errors('before', state(current=None, publication='draft')))

    def test_current_absent_revision_fails(self):
        self.assertTrue(any('resolve to an included' in e for e in
                            snapshot_integrity_errors('before', state(current='V4'))))

    def test_current_points_to_draft_fails(self):
        self.assertTrue(any('published revision' in e for e in
                            snapshot_integrity_errors('after', state(publication='draft'))))

    def test_current_points_to_withdrawn_fails(self):
        self.assertTrue(snapshot_integrity_errors('after', state(publication='withdrawn')))

    def test_empty_current_identifier_fails(self):
        self.assertTrue(snapshot_integrity_errors('after', state(current='')))

    def test_orphan_lifecycle_event_fails(self):
        self.assertTrue(any('absent revision' in e for e in
                            snapshot_integrity_errors('after', state(effects={'event4':'V4'}))))

    def test_empty_event_map_valid(self):
        self.assertEqual([], snapshot_integrity_errors('after', state(effects={})))

    def test_null_pointer_with_no_revisions_valid(self):
        s = state(current=None, effects={})
        s['revisions'] = {}
        self.assertEqual([], snapshot_integrity_errors('before', s))

    def test_malformed_snapshot_fails_closed(self):
        s = state(); s['revisions'] = None
        self.assertTrue(snapshot_integrity_errors('after', s))


if __name__ == '__main__':
    unittest.main()
