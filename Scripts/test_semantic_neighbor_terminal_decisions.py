#!/usr/bin/env python3
from __future__ import annotations

import copy
from pathlib import Path
import tempfile
import unittest
import yaml

from semantic_neighbor_terminal_decisions import validate_register, terminal_decision_errors, load_register, DECISIONS_REL

REL = 'brapi-genx.genx.v1.farms.list -> genxRegisterFarm'
OTHER = 'brapi-genx.genx.v1.quality-flags.list -> genxRegisterQualityFlag'


def item(**kwargs):
    a = {'decisionId': 'SEM-DEC-0001', 'relationshipId': REL,
         'action': 'reject', 'approvedBy': 'project-maintainer',
         'approvedAt': '2026-11-24',
         'approvalEvidence': 'https://github.com/denishdholaria/BrAPI-genX/issues/17#issuecomment-1234',
         'rationale': 'Source schema has no supported mapping.',
         'evidenceRefs': ['docs/assessment/test-source.md']}
    a.update(kwargs)
    return a


def register(*rows):
    return {'schemaVersion': 1, 'entries': list(rows)}


def row(**kwargs):
    base = {'id': REL, 'reviewStatus': 'rejected', 'authorizationReference': 'SEM-DEC-0001'}
    base.update(kwargs)
    return base


class DecisionGateTests(unittest.TestCase):
    def test_empty_is_valid(self):
        self.assertEqual([], validate_register(register()))

    def test_exact_rejected_link_is_valid_shape(self):
        manifest = register(item())
        self.assertEqual([], validate_register(manifest, known_ids={REL}))
        self.assertEqual([], terminal_decision_errors(row(), manifest))

    def test_missing_decision_denies(self):
        self.assertTrue(terminal_decision_errors(row(), register()))

    def test_old_arbitrary_rfc_never_authorizes(self):
        self.assertTrue(terminal_decision_errors(row(authorizationReference='RFC-002'), register(item())))

    def test_mismatched_record_identity_denies(self):
        self.assertTrue(terminal_decision_errors(row(), register(item(relationshipId=OTHER))))

    def test_wrong_terminal_action_denies(self):
        self.assertTrue(terminal_decision_errors(row(reviewStatus='superseded', supersededBy=OTHER), register(item())))

    def test_supersede_exact_successor_matches(self):
        manifest = register(item(action='supersede', supersededBy=OTHER))
        self.assertEqual([], validate_register(manifest, known_ids={REL, OTHER}))
        self.assertEqual([], terminal_decision_errors(row(reviewStatus='superseded', supersededBy=OTHER), manifest))

    def test_supersede_wrong_successor_denies(self):
        manifest = register(item(action='supersede', supersededBy=OTHER))
        self.assertTrue(terminal_decision_errors(row(reviewStatus='superseded', supersededBy='different'), manifest))

    def test_duplicate_decision_id_denied(self):
        x = item(); y = item(relationshipId=OTHER)
        self.assertTrue(any('duplicate decisionId' in e for e in validate_register(register(x,y))))

    def test_duplicate_relationship_denied(self):
        x = item(); y = item(decisionId='SEM-DEC-0002')
        self.assertTrue(any('duplicate relationshipId' in e for e in validate_register(register(x,y))))

    def test_unregistered_relationship_denied(self):
        self.assertTrue(any('absent from retained ledger' in e for e in validate_register(register(item()), known_ids={OTHER})))

    def test_unregistered_successor_denied(self):
        self.assertTrue(any('successor absent' in e for e in validate_register(register(item(action='supersede', supersededBy=OTHER)), known_ids={REL})))

    def test_invalid_approval_ref_denied(self):
        self.assertTrue(any('approvalEvidence' in e for e in validate_register(register(item(approvalEvidence='https://example.com/fake')))))

    def test_mismatched_approved_by_denied(self):
        self.assertTrue(any('approvedBy' in e for e in validate_register(register(item(approvedBy='agent')))))

    def test_malformed_record_denied(self):
        self.assertTrue(validate_register({'schemaVersion': 2, 'entries': []}))

    def test_extra_properties_denied(self):
        self.assertTrue(validate_register(register(item(status='approved'))))

    def test_nonterminal_does_not_require_terminal_approval(self):
        self.assertEqual([], terminal_decision_errors(row(reviewStatus='requires-decision'), register()))

    def test_invalid_date_denied(self):
        self.assertTrue(validate_register(register(item(approvedAt='2026-02-30'))))

    def test_reject_cannot_have_successor(self):
        self.assertTrue(validate_register(register(item(supersededBy=OTHER))))

    def test_loading_manifest_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            doc, errors = load_register(Path(d))
            self.assertIsNone(doc)
            self.assertTrue(errors)

    def test_loading_empty_manifest(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/DECISIONS_REL
            p.parent.mkdir(parents=True)
            p.write_text(yaml.safe_dump(register()))
            doc, errors = load_register(Path(d))
            self.assertEqual([], errors)
            self.assertEqual(register(), doc)


if __name__ == '__main__':
    unittest.main()
