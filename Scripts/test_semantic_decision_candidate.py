#!/usr/bin/env python3
"""Positive and adversarial tests for the non-normative decision candidate."""
from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

from validate_semantic_decision_candidate import main, validate

ORIGINAL = 'example.source -> genxOriginal'
SUCCESSOR = 'another.source -> genxReplacement'


def draft():
    return {'schemaVersion': 1,
            'recordType': 'semantic-neighbor-terminal-decision-candidate',
            'status': 'draft-not-authorized', 'decisionId': 'SEM-CAND-0001',
            'relationshipId': ORIGINAL, 'sourceCatalogId': 'example.source',
            'targetOperationId': 'genxOriginal', 'action': 'reject',
            'rationale': 'No authority-qualified relationship demonstrated.',
            'evidenceRefs': ['docs/assessment/example.md'],
            'proposedBy': 'specification-engineering', 'proposedAt': '2026-11-24'}


class DecisionCandidateTests(unittest.TestCase):
    def test_valid_draft_passes(self):
        self.assertEqual([], validate(draft()))

    def test_invalid_record_type_fails(self):
        d = draft(); d['recordType'] = 'ratified-decision'
        self.assertTrue(validate(d))

    def test_fake_approved_status_fails(self):
        d = draft(); d['status'] = 'ratified'
        self.assertTrue(any('draft-not-authorized' in x for x in validate(d)))

    def test_approval_reference_in_candidate_fails(self):
        d = draft(); d['authorizationReference'] = 'D-02'
        self.assertTrue(any('unknown candidate fields' in x for x in validate(d)))

    def test_wrong_relationship_identity_fails(self):
        d = draft(); d['relationshipId'] = 'another.source -> genxOriginal'
        self.assertTrue(any('must equal' in x for x in validate(d)))

    def test_missing_ledger_identity_fails(self):
        self.assertTrue(any('does not exist' in x for x in validate(draft(), known_ids={SUCCESSOR})))

    def test_valid_supersession_shape(self):
        d = draft(); d['action'] = 'supersede'; d['supersededBy'] = SUCCESSOR
        self.assertEqual([], validate(d, known_ids={ORIGINAL, SUCCESSOR}))

    def test_unknown_successor_fails(self):
        d = draft(); d['action'] = 'supersede'; d['supersededBy'] = SUCCESSOR
        self.assertTrue(any('supersededBy does not exist' in x for x in validate(d, known_ids={ORIGINAL})))

    def test_self_supersession_fails(self):
        d = draft(); d['action'] = 'supersede'; d['supersededBy'] = ORIGINAL
        self.assertTrue(any('non-self' in x for x in validate(d)))

    def test_duplicate_evidence_fails(self):
        d = draft(); d['evidenceRefs'].append(d['evidenceRefs'][0])
        self.assertTrue(any('duplicates' in x for x in validate(d)))

    def test_missing_rationale_fails(self):
        d = draft(); d['rationale'] = ' '
        self.assertTrue(any('rationale' in x for x in validate(d)))

    def test_noncalendar_date_fails(self):
        d = draft(); d['proposedAt'] = '2026-02-30'
        self.assertTrue(any('real calendar date' in x for x in validate(d)))

    def test_wrong_ledger_shape_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            c = root / 'candidate.yaml'; c.write_text(yaml.safe_dump(draft()))
            l = root / 'ledger.yaml'; l.write_text('entries: null\n')
            with patch('sys.argv', ['program', '--candidate', str(c), '--ledger', str(l)]):
                self.assertEqual(1, main())

    def test_draft_command_prints_not_authorization(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp) / 'draft.yaml'; p.write_text(yaml.safe_dump(draft()))
            with patch('sys.argv', ['program', '--candidate', str(p)]):
                self.assertEqual(0, main())


if __name__ == '__main__':
    unittest.main()
