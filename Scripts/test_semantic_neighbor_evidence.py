#!/usr/bin/env python3
"""Mutation tests for semantic-neighbor documentary evidence hygiene."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import yaml

from check_semantic_neighbor_evidence import LEDGER, check


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.ledger = self.root / LEDGER
        self.ledger.parent.mkdir(parents=True)
        self.paths = [
            'Specification/BrAPI-GenX/Core/Alpha/Schemas/Alpha.yaml',
            'Specification/BrAPI-GenX/Genotyping/Beta/Schemas/Beta.yaml',
            'docs/assessment/ALPHA-BETA.md',
        ]
        for relative in self.paths:
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('Evidence placeholder for file-presence test\n')
        self.entry = {
            'id': 'source.get -> target.register',
            'sourceModule': 'Alpha', 'targetModule': 'Beta',
            'reviewStatus': 'requires-decision',
            'documentaryEvidence': self.paths[:],
            'rationale': 'No typed relation established',
            'openQuestion': 'Should a link be formalized?',
        }
        self.save()

    def save(self):
        self.ledger.write_text(yaml.safe_dump({'entries': [self.entry]}, sort_keys=False))

    def errors(self):
        return check(self.root)[0]

    def test_valid_reviewed_evidence_passes(self):
        self.assertEqual(([], 1), check(self.root))

    def test_inherited_entries_not_forced_to_have_review_evidence(self):
        self.entry['reviewStatus'] = 'inherited-unreviewed'
        self.entry['documentaryEvidence'] = []
        self.save()
        self.assertEqual(([], 0), check(self.root))

    def test_missing_evidence_list_fails(self):
        self.entry.pop('documentaryEvidence')
        self.save()
        self.assertTrue(any('requires documentaryEvidence' in x for x in self.errors()))

    def test_missing_source_schema_fails(self):
        self.entry['documentaryEvidence'].pop(0)
        self.save()
        self.assertTrue(any('source-module schema' in x for x in self.errors()))

    def test_missing_target_schema_fails(self):
        self.entry['documentaryEvidence'].pop(1)
        self.save()
        self.assertTrue(any('target-module schema' in x for x in self.errors()))

    def test_missing_assessment_fails(self):
        self.entry['documentaryEvidence'].pop()
        self.save()
        self.assertTrue(any('assessment document' in x for x in self.errors()))

    def test_missing_file_fails(self):
        (self.root / self.paths[0]).unlink()
        self.assertTrue(any('file missing' in x for x in self.errors()))

    def test_path_traversal_fails(self):
        self.entry['documentaryEvidence'].append('../outside.md')
        self.save()
        self.assertTrue(any('repository-relative' in x for x in self.errors()))

    def test_duplicate_evidence_fails(self):
        self.entry['documentaryEvidence'].append(self.paths[0])
        self.save()
        self.assertTrue(any('repeated' in x for x in self.errors()))

    def test_missing_open_question_fails(self):
        self.entry['openQuestion'] = ''
        self.save()
        self.assertTrue(any('without openQuestion' in x for x in self.errors()))

    def test_terminal_status_not_reclassified(self):
        self.entry['reviewStatus'] = 'rejected'
        self.entry['documentaryEvidence'] = []
        self.save()
        self.assertEqual(([], 0), check(self.root))

    def test_malformed_ledger_fails(self):
        self.ledger.write_text(yaml.safe_dump({'wrong': []}))
        self.assertTrue(any('entries list' in x for x in self.errors()))


if __name__ == '__main__':
    unittest.main()
