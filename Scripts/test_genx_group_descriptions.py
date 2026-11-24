#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import tempfile
import os
import unittest

import yaml

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

    def test_germplasm_conservation_source_groups_are_pinned(self):
        self.assertTrue({'Germplasm/CollectingMission',
                         'Germplasm/ConservationMembership',
                         'Germplasm/McpdAdapter'}.issubset(REVIEWED))

    def test_official_passport_source_precedes_candidate_adapter(self):
        root = Path(__file__).resolve().parents[1]
        route = (root / 'Specification/BrAPI-Germplasm/Germplasm'
                 / 'Germplasm_GermplasmDbId_MCPD_GET.yaml').read_text()
        self.assertIn('/germplasm/{germplasmDbId}/mcpd:', route)
        mcpd = (root / 'Specification/BrAPI-Germplasm/Germplasm/Schemas'
                / 'GermplasmMCPD.yaml').read_text()
        self.assertIn('collectingMissionIdentifier:', mcpd)
        for name, rfc, decision in (
            ('CollectingMission', 'RFC-101-Collecting-Mission.md', 'D-302'),
            ('ConservationMembership', 'RFC-102-Conservation-Membership.md', 'D-306'),
            ('McpdAdapter', 'RFC-103-Mcpd-Adapter.md', 'D-308'),
        ):
            with self.subTest(name=name):
                proposal = (root / 'Specification/BrAPI-GenX/RFCs' / rfc).read_text()
                self.assertIn('No typed link', proposal)
                self.assertIn(decision, proposal)
                group = (root / 'Specification/BrAPI-GenX/Germplasm' /
                         name / 'GroupDescription.md').read_text()
                self.assertIn('STRUCTURAL_DRAFT', group)
                self.assertIn(decision, group)

    def test_phenotyping_quality_and_capture_groups_are_pinned(self):
        self.assertTrue({'Phenotyping/QualityFlag',
                         'Phenotyping/ValueMissingness',
                         'Phenotyping/CaptureWorkflow'}.issubset(REVIEWED))

    def test_missingness_ambiguity_is_explicit_not_assumed(self):
        root = Path(__file__).resolve().parents[1]
        official = (root / 'Specification/BrAPI-Phenotyping/Observations/Schemas'
                    / 'ObservationNewRequest.yaml').read_text()
        for token in ('observationTimeStamp:', 'observationUnitDbId:',
                      'observationVariableDbId:', 'value:'):
            self.assertIn(token, official)
        candidate = (root / 'Specification/BrAPI-GenX/Phenotyping'
                     / 'ValueMissingness/Schemas/ValueMissingness.yaml').read_text()
        self.assertIn('missing:', candidate)
        self.assertIn('value:', candidate)
        self.assertNotIn('oneOf:', candidate)
        for name, rfc, decision in (
            ('QualityFlag', 'RFC-111-Quality-Flag.md', 'D-333'),
            ('ValueMissingness', 'RFC-112-Value-Missingness.md', 'D-336'),
            ('CaptureWorkflow', 'RFC-110-Capture-Workflow.md', 'D-330'),
        ):
            with self.subTest(name=name):
                proposal = (root / 'Specification/BrAPI-GenX/RFCs' / rfc).read_text()
                self.assertIn('No typed link', proposal)
                self.assertIn(decision, proposal)
                group = (root / 'Specification/BrAPI-GenX/Phenotyping' /
                         name / 'GroupDescription.md').read_text()
                self.assertIn('STRUCTURAL_DRAFT', group)
                self.assertIn(decision, group)

    def test_genomic_reference_and_pipeline_provenance_are_reviewed(self):
        self.assertTrue({'Genotyping/ReferenceAssembly',
                         'Genotyping/PipelineProvenance'}.issubset(REVIEWED))

    def test_reference_assembly_and_pipeline_are_not_conflated(self):
        root = Path(__file__).resolve().parents[1]
        official = (root / 'Specification/BrAPI-Genotyping/ReferenceSets/Schemas'
                    / 'ReferenceSet.yaml').read_text()
        self.assertIn('referenceSetDbId:', official)
        self.assertIn('referenceSetName:', official)
        for module, proposal, decision in (
            ('ReferenceAssembly', 'RFC-115-Reference-Assembly.md', 'D-345'),
            ('PipelineProvenance', 'RFC-116-Pipeline-Provenance.md', 'D-348'),
        ):
            with self.subTest(module=module):
                rfc = (root / 'Specification/BrAPI-GenX/RFCs' / proposal).read_text()
                self.assertIn('no typed', rfc)
                self.assertIn(decision, rfc)
                group = (root / 'Specification/BrAPI-GenX/Genotyping' /
                         module / 'GroupDescription.md').read_text()
                self.assertIn('STRUCTURAL_DRAFT', group)
                self.assertIn(decision, group)
        pipeline = (root / 'Specification/BrAPI-GenX/RFCs'
                    / 'RFC-116-Pipeline-Provenance.md').read_text()
        self.assertIn('not a reference genome assembly', pipeline)
        self.assertNotIn('the assembly is validated or endorsed', pipeline)

    def test_vcf_import_group_is_evidence_reviewed(self):
        self.assertIn('Genotyping/VcfImport', REVIEWED)

    def test_vcf_import_dataset_link_is_present_but_unverified(self):
        root = Path(__file__).resolve().parents[1]
        candidate = (root / 'Specification/BrAPI-GenX/Genotyping/VcfImport/Schemas'
                     / 'VcfImport.yaml').read_text()
        request = (root / 'Specification/BrAPI-GenX/Genotyping/VcfImport/Schemas'
                   / 'VcfImportNewRequest.yaml').read_text()
        self.assertIn('genomicDatasetDbId:', candidate)
        self.assertIn('genomicDatasetDbId:', request)
        self.assertNotIn('variantMatrixDbId:', candidate)
        rfc = (root / 'Specification/BrAPI-GenX/RFCs/RFC-043-Vcf-Import.md').read_text()
        self.assertIn('explicit identifier property', rfc)
        self.assertIn('no typed VariantMatrix', rfc)
        desc = (root / 'Specification/BrAPI-GenX/Genotyping/VcfImport'
                / 'GroupDescription.md').read_text()
        self.assertIn('STRUCTURAL_DRAFT', desc)
        self.assertIn('D-128', desc)

    def test_phenotype_capture_series_annotation_review_is_pinned(self):
        self.assertTrue({'Phenotyping/PhenotypeCapture',
                         'Phenotyping/RepeatedMeasurement',
                         'Phenotyping/PhenotypeAnnotation'}.issubset(REVIEWED))

    def test_numeric_capture_and_missing_series_conflict_is_documented(self):
        import yaml
        root = Path(__file__).resolve().parents[1]
        official = yaml.safe_load(
            (root / 'Specification/BrAPI-Phenotyping/Observations/Schemas'
             / 'ObservationNewRequest.yaml').read_text())
        source_props = official['components']['schemas']['ObservationNewRequest']['properties']
        self.assertEqual('string', source_props['value']['type'])
        capture = yaml.safe_load(
            (root / 'Specification/BrAPI-GenX/Phenotyping/PhenotypeCapture/Schemas'
             / 'PhenotypeCapture.yaml').read_text())
        item = capture['components']['schemas']['PhenotypeCapture']['properties']['entries']['items']
        self.assertEqual('number', item['properties']['value']['type'])
        self.assertTrue(item['properties']['value']['nullable'])
        self.assertNotIn('missingReason', item.get('required', []))
        series = yaml.safe_load(
            (root / 'Specification/BrAPI-GenX/Phenotyping/RepeatedMeasurement/Schemas'
             / 'MeasurementSeries.yaml').read_text())
        entry = series['components']['schemas']['MeasurementSeries']['properties']['measurements']['items']
        self.assertIn('value', entry['required'])
        self.assertEqual('number', entry['properties']['value']['type'])
        self.assertNotIn('nullable', entry['properties']['value'])
        self.assertNotIn('missingReason', entry['properties'])
        for module, decision in (
            ('PhenotypeCapture', 'D-33'),
            ('RepeatedMeasurement', 'D-73'),
            ('PhenotypeAnnotation', 'D-131'),
        ):
            group = (root / 'Specification/BrAPI-GenX/Phenotyping' /
                     module / 'GroupDescription.md').read_text()
            self.assertIn('STRUCTURAL_DRAFT', group)
            self.assertIn(decision, group)

    def test_geospatial_source_evidence_groups_are_pinned(self):
        self.assertTrue({
            'Geospatial/LocationGeometry', 'Geospatial/FieldGeometry',
            'Geospatial/CrsTransform', 'Geospatial/FieldBoundary',
        }.issubset(REVIEWED))

    def test_location_geometry_and_payload_verification_are_distinct(self):
        import yaml
        root = Path(__file__).resolve().parents[1]
        source = yaml.safe_load((root / 'Specification/BrAPI-Core/Locations/Schemas'
                                 / 'LocationNewRequest.yaml').read_text())
        official = source['components']['schemas']['LocationNewRequest']['properties']
        self.assertIn('coordinates', official)
        self.assertIn('geoJSON', official['coordinates']['$ref'])
        self.assertIn('coordinateUncertainty', official)
        for name in ('LocationGeometry', 'FieldBoundary'):
            with self.subTest(name=name):
                candidate = yaml.safe_load(
                    (root / 'Specification/BrAPI-GenX/Geospatial' /
                     name / 'Schemas' / (name + '.yaml')).read_text())
                properties = candidate['components']['schemas'][name]['properties']
                self.assertIn('geometryUri', properties)
                self.assertNotIn('checksum', properties)
                group = (root / 'Specification/BrAPI-GenX/Geospatial' /
                         name / 'GroupDescription.md').read_text()
                self.assertIn('STRUCTURAL_DRAFT', group)
                self.assertIn('payload integrity', group)
        geometry = yaml.safe_load(
            (root / 'Specification/BrAPI-GenX/Geospatial/FieldGeometry/Schemas'
             / 'FieldGeometry.yaml').read_text())
        self.assertEqual('object', geometry['components']['schemas']['FieldGeometry']
                         ['properties']['geometry']['type'])
        self.assertNotIn('fieldDbId',
                         geometry['components']['schemas']['FieldGeometry']['properties'])
        transform = yaml.safe_load(
            (root / 'Specification/BrAPI-GenX/Geospatial/CrsTransform/Schemas'
             / 'CrsTransform.yaml').read_text())
        self.assertEqual('string', transform['components']['schemas']['CrsTransform']
                         ['properties']['parameters']['type'])

    def test_instrumentation_device_quality_groups_are_reviewed(self):
        self.assertTrue({
            'Instrumentation/CalibrationQuality', 'Instrumentation/SensorDevice',
            'Instrumentation/TelemetryNormalization', 'Instrumentation/EdgeGatewayHealth',
        }.issubset(REVIEWED))

    def test_instrumentation_route_docs_match_source_operation_identity(self):
        import yaml
        root = Path(__file__).resolve().parents[1]
        for name, number in (
            ('CalibrationQuality', '150'),
            ('SensorDevice', '149'),
            ('TelemetryNormalization', '148'),
            ('EdgeGatewayHealth', '151'),
        ):
            with self.subTest(module=name):
                module = root / 'Specification/BrAPI-GenX/Instrumentation' / name
                paths = yaml.safe_load((module / (name + '_GET_POST.yaml')).read_text())['paths']
                source_route, ops = next(iter(paths.items()))
                route = '/genx/v1' + source_route
                opid = ops['get']['operationId']
                readme = (module / 'README.md').read_text()
                rfc = (root / 'Specification/BrAPI-GenX/RFCs' /
                       ('RFC-' + number + '-' + name + '.md')).read_text()
                for prose in (readme, rfc):
                    self.assertIn(route, prose)
                    self.assertIn(opid, prose)
                candidate = yaml.safe_load((module / 'Schemas' /
                                             (name + '.yaml')).read_text())
                self.assertNotIn('researchAssetDbId',
                    candidate['components']['schemas'][name]['properties'])
                self.assertIn('STRUCTURAL_DRAFT',
                    (module / 'GroupDescription.md').read_text())

    def test_environmental_source_evidence_is_pinned(self):
        self.assertTrue({
            'Environment/WeatherObservations', 'Environment/WeatherForecast',
            'Environment/ClimateNormals', 'Environment/SoilProfile',
            'Environment/WaterBalance',
        }.issubset(REVIEWED))

    def test_weather_climate_soil_water_accounting_limits(self):
        import yaml
        root = Path(__file__).resolve().parents[1]
        def schema(folder, record):
            filename = root / 'Specification/BrAPI-GenX/Environment' / folder
            data = yaml.safe_load((filename / 'Schemas' / (record + '.yaml')).read_text())
            return data['components']['schemas'][record]
        observed = schema('WeatherObservations', 'WeatherObservation')
        self.assertIn('measurements', observed['required'])
        self.assertNotIn('minItems', observed['properties']['measurements'])
        forecast = schema('WeatherForecast', 'WeatherForecast')
        for time in ('forecastedAt', 'validFrom', 'validTo'):
            self.assertIn(time, forecast['required'])
        self.assertNotIn('weatherObservationDbId', forecast['properties'])
        normal = schema('ClimateNormals', 'ClimateNormal')
        self.assertEqual('string', normal['properties']['period']['type'])
        soil = schema('SoilProfile', 'SoilProfile')
        self.assertNotIn('samplingDepth', soil['properties'])
        water = schema('WaterBalance', 'WaterBalance')
        for column in ('periodStart', 'periodEnd', 'precipitationMm',
                       'irrigationMm', 'storageChangeMm'):
            self.assertIn(column, water['properties'])
            self.assertNotIn(column, water['required'])
        for name, decision in (
            ('WeatherObservations', 'D-27'),
            ('WeatherForecast', 'D-91'),
            ('ClimateNormals', 'D-97'),
            ('SoilProfile', 'D-67'),
            ('WaterBalance', 'D-204'),
        ):
            with self.subTest(group=name):
                group = (root / 'Specification/BrAPI-GenX/Environment' /
                         name / 'GroupDescription.md').read_text()
                self.assertIn('STRUCTURAL_DRAFT', group)
                self.assertIn(decision, group)

    def test_plant_health_source_claims_are_pinned(self):
        root = Path(__file__).resolve().parents[1]
        self.assertTrue({'PlantHealth/DiseaseObservation',
                         'PlantHealth/DiagnosticEvidence',
                         'PlantHealth/FieldScouting',
                         'PlantHealth/DiseaseResistance'}.issubset(REVIEWED))
        source = (root / 'Specification/BrAPI-Phenotyping/Observations' /
                  'Observations_GET_POST_PUT.yaml').read_text()
        self.assertIn('/observations:', source)
        for name, decision in (
            ('DiseaseObservation', 'D-367'),
            ('DiagnosticEvidence', 'D-370'),
            ('FieldScouting', 'D-220'),
            ('DiseaseResistance', 'D-379'),
        ):
            group = (root / 'Specification/BrAPI-GenX/PlantHealth' /
                     name / 'GroupDescription.md').read_text()
            self.assertIn('STRUCTURAL_DRAFT', group)
            self.assertIn(decision, group)
            self.assertIn('**Sources:**', group)
        for name in ('DiseaseObservation', 'DiseaseResistance'):
            readme = (root / 'Specification/BrAPI-GenX/PlantHealth' /
                      name / 'README.md').read_text()
            self.assertIn('/brapi/v2/observations', readme)
        scouting = (root / 'Specification/BrAPI-GenX/RFCs' /
                    'RFC-074-Field-Scouting.md').read_text()
        self.assertIn('does not implement typed references', ' '.join(scouting.split()))

    def test_plant_health_image_and_alert_reviewed(self):
        root = Path(__file__).resolve().parents[1]
        modules = ('CropHealthImage', 'IpmStrategy', 'PestDiseaseRisk',
                   'ThresholdAlert')
        self.assertTrue({f'PlantHealth/{name}' for name in modules}.issubset(REVIEWED))
        image_source = (root / 'Specification/BrAPI-Phenotyping/Images' /
                        'Images_GET_POST.yaml').read_text()
        self.assertIn('/images:', image_source)
        for name, decision in (
            ('CropHealthImage', 'D-382'), ('IpmStrategy', 'D-373'),
            ('PestDiseaseRisk', 'D-397'), ('ThresholdAlert', 'D-376')
        ):
            doc = (root / 'Specification/BrAPI-GenX/PlantHealth' /
                   name / 'GroupDescription.md').read_text()
            self.assertIn('STRUCTURAL_DRAFT', doc)
            self.assertIn(decision, doc)
        readme = (root / 'Specification/BrAPI-GenX/PlantHealth' /
                  'CropHealthImage/README.md').read_text()
        self.assertIn('/brapi/v2/images', readme)
        rfc = (root / 'Specification/BrAPI-GenX/RFCs' /
               'RFC-128-CropHealthImage.md').read_text()
        self.assertIn('/brapi/v2/images', rfc)

    def test_crop_operation_source_boundaries_are_pinned(self):
        root = Path(__file__).resolve().parents[1]
        entries = (
            ('HarvestRecords', 'D-30', 'HarvestRecord'),
            ('IrrigationOperation', 'D-69', 'IrrigationEvent'),
            ('PlantingOperation', 'D-196', 'PlantingOperation'),
            ('SprayApplication', 'D-241', 'SprayApplication'),
        )
        for folder, decision, resource in entries:
            with self.subTest(module=folder):
                self.assertIn(f'CropProduction/{folder}', REVIEWED)
                path = (root / 'Specification/BrAPI-GenX/CropProduction' /
                        folder / 'GroupDescription.md')
                text = path.read_text()
                self.assertIn('STRUCTURAL_DRAFT', text)
                self.assertIn(decision, text)
                self.assertIn(resource, text)
        for name in ('RFC-024-Irrigation-Operation.md', 'RFC-081-Spray-Application.md'):
            path = root / 'Specification/BrAPI-GenX/RFCs' / name
            text = ' '.join(path.read_text().split())
            self.assertIn('plain strings' if name.startswith('RFC-024')
                          else 'untyped', text)

    def test_crop_input_and_forecast_group_evidence(self):
        root = Path(__file__).resolve().parents[1]
        groups = (
            ('FertilizerApplication', 'D-75'),
            ('Tillage', 'D-112'),
            ('YieldForecast', 'D-400'),
            ('IrrigationAdvice', 'D-391'),
        )
        for module, decision in groups:
            with self.subTest(module=module):
                self.assertIn(f'CropProduction/{module}', REVIEWED)
                content = (root / 'Specification/BrAPI-GenX/CropProduction' /
                           module / 'GroupDescription.md').read_text()
                self.assertIn('STRUCTURAL_DRAFT', content)
                self.assertIn(decision, content)
        candidate = (root / 'Specification/BrAPI-GenX/CropProduction' /
                     'IrrigationAdvice/IrrigationAdvice_GET_POST.yaml').read_text()
        rfc = (root / 'Specification/BrAPI-GenX/RFCs' /
               'RFC-131-IrrigationAdvice.md').read_text()
        self.assertIn('/irrigation-advices:', candidate)
        self.assertIn('genxListIrrigationAdvices', rfc)
        self.assertNotIn('/genx/v1/irrigation-advice`', rfc)

    def test_crop_cycle_sowing_and_constraint_reviewed(self):
        root = Path(__file__).resolve().parents[1]
        modules = (
            ('CropCycle', 'D-84'), ('SowingWindow', 'D-388'),
            ('CropSuitability', 'D-403'), ('LocalConstraint', 'D-415'),
        )
        for module, decision in modules:
            with self.subTest(module=module):
                self.assertIn(f'CropProduction/{module}', REVIEWED)
                content = (root / 'Specification/BrAPI-GenX/CropProduction' /
                           module / 'GroupDescription.md').read_text()
                self.assertIn('STRUCTURAL_DRAFT', content)
                self.assertIn(decision, content)
        rfc = (root / 'Specification/BrAPI-GenX/RFCs' /
               'RFC-139-LocalConstraint.md').read_text()
        self.assertIn('cannot itself enforce', rfc)
        cycle = (root / 'Specification/BrAPI-GenX/RFCs' /
                 'RFC-029-Crop-Cycle.md').read_text()
        self.assertIn('no typed', ' '.join(cycle.split()))

    def test_remaining_crop_production_groups_and_nutrient_route(self):
        root = Path(__file__).resolve().parents[1]
        for group, decision in (
            ('Farm', 'D-205'), ('NutrientAdvice', 'D-394'),
            ('CropRecommendation', 'D-385'),
        ):
            with self.subTest(group=group):
                self.assertIn('CropProduction/' + group, REVIEWED)
                doc = (root / 'Specification/BrAPI-GenX/CropProduction' /
                       group / 'GroupDescription.md').read_text()
                self.assertIn('STRUCTURAL_DRAFT', doc)
                self.assertIn(decision, doc)
        source = (root / 'Specification/BrAPI-GenX/CropProduction' /
                  'NutrientAdvice/NutrientAdvice_GET_POST.yaml').read_text()
        rfc = (root / 'Specification/BrAPI-GenX/RFCs' /
               'RFC-132-NutrientAdvice.md').read_text()
        self.assertIn('/nutrient-advices:', source)
        self.assertIn('/genx/v1/nutrient-advices', rfc)
        self.assertNotIn('/genx/v1/nutrient-advice`', rfc)
        farm = (root / 'Specification/BrAPI-GenX/RFCs' /
                'RFC-069-Farm.md').read_text()
        self.assertIn('does not encode a farm-membership', farm)


    def test_crop_production_rfc_route_and_operation_parity(self):
        """Pinned CropProduction RFCs, module overviews and source YAML agree.

        Prevent reintroducing the routing drift seen in RFC-131 and RFC-132.
        This checks documented contract identity, not interoperability maturity.
        """
        import re
        import yaml

        root = Path(__file__).resolve().parents[1]
        contract_re = re.compile(
            r'`((?:GET|POST|PUT|PATCH|DELETE) /genx/v1/[^`]+)` '
            r'\(`(genx[A-Za-z0-9]+)`\)'
        )
        candidates = (
            ('CropCycle', '029-Crop-Cycle'),
            ('CropRecommendation', '129-CropRecommendation'),
            ('CropSuitability', '135-CropSuitability'),
            ('Farm', '069-Farm'),
            ('FertilizerApplication', '026-Fertilizer-Application'),
            ('HarvestRecords', '011-Harvest-Records'),
            ('IrrigationAdvice', '131-IrrigationAdvice'),
            ('IrrigationOperation', '024-Irrigation-Operation'),
            ('LocalConstraint', '139-LocalConstraint'),
            ('LotLedger', '003-Seed-Lot-Ledger'),
            ('NutrientAdvice', '132-NutrientAdvice'),
            ('PlantingOperation', '066-Planting-Operation'),
            ('SowingWindow', '130-SowingWindow'),
            ('SprayApplication', '081-Spray-Application'),
            ('Tillage', '038-Tillage'),
            ('YieldForecast', '134-YieldForecast'),
        )
        spec_root = root / 'Specification/BrAPI-GenX'
        for name, rfc_number in candidates:
            with self.subTest(module=name):
                folder = spec_root / 'CropProduction' / name
                overview = (folder / 'README.md').read_text()
                rfc = (spec_root / 'RFCs' / ('RFC-' + rfc_number + '.md')).read_text()
                readme_operations = set(contract_re.findall(' '.join(overview.split())))
                rfc_operations = set(contract_re.findall(' '.join(rfc.split())))
                self.assertTrue(readme_operations, msg=name + ' missing documented routes')
                self.assertEqual(readme_operations, rfc_operations,
                                 msg=name + ' README / RFC route disagreement')
                published = set()
                for path in folder.glob('*.yaml'):
                    spec = yaml.safe_load(path.read_text())
                    for route, operations in spec.get('paths', {}).items():
                        for method, operation in operations.items():
                            if method in ('get', 'post', 'put', 'patch', 'delete'):
                                published.add((method.upper() + ' /genx/v1' + route,
                                               operation.get('operationId')))
                self.assertEqual(readme_operations, published,
                                 msg=name + ' README / YAML source disagreement')

    def test_research_review_and_evidence_groups_are_pinned(self):
        root = Path(__file__).resolve().parents[1]
        groups = (
            ('HumanReview', 'D-406'), ('ExplanationEvidence', 'D-409'),
            ('EvidencePack', 'D-364'), ('OutcomeFeedback', 'D-412'),
        )
        for name, decision in groups:
            with self.subTest(module=name):
                self.assertIn(f'Research/{name}', REVIEWED)
                description = (root / 'Specification/BrAPI-GenX/Research' /
                               name / 'GroupDescription.md').read_text()
                self.assertIn('STRUCTURAL_DRAFT', description)
                self.assertIn(decision, description)
                self.assertIn('**Sources:**', description)

    def test_analysis_method_and_result_evidence_pinned(self):
        root = Path(__file__).resolve().parents[1]
        for module, decision in (
            ('AnalysisMethods', 'D-24'), ('AnalysisResult', 'D-133'),
            ('MixedModel', 'D-142'), ('PcaResult', 'D-157'),
        ):
            with self.subTest(module=module):
                self.assertIn('Research/' + module, REVIEWED)
                description = (root / 'Specification/BrAPI-GenX/Research' /
                               module / 'GroupDescription.md').read_text()
                self.assertIn('STRUCTURAL_DRAFT', description)
                self.assertIn(decision, description)
                self.assertIn('**Sources:**', description)

    def test_research_artifact_protocol_publication_evidence(self):
        root = Path(__file__).resolve().parents[1]
        for module, decision in (
            ('ArtifactCatalogue', 'D-352'), ('ProtocolLibrary', 'D-355'),
            ('PublicationReview', 'D-358'), ('ResearchAssets', 'D-45'),
        ):
            with self.subTest(module=module):
                self.assertIn('Research/' + module, REVIEWED)
                doc = (root / 'Specification/BrAPI-GenX/Research' /
                       module / 'GroupDescription.md').read_text()
                self.assertIn('STRUCTURAL_DRAFT', doc)
                self.assertIn(decision, doc)
        rfc = (root / 'Specification/BrAPI-GenX/RFCs' /
               'RFC-016-Research-Assets.md').read_text()
        self.assertIn('no typed BrAPI data-resource references', ' '.join(rfc.split()))

    def test_research_reference_deferred_program_authority(self):
        root = Path(__file__).resolve().parents[1]
        for name, decision, status in (
            ('Project', 'D-265', 'STRUCTURAL_DRAFT'),
            ('ResearchLocation', 'D-298', 'STRUCTURAL_DRAFT'),
            ('ResearchProgram', 'D-BP-12', 'DEFERRED'),
        ):
            with self.subTest(module=name):
                self.assertIn('Research/' + name, REVIEWED)
                doc = (root / 'Specification/BrAPI-GenX/Research' /
                       name / 'GroupDescription.md').read_text()
                self.assertIn(status, doc)
                self.assertIn(decision, doc)
        historical = (root / 'Specification/BrAPI-GenX/RFCs' /
                      'RFC-098-Research-Program.md').read_text()
        self.assertIn('deferred under D-BP-12', historical)
        location = (root / 'Specification/BrAPI-GenX/RFCs' /
                    'RFC-100-Research-Location.md').read_text()
        self.assertIn('already defines', location)

    def test_genebank_storage_viability_regeneration_safety_evidence(self):
        root = Path(__file__).resolve().parents[1]
        for module, decision in (
            ('GenebankStorage', 'D-42'), ('ViabilityTesting', 'D-60'),
            ('Regeneration', 'D-106'), ('SafetyDuplication', 'D-99'),
        ):
            with self.subTest(module=module):
                self.assertIn('Germplasm/' + module, REVIEWED)
                doc = (root / 'Specification/BrAPI-GenX/Germplasm' /
                       module / 'GroupDescription.md').read_text()
                self.assertIn('STRUCTURAL_DRAFT', doc)
                self.assertIn(decision, doc)
                self.assertIn('**Sources:**', doc)

    def test_germplasm_transfer_disposal_quarantine_duplicate_review(self):
        root = Path(__file__).resolve().parents[1]
        for module, decision in (
            ('Acquisition', 'D-121'), ('CustodyTransfer', 'D-187'),
            ('DisposalRecord', 'D-193'), ('Quarantine', 'D-87'),
            ('DuplicateReview', 'D-310'),
        ):
            with self.subTest(module=module):
                self.assertIn('Germplasm/' + module, REVIEWED)
                doc = (root / 'Specification/BrAPI-GenX/Germplasm' /
                       module / 'GroupDescription.md').read_text()
                self.assertIn('STRUCTURAL_DRAFT', doc)
                self.assertIn(decision, doc)
        rfc = (root / 'Specification/BrAPI-GenX/RFCs' /
               'RFC-104-Duplicate-Review.md').read_text()
        self.assertIn('no validated BrAPI', ' '.join(rfc.split()))

    def test_genotyping_assay_design_execution_vendor_probe_evidence(self):
        root = Path(__file__).resolve().parents[1]
        genx = root / 'Specification/BrAPI-GenX'
        cases = (
            ('AssayDesign', 'AssayDesign', 'D-181', 'assayDesignDbId'),
            ('AssayExecution', 'AssayExecution', 'D-337', 'assayExecutionDbId'),
            ('VendorOrder', 'VendorOrderRecord', 'D-217', 'vendorOrderDbId'),
            ('MarkerProbe', 'MarkerProbe', 'D-211', 'markerProbeDbId'),
        )
        for module, resource, decision, identifier in cases:
            with self.subTest(module=module):
                self.assertIn('Genotyping/' + module, REVIEWED)
                folder = genx / 'Genotyping' / module
                doc = (folder / 'GroupDescription.md').read_text()
                self.assertIn('STRUCTURAL_DRAFT', doc)
                self.assertIn(decision, doc)
                self.assertIn('**Sources:**', doc)
                schema = yaml.safe_load(
                    (folder / 'Schemas' / (module + '.yaml')).read_text()
                )['components']['schemas'][resource]
                self.assertEqual(set(schema['required']), {identifier, 'status'})
                self.assertIn('provenance', schema['properties'])

        assay = yaml.safe_load(
            (genx / 'Genotyping/AssayExecution/Schemas/AssayExecution.yaml').read_text()
        )['components']['schemas']['AssayExecution']
        self.assertIn('assayDbId', assay['properties'])
        self.assertNotIn('assayDbId', assay['required'])
        self.assertNotIn('assayDesignDbId', assay['properties'])
        vendor = yaml.safe_load(
            (genx / 'Genotyping/VendorOrder/Schemas/VendorOrder.yaml').read_text()
        )['components']['schemas']['VendorOrderRecord']
        for missing in ('sampleDbId', 'genomicDatasetDbId', 'orderId', 'serviceIds'):
            self.assertNotIn(missing, vendor['properties'])
        official_vendor = yaml.safe_load(
            (root / 'Specification/BrAPI-Genotyping/VendorSamples/'
             'Vendor_Orders_GET_POST.yaml').read_text()
        )
        self.assertIn('/vendor/orders', official_vendor['paths'])
        self.assertTrue({'get', 'post'}.issubset(
            official_vendor['paths']['/vendor/orders']))
        vendor_rfc = (genx / 'RFCs/RFC-073-Vendor-Order.md').read_text()
        vendor_readme = (
            genx / 'Genotyping/VendorOrder/README.md'
        ).read_text()
        self.assertIn('/brapi/v2/vendor/orders', vendor_rfc)
        self.assertIn('/brapi/v2/vendor/orders', vendor_readme)
        self.assertNotIn('BrAPI v2.1 has no vendor order record', vendor_readme)

        official_markers = yaml.safe_load(
            (root / 'Specification/BrAPI-Genotyping/GenomeMaps/'
             'MarkerPositions_GET.yaml').read_text()
        )
        self.assertIn('variantDbId', [
            p.get('name') for p in
            official_markers['paths']['/markerpositions']['get']['parameters']
            if isinstance(p, dict)
        ])
        marker = yaml.safe_load(
            (genx / 'Genotyping/MarkerProbe/Schemas/MarkerProbe.yaml').read_text()
        )['components']['schemas']['MarkerProbe']
        self.assertIn('markerDbId', marker['properties'])
        self.assertNotIn('markerDbId', marker['required'])
        self.assertIn('variantDbId', (
            genx / 'RFCs/RFC-071-Marker-Probe.md'
        ).read_text())


    def test_genomic_dataset_vcf_export_source_identity(self):
        root = Path(__file__).resolve().parents[1]
        genx = root / 'Specification/BrAPI-GenX'
        cases = (
            ('GenomicDatasets', 'GenomicDataset', 'D-36',
             {'genomicDatasetDbId', 'datasetName', 'datasetType',
              'referenceAssembly', 'status'}),
            ('VcfExport', 'VcfExport', 'D-340',
             {'vcfExportDbId', 'status'}),
        )
        for module, resource, decision, required in cases:
            with self.subTest(module=module):
                self.assertIn('Genotyping/' + module, REVIEWED)
                folder = genx / 'Genotyping' / module
                doc = (folder / 'GroupDescription.md').read_text()
                self.assertIn('STRUCTURAL_DRAFT', doc)
                self.assertIn(decision, doc)
                self.assertIn('**Sources:**', doc)
                schema = yaml.safe_load(
                    (folder / 'Schemas' / (resource + '.yaml')).read_text()
                )['components']['schemas'][resource]
                self.assertEqual(required, set(schema['required']))
                for absent in ('variantSetDbId', 'callSetDbId',
                               'variantMatrixDbId'):
                    self.assertNotIn(absent, schema['properties'])

        dataset = yaml.safe_load(
            (genx / 'Genotyping/GenomicDatasets/Schemas/GenomicDataset.yaml').read_text()
        )['components']['schemas']['GenomicDataset']
        self.assertEqual('string', dataset['properties']['referenceAssembly']['type'])
        for field in ('pipelineName', 'pipelineVersion', 'inputDigest',
                      'outputDigest', 'accessPolicy', 'releaseStatus'):
            self.assertNotIn(field, dataset['required'])
        exported = yaml.safe_load(
            (genx / 'Genotyping/VcfExport/Schemas/VcfExport.yaml').read_text()
        )['components']['schemas']['VcfExport']
        for absent in ('vcfImportDbId', 'genomicDatasetDbId',
                       'exportFileUri', 'outputDigest'):
            self.assertNotIn(absent, exported['properties'])
        self.assertNotIn('format', exported['required'])
        official = yaml.safe_load(
            (root / 'Specification/BrAPI-Genotyping/VariantSets/'
             'VariantSets_Extract_POST.yaml').read_text()
        )
        self.assertIn('post', official['paths']['/variantsets/extract'])
        self.assertIn('variantSetDbId', (
            genx / 'RFCs/RFC-013-Genomic-Datasets.md'
        ).read_text())
        self.assertIn('vcfImportDbId', (
            genx / 'RFCs/RFC-114-Vcf-Export.md'
        ).read_text())


    def test_genotype_qc_and_call_semantics_optional_links(self):
        root = Path(__file__).resolve().parents[1]
        genx = root / 'Specification/BrAPI-GenX'
        cases = (
            ('GenotypeQc', 'GenotypeQcReport', 'D-190', 'genotypeQcReportDbId',
             ('genomicDatasetDbId', 'vcfImportDbId', 'metrics')),
            ('GenotypeCallSemantics', 'GenotypeCallSemantics', 'D-214',
             'genotypeCallSemanticsDbId',
             ('callSetDbId', 'missingCallPolicy', 'zygosityEncoding',
              'confidenceThreshold')),
        )
        for module, resource, decision, identifier, optional in cases:
            with self.subTest(module=module):
                self.assertIn('Genotyping/' + module, REVIEWED)
                folder = genx / 'Genotyping' / module
                description = (folder / 'GroupDescription.md').read_text()
                self.assertIn('STRUCTURAL_DRAFT', description)
                self.assertIn(decision, description)
                self.assertIn('**Sources:**', description)
                schema = yaml.safe_load(
                    (folder / 'Schemas' / (resource + '.yaml')).read_text()
                )['components']['schemas'][resource]
                self.assertEqual({identifier, 'status'}, set(schema['required']))
                self.assertTrue(set(optional).issubset(schema['properties']))
                for field in optional:
                    self.assertNotIn(field, schema['required'])
                request = yaml.safe_load(
                    (folder / 'Schemas' / (resource + 'NewRequest.yaml')).read_text()
                )['components']['schemas'][resource + 'NewRequest']
                self.assertEqual({identifier}, set(request['required']))

        quality = yaml.safe_load(
            (genx / 'Genotyping/GenotypeQc/Schemas/GenotypeQcReport.yaml').read_text()
        )['components']['schemas']['GenotypeQcReport']
        self.assertEqual('object', quality['properties']['metrics']['type'])
        self.assertNotIn('properties', quality['properties']['metrics'])
        self.assertNotIn('verdict', quality['properties'])
        call = yaml.safe_load(
            (genx / 'Genotyping/GenotypeCallSemantics/Schemas/'
             'GenotypeCallSemantics.yaml').read_text()
        )['components']['schemas']['GenotypeCallSemantics']
        self.assertEqual('number',
                         call['properties']['confidenceThreshold']['type'])
        self.assertNotIn('minimum', call['properties']['confidenceThreshold'])
        self.assertNotIn('maximum', call['properties']['confidenceThreshold'])
        official = yaml.safe_load(
            (root / 'Specification/BrAPI-Genotyping/CallSets/'
             'CallSets_GET.yaml').read_text()
        )
        self.assertIn('get', official['paths']['/callsets'])
        self.assertIn('callSetDbId', [
            p.get('name') for p in official['paths']['/callsets']['get']['parameters']
            if isinstance(p, dict)])


    def test_variant_annotation_and_gwas_result_scientific_boundaries(self):
        root = Path(__file__).resolve().parents[1]
        genx = root / 'Specification/BrAPI-GenX'
        cases = (
            ('VariantAnnotation', 'VariantAnnotation', 'D-184',
             {'variantAnnotationDbId', 'status'}, {'variantAnnotationDbId'}),
            ('GwasResult', 'GwasResult', 'D-139',
             {'gwasResultDbId', 'analysisMethodDbId', 'status'},
             {'gwasResultDbId', 'analysisMethodDbId'}),
        )
        for module, resource, decision, response_required, request_required in cases:
            with self.subTest(module=module):
                self.assertIn('Genotyping/' + module, REVIEWED)
                folder = genx / 'Genotyping' / module
                description = (folder / 'GroupDescription.md').read_text()
                self.assertIn('STRUCTURAL_DRAFT', description)
                self.assertIn(decision, description)
                self.assertIn('**Sources:**', description)
                response = yaml.safe_load(
                    (folder / 'Schemas' / (resource + '.yaml')).read_text()
                )['components']['schemas'][resource]
                request = yaml.safe_load(
                    (folder / 'Schemas' / (resource + 'NewRequest.yaml')).read_text()
                )['components']['schemas'][resource + 'NewRequest']
                self.assertEqual(response_required, set(response['required']))
                self.assertEqual(request_required, set(request['required']))
                for field in ('provenance', 'studyDbId'):
                    self.assertIn(field, response['properties'])
                    self.assertNotIn(field, response['required'])
                    self.assertNotIn(field, request['required'])

        annotated = yaml.safe_load(
            (genx / 'Genotyping/VariantAnnotation/Schemas/VariantAnnotation.yaml').read_text()
        )['components']['schemas']['VariantAnnotation']
        request = yaml.safe_load(
            (genx / 'Genotyping/VariantAnnotation/Schemas/'
             'VariantAnnotationNewRequest.yaml').read_text()
        )['components']['schemas']['VariantAnnotationNewRequest']
        for field in ('variantDbId', 'analysisMethodDbId', 'annotations'):
            self.assertIn(field, annotated['properties'])
            self.assertNotIn(field, annotated['required'])
            self.assertNotIn(field, request['required'])
        self.assertEqual('object', annotated['properties']['annotations']['type'])
        self.assertNotIn('properties', annotated['properties']['annotations'])
        self.assertNotIn('methodVersion', annotated['properties'])
        official = yaml.safe_load(
            (root / 'Specification/BrAPI-Genotyping/Variants/Schemas/Variant.yaml').read_text()
        )['components']['schemas']['Variant']
        self.assertIn('additionalInfo', official['properties'])
        self.assertIn('variantDbId', official['required'])
        self.assertIn('D-184', (
            genx / 'RFCs/RFC-062-Variant-Annotation.md').read_text())

        gwas = yaml.safe_load(
            (genx / 'Genotyping/GwasResult/Schemas/GwasResult.yaml').read_text()
        )['components']['schemas']['GwasResult']
        new_gwas = yaml.safe_load(
            (genx / 'Genotyping/GwasResult/Schemas/GwasResultNewRequest.yaml').read_text()
        )['components']['schemas']['GwasResultNewRequest']
        for field in ('significantMarkers', 'topPValue', 'jobDbId', 'resultData'):
            self.assertIn(field, gwas['properties'])
            self.assertNotIn(field, gwas['required'])
            self.assertNotIn(field, new_gwas['required'])
        self.assertEqual('integer', gwas['properties']['significantMarkers']['type'])
        self.assertNotIn('minimum', gwas['properties']['significantMarkers'])
        self.assertEqual('number', gwas['properties']['topPValue']['type'])
        for constraint in ('minimum', 'maximum'):
            self.assertNotIn(constraint, gwas['properties']['topPValue'])
        self.assertEqual('object', gwas['properties']['resultData']['type'])
        self.assertNotIn('properties', gwas['properties']['resultData'])
        for field in ('methodVersion', 'genomicDatasetDbId'):
            self.assertNotIn(field, gwas['properties'])
            self.assertNotIn(field, new_gwas['properties'])
        method = yaml.safe_load(
            (genx / 'Research/AnalysisMethods/Schemas/AnalysisMethod.yaml').read_text()
        )['components']['schemas']['AnalysisMethod']
        self.assertIn('methodVersion', method['required'])
        self.assertIn('D-140', (
            genx / 'RFCs/RFC-047-Gwas-Result.md').read_text())


    def test_heritability_and_gxe_require_statistical_context_not_assumed(self):
        root = Path(__file__).resolve().parents[1]
        genx = root / 'Specification/BrAPI-GenX'
        cases = (
            ('Heritability', 'HeritabilityEstimate', 'D-148',
             'heritabilityEstimateDbId', 'heritabilityValue'),
            ('GxeAnalysis', 'GxeAnalysisResult', 'D-151',
             'gxeAnalysisResultDbId', 'gxeEffect'),
        )
        for module, resource, decision, identifier, measurement in cases:
            with self.subTest(module=module):
                self.assertIn('Breeding/' + module, REVIEWED)
                folder = genx / 'Breeding' / module
                description = (folder / 'GroupDescription.md').read_text()
                self.assertIn('STRUCTURAL_DRAFT', description)
                self.assertIn(decision, description)
                self.assertIn('**Sources:**', description)
                response = yaml.safe_load(
                    (folder / 'Schemas' / (resource + '.yaml')).read_text()
                )['components']['schemas'][resource]
                request = yaml.safe_load(
                    (folder / 'Schemas' / (resource + 'NewRequest.yaml')).read_text()
                )['components']['schemas'][resource + 'NewRequest']
                self.assertEqual({identifier, 'analysisMethodDbId', 'status'},
                                 set(response['required']))
                self.assertEqual({identifier, 'analysisMethodDbId'},
                                 set(request['required']))
                for field in ('jobDbId', 'studyDbId', 'traitDbId',
                              measurement, 'provenance'):
                    self.assertIn(field, response['properties'])
                    self.assertNotIn(field, response['required'])
                    self.assertNotIn(field, request['required'])
                for field in ('methodVersion', 'genomicDatasetDbId'):
                    self.assertNotIn(field, response['properties'])
                    self.assertNotIn(field, request['properties'])
                self.assertIn('type', response['properties'][measurement])

        estimate = yaml.safe_load(
            (genx / 'Breeding/Heritability/Schemas/HeritabilityEstimate.yaml'
             ).read_text()
        )['components']['schemas']['HeritabilityEstimate']
        self.assertEqual('number', estimate['properties']['heritabilityValue']['type'])
        for constraint in ('minimum', 'maximum', 'exclusiveMinimum',
                           'exclusiveMaximum'):
            self.assertNotIn(constraint, estimate['properties']['heritabilityValue'])
        self.assertIn('D-149', (
            genx / 'RFCs/RFC-050-Heritability.md').read_text())

        gxe = yaml.safe_load(
            (genx / 'Breeding/GxeAnalysis/Schemas/GxeAnalysisResult.yaml').read_text()
        )['components']['schemas']['GxeAnalysisResult']
        self.assertEqual('object', gxe['properties']['gxeEffect']['type'])
        self.assertNotIn('properties', gxe['properties']['gxeEffect'])
        self.assertIn('D-152', (
            genx / 'RFCs/RFC-051-Gxe-Analysis.md').read_text())

        method = yaml.safe_load(
            (genx / 'Research/AnalysisMethods/Schemas/AnalysisMethod.yaml').read_text()
        )['components']['schemas']['AnalysisMethod']
        self.assertIn('methodVersion', method['required'])


    def test_genomic_prediction_and_selection_are_not_verified_decisions(self):
        root = Path(__file__).resolve().parents[1]
        genx = root / 'Specification/BrAPI-GenX'
        cases = (
            ('GenomicPrediction', 'genomicPredictionDbId', 'D-160',
             ('predictions', 'accuracy', 'traitDbId')),
            ('GenomicSelection', 'genomicSelectionDbId', 'D-163',
             ('selectedGermplasm', 'selectionThreshold')),
        )
        for name, identifier, decision, optional_fields in cases:
            with self.subTest(group=name):
                folder = genx / 'Breeding' / name
                self.assertIn('Breeding/' + name, REVIEWED)
                description = (folder / 'GroupDescription.md').read_text()
                self.assertIn('STRUCTURAL_DRAFT', description)
                self.assertIn(decision, description)
                self.assertIn('**Sources:**', description)
                record = yaml.safe_load(
                    (folder / 'Schemas' / (name + '.yaml')).read_text()
                )['components']['schemas'][name]
                request = yaml.safe_load(
                    (folder / 'Schemas' / (name + 'NewRequest.yaml')).read_text()
                )['components']['schemas'][name + 'NewRequest']
                self.assertEqual({identifier, 'analysisMethodDbId', 'status'},
                                 set(record['required']))
                self.assertEqual({identifier, 'analysisMethodDbId'},
                                 set(request['required']))
                for field in (*optional_fields, 'studyDbId', 'jobDbId', 'provenance'):
                    self.assertIn(field, record['properties'])
                    self.assertNotIn(field, record['required'])
                    self.assertNotIn(field, request['required'])
                for absent in ('methodVersion', 'genomicDatasetDbId'):
                    self.assertNotIn(absent, record['properties'])
                    self.assertNotIn(absent, request['properties'])

        predicted = yaml.safe_load(
            (genx / 'Breeding/GenomicPrediction/Schemas/GenomicPrediction.yaml'
             ).read_text()
        )['components']['schemas']['GenomicPrediction']
        self.assertEqual('object', predicted['properties']['predictions']['type'])
        self.assertNotIn('properties', predicted['properties']['predictions'])
        self.assertEqual('number', predicted['properties']['accuracy']['type'])
        for bound in ('minimum', 'maximum', 'exclusiveMinimum',
                      'exclusiveMaximum'):
            self.assertNotIn(bound, predicted['properties']['accuracy'])
        self.assertIn('D-161', (
            genx / 'RFCs/RFC-054-Genomic-Prediction.md').read_text())

        selection = yaml.safe_load(
            (genx / 'Breeding/GenomicSelection/Schemas/GenomicSelection.yaml'
             ).read_text()
        )['components']['schemas']['GenomicSelection']
        self.assertEqual('array', selection['properties']['selectedGermplasm']['type'])
        self.assertEqual('string',
                         selection['properties']['selectedGermplasm']['items']['type'])
        self.assertEqual('number', selection['properties']['selectionThreshold']['type'])
        self.assertIn('D-164', (
            genx / 'RFCs/RFC-055-Genomic-Selection.md').read_text())
        verdict = yaml.safe_load(
            (genx / 'Breeding/SelectionDecisions/Schemas/SelectionDecision.yaml'
             ).read_text()
        )['components']['schemas']['SelectionDecision']
        self.assertTrue({'decision', 'decisionDate', 'programReference'}.issubset(
            set(verdict['required'])))
        self.assertNotIn('decision', selection['properties'])


    def test_genetic_gain_and_stability_units_methods_and_optional_index(self):
        root = Path(__file__).resolve().parents[1]
        genx = root / 'Specification/BrAPI-GenX'
        gain_folder = genx / 'Breeding/GeneticGain'
        stability_folder = genx / 'Breeding/StabilityAnalysis'
        for name, folder, decision in (
            ('GeneticGain', gain_folder, 'D-136'),
            ('StabilityAnalysis', stability_folder, 'D-145'),
        ):
            with self.subTest(group=name):
                self.assertIn('Breeding/' + name, REVIEWED)
                description = (folder / 'GroupDescription.md').read_text()
                self.assertIn('STRUCTURAL_DRAFT', description)
                self.assertIn('**Sources:**', description)
                self.assertIn(decision, description)

        gain = yaml.safe_load(
            (gain_folder / 'Schemas/GeneticGainRecord.yaml').read_text()
        )['components']['schemas']['GeneticGainRecord']
        gain_req = yaml.safe_load(
            (gain_folder / 'Schemas/GeneticGainRecordNewRequest.yaml').read_text()
        )['components']['schemas']['GeneticGainRecordNewRequest']
        base = {'geneticGainRecordDbId', 'programDbId', 'traitDbId', 'gainValue'}
        self.assertEqual(base | {'status'}, set(gain['required']))
        self.assertEqual(base, set(gain_req['required']))
        self.assertEqual('number', gain['properties']['gainValue']['type'])
        for field in ('unit', 'period', 'method', 'provenance'):
            self.assertIn(field, gain['properties'])
            self.assertNotIn(field, gain['required'])
            self.assertNotIn(field, gain_req['required'])
        for field in ('analysisMethodDbId', 'methodVersion'):
            self.assertNotIn(field, gain['properties'])
            self.assertNotIn(field, gain_req['properties'])
        self.assertEqual('string', gain['properties']['unit']['type'])
        self.assertEqual('string', gain['properties']['period']['type'])
        self.assertIn('D-137', (
            genx / 'RFCs/RFC-046-Genetic-Gain.md').read_text())

        stability = yaml.safe_load(
            (stability_folder / 'Schemas/StabilityAnalysisResult.yaml').read_text()
        )['components']['schemas']['StabilityAnalysisResult']
        stab_req = yaml.safe_load(
            (stability_folder / 'Schemas/'
             'StabilityAnalysisResultNewRequest.yaml').read_text()
        )['components']['schemas']['StabilityAnalysisResultNewRequest']
        main = {'stabilityAnalysisResultDbId', 'analysisMethodDbId'}
        self.assertEqual(main | {'status'}, set(stability['required']))
        self.assertEqual(main, set(stab_req['required']))
        for field in ('stabilityIndex', 'traitDbId', 'studyDbId',
                      'jobDbId', 'provenance'):
            self.assertIn(field, stability['properties'])
            self.assertNotIn(field, stability['required'])
            self.assertNotIn(field, stab_req['required'])
        self.assertEqual('number', stability['properties']['stabilityIndex']['type'])
        for bound in ('minimum', 'maximum', 'exclusiveMinimum',
                      'exclusiveMaximum'):
            self.assertNotIn(bound, stability['properties']['stabilityIndex'])
        for field in ('methodVersion', 'genomicDatasetDbId'):
            self.assertNotIn(field, stability['properties'])
            self.assertNotIn(field, stab_req['properties'])
        self.assertIn('D-146', (
            genx / 'RFCs/RFC-049-Stability-Analysis.md').read_text())


    def test_relatedness_and_pedigree_matrix_evidence_is_optional(self):
        root = Path(__file__).resolve().parents[1]
        genx = root / 'Specification/BrAPI-GenX'
        cases = (
            ('Breeding/Kinship', 'KinshipMatrix', 'kinshipMatrixDbId',
             ('matrixRef', 'matrixDigest'), 'D-154'),
            ('Genotyping/GenomicRelationship', 'GenomicRelationship',
             'genomicRelationshipDbId', ('matrixRef', 'digest'), 'D-166'),
            ('Breeding/PedigreeAnalysis', 'PedigreeAnalysis',
             'pedigreeAnalysisDbId', ('pedigreeMetrics',), 'D-178'),
        )
        for module, resource, identifier, special, decision in cases:
            with self.subTest(module=module):
                self.assertIn(module, REVIEWED)
                folder = genx / module
                desc = (folder / 'GroupDescription.md').read_text()
                self.assertIn('STRUCTURAL_DRAFT', desc)
                self.assertIn('**Sources:**', desc)
                self.assertIn(decision, desc)
                response = yaml.safe_load(
                    (folder / 'Schemas' / (resource + '.yaml')).read_text()
                )['components']['schemas'][resource]
                request = yaml.safe_load(
                    (folder / 'Schemas' / (resource + 'NewRequest.yaml')).read_text()
                )['components']['schemas'][resource + 'NewRequest']
                self.assertEqual({identifier, 'analysisMethodDbId', 'status'},
                                 set(response['required']))
                self.assertEqual({identifier, 'analysisMethodDbId'},
                                 set(request['required']))
                for field in (*special, 'jobDbId', 'studyDbId', 'provenance'):
                    self.assertIn(field, response['properties'])
                    self.assertNotIn(field, response['required'])
                    self.assertNotIn(field, request['required'])
                for missing in ('methodVersion', 'genomicDatasetDbId',
                                'sampleOrder', 'referencePopulation'):
                    self.assertNotIn(missing, response['properties'])
                    self.assertNotIn(missing, request['properties'])

        kin = yaml.safe_load(
            (genx / 'Breeding/Kinship/Schemas/KinshipMatrix.yaml').read_text()
        )['components']['schemas']['KinshipMatrix']
        genomic = yaml.safe_load(
            (genx / 'Genotyping/GenomicRelationship/Schemas/'
             'GenomicRelationship.yaml').read_text()
        )['components']['schemas']['GenomicRelationship']
        self.assertEqual('string', kin['properties']['matrixDigest']['type'])
        self.assertNotIn('pattern', kin['properties']['matrixDigest'])
        self.assertEqual('string', genomic['properties']['digest']['type'])
        self.assertNotIn('pattern', genomic['properties']['digest'])
        for resource in (kin, genomic):
            self.assertEqual('string', resource['properties']['matrixRef']['type'])

        pedigree = yaml.safe_load(
            (genx / 'Breeding/PedigreeAnalysis/Schemas/'
             'PedigreeAnalysis.yaml').read_text()
        )['components']['schemas']['PedigreeAnalysis']
        self.assertEqual('object', pedigree['properties']['pedigreeMetrics']['type'])
        self.assertNotIn('properties', pedigree['properties']['pedigreeMetrics'])
        official = yaml.safe_load(
            (root / 'Specification/BrAPI-Germplasm/Germplasm/Schemas/'
             'Germplasm.yaml').read_text()
        )['components']['schemas']['Germplasm']
        self.assertIn('allOf', official)
        method = yaml.safe_load(
            (genx / 'Research/AnalysisMethods/Schemas/'
             'AnalysisMethod.yaml').read_text()
        )['components']['schemas']['AnalysisMethod']
        self.assertIn('methodVersion', method['required'])
        for rfc, deferred in (
            ('RFC-052-Kinship.md', 'D-155'),
            ('RFC-056-Genomic-Relationship.md', 'D-167'),
            ('RFC-060-Pedigree-Analysis.md', 'D-179'),
        ):
            self.assertIn(deferred, (genx / 'RFCs' / rfc).read_text())


    def test_haplotype_eqtl_methylation_scientific_payloads_are_opaque(self):
        root = Path(__file__).resolve().parents[1]
        genx = root / 'Specification/BrAPI-GenX'
        cases = (
            ('HaplotypeAnalysis', 'haplotypeAnalysisDbId', 'haplotypes',
             'D-175', 'RFC-059-Haplotype-Analysis.md'),
            ('ExpressionQtl', 'expressionQtlDbId', 'qtls',
             'D-172', 'RFC-058-Expression-Qtl.md'),
            ('MethylationAnalysis', 'methylationAnalysisDbId', 'regions',
             'D-169', 'RFC-057-Methylation-Analysis.md'),
        )
        for name, identity, result_field, decision, rfc in cases:
            with self.subTest(group=name):
                self.assertIn('Genotyping/' + name, REVIEWED)
                folder = genx / 'Genotyping' / name
                description = (folder / 'GroupDescription.md').read_text()
                self.assertIn('STRUCTURAL_DRAFT', description)
                self.assertIn('**Sources:**', description)
                self.assertIn(decision, description)
                response = yaml.safe_load(
                    (folder / 'Schemas' / (name + '.yaml')).read_text()
                )['components']['schemas'][name]
                request = yaml.safe_load(
                    (folder / 'Schemas' / (name + 'NewRequest.yaml')).read_text()
                )['components']['schemas'][name + 'NewRequest']
                self.assertEqual({identity, 'analysisMethodDbId', 'status'},
                                 set(response['required']))
                self.assertEqual({identity, 'analysisMethodDbId'},
                                 set(request['required']))
                for field in (result_field, 'jobDbId', 'studyDbId', 'provenance'):
                    self.assertIn(field, response['properties'])
                    self.assertNotIn(field, response['required'])
                    self.assertNotIn(field, request['required'])
                self.assertEqual('object',
                                 response['properties'][result_field]['type'])
                self.assertNotIn('properties',
                                 response['properties'][result_field])
                for absent in ('methodVersion', 'genomicDatasetDbId'):
                    self.assertNotIn(absent, response['properties'])
                    self.assertNotIn(absent, request['properties'])
                self.assertIn('no `genomicDatasetDbId`',
                              (genx / 'RFCs' / rfc).read_text())

        # Examples nested inside opaque objects must not become required
        # statistical, phasing or methylation fields by assertion.
        hap = yaml.safe_load(
            (genx / 'Genotyping/HaplotypeAnalysis/Schemas/'
             'HaplotypeAnalysis.yaml').read_text()
        )['components']['schemas']['HaplotypeAnalysis']
        eqtl = yaml.safe_load(
            (genx / 'Genotyping/ExpressionQtl/Schemas/'
             'ExpressionQtl.yaml').read_text()
        )['components']['schemas']['ExpressionQtl']
        methyl = yaml.safe_load(
            (genx / 'Genotyping/MethylationAnalysis/Schemas/'
             'MethylationAnalysis.yaml').read_text()
        )['components']['schemas']['MethylationAnalysis']
        for document, property_name in (
            (hap, 'haplotypes'), (eqtl, 'qtls'), (methyl, 'regions')
        ):
            self.assertNotIn('required',
                             document['properties'][property_name])
            self.assertNotIn('additionalProperties',
                             document['properties'][property_name])
        for key in ('pValue', 'pValueThreshold', 'methylationLevel',
                    'haplotypeLength', 'phaseConfidence', 'referenceAssembly'):
            for document in (hap, eqtl, methyl):
                self.assertNotIn(key, document['properties'])
        method = yaml.safe_load(
            (genx / 'Research/AnalysisMethods/Schemas/'
             'AnalysisMethod.yaml').read_text()
        )['components']['schemas']['AnalysisMethod']
        self.assertIn('methodVersion', method['required'])


    def test_image_phenology_and_vegetation_index_source_boundaries(self):
        root = Path(__file__).resolve().parents[1]
        genx = root / 'Specification/BrAPI-GenX'
        cases = (
            ('Phenotyping/ImageMetadata', 'ImageMetadata', 'D-93',
             {'imageMetadataDbId', 'imageDbId', 'capturedAt'}),
            ('Phenotyping/PhenologyObservation', 'PhenologyObservation',
             'D-78', {'phenologyObservationDbId', 'studyDbId',
                      'observationUnitDbId', 'observedAt', 'stage'}),
            ('Geospatial/VegetationIndex', 'VegetationIndex',
             'D-436', {'vegetationIndexDbId'}),
        )
        for module, name, decision, request_required in cases:
            with self.subTest(module=module):
                self.assertIn(module, REVIEWED)
                folder = genx / module
                desc = (folder / 'GroupDescription.md').read_text()
                self.assertIn('STRUCTURAL_DRAFT', desc)
                self.assertIn('**Sources:**', desc)
                self.assertIn(decision, desc)
                response = yaml.safe_load(
                    (folder / 'Schemas' / (name + '.yaml')).read_text()
                )['components']['schemas'][name]
                request = yaml.safe_load(
                    (folder / 'Schemas' / (name + 'NewRequest.yaml')).read_text()
                )['components']['schemas'][name + 'NewRequest']
                self.assertEqual(request_required,
                                 set(request['required']))
                self.assertEqual(request_required | {'status'},
                                 set(response['required']))

        image = yaml.safe_load(
            (genx / 'Phenotyping/ImageMetadata/Schemas/ImageMetadata.yaml'
             ).read_text()
        )['components']['schemas']['ImageMetadata']
        self.assertEqual('date-time', image['properties']['capturedAt']['format'])
        for field in ('camera', 'resolution', 'observationUnitDbId',
                      'studyDbId', 'provenance'):
            self.assertIn(field, image['properties'])
            self.assertNotIn(field, image['required'])
        self.assertEqual('string', image['properties']['resolution']['type'])
        official = yaml.safe_load(
            (root / 'Specification/BrAPI-Phenotyping/Images/Schemas/'
             'ImageNewRequest.yaml').read_text()
        )['components']['schemas']['ImageNewRequest']
        for overlapping in ('imageTimeStamp', 'imageHeight', 'imageWidth',
                            'imageLocation', 'observationUnitDbId',
                            'additionalInfo'):
            self.assertIn(overlapping, official['properties'])

        phen = yaml.safe_load(
            (genx / 'Phenotyping/PhenologyObservation/Schemas/'
             'PhenologyObservation.yaml').read_text()
        )['components']['schemas']['PhenologyObservation']
        self.assertIn('bbchCode', phen['properties'])
        self.assertNotIn('bbchCode', phen['required'])
        self.assertEqual('string', phen['properties']['stage']['type'])
        for attribute in ('enum', 'pattern'):
            self.assertNotIn(attribute, phen['properties']['stage'])
            self.assertNotIn(attribute, phen['properties']['bbchCode'])
        self.assertNotIn('measurementSeriesDbId', phen['properties'])

        vegetation = yaml.safe_load(
            (genx / 'Geospatial/VegetationIndex/Schemas/'
             'VegetationIndex.yaml').read_text()
        )['components']['schemas']['VegetationIndex']
        for field in ('indexType', 'indexName', 'acquisitionDate',
                      'crs', 'resolution', 'provenance'):
            self.assertIn(field, vegetation['properties'])
            self.assertNotIn(field, vegetation['required'])
        for unmodelled in ('indexValue', 'rasterRef', 'sourceImageDbId',
                           'algorithm', 'bandMapping'):
            self.assertNotIn(unmodelled, vegetation['properties'])
        self.assertNotIn('format',
                         vegetation['properties']['acquisitionDate'])
        ops = yaml.safe_load(
            (genx / 'Geospatial/VegetationIndex/'
             'VegetationIndex_GET_POST.yaml').read_text()
        )['paths']
        self.assertEqual(['/vegetation-indexes'], list(ops))
        self.assertEqual('genxListVegetationIndexes',
                         ops['/vegetation-indexes']['get']['operationId'])
        self.assertEqual('genxRegisterVegetationIndex',
                         ops['/vegetation-indexes']['post']['operationId'])
        overview = (genx / 'Geospatial/VegetationIndex/README.md').read_text()
        self.assertIn('GET /genx/v1/vegetation-indexes', overview)
        self.assertNotIn('GET /genx/v1/vegetation-index`', overview)


    def test_advancement_variety_not_scheme_or_regulatory_approval(self):
        root = Path(__file__).resolve().parents[1]
        genx = root / 'Specification/BrAPI-GenX'
        advance = genx / 'Breeding/PopulationAdvancement'
        variety = genx / 'Breeding/CandidateVarietyLifecycle'
        for module, decision in (
            ('Breeding/PopulationAdvancement', 'D-BP-10'),
            ('Breeding/CandidateVarietyLifecycle', 'D-115'),
        ):
            with self.subTest(module=module):
                self.assertIn(module, REVIEWED)
                text = (genx / module / 'GroupDescription.md').read_text()
                self.assertIn('STRUCTURAL_DRAFT', text)
                self.assertIn('**Sources:**', text)
                self.assertIn(decision, text)

        actual = yaml.safe_load(
            (advance / 'Schemas/PopulationAdvancement.yaml').read_text()
        )['components']['schemas']['PopulationAdvancement']
        request = yaml.safe_load(
            (advance / 'Schemas/PopulationAdvancementNewRequest.yaml').read_text()
        )['components']['schemas']['PopulationAdvancementNewRequest']
        base = {'populationAdvancementDbId', 'programReference',
                'populationReference', 'advancedAt'}
        self.assertEqual(base | {'status'}, set(actual['required']))
        self.assertEqual(base, set(request['required']))
        self.assertEqual('date', actual['properties']['advancedAt']['format'])
        for field in ('pipelineContext', 'schemeContext', 'provenance'):
            self.assertIn(field, actual['properties'])
            self.assertNotIn(field, actual['required'])
            self.assertNotIn(field, request['required'])
        for field in ('fromStageId', 'toStageId', 'decision', 'decisionDate'):
            self.assertNotIn(field, actual['properties'])
        for field in ('programReference', 'populationReference'):
            self.assertTrue(
                actual['properties'][field]['$ref'].endswith(
                    '/BrapiResourceReference'))
        decision = yaml.safe_load(
            (genx / 'Breeding/SelectionDecisions/Schemas/'
             'SelectionDecision.yaml').read_text()
        )['components']['schemas']['SelectionDecision']
        self.assertTrue({'decision', 'decisionDate'}.issubset(
            set(decision['required'])))

        registration = yaml.safe_load(
            (variety / 'Schemas/CandidateVarietyNewRequest.yaml').read_text()
        )['components']['schemas']['CandidateVarietyNewRequest']
        response = yaml.safe_load(
            (variety / 'Schemas/CandidateVariety.yaml').read_text()
        )['components']['schemas']['CandidateVariety']
        expected = {'candidateVarietyDbId', 'programDbId', 'varietyName'}
        self.assertEqual(expected, set(registration['required']))
        self.assertEqual(expected | {'status'}, set(response['required']))
        self.assertEqual('candidate',
                         registration['properties']['status']['default'])
        self.assertTrue({'registered', 'released'}.issubset(
            set(response['properties']['status']['enum'])))
        self.assertNotIn('registeredAt', registration['required'])
        for not_modelled in ('registrationAuthority', 'certificateId',
                             'germplasmDbId', 'breedingPipelineDbId'):
            self.assertNotIn(not_modelled, response['properties'])
            self.assertNotIn(not_modelled, registration['properties'])
        crossing = (genx / 'Breeding/CrossingSchedule/README.md').read_text()
        self.assertIn('D-BP-11', crossing)
        self.assertIn('Deferred', crossing)
        self.assertNotIn('Breeding/CrossingSchedule', REVIEWED)


    def test_environment_soil_and_remote_sensing_are_not_validated_measurements(self):
        root = Path(__file__).resolve().parents[1]
        genx = root / 'Specification/BrAPI-GenX'
        cases = (
            ('Environment/ExtremeWeather', 'ExtremeWeatherEvent',
             'D-124', {'extremeWeatherEventDbId', 'locationDbId',
                       'occurredAt', 'eventType'}),
            ('Environment/SoilChemistry', 'SoilChemistry', 'D-229',
             {'soilChemistryDbId'}),
            ('Geospatial/RemoteSensingMetadata', 'RemoteSensingMetadata',
             'D-433', {'remoteSensingMetadataDbId'}),
        )
        for module, resource, decision, required in cases:
            with self.subTest(module=module):
                self.assertIn(module, REVIEWED)
                folder = genx / module
                doc = (folder / 'GroupDescription.md').read_text()
                self.assertIn('STRUCTURAL_DRAFT', doc)
                self.assertIn('**Sources:**', doc)
                self.assertIn(decision, doc)
                record = yaml.safe_load(
                    (folder / 'Schemas' / (resource + '.yaml')).read_text()
                )['components']['schemas'][resource]
                request = yaml.safe_load(
                    (folder / 'Schemas' / (resource + 'NewRequest.yaml')).read_text()
                )['components']['schemas'][resource + 'NewRequest']
                self.assertEqual(required | {'status'}, set(record['required']))
                self.assertEqual(required, set(request['required']))

        weather = yaml.safe_load(
            (genx / 'Environment/ExtremeWeather/Schemas/'
             'ExtremeWeatherEvent.yaml').read_text()
        )['components']['schemas']['ExtremeWeatherEvent']
        self.assertEqual('date-time', weather['properties']['occurredAt']['format'])
        self.assertNotIn('enum', weather['properties']['eventType'])
        self.assertEqual({'low', 'moderate', 'high', 'extreme'},
                         set(weather['properties']['severity']['enum']))
        self.assertNotIn('severity', weather['required'])
        self.assertNotIn('weatherObservationDbId', weather['properties'])

        soil = yaml.safe_load(
            (genx / 'Environment/SoilChemistry/Schemas/'
             'SoilChemistry.yaml').read_text()
        )['components']['schemas']['SoilChemistry']
        for field in ('siteDbId', 'texture', 'chemistry',
                      'moistureDepthCm', 'provenance'):
            self.assertIn(field, soil['properties'])
            self.assertNotIn(field, soil['required'])
        self.assertEqual('object', soil['properties']['chemistry']['type'])
        self.assertNotIn('properties', soil['properties']['chemistry'])
        self.assertEqual('number', soil['properties']['moistureDepthCm']['type'])
        for field in ('soilProfileDbId', 'moistureContent', 'sampledAt'):
            self.assertNotIn(field, soil['properties'])

        sensing = yaml.safe_load(
            (genx / 'Geospatial/RemoteSensingMetadata/Schemas/'
             'RemoteSensingMetadata.yaml').read_text()
        )['components']['schemas']['RemoteSensingMetadata']
        for field in ('platform', 'sensor', 'acquisitionDate', 'crs',
                      'resolution', 'provenance'):
            self.assertIn(field, sensing['properties'])
            self.assertNotIn(field, sensing['required'])
        for field in ('acquisitionDate', 'crs', 'resolution'):
            self.assertEqual('string', sensing['properties'][field]['type'])
        self.assertNotIn('format', sensing['properties']['acquisitionDate'])
        for absent in ('rasterRef', 'sourceImageDbId',
                       'bandMapping', 'cloudMaskDbId'):
            self.assertNotIn(absent, sensing['properties'])
        self.assertIn('D-435', (
            genx / 'RFCs/RFC-145-RemoteSensingMetadata.md').read_text())


    def test_calendar_and_developmental_stage_source_boundaries(self):
        root = Path(__file__).resolve().parents[1]
        genx = root / 'Specification/BrAPI-GenX'
        cases = (
            ('ReferenceData/Calendar', 'Calendar', 'calendarDbId', 'D-271'),
            ('ReferenceData/DevelopmentalStage', 'DevelopmentalStage',
             'developmentalStageDbId', 'D-235'),
        )
        for module, name, identity, decision in cases:
            with self.subTest(module=module):
                self.assertIn(module, REVIEWED)
                folder = genx / module
                desc = (folder / 'GroupDescription.md').read_text()
                self.assertIn('STRUCTURAL_DRAFT', desc)
                self.assertIn('**Sources:**', desc)
                self.assertIn(decision, desc)
                response = yaml.safe_load(
                    (folder / 'Schemas' / (name + '.yaml')).read_text()
                )['components']['schemas'][name]
                request = yaml.safe_load(
                    (folder / 'Schemas' / (name + 'NewRequest.yaml')).read_text()
                )['components']['schemas'][name + 'NewRequest']
                self.assertEqual({identity, 'status'}, set(response['required']))
                self.assertEqual({identity}, set(request['required']))
                self.assertEqual(
                    {'active', 'superseded', 'withdrawn'},
                    set(response['properties']['status']['enum'])
                )

        cal = yaml.safe_load(
            (genx / 'ReferenceData/Calendar/Schemas/Calendar.yaml').read_text()
        )['components']['schemas']['Calendar']
        for optional in ('name', 'convention', 'supersedes', 'provenance'):
            self.assertIn(optional, cal['properties'])
            self.assertNotIn(optional, cal['required'])
        self.assertEqual('string', cal['properties']['convention']['type'])
        self.assertNotIn('enum', cal['properties']['convention'])
        for absent in ('studyDbId', 'seasonDbId', 'timezone', 'startDate', 'endDate'):
            self.assertNotIn(absent, cal['properties'])
        official_season = yaml.safe_load(
            (root / 'Specification/BrAPI-Core/Seasons/Schemas/Season.yaml').read_text()
        )['components']['schemas']['Season']
        self.assertIn('seasonDbId', official_season['required'])
        for field in ('seasonName', 'year'):
            self.assertIn(field, official_season['properties'])
        cal_rfc = (genx / 'RFCs/RFC-091-Calendar.md').read_text()
        self.assertIn('no `studyDbId` or `seasonDbId`', cal_rfc)

        stage = yaml.safe_load(
            (genx / 'ReferenceData/DevelopmentalStage/Schemas/'
             'DevelopmentalStage.yaml').read_text()
        )['components']['schemas']['DevelopmentalStage']
        for optional in ('cropDbId', 'stageCode', 'stageName', 'definition',
                         'supersedes', 'provenance'):
            self.assertIn(optional, stage['properties'])
            self.assertNotIn(optional, stage['required'])
        self.assertEqual('string', stage['properties']['stageCode']['type'])
        self.assertNotIn('enum', stage['properties']['stageCode'])
        for absent in ('observationVariableDbId', 'variableDbId',
                       'stageVocabularyDbId', 'bbchCode'):
            self.assertNotIn(absent, stage['properties'])
        official_variable = yaml.safe_load(
            (root / 'Specification/BrAPI-Phenotyping/ObservationVariables/'
             'Schemas/ObservationVariable.yaml').read_text()
        )['components']['schemas']['ObservationVariable']
        self.assertTrue(any(
            'observationVariableDbId' in part.get('required', [])
            for part in official_variable['allOf']
        ))
        stage_rfc = (genx / 'RFCs/RFC-079-Developmental-Stage.md').read_text()
        self.assertIn('Optional `cropDbId`', stage_rfc)


    def test_cloud_mask_and_raster_catalogue_remain_unverified_metadata(self):
        root = Path(__file__).resolve().parents[1]
        genx = root / 'Specification/BrAPI-GenX'
        cases = (
            ('Geospatial/CloudMask', 'CloudMask', 'cloudMaskDbId', 'D-439'),
            ('Geospatial/RasterCatalogue', 'RasterCatalogue',
             'rasterCatalogueDbId', 'D-430'),
        )
        for module, resource, identity, decision in cases:
            with self.subTest(module=module):
                self.assertIn(module, REVIEWED)
                folder = genx / module
                doc = (folder / 'GroupDescription.md').read_text()
                self.assertIn('STRUCTURAL_DRAFT', doc)
                self.assertIn('**Sources:**', doc)
                self.assertIn(decision, doc)
                response = yaml.safe_load(
                    (folder / 'Schemas' / (resource + '.yaml')).read_text()
                )['components']['schemas'][resource]
                request = yaml.safe_load(
                    (folder / 'Schemas' / (resource + 'NewRequest.yaml')).read_text()
                )['components']['schemas'][resource + 'NewRequest']
                self.assertEqual({identity, 'status'}, set(response['required']))
                self.assertEqual({identity}, set(request['required']))
                for optional in ('crs', 'resolution', 'extent', 'provenance',
                                 'supersedes'):
                    self.assertIn(optional, response['properties'])
                    self.assertNotIn(optional, response['required'])
                    self.assertEqual('string', response['properties'][optional]['type']) if optional in ('crs', 'resolution', 'extent') else None
                for missing in ('imageDbId', 'rasterCatalogueDbId',
                                'assetUri', 'pixelData', 'cloudCoverPercent'):
                    if missing != identity:
                        self.assertNotIn(missing, response['properties'])

        cloud = yaml.safe_load(
            (genx / 'Geospatial/CloudMask/Schemas/CloudMask.yaml').read_text()
        )['components']['schemas']['CloudMask']
        for optional in ('maskType', 'acquisitionDate'):
            self.assertIn(optional, cloud['properties'])
            self.assertNotIn(optional, cloud['required'])
            self.assertEqual('string', cloud['properties'][optional]['type'])
        self.assertNotIn('enum', cloud['properties']['maskType'])
        self.assertNotIn('format', cloud['properties']['acquisitionDate'])
        cloud_ops = yaml.safe_load(
            (genx / 'Geospatial/CloudMask/CloudMask_GET_POST.yaml').read_text()
        )
        self.assertEqual(
            'genxListCloudMasks',
            cloud_ops['paths']['/cloud-masks']['get']['operationId']
        )
        cloud_readme = (genx / 'Geospatial/CloudMask/README.md').read_text()
        self.assertIn('(`genxListCloudMasks`)', cloud_readme)
        self.assertNotIn('(`genxListCloudMask`)', cloud_readme)
        self.assertIn('../../RFCs/RFC-147-CloudMask.md', cloud_readme)
        for d in ('D-439', 'D-440', 'D-441'):
            self.assertIn(d, (genx / 'Geospatial/CloudMask/GroupDescription.md').read_text())

        raster = yaml.safe_load(
            (genx / 'Geospatial/RasterCatalogue/Schemas/RasterCatalogue.yaml').read_text()
        )['components']['schemas']['RasterCatalogue']
        for optional in ('datasetName', 'datasetType'):
            self.assertIn(optional, raster['properties'])
            self.assertNotIn(optional, raster['required'])
            self.assertEqual('string', raster['properties'][optional]['type'])
        self.assertNotIn('enum', raster['properties']['datasetType'])
        for missing in ('rasterUri', 'imageURL', 'bandMetadata',
                        'pixelWidth', 'pixelHeight', 'contentDigest'):
            self.assertNotIn(missing, raster['properties'])
        official_image = yaml.safe_load(
            (root / 'Specification/BrAPI-Phenotyping/Images/Schemas/'
             'ImageNewRequest.yaml').read_text()
        )['components']['schemas']['ImageNewRequest']
        for field in ('imageURL', 'imageLocation', 'imageWidth',
                      'imageHeight', 'imageTimeStamp'):
            self.assertIn(field, official_image['properties'])
        for d in ('D-430', 'D-431', 'D-432'):
            self.assertIn(d, (genx / 'Geospatial/RasterCatalogue/GroupDescription.md').read_text())


    def test_bulk_capture_is_not_official_observation_batch_ingestion(self):
        root = Path(__file__).resolve().parents[1]
        genx = root / 'Specification/BrAPI-GenX'
        module = 'Phenotyping/BulkCapture'
        self.assertIn(module, REVIEWED)
        folder = genx / module
        desc = (folder / 'GroupDescription.md').read_text()
        self.assertIn('STRUCTURAL_DRAFT', desc)
        self.assertIn('**Sources:**', desc)
        for decision in ('D-118', 'D-119', 'D-120'):
            self.assertIn(decision, desc)

        response = yaml.safe_load(
            (folder / 'Schemas/BulkCapture.yaml').read_text()
        )['components']['schemas']['BulkCapture']
        request = yaml.safe_load(
            (folder / 'Schemas/BulkCaptureNewRequest.yaml').read_text()
        )['components']['schemas']['BulkCaptureNewRequest']
        required = {'bulkCaptureDbId', 'studyDbId', 'capturedAt', 'entries'}
        self.assertEqual(required, set(request['required']))
        self.assertEqual(required | {'status'}, set(response['required']))
        self.assertEqual('date-time', response['properties']['capturedAt']['format'])

        for record in (response, request):
            entries = record['properties']['entries']
            self.assertEqual('array', entries['type'])
            self.assertNotIn('minItems', entries)
            item = entries['items']
            self.assertEqual({'variableDbId'}, set(item['required']))
            for optional in ('observationUnitDbId', 'value', 'unit', 'qualityFlag'):
                self.assertIn(optional, item['properties'])
                self.assertNotIn(optional, item['required'])
            self.assertEqual('number', item['properties']['value']['type'])
            self.assertIs(True, item['properties']['value']['nullable'])
            self.assertEqual(
                {'valid', 'suspect', 'invalid', 'missing'},
                set(item['properties']['qualityFlag']['enum'])
            )
            for absent in ('observationDbId', 'observationVariableDbId',
                           'missingReason', 'capturedAt'):
                self.assertNotIn(absent, item['properties'])
            for absent in ('phenotypeCaptureDbId', 'fieldBookDbId'):
                self.assertNotIn(absent, record['properties'])

        official_operations = yaml.safe_load(
            (root / 'Specification/BrAPI-Phenotyping/Observations/'
             'Observations_GET_POST_PUT.yaml').read_text()
        )
        official_batch = (
            official_operations['paths']['/observations']['post']
            ['requestBody']['content']['application/json']['schema']
        )
        self.assertEqual('array', official_batch['type'])
        self.assertEqual(
            '#/components/schemas/ObservationNewRequest',
            official_batch['items']['$ref']
        )
        official_request = yaml.safe_load(
            (root / 'Specification/BrAPI-Phenotyping/Observations/Schemas/'
             'ObservationNewRequest.yaml').read_text()
        )['components']['schemas']['ObservationNewRequest']
        self.assertEqual('string', official_request['properties']['value']['type'])
        self.assertIs(True, official_request['properties']['value']['nullable'])
        rfc = (genx / 'RFCs/RFC-040-Bulk-Capture.md').read_text()
        self.assertIn('no `phenotypeCaptureDbId` property', rfc)
        self.assertIn('no `fieldBookDbId` property', rfc)


    def test_environmental_carbon_emissions_and_treatment_science_boundaries(self):
        root = Path(__file__).resolve().parents[1]
        genx = root / 'Specification/BrAPI-GenX'
        cases = (
            ('CarbonStock', 'carbonStockDbId', ('D-199', 'D-200', 'D-201')),
            ('Emissions', 'emissionsDbId', ('D-226', 'D-227', 'D-228')),
            ('EnvironmentalTreatment', 'environmentalTreatmentDbId',
             ('D-232', 'D-233', 'D-234')),
        )
        for name, identity, decisions in cases:
            with self.subTest(module=name):
                module = 'Environment/' + name
                self.assertIn(module, REVIEWED)
                folder = genx / module
                description = (folder / 'GroupDescription.md').read_text()
                self.assertIn('STRUCTURAL_DRAFT', description)
                self.assertIn('**Sources:**', description)
                for decision in decisions:
                    self.assertIn(decision, description)
                record = yaml.safe_load(
                    (folder / 'Schemas' / (name + '.yaml')).read_text()
                )['components']['schemas'][name]
                request = yaml.safe_load(
                    (folder / 'Schemas' / (name + 'NewRequest.yaml')).read_text()
                )['components']['schemas'][name + 'NewRequest']
                self.assertEqual({identity}, set(request['required']))
                self.assertEqual({identity, 'status'}, set(record['required']))
                self.assertEqual(
                    {'active', 'superseded', 'withdrawn'},
                    set(record['properties']['status']['enum'])
                )
                self.assertNotIn('provenance', request['required'])

        carbon = yaml.safe_load(
            (genx / 'Environment/CarbonStock/Schemas/CarbonStock.yaml').read_text()
        )['components']['schemas']['CarbonStock']
        for field in ('studyDbId', 'locationDbId', 'pool', 'stockMgPerHa',
                      'depthCm', 'measuredAt', 'supersedes', 'provenance'):
            self.assertIn(field, carbon['properties'])
            self.assertNotIn(field, carbon['required'])
        self.assertEqual(
            {'soil', 'biomass', 'litter', 'coarse-woody-debris'},
            set(carbon['properties']['pool']['enum'])
        )
        for field in ('stockMgPerHa', 'depthCm'):
            self.assertEqual('number', carbon['properties'][field]['type'])
        self.assertEqual('date-time', carbon['properties']['measuredAt']['format'])
        for missing in ('bulkDensity', 'uncertainty', 'samplingArea',
                        'telemetryDbId', 'analysisResultDbId'):
            self.assertNotIn(missing, carbon['properties'])

        emissions = yaml.safe_load(
            (genx / 'Environment/Emissions/Schemas/Emissions.yaml').read_text()
        )['components']['schemas']['Emissions']
        for field in ('siteDbId', 'period', 'greenhouseGas',
                      'quantity', 'unit', 'provenance'):
            self.assertIn(field, emissions['properties'])
            self.assertNotIn(field, emissions['required'])
        self.assertEqual('number', emissions['properties']['quantity']['type'])
        for field in ('period', 'greenhouseGas', 'unit'):
            self.assertEqual('string', emissions['properties'][field]['type'])
            self.assertNotIn('enum', emissions['properties'][field])
        self.assertNotIn('format', emissions['properties']['period'])
        for missing in ('carbonStockDbId', 'globalWarmingPotentialVersion',
                        'reportingScope', 'emissionFactorDbId'):
            self.assertNotIn(missing, emissions['properties'])
        self.assertIn('no', (genx / 'RFCs/RFC-076-Emissions.md').read_text())

        treatment = yaml.safe_load(
            (genx / 'Environment/EnvironmentalTreatment/Schemas/'
             'EnvironmentalTreatment.yaml').read_text()
        )['components']['schemas']['EnvironmentalTreatment']
        for field in ('siteDbId', 'treatmentType', 'exposure', 'provenance'):
            self.assertIn(field, treatment['properties'])
            self.assertNotIn(field, treatment['required'])
        for field in ('treatmentType', 'exposure'):
            self.assertEqual('string', treatment['properties'][field]['type'])
            self.assertNotIn('enum', treatment['properties'][field])
        for missing in ('extremeWeatherEventDbId', 'studyDbId',
                        'observationUnitDbId', 'exposureDuration',
                        'controlGroupDbId'):
            self.assertNotIn(missing, treatment['properties'])
        self.assertIn('No `extremeWeatherEventDbId`',
                      (genx / 'RFCs/RFC-078-Environmental-Treatment.md').read_text())

        official = yaml.safe_load(
            (root / 'Specification/BrAPI-Phenotyping/Observations/Schemas/'
             'ObservationNewRequest.yaml').read_text()
        )['components']['schemas']['ObservationNewRequest']
        self.assertEqual('string', official['properties']['value']['type'])
        self.assertIn('studyDbId', official['properties'])


    def test_biodiversity_export_is_metadata_not_a_published_archive(self):
        root = Path(__file__).resolve().parents[1]
        genx = root / 'Specification/BrAPI-GenX'
        module = 'Interoperability/BiodiversityExport'
        self.assertIn(module, REVIEWED)
        folder = genx / module
        description = (folder / 'GroupDescription.md').read_text()
        self.assertIn('STRUCTURAL_DRAFT', description)
        self.assertIn('**Sources:**', description)
        for decision in ('D-361', 'D-362', 'D-363'):
            self.assertIn(decision, description)
        record = yaml.safe_load(
            (folder / 'Schemas/BiodiversityExport.yaml').read_text()
        )['components']['schemas']['BiodiversityExport']
        request = yaml.safe_load(
            (folder / 'Schemas/BiodiversityExportNewRequest.yaml').read_text()
        )['components']['schemas']['BiodiversityExportNewRequest']
        self.assertEqual({'biodiversityExportDbId'}, set(request['required']))
        self.assertEqual({'biodiversityExportDbId', 'status'},
                         set(record['required']))
        self.assertEqual({'active', 'superseded', 'withdrawn'},
                         set(record['properties']['status']['enum']))
        for optional in ('specimenType', 'occurrenceId', 'collectionDate',
                         'location', 'taxon', 'supersedes', 'provenance'):
            self.assertIn(optional, record['properties'])
            self.assertNotIn(optional, record['required'])
            self.assertNotIn(optional, request['required'])
        for optional in ('specimenType', 'occurrenceId', 'collectionDate',
                         'location', 'taxon'):
            self.assertEqual('string', record['properties'][optional]['type'])
        self.assertNotIn('format', record['properties']['collectionDate'])
        self.assertNotIn('enum', record['properties']['taxon'])
        for missing in ('germplasmDbId', 'basisOfRecord', 'scientificName',
                        'decimalLatitude', 'decimalLongitude', 'datasetId',
                        'archiveUri', 'archiveDigest', 'license',
                        'publisherId', 'deliveryStatus', 'researchAssetDbId'):
            self.assertNotIn(missing, record['properties'])
            self.assertNotIn(missing, request['properties'])
        operations = yaml.safe_load(
            (folder / 'BiodiversityExport_GET_POST.yaml').read_text()
        )
        self.assertEqual(
            'genxListBiodiversityExports',
            operations['paths']['/biodiversity-exports']['get']['operationId']
        )
        self.assertEqual(
            'genxRegisterBiodiversityExport',
            operations['paths']['/biodiversity-exports']['post']['operationId']
        )
        rfc = (genx / 'RFCs/RFC-121-BiodiversityExport.md').read_text()
        self.assertIn('No `germplasmDbId`', rfc)
        self.assertIn('Darwin Core Archive', rfc)



    def test_experimental_planning_drafts_and_official_overlap(self):
        root = Path(__file__).resolve().parents[1]
        genx = root / 'Specification/BrAPI-GenX'
        official = root / 'Specification'
        cases = (
            ('ExperimentalDesign', 'experimentalDesignDbId',
             {'experimentalDesignDbId', 'studyDbId', 'designType'},
             ('D-51', 'D-52', 'D-53')),
            ('ExperimentalProtocol', 'experimentalProtocolDbId',
             {'experimentalProtocolDbId'}, ('D-349', 'D-350', 'D-351')),
            ('TreatmentAssignment', 'treatmentAssignmentDbId',
             {'treatmentAssignmentDbId'}, ('D-316', 'D-317', 'D-318')),
        )
        for module, identity, mandatory, decisions in cases:
            with self.subTest(module=module):
                folder = genx / 'Breeding' / module
                self.assertIn('Breeding/' + module, REVIEWED)
                description = (folder / 'GroupDescription.md').read_text()
                self.assertIn('STRUCTURAL_DRAFT', description)
                self.assertIn('**Sources:**', description)
                for decision in decisions:
                    self.assertIn(decision, description)
                request = yaml.safe_load(
                    (folder / 'Schemas' / (module + 'NewRequest.yaml')).read_text()
                )['components']['schemas'][module + 'NewRequest']
                response = yaml.safe_load(
                    (folder / 'Schemas' / (module + '.yaml')).read_text()
                )['components']['schemas'][module]
                self.assertEqual(mandatory, set(request['required']))
                self.assertEqual(mandatory | {'status'}, set(response['required']))
                self.assertNotIn('provenance', request['required'])
                self.assertNotIn('provenance', response['required'])
                self.assertIn(identity, response['properties'])

        design = yaml.safe_load(
            (genx / 'Breeding/ExperimentalDesign/Schemas/ExperimentalDesign.yaml')
            .read_text()
        )['components']['schemas']['ExperimentalDesign']
        for optional in ('replicationCount', 'blockSize', 'randomizationSeed',
                         'treatmentAssignments'):
            self.assertIn(optional, design['properties'])
            self.assertNotIn(optional, design['required'])
        entries = design['properties']['treatmentAssignments']
        self.assertEqual('array', entries['type'])
        self.assertNotIn('minItems', entries)
        self.assertNotIn('required', entries['items'])
        self.assertEqual({'plotId', 'treatment', 'replication', 'block'},
                         set(entries['items']['properties']))
        for absent in ('observationUnitDbId', 'experimentalProtocolDbId',
                       'randomizationAlgorithm'):
            self.assertNotIn(absent, design['properties'])

        protocol = yaml.safe_load(
            (genx / 'Breeding/ExperimentalProtocol/Schemas/'
             'ExperimentalProtocol.yaml').read_text()
        )['components']['schemas']['ExperimentalProtocol']
        for field in ('protocolName', 'version', 'designType', 'treatments',
                      'replicates', 'randomization', 'blocks'):
            self.assertEqual('string', protocol['properties'][field]['type'])
            self.assertNotIn(field, protocol['required'])
        for absent in ('name', 'studyDbId', 'experimentalDesignDbId',
                       'protocolLibraryDbId', 'genomicDatasetDbId', 'steps'):
            self.assertNotIn(absent, protocol['properties'])

        treatment = yaml.safe_load(
            (genx / 'Breeding/TreatmentAssignment/Schemas/'
             'TreatmentAssignment.yaml').read_text()
        )['components']['schemas']['TreatmentAssignment']
        for optional in ('fieldDbId', 'treatment'):
            self.assertEqual('string', treatment['properties'][optional]['type'])
            self.assertNotIn(optional, treatment['required'])
        for absent in ('studyDbId', 'locationDbId', 'observationUnitDbId',
                       'experimentalDesignDbId', 'replication', 'appliedAt',
                       'dose', 'duration'):
            self.assertNotIn(absent, treatment['properties'])

        study = yaml.safe_load(
            (official / 'BrAPI-Core/Studies/Schemas/StudyNewRequest.yaml')
            .read_text()
        )['components']['schemas']['StudyNewRequest']
        self.assertIn('experimentalDesign', study['properties'])
        self.assertIn('description',
                      study['properties']['experimentalDesign']['properties'])
        self.assertIn('observationLevels', study['properties'])
        units = yaml.safe_load(
            (official / 'BrAPI-Phenotyping/ObservationUnits/Schemas/'
             'ObservationUnitNewRequest.yaml').read_text()
        )['components']['schemas']['ObservationUnitNewRequest']
        self.assertEqual('#/components/schemas/ObservationTreatment',
                         units['properties']['treatments']['items']['$ref'])
        self.assertIn('observationUnitPosition', units['properties'])
        factors = yaml.safe_load(
            (official / 'BrAPI-Phenotyping/ObservationUnits/Schemas/'
             'ObservationTreatment.yaml').read_text()
        )['components']['schemas']['ObservationTreatment']
        self.assertTrue({'factor', 'modality'}.issubset(factors['properties']))
        event = yaml.safe_load(
            (official / 'BrAPI-Phenotyping/Events/Schemas/Event.yaml').read_text()
        )['components']['schemas']['Event']
        self.assertTrue({'studyDbId', 'observationUnitDbIds',
                         'eventDateRange'}.issubset(event['properties']))

        rfc18 = (genx / 'RFCs/RFC-018-Experimental-Design.md').read_text()
        rfc106 = (genx / 'RFCs/RFC-106-Treatment-Assignment.md').read_text()
        rfc117 = (genx / 'RFCs/RFC-117-ExperimentalProtocol.md').read_text()
        self.assertIn('StudyNewRequest.experimentalDesign', rfc18)
        self.assertIn('no typed BrAPI', rfc106)
        self.assertNotIn('records reference BrAPI `Study`/`Location`', rfc106)
        self.assertIn('D-349: Should `protocolName` be required?', rfc117)

        for module, route, getter, setter in (
            ('ExperimentalDesign', '/experimental-designs',
             'genxListExperimentalDesigns', 'genxRegisterExperimentalDesign'),
            ('ExperimentalProtocol', '/experimental-protocols',
             'genxListExperimentalProtocols', 'genxRegisterExperimentalProtocol'),
            ('TreatmentAssignment', '/treatment-assignments',
             'genxListTreatmentAssignments', 'genxRegisterTreatmentAssignment'),
        ):
            operations = yaml.safe_load(
                (genx / 'Breeding' / module / (module + '_GET_POST.yaml'))
                .read_text()
            )
            self.assertEqual(getter, operations['paths'][route]['get']['operationId'])
            self.assertEqual(setter, operations['paths'][route]['post']['operationId'])



    def test_parent_candidate_and_selection_decisions_are_not_equivalent(self):
        """Pin difference between a parent Boolean and a dated verdict."""
        root = Path(__file__).resolve().parents[1]
        genx = root / 'Specification/BrAPI-GenX'
        parent = genx / 'Breeding/ParentCandidateSelection'
        verdict = genx / 'Breeding/SelectionDecisions'
        for module, folder in (('ParentCandidateSelection', parent),
                               ('SelectionDecisions', verdict)):
            self.assertIn('Breeding/' + module, REVIEWED)
            description = (folder / 'GroupDescription.md').read_text()
            self.assertIn('STRUCTURAL_DRAFT', description)
            self.assertIn('**Sources:**', description)

        parent_request = yaml.safe_load(
            (parent / 'Schemas/ParentCandidateSelectionNewRequest.yaml')
            .read_text()
        )['components']['schemas']['ParentCandidateSelectionNewRequest']
        parent_response = yaml.safe_load(
            (parent / 'Schemas/ParentCandidateSelection.yaml').read_text()
        )['components']['schemas']['ParentCandidateSelection']
        required_parent = {'parentCandidateSelectionDbId', 'programDbId',
                           'candidateGermplasmDbId', 'selected'}
        self.assertEqual(required_parent, set(parent_request['required']))
        self.assertEqual(required_parent | {'status'},
                         set(parent_response['required']))
        self.assertEqual('boolean', parent_request['properties']['selected']['type'])
        for optional in ('selectionCriterion', 'rationale', 'provenance'):
            self.assertIn(optional, parent_request['properties'])
            self.assertNotIn(optional, parent_request['required'])
        for raw in ('programDbId', 'candidateGermplasmDbId'):
            self.assertEqual('string', parent_request['properties'][raw]['type'])
        for absent in ('selectionDecisionDbId', 'decisionDate', 'decisionMaker',
                       'linkedObservationReferences', 'crossDbId', 'plannedCrossDbId'):
            self.assertNotIn(absent, parent_request['properties'])

        selection_request = yaml.safe_load(
            (verdict / 'Schemas/SelectionDecisionNewRequest.yaml')
            .read_text()
        )['components']['schemas']['SelectionDecisionNewRequest']
        selection_response = yaml.safe_load(
            (verdict / 'Schemas/SelectionDecision.yaml').read_text()
        )['components']['schemas']['SelectionDecision']
        required_verdict = {'selectionDecisionDbId', 'programReference',
                            'decision', 'decisionDate'}
        self.assertEqual(required_verdict, set(selection_request['required']))
        self.assertEqual(required_verdict, set(selection_response['required']))
        self.assertEqual({'selected', 'rejected', 'deferred', 'advanced'},
                         set(selection_request['properties']['decision']['enum']))
        self.assertEqual('date',
                         selection_request['properties']['decisionDate']['format'])
        self.assertEqual('#/components/schemas/BrapiResourceReference',
                         selection_request['properties']['programReference']['$ref'])
        for optional in ('candidateGermplasmReference', 'studyReference',
                         'decisionMaker', 'selectionCriterion', 'rationale',
                         'linkedObservationReferences', 'pipelineContext',
                         'schemeContext', 'status', 'provenance'):
            self.assertIn(optional, selection_request['properties'])
            self.assertNotIn(optional, selection_request['required'])
        self.assertNotIn('parentCandidateSelectionDbId',
                         selection_request['properties'])

        reference = yaml.safe_load(
            (genx / 'Breeding/BreedingPipeline/Schemas/'
             'BreedingPipeline.yaml').read_text()
        )['components']['schemas']['BrapiResourceReference']
        self.assertEqual({'apiGeneration', 'resourceType', 'server', 'dbId'},
                         set(reference['required']))
        cross_parent = yaml.safe_load(
            (root / 'Specification/BrAPI-Germplasm/Crosses/Schemas/'
             'CrossParent.yaml').read_text()
        )['components']['schemas']['CrossParent']
        self.assertTrue({'germplasmDbId', 'parentType'}
                        .issubset(cross_parent['properties']))
        planned = yaml.safe_load(
            (root / 'Specification/BrAPI-Germplasm/PlannedCrosses/Schemas/'
             'PlannedCrossNewRequest.yaml').read_text()
        )['components']['schemas']['PlannedCrossNewRequest']
        self.assertTrue({'parent1', 'parent2'}.issubset(planned['properties']))

        parent_rfc = (genx / 'RFCs/RFC-028-Parent-Candidate-Selection.md').read_text()
        self.assertIn('no `selectionDecisionDbId`', parent_rfc)
        self.assertIn('D-83:', parent_rfc)
        verdict_rfc = (genx / 'RFCs/RFC-008-Selection-Decisions.md').read_text()
        self.assertIn('`decisionMaker` is optional', verdict_rfc)

        for folder, route, read_id, write_id in (
            (parent, '/parent-candidate-selections',
             'genxListParentCandidateSelections',
             'genxRecordParentCandidateSelection'),
            (verdict, '/selection-decisions',
             'genxListSelectionDecisions', 'genxRecordSelectionDecision'),
        ):
            name = folder.name
            ops = yaml.safe_load((folder / (name + '_GET_POST.yaml')).read_text())
            self.assertEqual(read_id, ops['paths'][route]['get']['operationId'])
            self.assertEqual(write_id, ops['paths'][route]['post']['operationId'])



    def test_doubled_haploid_and_speed_breeding_science_boundaries(self):
        """Protect source claims without asserting validated lifecycle science."""
        root = Path(__file__).resolve().parents[1]
        genx = root / 'Specification/BrAPI-GenX'
        cases = (
            ('DoubledHaploid', 'DoubledHaploidProgram',
             {'doubledHaploidProgramDbId', 'programDbId', 'method'},
             {'active', 'completed', 'superseded'},
             ('D-57', 'D-58', 'D-59')),
            ('SpeedBreeding', 'SpeedBreedingProtocol',
             {'speedBreedingProtocolDbId', 'programDbId', 'protocolName'},
             {'active', 'deprecated', 'superseded'},
             ('D-63', 'D-64', 'D-65')),
        )
        for module, model, mandatory, statuses, decisions in cases:
            with self.subTest(module=module):
                folder = genx / 'Breeding' / module
                self.assertIn('Breeding/' + module, REVIEWED)
                desc = (folder / 'GroupDescription.md').read_text()
                self.assertIn('STRUCTURAL_DRAFT', desc)
                self.assertIn('**Sources:**', desc)
                for decision in decisions:
                    self.assertIn(decision, desc)
                request = yaml.safe_load(
                    (folder / 'Schemas' / (model + 'NewRequest.yaml')).read_text()
                )['components']['schemas'][model + 'NewRequest']
                record = yaml.safe_load(
                    (folder / 'Schemas' / (model + '.yaml')).read_text()
                )['components']['schemas'][model]
                self.assertEqual(mandatory, set(request['required']))
                self.assertEqual(mandatory | {'status'}, set(record['required']))
                self.assertEqual(statuses, set(record['properties']['status']['enum']))
                for optional in ('provenance', 'supersedes'):
                    self.assertIn(optional, request['properties'])
                    self.assertNotIn(optional, request['required'])

        dh = yaml.safe_load(
            (genx / 'Breeding/DoubledHaploid/Schemas/'
             'DoubledHaploidProgram.yaml').read_text()
        )['components']['schemas']['DoubledHaploidProgram']
        for name in ('haploidCount', 'doubledCount'):
            self.assertEqual('integer', dh['properties'][name]['type'])
            self.assertNotIn('minimum', dh['properties'][name])
            self.assertNotIn(name, dh['required'])
        for name in ('startedAt', 'completedAt'):
            self.assertEqual('date', dh['properties'][name]['format'])
            self.assertNotIn(name, dh['required'])
        self.assertNotIn('donorGermplasmDbId', dh['required'])
        for absent in ('crossDbId', 'ploidyAssayDbId', 'doublingTreatment',
                       'generationDbId', 'offspringGermplasmDbIds'):
            self.assertNotIn(absent, dh['properties'])

        sb = yaml.safe_load(
            (genx / 'Breeding/SpeedBreeding/Schemas/'
             'SpeedBreedingProtocol.yaml').read_text()
        )['components']['schemas']['SpeedBreedingProtocol']
        self.assertEqual('number', sb['properties']['photoperiod']['type'])
        self.assertEqual('integer', sb['properties']['generationTime']['type'])
        for field in ('photoperiod', 'generationTime'):
            self.assertNotIn(field, sb['required'])
            self.assertNotIn('minimum', sb['properties'][field])
            self.assertNotIn('maximum', sb['properties'][field])
        for field in ('lightRegime', 'temperatureRegime'):
            self.assertEqual('string', sb['properties'][field]['type'])
            self.assertNotIn(field, sb['required'])
        for absent in ('studyDbId', 'breedingPipelineDbId', 'cropDbId',
                       'lightIntensity', 'relativeHumidity', 'measuredAt'):
            self.assertNotIn(absent, sb['properties'])

        cross = yaml.safe_load(
            (root / 'Specification/BrAPI-Germplasm/Crosses/Schemas/'
             'CrossNewRequest.yaml').read_text()
        )['components']['schemas']['CrossNewRequest']
        self.assertIn('DOUBLE_HAPLOID', cross['properties']['crossType']['enum'])
        self.assertIn('parent1', cross['properties'])

        study = yaml.safe_load(
            (root / 'Specification/BrAPI-Core/Studies/Schemas/'
             'StudyNewRequest.yaml').read_text()
        )['components']['schemas']['StudyNewRequest']
        for field in ('environmentParameters', 'growthFacility',
                      'culturalPractices', 'experimentalDesign'):
            self.assertIn(field, study['properties'])

        dh_rfc = (genx / 'RFCs/RFC-020-Doubled-Haploid.md').read_text()
        self.assertIn('crossType: DOUBLE_HAPLOID', dh_rfc)
        sb_rfc = (genx / 'RFCs/RFC-022-Speed-Breeding.md').read_text()
        self.assertIn('no `breedingPipelineDbId`', sb_rfc)
        for module, route, listing, posting in (
            ('DoubledHaploid', '/doubled-haploid-programs',
             'genxListDoubledHaploidPrograms', 'genxRegisterDoubledHaploidProgram'),
            ('SpeedBreeding', '/speed-breeding-protocols',
             'genxListSpeedBreedingProtocols', 'genxRegisterSpeedBreedingProtocol'),
        ):
            f = genx / 'Breeding' / module / (module + '_GET_POST.yaml')
            operations = yaml.safe_load(f.read_text())
            self.assertEqual(listing, operations['paths'][route]['get']['operationId'])
            self.assertEqual(posting, operations['paths'][route]['post']['operationId'])



    def test_spatial_registry_records_remain_non_executable_until_decision(self):
        """Do not reinterpret sparse draft records as executable geospatial APIs."""
        root = Path(__file__).resolve().parents[1]
        genx = root / 'Specification/BrAPI-GenX'
        candidates = (
            ('SpatialIndex', 'spatialIndexDbId', 'RFC-141-SpatialIndex.md',
             'G-090-1'),
            ('SpatialQuery', 'spatialQueryDbId', 'RFC-143-SpatialQuery.md',
             'G-090-2'),
            ('YieldMap', 'yieldMapDbId', 'RFC-070-Yield-Map.md',
             'G-090-3'),
        )
        for module, identity, rfc_name, decision in candidates:
            with self.subTest(module=module):
                folder = genx / 'Geospatial' / module
                self.assertNotIn('Geospatial/' + module, REVIEWED)
                description = (folder / 'GroupDescription.md').read_text()
                self.assertLess(len(description.strip()), 100)
                request = yaml.safe_load(
                    (folder / 'Schemas' / (module + 'NewRequest.yaml'))
                    .read_text()
                )['components']['schemas'][module + 'NewRequest']
                response = yaml.safe_load(
                    (folder / 'Schemas' / (module + '.yaml')).read_text()
                )['components']['schemas'][module]
                self.assertEqual({identity}, set(request['required']))
                self.assertEqual({identity, 'status'}, set(response['required']))
                self.assertIn(decision, (folder / 'README.md').read_text())
                rfc = (genx / 'RFCs' / rfc_name).read_text()
                self.assertIn('non-normative', rfc)

        spatial_index = yaml.safe_load(
            (genx / 'Geospatial/SpatialIndex/Schemas/SpatialIndex.yaml')
            .read_text()
        )['components']['schemas']['SpatialIndex']
        for optional in ('indexType', 'indexName', 'coverageArea',
                         'resolution', 'provenance'):
            self.assertIn(optional, spatial_index['properties'])
            self.assertNotIn(optional, spatial_index['required'])
        self.assertEqual('string', spatial_index['properties']['coverageArea']['type'])
        for absent in ('datasetDbId', 'indexUri', 'geometryCrs', 'queryExecution'):
            self.assertNotIn(absent, spatial_index['properties'])

        spatial_query = yaml.safe_load(
            (genx / 'Geospatial/SpatialQuery/Schemas/SpatialQuery.yaml')
            .read_text()
        )['components']['schemas']['SpatialQuery']
        self.assertEqual('object', spatial_query['properties']['queryGeometry']['type'])
        self.assertEqual('string', spatial_query['properties']['queryParams']['type'])
        for optional in ('queryType', 'queryGeometry',
                         'queryParams', 'resultReference', 'provenance'):
            self.assertNotIn(optional, spatial_query['required'])
        for absent in ('datasetDbId', 'spatialIndexDbId', 'executionState',
                       'resultData', 'spatialPredicate'):
            self.assertNotIn(absent, spatial_query['properties'])

        yield_map = yaml.safe_load(
            (genx / 'Geospatial/YieldMap/Schemas/YieldMap.yaml').read_text()
        )['components']['schemas']['YieldMap']
        for optional in ('studyDbId', 'locationDbId', 'cropCycleDbId',
                         'harvestRecordDbId', 'mapType', 'resolutionM',
                         'storageUri', 'fileDigest', 'provenance'):
            self.assertIn(optional, yield_map['properties'])
            self.assertNotIn(optional, yield_map['required'])
        self.assertEqual('number', yield_map['properties']['resolutionM']['type'])
        self.assertNotIn('pattern', yield_map['properties']['fileDigest'])
        self.assertNotIn('format', yield_map['properties']['storageUri'])
        for absent in ('coordinateReferenceSystem', 'crs',
                       'verifiedAt', 'publishedAt', 'payloadStatus'):
            self.assertNotIn(absent, yield_map['properties'])

        self.assertIn('does **not** verify',
                      (genx / 'RFCs/RFC-070-Yield-Map.md').read_text())
        self.assertIn('does **not** build an index',
                      (genx / 'RFCs/RFC-141-SpatialIndex.md').read_text())
        self.assertIn('does not execute a query',
                      (genx / 'RFCs/RFC-143-SpatialQuery.md').read_text())

        assessment = (root / 'docs/assessment/'
                      'BRAPI-GENX-MISSION-090-SPATIAL-GOVERNANCE-PREFLIGHT.md')
        self.assertTrue(assessment.is_file())
        old = assessment.read_text()
        for decision in ('G-090-1', 'G-090-2', 'G-090-3'):
            self.assertIn(decision, old)
        self.assertIn('no ratification', old.lower())


if __name__ == '__main__':
    unittest.main()
