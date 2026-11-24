#!/usr/bin/env python3
"""Audit verified incumbent BrAPI overlaps and unratified GenX typed links.

This is a bounded, evidence-backed regression gate, not fuzzy semantic matching
or a claim that a candidate GenX object is semantically equivalent to BrAPI.
Unlisted modules remain unreviewed; no maturity promotion is implied.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path('docs/assessment/BRAPI-GENX-STANDARDS-OVERLAP-EVIDENCE.json')
GENX = Path('Specification/BrAPI-GenX')
REVIEWED = {'ReferenceData/MeasurementScale', 'ReferenceData/MeasurementMethods',
            'ReferenceData/ReusableList', 'ReferenceData/CommonCropName',
            'ReferenceData/PersonReference'}


def _read(root: Path, path: Path, errors: list[str]) -> str | None:
    full = (root / path).resolve()
    if not full.is_relative_to(root.resolve()) or not full.is_file():
        errors.append(f'missing or out-of-repository source: {path}')
        return None
    try:
        return full.read_text(encoding='utf-8')
    except (OSError, UnicodeError) as exc:
        errors.append(f'unreadable source {path}: {exc}')
        return None


def _schema(root: Path, module: str, resource: str,
            errors: list[str], schema_file: str | None = None) -> dict | None:
    path = GENX / module / 'Schemas' / (schema_file or f'{resource}.yaml')
    body = _read(root, path, errors)
    if body is None:
        return None
    try:
        raw = yaml.safe_load(body)
        schema = raw['components']['schemas'][resource]
        if not isinstance(schema, dict) or not isinstance(schema.get('properties'), dict):
            raise ValueError('schema properties missing')
        return schema
    except (ValueError, TypeError, KeyError, yaml.YAMLError) as exc:
        errors.append(f'{module}: invalid candidate resource schema: {exc}')
        return None


def audit(root: Path, manifest: Path = MANIFEST) -> dict:
    errors: list[str] = []
    content = _read(root, manifest, errors)
    if content is None:
        return {'overlaps_checked': 0, 'links_checked': 0, 'errors': errors}
    try:
        data = json.loads(content)
        rows = data['official_overlap']
        links = data['unratified_links']
        if data.get('version') != 1 or not isinstance(rows, list) or not isinstance(links, list):
            raise ValueError('invalid evidence manifest version or collections')
    except (json.JSONDecodeError, KeyError, ValueError, TypeError) as exc:
        return {'overlaps_checked': 0, 'links_checked': 0,
                'errors': [f'invalid evidence manifest: {exc}']}
    seen: set[str] = set()
    for entry in rows:
        try:
            module, rfc, resource = (entry[key] for key in ('module', 'rfc', 'resource'))
            official, route, public = (entry[key] for key in ('official', 'route', 'public_route'))
        except (KeyError, TypeError) as exc:
            errors.append(f'malformed overlap entry: {exc}')
            continue
        if module in seen:
            errors.append(f'duplicate overlap evidence for: {module}')
        seen.add(module)
        if module not in REVIEWED:
            errors.append(f'unreviewed module asserted as accepted evidence: {module}')
        if not public.startswith('/brapi/v2/') or public != '/brapi/v2' + route:
            errors.append(f'{module}: official public route identity invalid: {public}')
        source = _read(root, Path(official), errors)
        if source is not None:
            try:
                official_spec = yaml.safe_load(source)
                operations = official_spec['paths'][route]
                if not isinstance(operations, dict) or not ('get' in operations or 'post' in operations):
                    raise ValueError('missing GET/POST')
            except (KeyError, TypeError, ValueError, yaml.YAMLError) as exc:
                errors.append(f'{module}: official operation {route} missing: {exc}')
        _schema(root, module, resource, errors)
        for path in (GENX / module / 'README.md',
                     GENX / module / 'GroupDescription.md',
                     GENX / 'RFCs' / rfc):
            prose = _read(root, path, errors)
            if prose is None:
                continue
            if public not in prose:
                errors.append(f'{path}: must acknowledge official {public}')
            human_resource = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', resource)
            if re.search(r'BrAPI\s+v2\.1\s+has\s+no\s+(?:place\s+to\s+record\s+)?'
                         + re.escape(human_resource) + r'\b',
                         prose, flags=re.IGNORECASE):
                errors.append(f'{path}: unsupported absence claim for {resource}')
    if seen != REVIEWED:
        errors.append('overlap evidence inventory does not cover exactly the pinned modules: '
                      + ', '.join(sorted(REVIEWED.symmetric_difference(seen))))
    checked_links = 0
    for entry in links:
        try:
            module, rfc, resource, target, decision = (
                entry[key] for key in ('module', 'rfc', 'resource', 'target', 'decision'))
        except (KeyError, TypeError) as exc:
            errors.append(f'malformed unratified-link entry: {exc}')
            continue
        schema = _schema(root, module, resource, errors, entry.get('schema_file'))
        if schema is None:
            continue
        checked_links += 1
        # No candidate field or $ref can assert the unapproved target
        # without re-reviewing both this manifest and the open decision.
        if target.lower() in json.dumps(schema, sort_keys=True).lower():
            errors.append(f'{module}: candidate now mentions unratified target {target} ({decision})')
        proposal = _read(root, GENX / 'RFCs' / rfc, errors)
        if proposal is not None:
            if decision not in proposal:
                errors.append(f'{module}: missing open decision {decision}')
            if not re.search(r'(?:no typed|not present|no link)', proposal, re.IGNORECASE):
                errors.append(f'{module}: RFC must qualify missing typed link')
    return {'overlaps_checked': len(seen), 'links_checked': checked_links,
            'errors': errors,
            'note': 'Source overlap does not establish semantic equivalence or normative maturity.'}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    result = audit(args.root)
    if args.json:
        print(json.dumps(result, sort_keys=True, indent=2))
    else:
        print(f"Official overlaps: {result['overlaps_checked']}; "
              f"unratified links: {result['links_checked']}")
        for error in result['errors']:
            print('FAIL: ' + error)
        print(result.get('note', ''))
    return int(bool(result['errors']))


if __name__ == '__main__':
    raise SystemExit(main())
