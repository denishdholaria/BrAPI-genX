#!/usr/bin/env python3
"""Read-only evidence coverage reporting regression tests."""
from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from report_genx_evidence_coverage import summarize, register_maturity
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


if __name__ == '__main__':
    unittest.main()
