#!/usr/bin/env python3
"""Mutation tests for non-normative scientific source-field evidence."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import yaml

from check_scientific_contract_boundaries import BASE, LEDGER, REVIEW, PAIRS, SCHEMAS, check


class BoundaryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for module, (relative, name, present, required, absent) in SCHEMAS.items():
            file = self.root / BASE / relative
            file.parent.mkdir(parents=True, exist_ok=True)
            props = {x: {'type': 'string'} for x in set(present) | set(required)}
            file.write_text(yaml.safe_dump({'components': {'schemas': {
                name: {'properties': props, 'required': list(required)}
            }}}, sort_keys=False))
        (self.root / REVIEW).parent.mkdir(parents=True, exist_ok=True)
        (self.root / REVIEW).write_text('Non-normative evidence\n')
        self.entries = []
        for source, target in PAIRS:
            for index in range(3):
                self.entries.append({'id': f'{source}.{index}', 'sourceModule': source,
                                     'targetModule': target, 'targetOperationId': f'target.{target}',
                                     'reviewStatus': 'requires-decision',
                                     'documentaryEvidence': [str(REVIEW)]})
        self.save_ledger()

    def save_ledger(self):
        file = self.root / LEDGER
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(yaml.safe_dump({'entries': self.entries}, sort_keys=False))

    def schema(self, module):
        relative, name, _, _, _ = SCHEMAS[module]
        file = self.root / BASE / relative
        return file, name, yaml.safe_load(file.read_text())

    def save_schema(self, module, doc):
        file, _, _ = self.schema(module)
        file.write_text(yaml.safe_dump(doc, sort_keys=False))

    def test_valid_source_contract_snapshot(self):
        self.assertEqual([], check(self.root))

    def test_existing_harvest_reference_removed_fails(self):
        file, name, doc = self.schema('YieldMap')
        doc['components']['schemas'][name]['properties'].pop('harvestRecordDbId')
        self.save_schema('YieldMap', doc)
        self.assertTrue(any('YieldMap: documented property harvestRecordDbId' in x for x in check(self.root)))

    def test_required_scientific_quantity_made_optional_fails(self):
        file, name, doc = self.schema('HarvestRecords')
        doc['components']['schemas'][name]['required'].remove('unit')
        self.save_schema('HarvestRecords', doc)
        self.assertTrue(any('HarvestRecords: documented required property unit' in x for x in check(self.root)))

    def test_new_reference_requires_evidence_revision(self):
        file, name, doc = self.schema('FieldScouting')
        doc['components']['schemas'][name]['properties']['fieldBookDbId'] = {'type': 'string'}
        self.save_schema('FieldScouting', doc)
        self.assertTrue(any('FieldScouting: formerly absent property fieldBookDbId' in x for x in check(self.root)))

    def test_no_schema_fails(self):
        (self.root / BASE / SCHEMAS['QualityFlag'][0]).unlink()
        self.assertTrue(any('QualityFlag: missing schema' in x for x in check(self.root)))

    def test_malformed_schema_fails(self):
        (self.root / BASE / SCHEMAS['AssayExecution'][0]).write_text('%%% malformed !\n')
        self.assertTrue(any('AssayExecution: malformed schema' in x for x in check(self.root)))

    def test_missing_assessment_fails(self):
        (self.root / REVIEW).unlink()
        self.assertTrue(any('Missing Mission 008 assessment' in x for x in check(self.root)))

    def test_missing_triads_fails(self):
        self.entries = [e for e in self.entries if e['id'] != 'VcfExport.0']
        self.save_ledger()
        self.assertTrue(any('VcfExport -> VcfImport: expected three' in x for x in check(self.root)))

    def test_review_state_regression_fails(self):
        self.entries[0]['reviewStatus'] = 'inherited-unreviewed'
        self.save_ledger()
        self.assertTrue(any('reviewed relation reverted' in x for x in check(self.root)))

    def test_evidence_backed_proposal_can_retain_review_evidence(self):
        self.entries[0]['reviewStatus'] = 'evidence-backed-proposed'
        self.save_ledger()
        self.assertEqual([], check(self.root))

    def test_terminal_authorized_state_can_retain_review_evidence(self):
        # Authorization and allowed transitions are enforced by the canonical ledger validator.
        for state in ('rejected', 'superseded'):
            self.entries[0]['reviewStatus'] = state
            self.save_ledger()
            self.assertEqual([], check(self.root))

    def test_unknown_review_status_fails(self):
        self.entries[0]['reviewStatus'] = 'accepted'
        self.save_ledger()
        self.assertTrue(any('reviewed relation reverted' in x for x in check(self.root)))

    def test_assessment_citation_missing_fails(self):
        self.entries[0]['documentaryEvidence'] = []
        self.save_ledger()
        self.assertTrue(any('assessment citation missing' in x for x in check(self.root)))

    def test_duplicate_identity_fails(self):
        self.entries[1]['id'] = self.entries[0]['id']
        self.save_ledger()
        self.assertTrue(any('three distinct retained neighbors' in x for x in check(self.root)))

    def test_malformed_ledger_fails(self):
        (self.root / LEDGER).write_text('entries: NOT A LIST\n')
        self.assertTrue(any('Cannot load semantic-neighbor ledger' in x for x in check(self.root)))


if __name__ == '__main__':
    unittest.main()
