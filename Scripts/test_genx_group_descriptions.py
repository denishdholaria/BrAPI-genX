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


if __name__ == '__main__':
    unittest.main()
