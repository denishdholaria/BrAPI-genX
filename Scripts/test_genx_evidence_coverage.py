#!/usr/bin/env python3
"""Read-only evidence coverage reporting regression tests."""
from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from report_genx_evidence_coverage import summarize, register_maturity, ROOT
from check_genx_group_descriptions import REL

GOOD = ('# Group Jobs\n\n**Status:** candidate and proposed, not normative.\n\n'
        + 'Source statements with no scientific approval. ' * 13
        + '\n**Sources:** [module](./README.md).\n')


class EvidenceCoverageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.root.joinpath('docs/governance').mkdir(parents=True)
        self.maturity = self.root / 'docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md'
        self.maturity.write_text(
            '| RFC | Title | Maturity status | Notes |\n'
            '|---|---|---|---|\n'
            '| RFC-087 | Candidate | DEFERRED | Still a proposal |\n'
        )
        jobs = self.root / REL / 'Core/Jobs'
        jobs.mkdir(parents=True)
        (jobs / 'README.md').write_text('Proposed [RFC-087](../../RFCs/RFC-087.md)\n')
        (jobs / 'GroupDescription.md').write_text(GOOD)
        later = self.root / REL / 'Core/Future'
        later.mkdir(parents=True)
        (later / 'README.md').write_text('No tracked RFC yet\n')
        (later / 'GroupDescription.md').write_text('# Group Future\n')

    def report(self):
        return summarize(self.root, frozenset({'Core/Jobs'}))

    def test_separates_documentation_evidence_and_maturity(self):
        report = self.report()
        self.assertEqual(2, report['totalModules'])
        self.assertEqual(1, report['reviewedDescriptions'])
        self.assertEqual(1, report['deferredDescriptions'])
        reviewed = next(x for x in report['modules'] if x['module'] == 'Core/Jobs')
        self.assertEqual('source-backed-description', reviewed['descriptionEvidence'])
        self.assertEqual({'RFC-087': 'DEFERRED'}, reviewed['rfcMaturityFromRegister'])
        self.assertIn('Neither establishes scientific adoption', report['interpretation'])

    def test_unreviewed_heading_never_becomes_ready(self):
        future = next(x for x in self.report()['modules'] if x['module'] == 'Core/Future')
        self.assertEqual('evidence-deferred', future['descriptionEvidence'])
        self.assertEqual({}, future['rfcMaturityFromRegister'])

    def test_missing_reviewed_description_fails_closed(self):
        (self.root / REL / 'Core/Jobs/GroupDescription.md').unlink()
        with self.assertRaisesRegex(ValueError, 'group description guard failed'):
            self.report()

    def test_missing_rfc_register_fails_closed(self):
        self.maturity.unlink()
        with self.assertRaisesRegex(ValueError, 'missing maturity register'):
            self.report()

    def test_unregistered_rfc_is_not_granted_maturity(self):
        overview = self.root / REL / 'Core/Jobs/README.md'
        overview.write_text('Source: RFC-999\n')
        result = self.report()
        jobs = next(x for x in result['modules'] if x['module'] == 'Core/Jobs')
        self.assertEqual({'RFC-999': 'UNVERIFIED_RFC_REFERENCE'},
                         jobs['rfcMaturityFromRegister'])

    def test_unknown_maturity_state_fails_closed(self):
        self.maturity.write_text('| RFC-087 | Candidate | PRODUCTION_READY | Not verified |\n')
        with self.assertRaisesRegex(ValueError, 'unknown RFC maturity'):
            register_maturity(self.root)



class RepositoryDeferredMaturityReconciliationTests(unittest.TestCase):
    """No draft description silently upgrades scientific or RFC maturity."""

    def test_five_remaining_deferred_modules_are_explicit(self):
        report = summarize(ROOT)
        self.assertEqual(156, report['totalModules'])
        self.assertEqual(151, report['reviewedDescriptions'])
        self.assertEqual(5, report['deferredDescriptions'])
        deferred = {
            module['module']: module
            for module in report['modules']
            if module['descriptionEvidence'] == 'evidence-deferred'
        }
        expected = {
            'Breeding/CrossingSchedule': ('RFC-037', 'DEFERRED'),
            'Breeding/ProgenyRecords': ('RFC-019', 'DEFERRED'),
            'Geospatial/SpatialIndex': ('RFC-141', 'STRUCTURAL_DRAFT'),
            'Geospatial/SpatialQuery': ('RFC-143', 'STRUCTURAL_DRAFT'),
            'Geospatial/YieldMap': ('RFC-070', 'STRUCTURAL_DRAFT'),
        }
        self.assertEqual(set(expected), set(deferred))
        for module, (rfc, maturity) in expected.items():
            with self.subTest(module=module):
                self.assertEqual({rfc: maturity},
                                 deferred[module]['rfcMaturityFromRegister'])
                doc = ROOT / REL / module / 'GroupDescription.md'
                self.assertTrue(doc.is_file())
                self.assertLess(len(doc.read_text().strip()), 100)

        approved = (ROOT / 'docs/assessment/'
                    'BRAPI-GENX-BREEDING-PIPELINE-DECISIONS-APPROVED.md')
        decisions = approved.read_text()
        self.assertIn('D-BP-08', decisions)
        self.assertIn('D-BP-11', decisions)
        spatial = (ROOT / 'docs/assessment/'
                   'BRAPI-GENX-MISSION-090-SPATIAL-GOVERNANCE-PREFLIGHT.md')
        preflight = spatial.read_text()
        for decision in ('G-090-1', 'G-090-2', 'G-090-3'):
            self.assertIn(decision, preflight)
        self.assertIn('no ratification', preflight.lower())

    def test_newly_documented_science_remains_draft(self):
        report = summarize(ROOT)
        modules = {m['module']: m for m in report['modules']}
        latest_reviewed = {
            'Breeding/ExperimentalDesign': 'RFC-018',
            'Breeding/ExperimentalProtocol': 'RFC-117',
            'Breeding/TreatmentAssignment': 'RFC-106',
            'Breeding/ParentCandidateSelection': 'RFC-028',
            'Breeding/SelectionDecisions': 'RFC-008',
            'Breeding/DoubledHaploid': 'RFC-020',
            'Breeding/SpeedBreeding': 'RFC-022',
        }
        for module, rfc in latest_reviewed.items():
            with self.subTest(module=module):
                self.assertEqual('source-backed-description',
                                 modules[module]['descriptionEvidence'])
                self.assertEqual('STRUCTURAL_DRAFT',
                                 modules[module]['rfcMaturityFromRegister'][rfc])
        self.assertIn('Neither establishes scientific adoption',
                      report['interpretation'])



if __name__ == '__main__':
    unittest.main()
