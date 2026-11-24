#!/usr/bin/env python3
"""Protect reviewed GenX group descriptions without promoting draft modules.

Unreviewed title-only placeholders are counted, never auto-populated or failed.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

REL = Path('Specification/BrAPI-GenX')
REVIEWED = frozenset({
    'Core/Jobs', 'Core/Provenance', 'ReferenceData/VariableTerms',
    'Breeding/BreedingPipeline', 'CropProduction/LotLedger',
    'Research/Models', 'Interoperability/FAIR',
    'Instrumentation/Telemetry', 'Genotyping/Genomics',
    'Core/CapabilityMetadata', 'Core/CapabilityNegotiation',
    'Core/ServerInfoV3',
    'Interoperability/ConformanceProbe', 'Interoperability/Crosswalk',
    'Interoperability/SchemaMapping',
    'ReferenceData/MeasurementScale', 'ReferenceData/MeasurementMethods',
    'ReferenceData/UnitsAndQuantity', 'ReferenceData/OntologyTerm',
    'ReferenceData/OntologyMapping',
    'ReferenceData/ReusableList', 'ReferenceData/CommonCropName',
    'ReferenceData/PersonReference',
    'ReferenceData/TaxonName', 'ReferenceData/CropSpecies',
    'ReferenceData/InstitutionCode',
    'ReferenceData/ExternalVocabulary', 'ReferenceData/TerminologyVersion',
    'ReferenceData/ReferenceDataVersion', 'ReferenceData/CropTraitDictionary',
    'Breeding/Plot', 'Breeding/FieldBook', 'Breeding/TrialNetwork',
    'Germplasm/CollectingMission', 'Germplasm/ConservationMembership',
    'Germplasm/McpdAdapter',
    'Germplasm/GenebankStorage', 'Germplasm/ViabilityTesting',
    'Germplasm/Regeneration', 'Germplasm/SafetyDuplication',
    'Germplasm/Acquisition', 'Germplasm/CustodyTransfer',
    'Germplasm/DisposalRecord', 'Germplasm/Quarantine',
    'Germplasm/DuplicateReview',
    'Phenotyping/QualityFlag', 'Phenotyping/ValueMissingness',
    'Phenotyping/CaptureWorkflow',
    'Genotyping/ReferenceAssembly', 'Genotyping/PipelineProvenance', 'Genotyping/VcfImport',
    'Genotyping/AssayDesign', 'Genotyping/AssayExecution',
    'Genotyping/VendorOrder', 'Genotyping/MarkerProbe',
    'Genotyping/GenomicDatasets', 'Genotyping/VcfExport',
    'Genotyping/GenotypeQc', 'Genotyping/GenotypeCallSemantics',
    'Genotyping/VariantAnnotation', 'Genotyping/GwasResult',
    'Breeding/Heritability', 'Breeding/GxeAnalysis',
    'Breeding/GenomicPrediction', 'Breeding/GenomicSelection',
    'Breeding/GeneticGain', 'Breeding/StabilityAnalysis',
    'Phenotyping/PhenotypeCapture', 'Phenotyping/RepeatedMeasurement',
    'Phenotyping/PhenotypeAnnotation',
    'Geospatial/LocationGeometry', 'Geospatial/FieldGeometry',
    'Geospatial/CrsTransform', 'Geospatial/FieldBoundary',
    'Instrumentation/CalibrationQuality', 'Instrumentation/SensorDevice',
    'Instrumentation/TelemetryNormalization', 'Instrumentation/EdgeGatewayHealth',
    'PlantHealth/DiseaseObservation', 'PlantHealth/DiagnosticEvidence',
    'PlantHealth/FieldScouting', 'PlantHealth/DiseaseResistance',
    'PlantHealth/CropHealthImage', 'PlantHealth/IpmStrategy',
    'PlantHealth/PestDiseaseRisk', 'PlantHealth/ThresholdAlert',
    'CropProduction/HarvestRecords', 'CropProduction/IrrigationOperation',
    'CropProduction/PlantingOperation', 'CropProduction/SprayApplication',
    'CropProduction/FertilizerApplication', 'CropProduction/Tillage',
    'CropProduction/YieldForecast', 'CropProduction/IrrigationAdvice',
    'CropProduction/CropCycle', 'CropProduction/SowingWindow',
    'CropProduction/CropSuitability', 'CropProduction/LocalConstraint',
    'CropProduction/Farm', 'CropProduction/NutrientAdvice',
    'CropProduction/CropRecommendation',
    'Research/HumanReview', 'Research/ExplanationEvidence',
    'Research/EvidencePack', 'Research/OutcomeFeedback',
    'Research/AnalysisMethods', 'Research/AnalysisResult',
    'Research/MixedModel', 'Research/PcaResult',
    'Research/ArtifactCatalogue', 'Research/ProtocolLibrary',
    'Research/PublicationReview', 'Research/ResearchAssets',
    'Research/Project', 'Research/ResearchLocation',
    'Research/ResearchProgram',
    'Environment/WeatherObservations', 'Environment/WeatherForecast',
    'Environment/ClimateNormals', 'Environment/SoilProfile',
    'Environment/WaterBalance',
})
LINK = re.compile(r'\]\(([^)]+)\)')


def audit(root: Path, reviewed: frozenset[str] = REVIEWED) -> dict:
    genx = root / REL
    errors: list[str] = []
    if not genx.is_dir():
        return {'total': 0, 'reviewed': 0, 'deferred': 0,
                'errors': [f'GenX specification directory absent: {genx}']}
    repository_root = root.resolve()
    files = sorted(genx.glob('*/*/GroupDescription.md'))
    known = {path.parent.relative_to(genx).as_posix(): path for path in files}
    for module in sorted(reviewed):
        file = known.get(module)
        if file is None:
            errors.append(f'{module}: reviewed GroupDescription.md missing')
            continue
        try:
            content = file.read_text(encoding='utf-8')
        except (OSError, UnicodeError) as exc:
            errors.append(f'{module}: unreadable group description: {exc}')
            continue
        if len(content.strip()) < 300:
            errors.append(f'{module}: reviewed group description reverted to a placeholder')
        if not re.search(r'^# Group\b', content, re.MULTILINE):
            errors.append(f'{module}: missing group heading')
        if '**Status:**' not in content or '**Sources:**' not in content:
            errors.append(f'{module}: status and source citations required')
        if not re.search(r'candidate|proposed', content, re.IGNORECASE):
            errors.append(f'{module}: draft or candidate maturity qualification missing')
        links = LINK.findall(content)
        if not links:
            errors.append(f'{module}: reviewed description requires local source links')
        for href in links:
            if '://' in href or href.startswith('/') or '#' in href:
                errors.append(f'{module}: source link must be a local, direct file path: {href}')
                continue
            # Resolve both traversal components and symlinks before trusting
            # a source link as repository-local evidence.
            target = (file.parent / href).resolve()
            if not target.is_relative_to(repository_root):
                errors.append(f'{module}: source link escapes repository: {href}')
                continue
            if not target.is_file():
                errors.append(f'{module}: dangling evidence link: {href}')
    return {'total': len(files), 'reviewed': len(reviewed),
            'deferred': len(set(known) - set(reviewed)), 'errors': errors,
            'note': 'Unreviewed placeholders are not evidence of finished scientific contracts.'}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    report = audit(args.root)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"GenX groups: {report['total']}; reviewed: {report['reviewed']}; deferred: {report['deferred']}")
        for error in report['errors']:
            print('FAIL: ' + error)
        print('No draft module is automatically deemed finalized.')
    return int(bool(report['errors']))


if __name__ == '__main__':
    raise SystemExit(main())
