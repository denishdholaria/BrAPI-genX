#!/usr/bin/env python3
"""Unit tests for deterministic, non-normative semantic review reporting."""
from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

from report_semantic_neighbor_inventory import LEDGER, main, render_markdown, summarize


def sample():
    return {'entry_count': 4, 'entries': [
        {'id': 'a.get -> targetOne', 'sourceModule': 'Alpha',
         'targetOperationId': 'targetOne', 'reviewStatus': 'inherited-unreviewed'},
        {'id': 'a.list -> targetOne', 'sourceModule': 'Alpha',
         'targetOperationId': 'targetOne', 'reviewStatus': 'requires-decision'},
        {'id': 'b.get -> targetOne', 'sourceModule': 'Beta',
         'targetOperationId': 'targetOne', 'reviewStatus': 'inherited-unreviewed'},
        {'id': 'c.get -> targetTwo', 'sourceModule': 'Gamma',
         'targetOperationId': 'targetTwo', 'reviewStatus': 'rejected'},
    ]}


class InventoryTests(unittest.TestCase):
    def test_counts_and_grouping(self):
        report = summarize(sample())
        self.assertEqual(4, report['totalLinks'])
        self.assertEqual(2, report['unreviewedLinks'])
        self.assertEqual(2, report['reviewedOrDecisionPending'])
        self.assertEqual(3, report['totalGroups'])
        self.assertEqual(2, report['unreviewedGroups'])
        self.assertEqual(3, report['targetConcentration'][0]['links'])

    def test_mixed_review_status_keeps_unreviewed_work_visible(self):
        report = summarize(sample())
        alpha = next(g for g in report['queue'] if g['sourceModule'] == 'Alpha')
        self.assertEqual(1, alpha['unreviewed'])
        self.assertEqual(2, alpha['links'])
        self.assertEqual({'inherited-unreviewed': 1, 'requires-decision': 1}, alpha['statusCounts'])

    def test_order_independent_determinism(self):
        first = sample()
        second = copy.deepcopy(first)
        second['entries'].reverse()
        self.assertEqual(json.dumps(summarize(first), sort_keys=True),
                         json.dumps(summarize(second), sort_keys=True))

    def test_no_accepted_claim_or_auto_promotion(self):
        text = render_markdown(summarize(sample()))
        self.assertIn('non-normative', text)
        self.assertIn('no acceptance is implied', text)
        self.assertIn('Unreviewed work queue', text)

    def test_duplicate_identity_fails(self):
        doc = sample()
        doc['entries'][1]['id'] = doc['entries'][0]['id']
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            summarize(doc)

    def test_unknown_status_fails(self):
        doc = sample()
        doc['entries'][0]['reviewStatus'] = 'approved'
        with self.assertRaisesRegex(ValueError, 'unknown'):
            summarize(doc)

    def test_bad_header_count_fails(self):
        doc = sample()
        doc['entry_count'] = 153
        with self.assertRaisesRegex(ValueError, 'entry_count'):
            summarize(doc)

    def test_missing_source_module_fails(self):
        doc = sample()
        doc['entries'][0].pop('sourceModule')
        with self.assertRaisesRegex(ValueError, 'requires ID'):
            summarize(doc)

    def test_nonmapping_entry_fails(self):
        doc = sample()
        doc['entries'][0] = None
        with self.assertRaisesRegex(ValueError, 'mapping'):
            summarize(doc)

    def test_empty_valid_ledger_is_supported(self):
        report = summarize({'entry_count': 0, 'entries': []})
        self.assertEqual(0, report['totalLinks'])
        self.assertEqual([], report['queue'])

    def test_command_check_is_read_only(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / LEDGER
            path.parent.mkdir(parents=True)
            path.write_text(yaml.safe_dump(sample()))
            before = path.read_bytes()
            with patch('sys.argv', ['report', '--root', td, '--check']):
                self.assertEqual(0, main())
            self.assertEqual(before, path.read_bytes())

    def test_invalid_ledger_command_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / LEDGER
            path.parent.mkdir(parents=True)
            path.write_text('entry_count: 2\nentries: 42\n')
            with patch('sys.argv', ['report', '--root', td, '--check']):
                self.assertEqual(1, main())

    def test_schema_mapping_to_dataset_triads_remain_decision_gated(self):
        root = Path(__file__).resolve().parents[1]
        live = yaml.safe_load((root / LEDGER).read_text(encoding='utf-8'))
        summary = summarize(live)
        self.assertEqual(153, summary['totalLinks'])
        rows = [row for row in live['entries']
                if row['sourceModule'] == 'SchemaMapping'
                and row['targetOperationId'] == 'genxRegisterGenomicDataset']
        self.assertEqual(3, len(rows))
        for row in rows:
            with self.subTest(link=row['id']):
                self.assertEqual('requires-decision', row['reviewStatus'])
                self.assertEqual('inherited-registry-only', row['provenance'])
                self.assertIn('schemaMappingDbId', row['rationale'])
                self.assertIn('transformation', row['openQuestion'])
                self.assertIn(
                    'docs/assessment/BRAPI-GENX-MISSION-050-SCHEMA-DATASET-RELATIONSHIP-TRIAGE.md',
                    row['documentaryEvidence'])
                self.assertEqual([], row['evidence'])


if __name__ == '__main__':
    unittest.main()
