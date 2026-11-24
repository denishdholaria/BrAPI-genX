#!/usr/bin/env python3
from __future__ import annotations
import copy
from pathlib import Path
import tempfile
import unittest
import yaml
from validate_typed_relationship_candidates import check, main, REL

P = 'Specification/BrAPI-GenX/Breeding/BreedingPipeline/Schemas/BreedingPipeline.yaml'
Q = 'Specification/BrAPI-GenX/Geospatial/YieldMap/Schemas/YieldMap.yaml'


def record(**updates):
    data = {'candidateId': 'SCI-REL-0001', 'status': 'proposal-only',
            'relationKind': 'typed-resource-reference', 'sourceSchema': P,
            'targetSchema': Q, 'claim': 'Hypothetical directional record reference',
            'evidenceRefs': ['docs/assessment/example.md'],
            'unresolvedQuestions': ['What is the authoritative identifier?'],
            'proposedBy': 'specification-review', 'proposedAt': '2026-11-24'}
    data.update(updates)
    return data


def registry(*items):
    return {'schemaVersion': 1, 'entries': list(items)}


class TypedRelationshipTests(unittest.TestCase):
    def test_empty_register(self):
        self.assertEqual([], check(registry()))

    def test_structural_proposal(self):
        self.assertEqual([], check(registry(record())))

    def test_alternative_kinds(self):
        for kind in ('provenance-derivation', 'operation-contract-equivalence'):
            self.assertEqual([], check(registry(record(relationKind=kind))))

    def test_cannot_approve(self):
        self.assertTrue(any('proposal-only' in s for s in check(registry(record(status='accepted')))))

    def test_cannot_add_authorization(self):
        self.assertTrue(check(registry(record(authorizationReference='D-026'))))

    def test_duplicate_id(self):
        self.assertTrue(any('duplicate candidateId' in s for s in check(registry(record(), record()))))

    def test_missing_question(self):
        self.assertTrue(check(registry(record(unresolvedQuestions=[]))))

    def test_invalid_source_schema(self):
        self.assertTrue(check(registry(record(sourceSchema='../../etc/passwd'))))

    def test_invalid_type(self):
        self.assertTrue(check(registry(record(relationKind='navigation-is-science'))))

    def test_malformed_document(self):
        self.assertTrue(check({'entries': []}))

    def test_duplicate_evidence(self):
        self.assertTrue(check(registry(record(evidenceRefs=['a','a']))))

    def test_invalid_date(self):
        self.assertTrue(check(registry(record(proposedAt='2026-02-30'))))

    def test_resolution_against_repo(self):
        with tempfile.TemporaryDirectory() as path:
            root = Path(path)
            for p in (P, Q):
                f = root/p; f.parent.mkdir(parents=True, exist_ok=True); f.write_text('type: object\n')
            self.assertEqual([], check(registry(record()), root=root))
            (root/P).unlink()
            self.assertTrue(check(registry(record()), root=root))

    def test_command_does_not_promote(self):
        with tempfile.TemporaryDirectory() as path:
            root = Path(path); dest = root/REL; dest.parent.mkdir(parents=True)
            dest.write_text(yaml.safe_dump(registry()))
            from unittest.mock import patch
            with patch('sys.argv', ['program', '--root', path]):
                self.assertEqual(0, main())
            self.assertEqual(registry(), yaml.safe_load(dest.read_text()))


if __name__ == '__main__':
    unittest.main()
