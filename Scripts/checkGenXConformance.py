#!/usr/bin/env python3
"""
Static and live conformance checks for the BrAPI-GenX proposal (RFC-001).

Static probes (S-01..S-08) execute against this repo only. Live probes
(L-01..L-07) execute against a GenX server and SKIP without --server.
The probe list in Specification/BrAPI-GenX/Conformance/probes.yaml is the
authority; this script is one execution of it.

Usage:
    python Scripts/checkGenXConformance.py [--root <workspace_root>]
    python Scripts/checkGenXConformance.py --server https://host/brapi/v3 [--expired-job JOB_0000]

Options:
    --root         Root of the BrAPI workspace (default: current directory)
    --server       Base URL of a GenX server, e.g. https://host/brapi/v3
    --expired-job  A known-expired jobDbId for probe L-05 (else L-05 skips)
"""

import argparse
import copy
import glob
import hashlib
import json
import os
import re
import sys
import uuid

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: python3 -c 'import yaml' must succeed")

try:
    from urllib import request as urlrequest
    from urllib.error import HTTPError
except ImportError:  # pragma: no cover
    urlrequest = None


REF_RE = re.compile(r"""\$ref:\s*['"]?#/components/(\w+)/([\w.-]+)['"]?""")
DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")
TERM_ID_RE = re.compile(r"^[^:/]+:[^:/]+:[^:/]+$")
DOI_RE = re.compile(r"^10\.\d{4,}/.+")
DECIMAL_RE = re.compile(r"^-?\d+(\.\d+)?$")
HTTP_METHODS = {"GET", "POST", "PUT", "DELETE"}
OPENAPI_METHODS = {"GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "TRACE"}
TERMINAL = {"COMPLETED", "FAILED", "CANCELLED", "EXPIRED"}


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def walk_files(root, *parts):
    return glob.glob(os.path.join(root, *parts), recursive=True)


def collect_definitions(paths):
    """Map (section, name) -> defining file for components blocks."""
    found = {}
    for path in paths:
        try:
            doc = load_yaml(path)
        except Exception:
            continue
        if not isinstance(doc, dict):
            continue
        components = doc.get("components")
        if not isinstance(components, dict):
            continue
        for section, block in components.items():
            if isinstance(block, dict):
                for name in block:
                    found.setdefault((section, name), path)
    return found


def collect_refs(paths):
    """List of (section, name, file) for every local components $ref."""
    refs = []
    ref_pattern = re.compile(r"#/components/(\w+)/([\w.-]+)")
    for path in paths:
        with open(path, "r", encoding="utf-8") as fh:
            for match in ref_pattern.finditer(fh.read()):
                refs.append((match.group(1), match.group(2), path))
    return refs


def collect_values(doc, keys):
    """Recursively collect values for any of the given keys."""
    hits = []
    if isinstance(doc, dict):
        for key, value in doc.items():
            if key in keys:
                hits.append(value)
            hits.extend(collect_values(value, keys))
    elif isinstance(doc, list):
        for item in doc:
            hits.extend(collect_values(item, keys))
    return hits


def parse_rfc3339(value):
    from datetime import datetime
    text = value.replace("Z", "+00:00") if value.endswith("Z") else value
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        raise ValueError("missing timezone offset")
    return parsed


class Results:
    def __init__(self):
        self.failures = 0
        self.skips = 0

    def report(self, probe_id, title, state, detail=""):
        suffix = f" — {detail}" if detail else ""
        print(f"{state} {probe_id} {title}{suffix}")
        if state == "FAIL":
            self.failures += 1
        elif state == "SKIP":
            self.skips += 1


# --------------------------------------------------------------------------
# Static probes
# --------------------------------------------------------------------------

def check_refs_resolve(root, probe, ctx, results):
    genx = os.path.join(root, "Specification", "BrAPI-GenX")
    genx_files = walk_files(genx, "**", "*.yaml")
    for path in genx_files:
        try:
            load_yaml(path)
        except Exception as exc:
            return results.report(
                probe["id"], probe["title"], "FAIL",
                f"{os.path.relpath(path, root)} is not parseable YAML: {exc}")
    shared = []
    for area in ("Components", "OpenAPI-Components"):
        for section in ("Parameters", "Responses", "Schemas"):
            shared.extend(walk_files(root, "Specification", area, section, "*.yaml"))
    # Committed V2.1 module files are a read-only definition scope: GenX may
    # reference these names (the generator merges all modules) but must never
    # redefine them. V2.1 files themselves are not modified by this check.
    v21 = []
    for module in ("BrAPI-Core", "BrAPI-Phenotyping", "BrAPI-Genotyping", "BrAPI-Germplasm"):
        v21.extend(walk_files(root, "Specification", module, "**", "*.yaml"))
    genx_defined = collect_definitions(genx_files)
    base_defined = collect_definitions(shared + v21)
    defined = dict(base_defined)
    defined.update(genx_defined)
    problems = [
        f"{name} (referenced from {os.path.relpath(path, root)})"
        for section, name, path in collect_refs(genx_files)
        if (section, name) not in defined
    ]
    problems.extend(
        f"GenX redefines '{name}' (also defined in {os.path.relpath(base_defined[(section, name)], root)})"
        for section, name in genx_defined
        if (section, name) in base_defined
    )
    if problems:
        results.report(probe["id"], probe["title"], "FAIL", "; ".join(problems))
    else:
        results.report(probe["id"], probe["title"], "PASS")


def check_required_fields(root, probe, ctx, results):
    conf = os.path.join(root, "Specification", "BrAPI-GenX", "Conformance")
    required_map = ctx["required_map"]
    problems = []
    for stem, spec in required_map.items():
        doc = load_json(os.path.join(conf, "fixtures", f"{stem}.json"))
        if spec["schema"] == "ProvenanceEnvelope" and "provenance" in doc:
            target = doc["provenance"]
        elif isinstance(doc.get("result"), dict):
            target = doc["result"]
        else:
            target = doc
        for field in spec.get("required", []):
            if field not in target or target[field] is None:
                problems.append(f"{stem}.json missing required '{field}'")
    if problems:
        results.report(probe["id"], probe["title"], "FAIL", "; ".join(problems))
    else:
        results.report(probe["id"], probe["title"], "PASS")


def check_job_enums(root, probe, ctx, results):
    conf = os.path.join(root, "Specification", "BrAPI-GenX", "Conformance")
    job_schema = load_yaml(
        os.path.join(root, "Specification", "BrAPI-GenX", "Jobs", "Schemas", "Job.yaml")
    )
    allowed_status = set(
        job_schema["components"]["schemas"]["Job"]["properties"]["status"]["enum"]
    )
    problems = []
    for stem in ("job_accepted", "job_completed"):
        status = load_json(os.path.join(conf, "fixtures", f"{stem}.json"))["result"]["status"]
        if status not in allowed_status:
            problems.append(f"{stem}.json status '{status}' outside schema enum")
    info = load_json(os.path.join(conf, "fixtures", "serverinfov3.json"))
    for cap in info["result"].get("capabilities", []):
        unknown = [m for m in cap.get("methods", []) if m not in HTTP_METHODS]
        if unknown:
            problems.append(f"capability '{cap.get('name')}' methods {unknown}")
    if problems:
        results.report(probe["id"], probe["title"], "FAIL", "; ".join(problems))
    else:
        results.report(probe["id"], probe["title"], "PASS")


def check_digest_format(root, probe, ctx, results):
    conf = os.path.join(root, "Specification", "BrAPI-GenX", "Conformance", "fixtures")
    keys = {"inputsDigest", "responseDigest", "queryDigest"}
    problems, checked = [], 0
    for path in walk_files(conf, "*.json"):
        for value in collect_values(load_json(path), keys):
            checked += 1
            if not isinstance(value, str) or not DIGEST_RE.match(value):
                problems.append(f"{os.path.basename(path)}: bad digest '{value}'")
    if not checked:
        problems.append("no digests found in fixtures")
    if problems:
        results.report(probe["id"], probe["title"], "FAIL", "; ".join(problems))
    else:
        results.report(probe["id"], probe["title"], "PASS", f"{checked} digests")


def check_datetime_format(root, probe, ctx, results):
    conf = os.path.join(root, "Specification", "BrAPI-GenX", "Conformance", "fixtures")
    keys = {"recordedAt", "createdAt", "updatedAt", "expiresAt"}
    problems, checked = [], 0
    for path in walk_files(conf, "*.json"):
        for value in collect_values(load_json(path), keys):
            checked += 1
            try:
                parse_rfc3339(value)
            except Exception:
                problems.append(f"{os.path.basename(path)}: bad date-time '{value}'")
    if not checked:
        problems.append("no date-times found in fixtures")
    if problems:
        results.report(probe["id"], probe["title"], "FAIL", "; ".join(problems))
    else:
        results.report(probe["id"], probe["title"], "PASS", f"{checked} date-times")


def canonical(doc):
    return json.dumps(doc, sort_keys=True, separators=(",", ":"))


def check_idempotency_relations(root, probe, ctx, results):
    conf = os.path.join(root, "Specification", "BrAPI-GenX", "Conformance", "fixtures")
    submit = load_json(os.path.join(conf, "job_submit.json"))
    replay = load_json(os.path.join(conf, "job_submit_replay.json"))
    conflict = load_json(os.path.join(conf, "job_submit_conflict.json"))
    problems = []
    if canonical(submit) != canonical(replay):
        problems.append("replay body differs from submit body")
    if conflict.get("idempotencyKey") != submit.get("idempotencyKey"):
        problems.append("conflict fixture shares no key with submit")
    if canonical(conflict) == canonical(submit):
        problems.append("conflict body identical to submit body")
    if problems:
        results.report(probe["id"], probe["title"], "FAIL", "; ".join(problems))
    else:
        results.report(probe["id"], probe["title"], "PASS")


def check_capability_grounding(root, probe, ctx, results):
    genx = os.path.join(root, "Specification", "BrAPI-GenX")
    info = load_json(os.path.join(genx, "Conformance", "fixtures", "serverinfov3.json"))
    dirs = ctx.get("capability_dirs", {})
    problems = []
    for cap in info["result"].get("capabilities", []):
        name = cap.get("name")
        if name not in ctx.get("genx_object_names", []):
            continue
        target = os.path.join(genx, dirs.get(name, ""))
        schemas = walk_files(target, "Schemas", "*.yaml") if dirs.get(name) else []
        if not schemas:
            problems.append(f"capability '{name}' has no backing schema")
    if problems:
        results.report(probe["id"], probe["title"], "FAIL", "; ".join(problems))
    else:
        results.report(probe["id"], probe["title"], "PASS")


def check_term_id_format(root, probe, ctx, results):
    conf = os.path.join(root, "Specification", "BrAPI-GenX", "Conformance", "fixtures")
    keys = {"variableDbId", "traitDbId", "methodDbId", "scaleDbId", "supersededBy"}
    problems, checked = [], 0
    for stem in ("term_submit", "term_submit_conflict", "term_accepted"):
        doc = load_json(os.path.join(conf, f"{stem}.json"))
        target = doc.get("result") if isinstance(doc.get("result"), dict) else doc
        for value in collect_values(target, keys):
            checked += 1
            if not isinstance(value, str) or not TERM_ID_RE.match(value):
                problems.append(f"{stem}.json: identifier '{value}' is not namespaced")
    if not checked:
        problems.append("no term identifiers found in fixtures")
    if problems:
        results.report(probe["id"], probe["title"], "FAIL", "; ".join(problems))
    else:
        results.report(probe["id"], probe["title"], "PASS", f"{checked} identifiers")


def check_decimal_format(root, probe, ctx, results):
    conf = os.path.join(root, "Specification", "BrAPI-GenX", "Conformance", "fixtures")
    problems, checked = [], 0
    for stem in ("ledger_submit", "ledger_submit_conflict", "ledger_accepted"):
        doc = load_json(os.path.join(conf, f"{stem}.json"))
        target = doc.get("result") if isinstance(doc.get("result"), dict) else doc
        for value in collect_values(target, {"quantity"}):
            checked += 1
            if not isinstance(value, str) or not DECIMAL_RE.match(value):
                problems.append(f"{stem}.json: quantity {value!r} is not a decimal string")
    if not checked:
        problems.append("no quantities found in fixtures")
    if problems:
        results.report(probe["id"], probe["title"], "FAIL", "; ".join(problems))
    else:
        results.report(probe["id"], probe["title"], "PASS", f"{checked} quantities")


def check_model_shape(root, probe, ctx, results):
    conf = os.path.join(root, "Specification", "BrAPI-GenX", "Conformance", "fixtures")
    schema = load_yaml(
        os.path.join(root, "Specification", "BrAPI-GenX", "Models",
                     "Schemas", "ModelArtifact.yaml")
    )
    allowed_status = set(
        schema["components"]["schemas"]["ModelArtifact"]["properties"]["status"]["enum"]
    )
    problems, checked = [], 0
    for stem in ("model_submit", "model_submit_conflict", "model_accepted"):
        doc = load_json(os.path.join(conf, f"{stem}.json"))
        target = doc.get("result") if isinstance(doc.get("result"), dict) else doc
        for value in collect_values(target, {"modelDbId", "supersededBy"}):
            checked += 1
            if not isinstance(value, str) or not TERM_ID_RE.match(value):
                problems.append(f"{stem}.json: identifier '{value}' is not namespaced")
        for value in collect_values(target, {"artifactDigest", "trainingDataDigest"}):
            checked += 1
            if not isinstance(value, str) or not DIGEST_RE.match(value):
                problems.append(f"{stem}.json: bad digest '{value}'")
        for value in collect_values(target, {"status"}):
            checked += 1
            if value not in allowed_status:
                problems.append(f"{stem}.json: status '{value}' outside schema enum")
    if not checked:
        problems.append("no model fields found in fixtures")
    if problems:
        results.report(probe["id"], probe["title"], "FAIL", "; ".join(problems))
    else:
        results.report(probe["id"], probe["title"], "PASS", f"{checked} fields")


def check_matrix_shape(root, probe, ctx, results):
    conf = os.path.join(root, "Specification", "BrAPI-GenX", "Conformance", "fixtures")
    schema = load_yaml(
        os.path.join(root, "Specification", "BrAPI-GenX", "Genomics",
                     "Schemas", "VariantMatrix.yaml")
    )
    allowed_format = set(
        schema["components"]["schemas"]["VariantMatrix"]["properties"]["format"]["enum"]
    )
    problems, checked = [], 0
    for stem in ("matrix_submit", "matrix_submit_conflict", "matrix_accepted"):
        doc = load_json(os.path.join(conf, f"{stem}.json"))
        target = doc.get("result") if isinstance(doc.get("result"), dict) else doc
        for value in collect_values(target, {"matrixDbId"}):
            checked += 1
            if not isinstance(value, str) or not TERM_ID_RE.match(value):
                problems.append(f"{stem}.json: identifier '{value}' is not namespaced")
        for value in collect_values(target, {"fileURL", "indexURL"}):
            checked += 1
            if not isinstance(value, str) or not value.startswith(("https://", "drs://")):
                problems.append(f"{stem}.json: URL '{value}' is not retrievable")
        for value in collect_values(target, {"fileDigest", "indexDigest"}):
            checked += 1
            if not isinstance(value, str) or not DIGEST_RE.match(value):
                problems.append(f"{stem}.json: bad digest '{value}'")
        for value in collect_values(target, {"format"}):
            checked += 1
            if value not in allowed_format:
                problems.append(f"{stem}.json: format '{value}' outside schema enum")
    if not checked:
        problems.append("no matrix fields found in fixtures")
    if problems:
        results.report(probe["id"], probe["title"], "FAIL", "; ".join(problems))
    else:
        results.report(probe["id"], probe["title"], "PASS", f"{checked} fields")


def check_package_shape(root, probe, ctx, results):
    conf = os.path.join(root, "Specification", "BrAPI-GenX", "Conformance", "fixtures")
    schema = load_yaml(
        os.path.join(root, "Specification", "BrAPI-GenX", "FAIR",
                     "Schemas", "FAIRPackage.yaml")
    )
    allowed_rights = set(
        schema["components"]["schemas"]["FAIRPackage"]["properties"]["accessRights"]["enum"]
    )
    problems, checked = [], 0
    for stem in ("package_submit", "package_submit_conflict", "package_accepted",
                 "package_embargoed"):
        doc = load_json(os.path.join(conf, f"{stem}.json"))
        target = doc.get("result") if isinstance(doc.get("result"), dict) else doc
        for value in collect_values(target, {"packageDbId"}):
            checked += 1
            if not isinstance(value, str) or not TERM_ID_RE.match(value):
                problems.append(f"{stem}.json: identifier '{value}' is not namespaced")
        for value in collect_values(target, {"license"}):
            checked += 1
            if not isinstance(value, str) or not value.strip():
                problems.append(f"{stem}.json: license is empty")
        for ident in collect_values(target, {"identifiers"}):
            for entry in ident if isinstance(ident, list) else []:
                if not isinstance(entry, dict):
                    continue
                checked += 1
                if entry.get("type") == "DOI" and not DOI_RE.match(entry.get("value", "")):
                    problems.append(f"{stem}.json: malformed DOI '{entry.get('value')}'")
                if not entry.get("value"):
                    problems.append(f"{stem}.json: identifier without value")
        for value in collect_values(target, {"accessRights"}):
            checked += 1
            if value not in allowed_rights:
                problems.append(f"{stem}.json: accessRights '{value}' outside schema enum")
        for value in collect_values(target, {"embargoUntil"}):
            checked += 1
            try:
                parse_rfc3339(value)
            except Exception:
                problems.append(f"{stem}.json: bad embargoUntil '{value}'")
    if not checked:
        problems.append("no package fields found in fixtures")
    if problems:
        results.report(probe["id"], probe["title"], "FAIL", "; ".join(problems))
    else:
        results.report(probe["id"], probe["title"], "PASS", f"{checked} fields")


def check_telemetry_required(root, probe, ctx, results):
    conf = os.path.join(root, "Specification", "BrAPI-GenX", "Conformance", "fixtures")
    problems, checked = [], 0
    for stem in ("telemetry_batch", "telemetry_batch_replay", "telemetry_batch_conflict"):
        doc = load_json(os.path.join(conf, f"{stem}.json"))
        if not isinstance(doc, list):
            problems.append(f"{stem}.json is not an array")
            continue
        for point in doc:
            checked += 1
            for field in ("deviceDbId", "sensorDbId", "timestamp", "value"):
                if field not in point or point[field] is None:
                    problems.append(f"{stem}.json point missing required '{field}'")
    if problems:
        results.report(probe["id"], probe["title"], "FAIL", "; ".join(problems))
    else:
        results.report(probe["id"], probe["title"], "PASS", f"{checked} points")


def check_telemetry_shape(root, probe, ctx, results):
    conf = os.path.join(root, "Specification", "BrAPI-GenX", "Conformance", "fixtures")
    schema = load_yaml(
        os.path.join(root, "Specification", "BrAPI-GenX", "Telemetry",
                     "Schemas", "TelemetryPoint.yaml")
    )
    allowed_quality = set(
        schema["components"]["schemas"]["TelemetryPoint"]["properties"]["quality"]["enum"]
    )
    problems, checked = [], 0
    for stem in ("telemetry_batch", "telemetry_batch_replay", "telemetry_batch_conflict"):
        for point in load_json(os.path.join(conf, f"{stem}.json")):
            checked += 1
            value = point.get("value")
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                problems.append(f"{stem}.json: value {value!r} is not a JSON number")
            try:
                parse_rfc3339(point.get("timestamp", ""))
            except Exception:
                problems.append(f"{stem}.json: bad timestamp '{point.get('timestamp')}'")
            quality = point.get("quality", "good")
            if quality not in allowed_quality:
                problems.append(f"{stem}.json: quality '{quality}' outside schema enum")
    if not checked:
        problems.append("no telemetry points found in fixtures")
    if problems:
        results.report(probe["id"], probe["title"], "FAIL", "; ".join(problems))
    else:
        results.report(probe["id"], probe["title"], "PASS", f"{checked} points")


def check_v21_fallback_shape(root, probe, ctx, results):
    doc = load_json(
        os.path.join(
            root, "Specification", "BrAPI-GenX", "Conformance",
            "fixtures", "serverinfo_v21_only.json",
        )
    )
    problems = []
    calls = doc.get("result", {}).get("calls")
    if not calls:
        problems.append("no calls array in fallback fixture")
    else:
        for call in calls:
            for field in ("service", "versions", "methods"):
                if field not in call:
                    problems.append(f"call missing '{field}': {call}")
    if problems:
        results.report(probe["id"], probe["title"], "FAIL", "; ".join(problems))
    else:
        results.report(probe["id"], probe["title"], "PASS")



def normalize_operation_path(path):
    """Normalize path parameter names for cross-file route comparison."""
    return re.sub(re.escape("{") + r"[^{}]+" + re.escape("}"), "{}", path)


def collect_api_operations(paths):
    """Read operation identity tuples from OpenAPI YAML files."""
    operations = []
    supported_methods = {method.lower() for method in OPENAPI_METHODS}
    for path in paths:
        doc = load_yaml(path)
        path_items = doc.get("paths", {}) if isinstance(doc, dict) else {}
        if not isinstance(path_items, dict):
            continue
        for route, path_item in path_items.items():
            if not isinstance(path_item, dict):
                continue
            for method, operation in path_item.items():
                if method.lower() not in supported_methods or not isinstance(operation, dict):
                    continue
                operations.append({
                    "method": method.upper(),
                    "path": normalize_operation_path(route),
                    "operation_id": operation.get("operationId"),
                    "summary": operation.get("summary"),
                    "description": operation.get("description"),
                    "file": path,
                })
    return operations


def check_endpoint_identity(root, probe, ctx, results):
    """Fail closed on unnamed GenX operations or unregistered V2.1 route reuse."""
    genx_root = os.path.join(root, "Specification", "BrAPI-GenX")
    genx_files = walk_files(genx_root, "**", "*.yaml")
    v21_files = []
    for module in ("BrAPI-Core", "BrAPI-Phenotyping", "BrAPI-Genotyping", "BrAPI-Germplasm"):
        v21_files.extend(walk_files(root, "Specification", module, "**", "*.yaml"))

    problems = []
    try:
        genx_ops = collect_api_operations(genx_files)
        v21_ops = collect_api_operations(v21_files)
        register = load_yaml(os.path.join(
            genx_root, "Conformance", "endpoint-overlaps.yaml"
        ))
    except Exception as exc:
        return results.report(
            probe["id"], probe["title"], "FAIL",
            f"could not load API operations/overlap register: {type(exc).__name__}: {exc}"
        )

    # Operation identifiers are the stable contract names consumed by tools,
    # generated clients, conformance evidence, and AI agents.
    ids = {}
    genx_route_keys = set()
    for op in genx_ops:
        op_id = op["operation_id"]
        where = f"{os.path.relpath(op['file'], root)}: {op['method']} {op['path']}"
        if not isinstance(op_id, str) or not op_id:
            problems.append(f"{where} has no operationId")
        else:
            if not re.fullmatch(r"genx[A-Z][A-Za-z0-9]*", op_id):
                problems.append(f"{where} has operationId '{op_id}' outside required genxVerbNoun form")
            if op_id in ids:
                problems.append(f"duplicate operationId '{op_id}' in {ids[op_id]} and {where}")
            else:
                ids[op_id] = where
        if not isinstance(op["summary"], str) or not op["summary"].strip():
            problems.append(f"{where} has no summary")
        if not isinstance(op["description"], str) or not op["description"].strip():
            problems.append(f"{where} has no description")
        route_key = (op["method"], op["path"])
        if route_key in genx_route_keys:
            problems.append(f"duplicate GenX method/path template {op['method']} {op['path']}")
        genx_route_keys.add(route_key)

    # Also check for future collisions with any operation IDs already present
    # in the V2.1 modules; empty IDs are not part of the uniqueness set.
    v21_ids = {
        op["operation_id"] for op in v21_ops
        if isinstance(op["operation_id"], str) and op["operation_id"]
    }
    for op_id in sorted(set(ids) & v21_ids):
        problems.append(f"GenX operationId '{op_id}' collides with a V2.1 operationId")

    # The human/agent-facing catalogue must describe exactly the same
    # operations as the machine-readable OpenAPI endpoint files.
    catalogue_path = os.path.join(genx_root, "ENDPOINT-IDENTITY.md")
    documented_operations = set()
    catalogue_rows_seen = set()
    try:
        with open(catalogue_path, "r", encoding="utf-8") as catalogue_file:
            catalogue_lines = catalogue_file.read().splitlines()
        in_catalogue = False
        catalogue_header_seen = False
        expected_catalogue_headers = [
            "full route", "method", "stable operation id",
            "primary meaning", "boundary / do not infer",
        ]
        for line in catalogue_lines:
            if line.startswith("## "):
                in_catalogue = line.strip() == "## 5. Current operation catalogue"
                continue
            # Do not interpret adjacent-resource comparison tables as route
            # inventory rows. Only the explicitly named catalogue is parsed.
            if not in_catalogue or not line.lstrip().startswith("|"):
                continue
            cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
            if not cells:
                continue
            if cells[0].lower() == "full route":
                headers = [cell.strip().lower() for cell in cells]
                if headers != expected_catalogue_headers:
                    problems.append(
                        "endpoint catalogue headers must be Full route | Method | "
                        "Stable operation ID | Primary meaning | Boundary / do not infer"
                    )
                catalogue_header_seen = True
                continue
            if not cells[0].startswith("/brapi/v3/"):
                continue
            if not catalogue_header_seen:
                problems.append("endpoint catalogue data appears before its required header row")
            if len(cells) < 5:
                problems.append(
                    f"catalogue row must include a meaning and a boundary / do not infer field: {line}"
                )
                continue
            full_route, method, op_id = cells[0], cells[1].upper(), cells[2]
            if not cells[3].strip():
                problems.append(f"catalogue row {method} {full_route} has no primary meaning")
            if not cells[4].strip():
                problems.append(f"catalogue row {method} {full_route} has no boundary / do not infer")
            if not re.fullmatch(r"/brapi/v3/.+", full_route):
                problems.append(f"catalogue route is not generation-qualified: {full_route}")
                continue
            if method not in OPENAPI_METHODS:
                problems.append(f"catalogue route {full_route} has invalid method '{method}'")
                continue
            if not re.fullmatch(r"genx[A-Z][A-Za-z0-9]*", op_id):
                problems.append(f"catalogue route {method} {full_route} has invalid/missing operationId '{op_id}'")
                continue
            triple = (method, normalize_operation_path(full_route[len("/brapi/v3"):]), op_id)
            if triple in catalogue_rows_seen:
                problems.append(f"duplicate endpoint catalogue row: {method} {full_route} ({op_id})")
            catalogue_rows_seen.add(triple)
            documented_operations.add(triple)
    except Exception as exc:
        problems.append(f"could not read endpoint catalogue {os.path.relpath(catalogue_path, root)}: {type(exc).__name__}: {exc}")

    if not catalogue_header_seen:
        problems.append("endpoint catalogue has no required header row")

    actual_operations = {
        (op["method"], op["path"], op["operation_id"])
        for op in genx_ops
        if isinstance(op["operation_id"], str) and op["operation_id"]
    }
    for item in sorted(actual_operations - documented_operations):
        problems.append(f"GenX operation missing from ENDPOINT-IDENTITY.md: {item[0]} {item[1]} ({item[2]})")
    for item in sorted(documented_operations - actual_operations):
        problems.append(f"endpoint catalogue entry has no matching GenX operation: {item[0]} {item[1]} ({item[2]})")

    actual_overlaps = set()
    v21_route_keys = {(op["method"], op["path"]) for op in v21_ops}
    for op in genx_ops:
        key = (op["method"], op["path"])
        if key in v21_route_keys and isinstance(op["operation_id"], str) and op["operation_id"]:
            actual_overlaps.add((key[0], key[1], op["operation_id"]))

    expected_overlaps = set()
    overlap_entries = register.get("allowed_relative_path_overlaps", [])
    if not isinstance(overlap_entries, list):
        problems.append("allowed_relative_path_overlaps must be a list")
        overlap_entries = []
    for entry in overlap_entries:
        if not isinstance(entry, dict):
            problems.append(f"invalid overlap entry: {entry!r}")
            continue
        required = ("method", "path", "genx_operation_id", "relationship", "risk", "rationale")
        missing = [key for key in required if not isinstance(entry.get(key), str) or not entry[key].strip()]
        if missing:
            problems.append(f"overlap entry missing/non-empty fields {missing}: {entry!r}")
            continue
        triple = (
            entry["method"].upper(),
            normalize_operation_path(entry["path"]),
            entry["genx_operation_id"],
        )
        if triple in expected_overlaps:
            problems.append(f"duplicate overlap-register entry: {triple[0]} {triple[1]} ({triple[2]})")
        expected_overlaps.add(triple)
        if entry["risk"] not in {"low", "medium", "high", "critical"}:
            problems.append(f"overlap entry has unknown risk class '{entry['risk']}'")
    for extra in sorted(actual_overlaps - expected_overlaps):
        problems.append(f"unregistered V2.1/GenX route overlap: {extra[0]} {extra[1]} ({extra[2]})")
    for stale in sorted(expected_overlaps - actual_overlaps):
        problems.append(f"stale/unverified overlap-register entry: {stale[0]} {stale[1]} ({stale[2]})")

    if register.get("api_base_paths", {}).get("brapi_v21") != "/brapi/v2":
        problems.append("overlap register must identify the V2.1 base path as /brapi/v2")
    if register.get("api_base_paths", {}).get("genx") != "/brapi/v3":
        problems.append("overlap register must identify the GenX base path as /brapi/v3")
    neighbors = register.get("semantic_neighbors", [])
    if not isinstance(neighbors, list) or not neighbors:
        problems.append("overlap register has no semantic-neighbor review entries")
        neighbors = []
    seen_neighbor_ids = set()
    for item in neighbors:
        if not isinstance(item, dict):
            problems.append(f"invalid semantic-neighbor entry: {item!r}")
            continue
        required = ("id", "v21_surface", "genx_surface", "relationship", "risk", "rationale")
        missing = [key for key in required if not isinstance(item.get(key), str) or not item[key].strip()]
        if missing:
            problems.append(f"semantic-neighbor entry missing/non-empty fields {missing}: {item!r}")
            continue
        if item["id"] in seen_neighbor_ids:
            problems.append(f"duplicate semantic-neighbor id '{item['id']}'")
        seen_neighbor_ids.add(item["id"])
        if item["risk"] not in {"low", "medium", "high", "critical"}:
            problems.append(f"semantic-neighbor '{item['id']}' has unknown risk class '{item['risk']}'")

    if problems:
        results.report(probe["id"], probe["title"], "FAIL", "; ".join(problems))
    else:
        results.report(
            probe["id"], probe["title"], "PASS",
            f"{len(genx_ops)} GenX operations named; {len(actual_overlaps)} cross-generation relative-path overlaps registered"
        )


STATIC = {
    "endpoint_identity": check_endpoint_identity,
    "refs_resolve": check_refs_resolve,
    "required_fields": check_required_fields,
    "job_enums": check_job_enums,
    "digest_format": check_digest_format,
    "datetime_format": check_datetime_format,
    "idempotency_relations": check_idempotency_relations,
    "capability_grounding": check_capability_grounding,
    "v21_fallback_shape": check_v21_fallback_shape,
    "term_id_format": check_term_id_format,
    "decimal_format": check_decimal_format,
    "model_shape": check_model_shape,
    "matrix_shape": check_matrix_shape,
    "package_shape": check_package_shape,
    "telemetry_required": check_telemetry_required,
    "telemetry_shape": check_telemetry_shape,
}


# --------------------------------------------------------------------------
# Live probes
# --------------------------------------------------------------------------

def http_call(server, method, path, body=None, token=None):
    url = server.rstrip("/") + path
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urlrequest.Request(url, data=data, method=method)
    req.add_header("Accept", "application/json")
    if body is not None:
        req.add_header("Content-Type", "application/json")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urlrequest.urlopen(req, timeout=10) as resp:
            payload = resp.read().decode("utf-8") or "{}"
            return resp.status, json.loads(payload)
    except HTTPError as exc:
        try:
            return exc.code, json.loads(exc.read().decode("utf-8") or "{}")
        except Exception:
            return exc.code, {}


def fresh_submit(conformance_dir, job_type="germplasm_search", parameters=None):
    body = load_json(os.path.join(conformance_dir, "fixtures", "job_submit.json"))
    body["jobType"] = job_type
    if parameters is not None:
        body["parameters"] = parameters
    body["idempotencyKey"] = str(uuid.uuid4())
    return body


def wait_terminal(server, job_id, token):
    import time
    deadline = time.time() + 30
    last = {}
    while time.time() < deadline:
        status, last = http_call(server, "GET", f"/jobs/{job_id}", token=token)
        if status != 200:
            return last
        if last.get("result", {}).get("status") in TERMINAL:
            return last
        time.sleep(1)
    return last


def run_live_probe(server, probe, ctx, results, token, expired_job):
    conformance_dir = ctx["conformance_dir"]
    calls = probe.get("calls", [])
    if any(s.get("capture_term") for s in calls):
        ctx["live_term_id"] = None
        ctx["live_term"] = None
    if any(s.get("capture_ledger") for s in calls):
        ctx["live_lot"] = None
        ctx["live_ledger"] = None
        ctx["live_ledger_body"] = None
    if any(s.get("capture_model") for s in calls):
        ctx["live_model_id"] = None
        ctx["live_model"] = None
    if any(s.get("capture_model_revoked") for s in calls):
        ctx["live_model_revoked_id"] = None
        ctx["live_model_revoked"] = None
    if any(s.get("capture_model_deprecated") for s in calls):
        ctx["live_model_deprecated_id"] = None
        ctx["live_model_deprecated"] = None
    if any(s.get("capture_matrix") for s in calls):
        ctx["live_matrix_id"] = None
        ctx["live_matrix"] = None
    if any(s.get("capture_package") for s in calls):
        ctx["live_package_id"] = None
        ctx["live_package"] = None
    if any(s.get("capture_telemetry") for s in calls):
        ctx["live_device"] = None
        ctx["live_batch"] = None
    captured = None
    try:
        for step in calls:
            body = None
            fixture = step.get("body_fixture")
            if fixture == "live_submit":
                body = fresh_submit(conformance_dir)
                if step.get("capture_job"):
                    ctx["live_key"] = body["idempotencyKey"]
            elif fixture == "live_submit_conflict":
                body = load_json(
                    os.path.join(conformance_dir, "fixtures", "job_submit_conflict.json")
                )
                body["idempotencyKey"] = ctx.get("live_key", body["idempotencyKey"])
            elif fixture == "live_submit_unknown_type":
                body = fresh_submit(conformance_dir, job_type="this-door-does-not-exist")
            elif fixture == "live_provenanced_submit":
                obs = load_json(
                    os.path.join(conformance_dir, "fixtures", "provenanced_observation.json")
                )
                body = fresh_submit(
                    conformance_dir, job_type="analysis",
                    parameters={"observation": obs},
                )
            elif fixture == "live_term_submit":
                body = load_json(
                    os.path.join(conformance_dir, "fixtures", "term_submit.json")
                )
                if not ctx.get("live_term_id"):
                    ctx["live_term_id"] = f"test-authority:variable:{uuid.uuid4().hex[:8]}"
                body["variableDbId"] = ctx["live_term_id"]
            elif fixture == "live_term_conflict":
                body = load_json(
                    os.path.join(conformance_dir, "fixtures", "term_submit_conflict.json")
                )
                body["variableDbId"] = ctx.get("live_term_id", body["variableDbId"])
            elif fixture == "live_ledger_submit":
                if ctx.get("live_ledger_body") is None:
                    fresh = load_json(
                        os.path.join(conformance_dir, "fixtures", "ledger_submit.json")
                    )
                    ctx["live_lot"] = f"LOT-{uuid.uuid4().hex[:8].upper()}"
                    fresh["idempotencyKey"] = str(uuid.uuid4())
                    ctx["live_ledger_body"] = fresh
                body = copy.deepcopy(ctx["live_ledger_body"])
            elif fixture == "live_ledger_conflict":
                body = load_json(
                    os.path.join(conformance_dir, "fixtures", "ledger_submit_conflict.json")
                )
                if ctx.get("live_ledger_body") is not None:
                    body["idempotencyKey"] = ctx["live_ledger_body"]["idempotencyKey"]
            elif fixture == "live_model_submit":
                body = load_json(
                    os.path.join(conformance_dir, "fixtures", "model_submit.json")
                )
                if not ctx.get("live_model_id"):
                    ctx["live_model_id"] = f"test-authority:model:{uuid.uuid4().hex[:8]}"
                body["modelDbId"] = ctx["live_model_id"]
            elif fixture == "live_model_conflict":
                body = load_json(
                    os.path.join(conformance_dir, "fixtures", "model_submit_conflict.json")
                )
                body["modelDbId"] = ctx.get("live_model_id", body["modelDbId"])
            elif fixture == "live_model_revoked":
                body = load_json(
                    os.path.join(conformance_dir, "fixtures", "model_submit.json")
                )
                if not ctx.get("live_model_revoked_id"):
                    ctx["live_model_revoked_id"] = (
                        f"test-authority:model:revoked-{uuid.uuid4().hex[:8]}")
                body["modelDbId"] = ctx["live_model_revoked_id"]
                body["status"] = "revoked"
            elif fixture == "live_model_deprecated":
                body = load_json(
                    os.path.join(conformance_dir, "fixtures", "model_submit.json")
                )
                if not ctx.get("live_model_deprecated_id"):
                    ctx["live_model_deprecated_id"] = (
                        f"test-authority:model:deprecated-{uuid.uuid4().hex[:8]}")
                body["modelDbId"] = ctx["live_model_deprecated_id"]
                body["status"] = "deprecated"
            elif fixture == "live_matrix_submit":
                body = load_json(
                    os.path.join(conformance_dir, "fixtures", "matrix_submit.json")
                )
                if not ctx.get("live_matrix_id"):
                    ctx["live_matrix_id"] = f"test-authority:matrix:{uuid.uuid4().hex[:8]}"
                body["matrixDbId"] = ctx["live_matrix_id"]
            elif fixture == "live_matrix_conflict":
                body = load_json(
                    os.path.join(conformance_dir, "fixtures", "matrix_submit_conflict.json")
                )
                body["matrixDbId"] = ctx.get("live_matrix_id", body["matrixDbId"])
            elif fixture == "live_package_submit":
                body = load_json(
                    os.path.join(conformance_dir, "fixtures", "package_submit.json")
                )
                if not ctx.get("live_package_id"):
                    ctx["live_package_id"] = f"test-authority:package:{uuid.uuid4().hex[:8]}"
                body["packageDbId"] = ctx["live_package_id"]
            elif fixture == "live_package_conflict":
                body = load_json(
                    os.path.join(conformance_dir, "fixtures", "package_submit_conflict.json")
                )
                body["packageDbId"] = ctx.get("live_package_id", body["packageDbId"])
            elif fixture == "live_package_embargoed":
                body = load_json(
                    os.path.join(conformance_dir, "fixtures", "package_embargoed.json")
                )
                if not ctx.get("live_package_id"):
                    ctx["live_package_id"] = f"test-authority:package:{uuid.uuid4().hex[:8]}"
                body["packageDbId"] = ctx["live_package_id"]
            elif fixture == "live_telemetry_batch":
                if ctx.get("live_batch") is None:
                    batch = load_json(
                        os.path.join(conformance_dir, "fixtures", "telemetry_batch.json")
                    )
                    device = f"test-station-{uuid.uuid4().hex[:6]}"
                    for point in batch:
                        point["deviceDbId"] = device
                    ctx["live_device"] = device
                    ctx["live_batch"] = batch
                body = copy.deepcopy(ctx["live_batch"])
            elif fixture == "live_telemetry_conflict":
                if ctx.get("live_batch") is None:
                    return results.report(
                        probe["id"], probe["title"], "FAIL", "no batch captured")
                point = copy.deepcopy(ctx["live_batch"][2])
                point["value"] = round(point["value"] + 10.0, 3)
                body = [point]
            elif fixture in ("live_inference_submit", "live_inference_revoked",
                             "live_inference_unknown", "live_inference_deprecated"):
                if fixture == "live_inference_unknown":
                    model_id, version = "test-authority:model:does-not-exist", "1"
                elif fixture == "live_inference_revoked":
                    model_id = ctx.get("live_model_revoked_id")
                    if not model_id or not ctx.get("live_model_revoked"):
                        return results.report(
                            probe["id"], probe["title"], "FAIL", "no revoked model captured")
                    version = ctx["live_model_revoked"][1]
                elif fixture == "live_inference_deprecated":
                    model_id = ctx.get("live_model_deprecated_id")
                    if not model_id or not ctx.get("live_model_deprecated"):
                        return results.report(
                            probe["id"], probe["title"], "FAIL", "no deprecated model captured")
                    version = ctx["live_model_deprecated"][1]
                else:
                    model_id = ctx.get("live_model_id")
                    if not model_id or not ctx.get("live_model"):
                        return results.report(
                            probe["id"], probe["title"], "FAIL", "no model captured")
                    version = ctx["live_model"][1]
                inputs = {"plotYield": [4.2, 4.5], "unit": "t_per_hectare"}
                body = {"jobType": "inference",
                        "parameters": {"modelDbId": model_id,
                                       "modelVersion": version,
                                       "inputs": inputs},
                        "idempotencyKey": str(uuid.uuid4())}
                ctx["live_inference_inputs"] = inputs
            path = step["path"]
            if "{jobDbId}" in path:
                if ctx.get("live_job") is None and "{expiredJobDbId}" not in path:
                    return results.report(probe["id"], probe["title"], "FAIL", "no captured job")
                path = path.replace("{jobDbId}", ctx.get("live_job", ""))
            if "{expiredJobDbId}" in path:
                if not expired_job:
                    return results.report(probe["id"], probe["title"], "SKIP", "needs --expired-job")
                path = path.replace("{expiredJobDbId}", expired_job)
            if "{lotDbId}" in path:
                if ctx.get("live_lot") is None:
                    return results.report(probe["id"], probe["title"], "FAIL", "no captured lot")
                path = path.replace("{lotDbId}", ctx["live_lot"])
            if "{packageDbId}" in path:
                if ctx.get("live_package_id") is None:
                    return results.report(probe["id"], probe["title"], "FAIL", "no captured package")
                path = path.replace("{packageDbId}", ctx["live_package_id"])
            if "{telemetry_device}" in path:
                if ctx.get("live_device") is None:
                    return results.report(probe["id"], probe["title"], "FAIL", "no captured device")
                path = path.replace("{telemetry_device}", ctx["live_device"])
            if step.get("replay_capture"):
                # Replay the exact first submission body and key.
                status, payload = http_call(server, "POST", "/jobs", body=ctx["live_body"], token=token)
                same = payload.get("result", {}).get("jobDbId") == ctx.get("live_job")
                if 200 <= status < 300 and same:
                    continue
                return results.report(
                    probe["id"], probe["title"], "FAIL",
                    f"replay returned jobDbId {payload.get('result', {}).get('jobDbId')}",
                )
            if step.get("concurrent_posts"):
                import concurrent.futures as futures
                count = int(step["concurrent_posts"])
                with futures.ThreadPoolExecutor(max_workers=count) as pool:
                    outcomes = list(pool.map(
                        lambda _: http_call(server, step["method"], path,
                                            body=copy.deepcopy(body), token=token),
                        range(count)))
                statuses = [s for s, _ in outcomes]
                ids = {p.get("result", {}).get("jobDbId") for _, p in outcomes}
                if (len(statuses) != count or any(not (200 <= s < 300) for s in statuses)
                        or len(ids) != 1 or None in ids):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        f"statuses {statuses}, jobDbIds {sorted(map(str, ids))}")
                if not step.get("assert", {}).get("single_effect"):
                    return results.report(
                        probe["id"], probe["title"], "FAIL", "no assertion for concurrent step")
                continue
            status, payload = http_call(server, step["method"], path, body=body, token=token)
            if step.get("capture_job"):
                if status not in (200, 202):
                    return results.report(
                        probe["id"], probe["title"], "FAIL", f"submit returned {status}")
                ctx["live_job"] = payload.get("result", {}).get("jobDbId")
                ctx["live_body"] = body
                if step.get("wait_terminal"):
                    payload = wait_terminal(server, ctx["live_job"], token)
            if step.get("capture_term"):
                if status not in (200, 202):
                    return results.report(
                        probe["id"], probe["title"], "FAIL", f"submit returned {status}")
                seen = payload.get("result", {})
                ctx["live_term"] = (seen.get("variableDbId"), seen.get("version"))
            if step.get("capture_ledger"):
                if status not in (200, 202):
                    return results.report(
                        probe["id"], probe["title"], "FAIL", f"submit returned {status}")
                seen = payload.get("result", {})
                ctx["live_ledger"] = (seen.get("seedLotDbId"), seen.get("entryDbId"))
            if step.get("capture_model"):
                if status not in (200, 202):
                    return results.report(
                        probe["id"], probe["title"], "FAIL", f"submit returned {status}")
                seen = payload.get("result", {})
                ctx["live_model"] = (seen.get("modelDbId"), seen.get("modelVersion"))
            if step.get("capture_model_revoked"):
                if status not in (200, 202):
                    return results.report(
                        probe["id"], probe["title"], "FAIL", f"submit returned {status}")
                seen = payload.get("result", {})
                ctx["live_model_revoked"] = (seen.get("modelDbId"), seen.get("modelVersion"))
            if step.get("capture_model_deprecated"):
                if status not in (200, 202):
                    return results.report(
                        probe["id"], probe["title"], "FAIL", f"submit returned {status}")
                seen = payload.get("result", {})
                ctx["live_model_deprecated"] = (seen.get("modelDbId"), seen.get("modelVersion"))
            if step.get("capture_matrix"):
                if status not in (200, 202):
                    return results.report(
                        probe["id"], probe["title"], "FAIL", f"submit returned {status}")
                seen = payload.get("result", {})
                ctx["live_matrix"] = seen.get("matrixDbId")
            if step.get("capture_package"):
                if status not in (200, 202):
                    return results.report(
                        probe["id"], probe["title"], "FAIL", f"submit returned {status}")
                seen = payload.get("result", {})
                ctx["live_package"] = seen.get("packageDbId")
            if step.get("capture_telemetry"):
                if status not in (200, 202):
                    return results.report(
                        probe["id"], probe["title"], "FAIL", f"submit returned {status}")
            assertion = step.get("assert", {})
            if assertion.get("rejected") and not (status >= 400):
                return results.report(
                    probe["id"], probe["title"], "FAIL", f"expected rejection, got {status}")
            if "status" in assertion and status != assertion["status"]:
                return results.report(
                    probe["id"], probe["title"], "FAIL",
                    f"expected {assertion['status']}, got {status}")
            if "data_length" in assertion:
                rows = payload.get("result", {}).get("data", [])
                if len(rows) != assertion["data_length"]:
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        f"{len(rows)} rows, expected {assertion['data_length']}")
            if "total_count" in assertion:
                total = payload.get("metadata", {}).get("pagination", {}).get("totalCount")
                if total != assertion["total_count"]:
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        f"totalCount is {total}, expected {assertion['total_count']}")
            if "status_message" in assertion:
                levels = [s.get("messageType")
                          for s in payload.get("metadata", {}).get("status", [])]
                if assertion["status_message"] not in levels:
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        f"no {assertion['status_message']} status message, got {levels}")
            if assertion.get("same_term"):
                seen = payload.get("result", {})
                if (seen.get("variableDbId"), seen.get("version")) != ctx.get("live_term"):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        f"replay returned {(seen.get('variableDbId'), seen.get('version'))}, "
                        f"expected {ctx.get('live_term')}")
            if assertion.get("same_ledger"):
                seen = payload.get("result", {})
                if (seen.get("seedLotDbId"), seen.get("entryDbId")) != ctx.get("live_ledger"):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        f"replay returned {(seen.get('seedLotDbId'), seen.get('entryDbId'))}, "
                        f"expected {ctx.get('live_ledger')}")
            if assertion.get("same_model"):
                seen = payload.get("result", {})
                if (seen.get("modelDbId"), seen.get("modelVersion")) != ctx.get("live_model"):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        f"replay returned {(seen.get('modelDbId'), seen.get('modelVersion'))}, "
                        f"expected {ctx.get('live_model')}")
            if assertion.get("same_matrix"):
                seen = payload.get("result", {})
                if seen.get("matrixDbId") != ctx.get("live_matrix"):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        f"replay returned {seen.get('matrixDbId')}, "
                        f"expected {ctx.get('live_matrix')}")
            if assertion.get("same_package"):
                seen = payload.get("result", {})
                if seen.get("packageDbId") != ctx.get("live_package"):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        f"replay returned {seen.get('packageDbId')}, "
                        f"expected {ctx.get('live_package')}")
            if "telemetry_counts" in assertion:
                seen = payload.get("result", {})
                want = assertion["telemetry_counts"]
                if (seen.get("appended"), seen.get("replayed")) != (
                        want.get("appended"), want.get("replayed")):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        f"counts are {(seen.get('appended'), seen.get('replayed'))}, "
                        f"expected {(want.get('appended'), want.get('replayed'))}")
            if "telemetry_conflicts" in assertion:
                seen = payload.get("result", {}).get("conflicts", [])
                if len(seen) != assertion["telemetry_conflicts"]:
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        f"{len(seen)} conflicts, expected {assertion['telemetry_conflicts']}")
            if "telemetry_mean" in assertion:
                rows = payload.get("result", {}).get("data", [])
                if len(rows) != 1:
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        f"{len(rows)} buckets, expected 1")
                if rows[0].get("sampleCount") != assertion.get("telemetry_samples"):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        f"sampleCount is {rows[0].get('sampleCount')}, "
                        f"expected {assertion.get('telemetry_samples')}")
                if abs(rows[0].get("value", 0) - assertion["telemetry_mean"]) > 1e-9:
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        f"mean is {rows[0].get('value')}, "
                        f"expected {assertion['telemetry_mean']}")
            if assertion.get("inference_intact"):
                rows = payload.get("result", {}).get("result", {}).get("data", [])
                if not rows:
                    return results.report(
                        probe["id"], probe["title"], "FAIL", "no inference record")
                seen = rows[0]
                want_digest = hashlib.sha256(
                    canonical(ctx["live_inference_inputs"]).encode("utf-8")).hexdigest()
                if seen.get("modelDbId") != ctx.get("live_model_id"):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        f"record names {seen.get('modelDbId')}, "
                        f"expected {ctx.get('live_model_id')}")
                if seen.get("inputsDigest") != want_digest:
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        f"inputsDigest {seen.get('inputsDigest')} != recomputed {want_digest}")
            if "ledger_count" in assertion:
                rows = payload.get("result", {}).get("data", [])
                if len(rows) != assertion["ledger_count"]:
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        f"ledger holds {len(rows)} entries, "
                        f"expected {assertion['ledger_count']}")
            if assertion.get("negotiable"):
                result = payload.get("result", {})
                if status == 200 and ("calls" in result):
                    continue
                return results.report(
                    probe["id"], probe["title"], "FAIL", "serverinfo not negotiable")
            if "body" in assertion:
                for dotted, expected in assertion["body"].items():
                    node = payload
                    for part in dotted.split("."):
                        node = (node or {}).get(part)
                    if node != expected:
                        return results.report(
                            probe["id"], probe["title"], "FAIL",
                            f"{dotted} is {node!r}, expected {expected!r}")
            if assertion.get("provenance_intact"):
                want = load_json(
                    os.path.join(conformance_dir, "fixtures", "provenanced_observation.json")
                )["provenance"]
                echoed = json.dumps(payload)
                if want["inputsDigest"] not in echoed:
                    return results.report(
                        probe["id"], probe["title"], "FAIL", "inputsDigest not echoed")
        results.report(probe["id"], probe["title"], "PASS")
    except Exception as exc:
        results.report(probe["id"], probe["title"], "FAIL", f"{type(exc).__name__}: {exc}")


