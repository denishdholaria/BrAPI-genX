#!/usr/bin/env python3
"""Synthetic positive and mutation tests for the CAS trace verifier."""
from __future__ import annotations

import copy
import unittest

from verify_breeding_pipeline_cas_trace import validate


def state(current='V3', revisions=None, effects=None):
    return {'currentVersionId': current,
            'revisions': {k: {'fingerprint': v, 'publicationState': 'published'}
                          for k, v in (revisions if revisions is not None else {'V3': 'digest3'}).items()},
            'effects': dict(effects if effects is not None else {'e3': 'V3'})}


def trace(scenario='CAS-01'):
    return {'scenario': scenario, 'before': state(), 'after': state(),
            'requests': [{'client': 'A', 'versionId': 'V4', 'fingerprint': 'digest4',
                          'expectedCurrentVersionId': 'V2'}],
            'responses': [{'client': 'A', 'status': 409,
                           'errorCode': 'current-version-precondition-failed'}]}


def race():
    t = trace('CAS-02')
    t['barrierObserved'] = True
    t['requests'] = [dict(client='A', versionId='V4A', fingerprint='digestA', expectedCurrentVersionId='V3'),
                     dict(client='B', versionId='V4B', fingerprint='digestB', expectedCurrentVersionId='V3')]
    t['responses'] = [dict(client='A', status=201, resultVersionId='V4A'),
                      dict(client='B', status=409, errorCode='current-version-precondition-failed')]
    t['after'] = state(current='V4A', revisions={'V3': 'digest3', 'V4A': 'digestA'}, effects={'e3': 'V3', 'e4a': 'V4A'})
    return t

def first_create_race():
    t = race()
    t['scenario'] = 'CAS-06'
    t['before'] = state(current=None, revisions={}, effects={})
    for row in t['requests']:
        row.pop('expectedCurrentVersionId')
    t['responses'][1]['errorCode'] = 'pipeline-identity-conflict'
    t['after'] = state(current='V4A', revisions={'V4A': 'digestA'}, effects={'e4a': 'V4A'})
    return t


class CasTraceTests(unittest.TestCase):
    def test_stale_conflict_passes(self):
        self.assertEqual([], validate(trace()))

    def test_stale_conflict_wrong_error_fails(self):
        t = trace(); t['responses'][0]['errorCode'] = 'version-content-conflict'
        self.assertTrue(validate(t))

    def test_rejected_revision_append_fails(self):
        t = trace(); t['after']['revisions']['V4'] = {'fingerprint': 'digest4', 'publicationState': 'published'}
        self.assertTrue(any('must not change' in e for e in validate(t)))

    def test_first_creation_race_passes(self):
        self.assertEqual([], validate(first_create_race()))

    def test_first_creation_loser_wrong_error_fails(self):
        t = first_create_race(); t['responses'][1]['errorCode'] = 'current-version-precondition-failed'
        self.assertTrue(validate(t))

    def test_first_creation_null_precondition_fails(self):
        t = first_create_race(); t['requests'][0]['expectedCurrentVersionId'] = None
        self.assertTrue(any('must omit expected-current' in e for e in validate(t)))

    def test_first_creation_cannot_start_with_existing_revision(self):
        t = first_create_race(); t['before'] = state()
        self.assertTrue(any('before the logical pipeline exists' in e for e in validate(t)))

    def test_first_creation_loser_does_not_append(self):
        t = first_create_race(); t['after']['revisions']['V4B'] = {'fingerprint': 'digestB', 'publicationState': 'published'}
        self.assertTrue(validate(t))

    def test_first_creation_loser_cannot_emit_event(self):
        t = first_create_race(); t['after']['effects']['e4b'] = 'V4B'
        self.assertTrue(validate(t))

    def test_race_one_winner_passes(self):
        self.assertEqual([], validate(race()))

    def test_race_winner_is_not_hard_coded(self):
        t = race(); t['responses'][0] = dict(client='A', status=409, errorCode='current-version-precondition-failed')
        t['responses'][1] = dict(client='B', status=200, resultVersionId='V4B')
        t['after'] = state(current='V4B', revisions={'V3': 'digest3', 'V4B': 'digestB'})
        self.assertEqual([], validate(t))

    def test_race_two_successes_fail(self):
        t = race(); t['responses'][1] = dict(client='B', status=201, resultVersionId='V4B')
        self.assertTrue(validate(t))

    def test_race_requires_barrier(self):
        t = race(); t.pop('barrierObserved')
        self.assertTrue(any('barrier' in e for e in validate(t)))

    def test_race_loser_must_not_appear(self):
        t = race(); t['after']['revisions']['V4B'] = 'digestB'
        self.assertTrue(validate(t))

    def test_race_winner_must_be_published(self):
        t = race(); t['after']['revisions']['V4A']['publicationState'] = 'draft'
        self.assertTrue(validate(t))

    def test_race_loser_lifecycle_side_effect_fails(self):
        t = race(); t['after']['effects']['e4b'] = 'V4B'
        self.assertTrue(any('must not emit' in e for e in validate(t)))

    def test_race_pointer_must_advance_to_winner(self):
        t = race(); t['after']['currentVersionId'] = 'V3'
        self.assertTrue(validate(t))

    def test_race_requires_same_expected_baseline(self):
        t = race(); t['requests'][1]['expectedCurrentVersionId'] = 'V2'
        self.assertTrue(validate(t))

    def test_race_historical_immutable_content(self):
        t = race(); t['after']['revisions']['V3']['fingerprint'] = 'tampered'
        self.assertTrue(validate(t))

    def test_identical_retry_passes(self):
        t = trace('CAS-03')
        t['requests'][0].update(versionId='V3', fingerprint='digest3')
        t['responses'][0] = dict(client='A', status=200, resultVersionId='V3')
        self.assertEqual([], validate(t))

    def test_identical_retry_cannot_add_effect(self):
        t = trace('CAS-03')
        t['requests'][0].update(versionId='V3', fingerprint='digest3')
        t['responses'][0] = dict(client='A', status=200, resultVersionId='V3')
        t['after']['effects']['duplicate-event'] = 'V3'
        self.assertTrue(validate(t))

    def test_retry_with_changed_content_fails(self):
        t = trace('CAS-03')
        t['requests'][0].update(versionId='V3', fingerprint='changed')
        t['responses'][0] = dict(client='A', status=200, resultVersionId='V3')
        self.assertTrue(validate(t))

    def test_content_conflict_passes(self):
        t = trace('CAS-04')
        t['requests'][0].update(versionId='V3', fingerprint='changed')
        t['responses'][0]['errorCode'] = 'version-content-conflict'
        self.assertEqual([], validate(t))

    def test_content_conflict_requires_immutable_record(self):
        t = trace('CAS-04')
        t['requests'][0].update(versionId='V3', fingerprint='changed')
        t['responses'][0]['errorCode'] = 'version-content-conflict'
        t['after']['revisions']['V3']['fingerprint'] = 'changed'
        self.assertTrue(validate(t))

    def test_missing_snapshot_fails(self):
        t = trace(); t['after'].pop('revisions')
        self.assertTrue(validate(t))

    def test_unknown_scenario_fails(self):
        t = trace(); t['scenario'] = 'CAS-99'
        self.assertTrue(validate(t))

    def test_missing_client_response_fails(self):
        t = race(); t['responses'][1]['client'] = 'missing'
        self.assertTrue(validate(t))


if __name__ == '__main__':
    unittest.main()
