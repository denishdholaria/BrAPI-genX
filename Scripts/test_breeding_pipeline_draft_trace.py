#!/usr/bin/env python3
"""Synthetic trace mutations for candidate CAS-07, CAS-08 and CAS-09."""
from __future__ import annotations

from copy import deepcopy
import unittest

from breeding_pipeline_draft_trace import validate_draft_trace


def snapshot(current, records, effects=None):
    return {'currentVersionId': current,
            'revisions': {k: {'fingerprint': fingerprint, 'publicationState': status}
                          for k, (fingerprint, status) in records.items()},
            'effects': effects or {}}


def cas07():
    before = snapshot(None, {'Vdraft': ('d0', 'draft')})
    after = snapshot('Vfirst', {'Vdraft': ('d0', 'draft'), 'Vfirst': ('d1', 'published')})
    request = dict(client='A', versionId='Vfirst', fingerprint='d1',
                   requestedPublicationState='published', expectedCurrentVersionId=None)
    responses = {'A': dict(status=201, resultVersionId='Vfirst')}
    return ({'scenario': 'CAS-07', 'pipelineExistsBefore': True}, before, after, [request], responses)


def cas08():
    before = snapshot('V3', {'V3': ('d3', 'published')})
    after = snapshot('V3', {'V3': ('d3', 'published'), 'Vdraft': ('d4', 'draft')})
    request = dict(client='A', versionId='Vdraft', fingerprint='d4',
                   requestedPublicationState='draft', expectedCurrentVersionId='V3',
                   basedOnVersionId='V3')
    responses = {'A': dict(status=201, resultVersionId='Vdraft')}
    return ({'scenario': 'CAS-08'}, before, after, [request], responses)


def cas09():
    t, before, after, requests, responses = cas08()
    t['scenario'] = 'CAS-09'
    t['barrierObserved'] = True
    requests.append(dict(client='B', versionId='VdraftB', fingerprint='db',
                         requestedPublicationState='draft', expectedCurrentVersionId='V3',
                         basedOnVersionId='V3'))
    after['revisions']['VdraftB'] = dict(fingerprint='db', publicationState='draft')
    responses['B'] = dict(status=201, resultVersionId='VdraftB')
    return t, before, after, requests, responses


class DraftTraceTests(unittest.TestCase):
    def check(self, maker):
        return validate_draft_trace(*maker())

    def test_cas07_first_publication(self):
        self.assertEqual([], self.check(cas07))

    def test_cas07_requires_explicit_null(self):
        t = cas07(); t[3][0].pop('expectedCurrentVersionId')
        self.assertTrue(any('explicit null' in e for e in validate_draft_trace(*t)))

    def test_cas07_must_preexist(self):
        t = cas07(); t[0].pop('pipelineExistsBefore')
        self.assertTrue(validate_draft_trace(*t))

    def test_cas07_cannot_mutate_draft(self):
        t = cas07(); t[2]['revisions']['Vdraft']['fingerprint'] = 'tampered'
        # Common immutable-history guard, not this narrower helper.
        self.assertEqual([], validate_draft_trace(*t))

    def test_cas07_requires_published_current(self):
        t = cas07(); t[2]['revisions']['Vfirst']['publicationState'] = 'draft'
        self.assertTrue(validate_draft_trace(*t))

    def test_cas08_draft_append(self):
        self.assertEqual([], self.check(cas08))

    def test_cas08_cannot_move_pointer(self):
        t = cas08(); t[2]['currentVersionId'] = 'Vdraft'
        self.assertTrue(any('must not move' in e for e in validate_draft_trace(*t)))

    def test_cas08_cannot_claim_supersession(self):
        t = cas08(); t[3][0]['supersedes'] = 'V3'
        self.assertTrue(validate_draft_trace(*t))

    def test_cas08_requires_preparation_baseline(self):
        t = cas08(); t[3][0]['basedOnVersionId'] = 'V2'
        self.assertTrue(validate_draft_trace(*t))

    def test_cas08_rejects_published_result(self):
        t = cas08(); t[2]['revisions']['Vdraft']['publicationState'] = 'published'
        self.assertTrue(validate_draft_trace(*t))

    def test_cas09_parallel_drafts(self):
        self.assertEqual([], self.check(cas09))

    def test_cas09_requires_barrier(self):
        t = cas09(); t[0]['barrierObserved'] = False
        self.assertTrue(validate_draft_trace(*t))

    def test_cas09_requires_both_append(self):
        t = cas09(); t[2]['revisions'].pop('VdraftB')
        self.assertTrue(validate_draft_trace(*t))

    def test_cas09_no_extra_revision(self):
        t = cas09(); t[2]['revisions']['unexpected'] = dict(fingerprint='bad', publicationState='draft')
        self.assertTrue(validate_draft_trace(*t))

    def test_cas09_no_unrelated_lifecycle_event(self):
        t = cas09(); t[2]['effects']['e9'] = 'unrelated'
        self.assertTrue(validate_draft_trace(*t))

    def test_cas09_wrong_expected_baseline(self):
        t = cas09(); t[3][1]['expectedCurrentVersionId'] = 'V2'
        self.assertTrue(validate_draft_trace(*t))


if __name__ == '__main__':
    unittest.main()