def main():
    parser = argparse.ArgumentParser(description="BrAPI-GenX conformance checks")
    parser.add_argument("--root", default=".")
    parser.add_argument("--server", default=None)
    parser.add_argument("--expired-job", default=None)
    parser.add_argument("--token", default=None)
    parser.add_argument("--only", default=None,
                        help="run one probe only, e.g. --only L-06")
    args = parser.parse_args()

    root = os.path.abspath(args.root)
    conf = os.path.join(root, "Specification", "BrAPI-GenX", "Conformance")
    spec = load_yaml(os.path.join(conf, "probes.yaml"))
    ctx = {
        "required_map": spec.get("required_map", {}),
        "genx_object_names": spec.get("genx_object_names", []),
        "capability_dirs": spec.get("capability_dirs", {}),
        "conformance_dir": conf,
        "live_job": None,
        "live_body": None,
        "live_key": None,
        "live_term": None,
        "live_term_id": None,
        "live_lot": None,
        "live_ledger": None,
        "live_ledger_body": None,
        "live_model": None,
        "live_model_id": None,
        "live_model_revoked_id": None,
        "live_model_revoked": None,
        "live_model_deprecated_id": None,
        "live_model_deprecated": None,
        "live_matrix_id": None,
        "live_matrix": None,
        "live_package_id": None,
        "live_package": None,
        "live_device": None,
        "live_batch": None,
        "live_inference_inputs": None,
    }
    results = Results()
    for probe in spec.get("probes", []):
        if args.only and probe.get("id") != args.only:
            continue
        if probe.get("tier") == "static":
            STATIC[probe["check"]](root, probe, ctx, results)
        elif args.server:
            if urlrequest is None:  # pragma: no cover
                results.report(probe["id"], probe["title"], "FAIL", "urllib unavailable")
            else:
                run_live_probe(args.server, probe, ctx, results, args.token, args.expired_job)
        else:
            results.report(probe["id"], probe["title"], "SKIP", "needs --server")

    print(f"done: {results.failures} failures, {results.skips} skipped")
    return 1 if results.failures else 0


if __name__ == "__main__":
    sys.exit(main())
