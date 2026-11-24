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


    def test_reviewed_ontology_and_unit_modules_are_pinned(self):
        self.assertTrue({
            'ReferenceData/UnitsAndQuantity',
            'ReferenceData/OntologyTerm',
            'ReferenceData/OntologyMapping',
        }.issubset(REVIEWED))

    def test_typed_terminology_links_remain_unratified(self):
        root = Path(__file__).resolve().parents[1]
        cases = (
            ('RFC-082-Units-And-Quantity.md', 'D-246', 'VariableTerm'),
            ('RFC-085-Ontology-Term.md', 'D-255', 'VariableTerm'),
            ('RFC-086-Ontology-Mapping.md', 'D-258', 'OntologyTerm'),
        )
        for filename, decision, target in cases:
            with self.subTest(rfc=filename):
                content = (root / 'Specification/BrAPI-GenX/RFCs' / filename).read_text()
                self.assertIn(decision, content)
                self.assertIn('no typed reference', content)
                self.assertIn(target, content)

    def test_reviewed_core_reference_overlaps_are_pinned(self):
        self.assertTrue({
            'ReferenceData/ReusableList',
            'ReferenceData/CommonCropName',
            'ReferenceData/PersonReference',
        }.issubset(REVIEWED))

    def test_official_list_crop_and_people_sources_are_acknowledged(self):
        repository = Path(__file__).resolve().parents[1]
        official = repository / 'Specification/BrAPI-Core'
        cases = (
            ('Lists/Lists_GET_POST.yaml', '/lists:',
             'ReusableList/README.md', 'RFC-090-Reusable-List.md', '/brapi/v2/lists'),
            ('Common Crop Names/CommonCropNames_GET.yaml', '/commoncropnames:',
             'CommonCropName/README.md', 'RFC-094-Common-Crop-Name.md',
             '/brapi/v2/commoncropnames'),
            ('People/People_GET_POST.yaml', '/people:',
             'PersonReference/README.md', 'RFC-097-Person-Reference.md',
             '/brapi/v2/people'),
        )
        for source, operation, readme, rfc, route in cases:
            with self.subTest(route=route):
                self.assertIn(operation, (official / source).read_text())
                path = repository / 'Specification/BrAPI-GenX/ReferenceData' / readme
                self.assertIn(route, path.read_text())
                proposal = repository / 'Specification/BrAPI-GenX/RFCs' / rfc
                self.assertIn(route, proposal.read_text())

    def test_taxonomy_and_institution_descriptions_are_pinned(self):
        self.assertTrue({
            'ReferenceData/TaxonName', 'ReferenceData/CropSpecies',
            'ReferenceData/InstitutionCode',
        }.issubset(REVIEWED))

    def test_official_taxonomy_and_institute_fields_preserved(self):
        root = Path(__file__).resolve().parents[1]
        official = (root / 'Specification/BrAPI-Germplasm/Germplasm/Schemas'
                    / 'GermplasmNewRequest.yaml').read_text()
        for field in ('genus:', 'species:', 'taxonIds:',
                      'speciesAuthority:', 'instituteCode:'):
            self.assertIn(field, official)
        for filename, module, decision in (
            ('RFC-080-Taxon-Name.md', 'TaxonName', 'D-240'),
            ('RFC-095-Crop-Species.md', 'CropSpecies', 'D-285'),
            ('RFC-096-Institution-Code.md', 'InstitutionCode', 'D-288'),
        ):
            with self.subTest(module=module):
                proposal = (root / 'Specification/BrAPI-GenX/RFCs' / filename).read_text()
                self.assertIn('no typed', proposal)
                self.assertIn(decision, proposal)
                description = (root / 'Specification/BrAPI-GenX/ReferenceData' /
                               module / 'GroupDescription.md').read_text()
                self.assertIn('STRUCTURAL_DRAFT', description)
                self.assertIn(decision, description)

    def test_version_and_vocabulary_group_reviews_are_pinned(self):
        required = {
            'ReferenceData/ExternalVocabulary',
            'ReferenceData/TerminologyVersion',
            'ReferenceData/ReferenceDataVersion',
            'ReferenceData/CropTraitDictionary',
        }
        self.assertTrue(required.issubset(REVIEWED))

    def test_incumbent_ontology_and_trait_apis_are_acknowledged(self):
        root = Path(__file__).resolve().parents[1]
        sources = [
            root / 'Specification/BrAPI-Phenotyping/Ontologies/README.md',
            root / 'Specification/BrAPI-Phenotyping/Traits/README.md',
        ]
        self.assertIn('/brapi/v2/ontologies', sources[0].read_text())
        self.assertIn('/brapi/v2/traits', sources[1].read_text())
        for name, decision in (
            ('ExternalVocabulary', 'D-249'),
            ('TerminologyVersion', 'D-252'),
            ('ReferenceDataVersion', 'D-279'),
            ('CropTraitDictionary', 'D-264'),
        ):
            with self.subTest(module=name):
                desc = (root / 'Specification/BrAPI-GenX/ReferenceData' /
                        name / 'GroupDescription.md').read_text()
                self.assertIn('STRUCTURAL_DRAFT', desc)
                self.assertIn(decision, desc)

    def test_experimental_design_group_review_is_pinned(self):
        self.assertTrue({'Breeding/Plot', 'Breeding/FieldBook',
                         'Breeding/TrialNetwork'}.issubset(REVIEWED))

    def test_official_plot_and_multistudy_semantics_are_preserved(self):
        root = Path(__file__).resolve().parents[1]
        level = (root / 'Specification/BrAPI-Phenotyping/ObservationUnits/Schemas'
                 / 'ObservationUnitLevel.yaml').read_text()
        self.assertIn('plot,', level)
        trials = (root / 'Specification/BrAPI-Core/Trials/README.md').read_text()
        self.assertIn('multiple studies', trials)
        for module, rfc, decision in (
            ('Plot', 'RFC-107-Plot.md', 'D-321'),
            ('FieldBook', 'RFC-108-Field-Book.md', 'D-324'),
            ('TrialNetwork', 'RFC-109-Trial-Network.md', 'D-326'),
        ):
            with self.subTest(module=module):
                proposal = (root / 'Specification/BrAPI-GenX/RFCs' / rfc).read_text()
                self.assertIn('no typed', proposal)
                self.assertIn(decision, proposal)
                description = (root / 'Specification/BrAPI-GenX/Breeding' /
                               module / 'GroupDescription.md').read_text()
                self.assertIn('STRUCTURAL_DRAFT', description)
                self.assertIn(decision, description)


if __name__ == '__main__':
    unittest.main()
