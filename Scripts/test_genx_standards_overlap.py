#!/usr/bin/env python3
"""Mutation checks for the verified standards-overlap audit."""
from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

import yaml

from audit_genx_standards_overlap import audit, MANIFEST, GENX

ROOT = Path(__file__).resolve().parents[1]


class StandardsOverlapAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.manifest = json.loads((ROOT / MANIFEST).read_text(encoding='utf-8'))
        targets = {MANIFEST}
        for entry in self.manifest['official_overlap']:
            module = GENX / entry['module']
            targets.update((Path(entry['official']), module / 'README.md',
                            module / 'GroupDescription.md', module / 'Schemas' /
                            (entry['resource'] + '.yaml'), GENX / 'RFCs' / entry['rfc']))
        for entry in self.manifest['unratified_links']:
            module = GENX / entry['module']
            targets.update((module / 'Schemas' / entry.get('schema_file', entry['resource'] + '.yaml'),
                            GENX / 'RFCs' / entry['rfc']))
        for relative in targets:
            full = self.root / relative
            full.parent.mkdir(parents=True, exist_ok=True)
            full.write_bytes((ROOT / relative).read_bytes())

    def run_audit(self):
        return audit(self.root)

    def test_verified_repository_sources_pass(self):
        self.assertEqual([], self.run_audit()['errors'])

    def test_deleted_official_route_fails(self):
        row = self.manifest['official_overlap'][0]
        path = self.root / row['official']
        doc = yaml.safe_load(path.read_text())
        doc['paths'].pop(row['route'])
        path.write_text(yaml.safe_dump(doc))
        self.assertTrue(any('official operation' in x for x in self.run_audit()['errors']))

    def test_deleted_official_acknowledgment_fails(self):
        row = self.manifest['official_overlap'][1]
        path = self.root / GENX / row['module'] / 'README.md'
        path.write_text(path.read_text().replace(row['public_route'], 'an unnamed route'))
        self.assertTrue(any('must acknowledge' in x for x in self.run_audit()['errors']))

    def test_unratified_link_added_to_candidate_fails(self):
        row = self.manifest['unratified_links'][0]
        path = self.root / GENX / row['module'] / 'Schemas' / row.get('schema_file', row['resource'] + '.yaml')
        schema = yaml.safe_load(path.read_text())
        schema['components']['schemas'][row['resource']]['properties']['linkedTerm'] = {
            '$ref': '#/components/schemas/VariableTerm'
        }
        path.write_text(yaml.safe_dump(schema))
        self.assertTrue(any('unratified target' in x for x in self.run_audit()['errors']))

    def test_unreviewed_invented_overlap_fails(self):
        path = self.root / MANIFEST
        content = json.loads(path.read_text())
        extra = dict(content['official_overlap'][0])
        extra['module'] = 'ReferenceData/FakeAcceptedModule'
        content['official_overlap'].append(extra)
        path.write_text(json.dumps(content))
        self.assertTrue(any('unreviewed module' in x for x in self.run_audit()['errors']))

    def test_missing_manifest_fails_closed(self):
        (self.root / MANIFEST).unlink()
        self.assertTrue(self.run_audit()['errors'])

    def test_schema_key_and_filename_may_differ(self):
        report = self.run_audit()
        self.assertEqual([], report['errors'])
        row = next(x for x in self.manifest['unratified_links']
                   if x['resource'] == 'OntologyTermRecord')
        self.assertEqual('OntologyTerm.yaml', row['schema_file'])
        self.assertEqual(20, report['links_checked'])

    def test_reintroduced_absence_claim_fails(self):
        row = self.manifest['official_overlap'][0]
        path = self.root / GENX / row['module'] / 'README.md'
        path.write_text(path.read_text() + '\\nBrAPI v2.1 has no measurement scale record.\\n')
        self.assertTrue(any('unsupported absence claim' in x
                            for x in self.run_audit()['errors']))

    def test_missing_rfc_decision_fails(self):
        row = self.manifest['unratified_links'][0]
        path = self.root / GENX / 'RFCs' / row['rfc']
        path.write_text(path.read_text().replace(row['decision'], 'unreviewed-decision'))
        self.assertTrue(any('missing open decision' in x for x in self.run_audit()['errors']))


if __name__ == '__main__':
    unittest.main()
