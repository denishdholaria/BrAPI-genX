#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import tempfile
import os
import unittest

from check_genx_group_descriptions import audit, REL, REVIEWED

GOOD = ('# Group Jobs\n\n**Status:** candidate and proposed, not normative.\n\n'
        + 'This module covers a reviewed metadata scope. ' * 10
        + '\n**Sources:** [module](./README.md).\n')


class GroupEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.doc = self.root / REL / 'Core/Jobs/GroupDescription.md'
        self.doc.parent.mkdir(parents=True)
        (self.doc.parent / 'README.md').write_text('A cited module contract')
        self.doc.write_text(GOOD)

    def audit(self):
        return audit(self.root, reviewed=frozenset({'Core/Jobs'}))

    def test_reviewed_doc_is_accepted(self):
        self.assertEqual([], self.audit()['errors'])

    def test_missing_reviewed_doc_fails(self):
        self.doc.unlink()
        self.assertTrue(self.audit()['errors'])

    def test_empty_heading_regresses(self):
        self.doc.write_text('# Group Jobs\n')
        self.assertTrue(any('placeholder' in e for e in self.audit()['errors']))

    def test_missing_status_fails(self):
        self.doc.write_text(GOOD.replace('**Status:**', 'Status:'))
        self.assertTrue(self.audit()['errors'])

    def test_missing_source_fails(self):
        self.doc.write_text(GOOD.replace('**Sources:**', 'Sources:'))
        self.assertTrue(self.audit()['errors'])

    def test_dangling_source_fails(self):
        self.doc.write_text(GOOD.replace('./README.md', './missing.md'))
        self.assertTrue(any('dangling' in e for e in self.audit()['errors']))

    def test_remote_link_fails(self):
        self.doc.write_text(GOOD.replace('./README.md', 'https://example.com'))
        self.assertTrue(any('local' in e for e in self.audit()['errors']))

    def test_missing_maturity_qualification_fails(self):
        self.doc.write_text(GOOD.replace('candidate and proposed', 'defined and recorded'))
        self.assertTrue(any('maturity' in e for e in self.audit()['errors']))

    def test_title_only_unreviewed_is_not_failed(self):
        extra = self.root / REL / 'Core/Unreviewed/GroupDescription.md'
        extra.parent.mkdir(parents=True)
        extra.write_text('# Group Unreviewed\n')
        report = self.audit()
        self.assertEqual([], report['errors'])
        self.assertEqual(1, report['deferred'])

    def test_unavailable_root_fails_closed(self):
        self.assertTrue(audit(self.root / 'no-such-repo', frozenset({'Core/Jobs'}))['errors'])

    def test_reviewed_discovery_modules_are_pinned(self):
        required = {
            'Core/Jobs', 'Core/Provenance', 'ReferenceData/VariableTerms',
            'Breeding/BreedingPipeline', 'CropProduction/LotLedger',
            'Research/Models', 'Interoperability/FAIR',
            'Instrumentation/Telemetry', 'Genotyping/Genomics',
            'Core/CapabilityMetadata', 'Core/CapabilityNegotiation',
            'Core/ServerInfoV3',
        }
        self.assertTrue(required.issubset(REVIEWED))

    def test_reviewed_interoperability_modules_are_pinned(self):
        self.assertTrue({
            'Interoperability/ConformanceProbe',
            'Interoperability/Crosswalk',
            'Interoperability/SchemaMapping',
        }.issubset(REVIEWED))

    def test_parent_relative_evidence_inside_repo_is_valid(self):
        evidence = self.root / REL / 'DECISIONS.md'
        evidence.write_text('Tracked project decision evidence')
        self.doc.write_text(GOOD.replace('./README.md', '../../DECISIONS.md'))
        self.assertEqual([], self.audit()['errors'])

    def test_parent_traversal_outside_repo_is_rejected(self):
        with tempfile.TemporaryDirectory() as outside:
            evidence = Path(outside) / 'evidence.md'
            evidence.write_text('Not a repository file')
            href = Path(os.path.relpath(evidence, self.doc.parent)).as_posix()
            self.doc.write_text(GOOD.replace('./README.md', href))
            self.assertTrue(any('escapes repository' in error
                                for error in self.audit()['errors']))

    def test_symlink_to_external_evidence_is_rejected(self):
        with tempfile.TemporaryDirectory() as outside:
            evidence = Path(outside) / 'evidence.md'
            evidence.write_text('Not a repository file')
            (self.root / 'external-link.md').symlink_to(evidence)
            self.doc.write_text(
                GOOD.replace('./README.md', '../../../../external-link.md')
            )
            self.assertTrue(any('escapes repository' in error
                                for error in self.audit()['errors']))


    def test_official_method_scale_sources_are_retained(self):
        repository = Path(__file__).resolve().parents[1]
        official = repository / 'Specification/BrAPI-Phenotyping'
        self.assertIn('/scales:', (official / 'Scales/Scales_GET_POST.yaml').read_text())
        self.assertIn('/methods:', (official / 'Methods/Methods_GET_POST.yaml').read_text())
        for path in (
            'Specification/BrAPI-GenX/ReferenceData/MeasurementScale/README.md',
            'Specification/BrAPI-GenX/RFCs/RFC-087-Measurement-Scale.md',
        ):
            content = (repository / path).read_text()
            self.assertIn('BrAPI v2.1', content)
            self.assertIn('/brapi/v2/scales', content)
            self.assertNotIn('BrAPI v2.1 has no place to record measurement scales', content)
        for path in (
            'Specification/BrAPI-GenX/ReferenceData/MeasurementMethods/README.md',
            'Specification/BrAPI-GenX/RFCs/RFC-017-Measurement-Methods.md',
        ):
            self.assertIn('/brapi/v2/methods', (repository / path).read_text())

    def test_reviewed_methods_and_scales_are_pinned(self):
        self.assertTrue({'ReferenceData/MeasurementScale',
                         'ReferenceData/MeasurementMethods'}.issubset(REVIEWED))


if __name__ == '__main__':
    unittest.main()
