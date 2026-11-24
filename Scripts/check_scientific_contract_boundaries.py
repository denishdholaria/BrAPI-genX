#!/usr/bin/env python3
"""Guard documented schema facts in the non-normative Mission 008 review.

This verifies source-contract field evidence only; it cannot approve a semantic
neighbor, a scientific mapping, or a normative interoperability contract.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import yaml

LEDGER = Path('Specification/BrAPI-GenX/Conformance/semantic-neighbor-review.yaml')
REVIEW = Path('docs/assessment/BRAPI-GENX-MISSION-008-EXECUTION-EVIDENCE-REVIEW.md')
BASE = Path('Specification/BrAPI-GenX')
# module, schema relative path, schema name, fields present, fields required, fields absent
SCHEMAS = {
    'AssayExecution': ('Genotyping/AssayExecution/Schemas/AssayExecution.yaml', 'AssayExecution', ('assayDbId',), ('assayExecutionDbId',), ('assayDesignDbId',)),
    'AssayDesign': ('Genotyping/AssayDesign/Schemas/AssayDesign.yaml', 'AssayDesign', (), ('assayDesignDbId',), ()),
    'VcfExport': ('Genotyping/VcfExport/Schemas/VcfExport.yaml', 'VcfExport', ('format',), ('vcfExportDbId',), ()),
    'VcfImport': ('Genotyping/VcfImport/Schemas/VcfImport.yaml', 'VcfImport', ('sourceFile',), ('genomicDatasetDbId',), ('vcfExportDbId',)),
    'FieldBook': ('Breeding/FieldBook/Schemas/FieldBook.yaml', 'FieldBook', ('fieldDbId',), ('fieldBookDbId',), ()),
    'FieldScouting': ('PlantHealth/FieldScouting/Schemas/FieldScouting.yaml', 'FieldScouting', ('fieldDbId',), ('fieldScoutingDbId',), ('fieldBookDbId',)),
    'YieldMap': ('Geospatial/YieldMap/Schemas/YieldMap.yaml', 'YieldMap', ('harvestRecordDbId', 'resolutionM'), ('yieldMapDbId',), ()),
    'HarvestRecords': ('CropProduction/HarvestRecords/Schemas/HarvestRecord.yaml', 'HarvestRecord', (), ('harvestRecordDbId', 'quantity', 'unit'), ()),
    'QualityFlag': ('Phenotyping/QualityFlag/Schemas/QualityFlag.yaml', 'QualityFlag', ('flag',), ('qualityFlagDbId',), ('variableDbId',)),
    'VariableTerms': ('ReferenceData/VariableTerms/Schemas/VariableTerm.yaml', 'VariableTerm', (), ('variableDbId', 'version'), ()),
    'ReferenceAssembly': ('Genotyping/ReferenceAssembly/Schemas/ReferenceAssembly.yaml', 'ReferenceAssembly', ('assemblyAccession', 'version'), ('referenceAssemblyDbId',), ()),
    'GenomicDatasets': ('Genotyping/GenomicDatasets/Schemas/GenomicDataset.yaml', 'GenomicDataset', (), ('genomicDatasetDbId', 'referenceAssembly'), ('referenceAssemblyDbId',)),
}
# Legal progression is validated by check_semantic_neighbor_governance.py.
# This source-evidence guard only rejects a regression to unreviewed or unknown status.
REVIEWED_STATES = frozenset({'requires-decision', 'evidence-backed-proposed', 'rejected', 'superseded'})
PAIRS = (
    ('AssayExecution', 'AssayDesign'),
    ('VcfExport', 'VcfImport'),
    ('FieldBook', 'FieldScouting'),
    ('YieldMap', 'HarvestRecords'),
    ('QualityFlag', 'VariableTerms'),
    ('ReferenceAssembly', 'GenomicDatasets'),
)


def check(root: Path) -> list[str]:
    """Return reasons for source-schema or reviewed-ledger drift."""
    problems: list[str] = []
    for module, (relative, name, present, required, absent) in SCHEMAS.items():
        file = root / BASE / relative
        if not file.is_file():
            problems.append(f'{module}: missing schema {file.relative_to(root)}')
            continue
        try:
            doc = yaml.safe_load(file.read_text(encoding='utf-8'))
            value = doc['components']['schemas'][name]
            properties = value['properties']
        except (OSError, UnicodeError, yaml.YAMLError, KeyError, TypeError) as exc:
            problems.append(f'{module}: malformed schema: {exc}')
            continue
        if not isinstance(properties, dict):
            problems.append(f'{module}: properties must be a mapping')
            continue
        required_fields = value.get('required', [])
        if not isinstance(required_fields, list):
            problems.append(f'{module}: required must be a list')
            continue
        for field in present:
            if field not in properties:
                problems.append(f'{module}: documented property {field} is absent')
        for field in required:
            if field not in properties or field not in required_fields:
                problems.append(f'{module}: documented required property {field} is absent or optional')
        for field in absent:
            if field in properties:
                problems.append(f'{module}: formerly absent property {field} was added; reassess Mission 008 evidence')

    if not (root / REVIEW).is_file():
        problems.append(f'Missing Mission 008 assessment: {REVIEW}')
    try:
        ledger = yaml.safe_load((root / LEDGER).read_text(encoding='utf-8'))
        entries = ledger['entries']
        if not isinstance(entries, list):
            raise TypeError('entries must be a list')
    except (OSError, UnicodeError, yaml.YAMLError, TypeError, KeyError) as exc:
        return problems + [f'Cannot load semantic-neighbor ledger: {exc}']

    for source, target in PAIRS:
        matches = [e for e in entries if isinstance(e, dict) and e.get('sourceModule') == source
                   and e.get('targetModule') == target and e.get('targetOperationId') is not None]
        if len(matches) != 3 or len({e.get('id') for e in matches}) != 3:
            problems.append(f'{source} -> {target}: expected three distinct retained neighbors')
            continue
        for e in matches:
            if e.get('reviewStatus') not in REVIEWED_STATES:
                problems.append(f'{source} -> {target}: reviewed relation reverted or has unknown status: {e.get("reviewStatus")}')
            evidence = e.get('documentaryEvidence')
            if not isinstance(evidence, list) or str(REVIEW) not in evidence:
                problems.append(f'{source} -> {target}: assessment citation missing from {e.get("id")}')
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    root = parser.parse_args().root.resolve()
    issues = check(root)
    if issues:
        for issue in issues:
            print('FAIL:', issue)
        return 1
    print('PASS: six non-normative scientific source-contract boundaries remain traceable')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
