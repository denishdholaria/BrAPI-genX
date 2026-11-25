#!/usr/bin/env python3
"""
Static and live conformance checks for the BrAPI-GenX proposal (RFC-001).

Static probes (S-01..S-08) execute against this repo only. Live probes
(L-01..L-07) execute against a GenX server and SKIP without --server.
The probe list in Specification/BrAPI-GenX/Conformance/probes.yaml is the
authority; this script is one execution of it.

Usage:
    python Scripts/checkGenXConformance.py [--root <workspace_root>]
    python Scripts/checkGenXConformance.py --server https://host/genx/v1 [--expired-job JOB_0000]

Options:
    --root         Root of the BrAPI workspace (default: current directory)
    --server       Base URL of a GenX server, e.g. https://host/genx/v1
    --expired-job  A known-expired jobDbId for probe L-05 (else L-05 skips)
"""

import argparse
import ast
import copy
import glob
import hashlib
import json
import math
import os
import re
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from brapi_genx.canonicalization import jcs_canonicalize
import uuid
from urllib.parse import parse_qs, quote, urlsplit

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
JOB_LIFECYCLE_STATES = frozenset(TERMINAL | {"SUBMITTED", "RUNNING"})


def valid_job_lifecycle_status(job):
    """Validate the required Job.status enum without constraining phase."""
    return (isinstance(job, dict)
            and isinstance(job.get("status"), str)
            and job["status"] in JOB_LIFECYCLE_STATES)


def valid_job_status_and_progress(job):
    """Check the required lifecycle enum and optional bounded Job.progress."""
    if not valid_job_lifecycle_status(job):
        return False
    if "progress" not in job:
        return True
    progress = job["progress"]
    # bool is an int subclass; the schema explicitly requires a number.
    # Test the range first to avoid overflow on arbitrarily large integers.
    return (type(progress) in (int, float)
            and 0 <= progress <= 1
            and math.isfinite(progress))


# Accept UTC Z, extended ISO offsets and the HHMM offsets documented in
# Specification/GeneralInfo/Date_Time_Encoding.md.
JOB_TIMESTAMP_RE = re.compile(
    r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}"
    r"(?:\.[0-9]+)?(?:Z|[+-][0-9]{2}:?[0-9]{2})"
)


def valid_optional_job_timestamps(job):
    """Validate timezone-bearing date-times only when a Job supplies them."""
    if not isinstance(job, dict):
        return False
    for field in ("createdAt", "updatedAt", "expiresAt"):
        if field not in job:
            continue
        value = job[field]
        if not isinstance(value, str) or not JOB_TIMESTAMP_RE.fullmatch(value):
            return False
        try:
            parse_rfc3339(value)
        except (TypeError, ValueError, OverflowError):
            return False
    return True


def valid_job_wire_fields(job):
    """Validate existing Job status, optional progress and timestamp fields."""
    return (valid_job_status_and_progress(job)
            and valid_optional_job_timestamps(job))


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
        os.path.join(root, "Specification", "BrAPI-GenX", "Core", "Jobs", "Schemas", "Job.yaml")
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
    raw = json.dumps(doc).encode("utf-8")
    return jcs_canonicalize(raw).decode("utf-8")


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


def capability_contract_problems(root, info, registry_path):
    """Check the experimental ServerInfoV3 operation mapping against OpenAPI."""
    problems = []
    try:
        registry = load_json(registry_path)
    except Exception as exc:
        return [f"cannot read capability registry: {type(exc).__name__}: {exc}"]

    if registry.get("schemaVersion") != 1:
        problems.append("capability registry schemaVersion must be 1")
    if registry.get("status") != "experimental-review-only":
        problems.append("capability registry must remain explicitly experimental-review-only")
    if registry.get("baseRoute") != "/genx/v1":
        problems.append("capability registry baseRoute must be /genx/v1")

    entries = registry.get("capabilities")
    if not isinstance(entries, list) or not entries:
        return problems + ["capability registry must contain a non-empty capabilities array"]

    registry_by_name = {}
    for entry in entries:
        if not isinstance(entry, dict):
            problems.append("capability registry contains a non-object entry")
            continue
        name = entry.get("name")
        if not isinstance(name, str) or not name.strip():
            problems.append("capability registry entry has a missing/blank name")
            continue
        if name in registry_by_name:
            problems.append(f"capability registry has duplicate name '{name}'")
        registry_by_name[name] = entry

    # Validate the registry itself; a fixture cannot make a malformed source of truth valid.
    for name, entry in registry_by_name.items():
        for field in ("versions", "methods"):
            value = entry.get(field)
            if not isinstance(value, list) or not value:
                problems.append(f"capability registry '{name}' {field} must be a non-empty array")
                continue
            if any(not isinstance(item, str) or not item.strip() for item in value):
                problems.append(f"capability registry '{name}' {field} must contain non-empty strings")
            elif len(value) != len(set(value)):
                problems.append(f"capability registry '{name}' {field} contains duplicates")
        job_types = entry.get("jobTypes")
        if name == "jobs":
            if not isinstance(job_types, list) or not job_types:
                problems.append("capability registry 'jobs' jobTypes must be a non-empty array")
            elif any(not isinstance(item, str) or not item.strip() for item in job_types):
                problems.append("capability registry 'jobs' jobTypes must contain non-empty strings")
            elif len(job_types) != len(set(job_types)):
                problems.append("capability registry 'jobs' jobTypes contains duplicates")
        elif job_types is not None:
            problems.append(f"capability registry '{name}' must not declare jobTypes; only the jobs capability can do so")

    result = info.get("result") if isinstance(info, dict) else None
    if not isinstance(result, dict):
        return problems + ["ServerInfoV3 fixture/result is not an object"]

    brapi_versions = result.get("brapiVersions")
    if not isinstance(brapi_versions, list) or not brapi_versions:
        problems.append("brapiVersions must be a non-empty array")
    else:
        if any(not isinstance(v, str) or not v.strip() for v in brapi_versions):
            problems.append("brapiVersions must contain non-empty opaque strings")
        if len(brapi_versions) != len(set(v for v in brapi_versions if isinstance(v, str))):
            problems.append("brapiVersions contains duplicate version tokens")

    capabilities = result.get("capabilities")
    if not isinstance(capabilities, list):
        return problems + ["capabilities must be an array"]
    fixture_by_name = {}
    for cap in capabilities:
        if not isinstance(cap, dict):
            problems.append("capabilities contains a non-object entry")
            continue
        name = cap.get("name")
        if not isinstance(name, str) or not name.strip():
            problems.append("capability entry has a missing/blank name")
            continue
        if name in fixture_by_name:
            problems.append(f"ServerInfoV3 has duplicate capability name '{name}'")
        fixture_by_name[name] = cap

    unknown = sorted(set(fixture_by_name) - set(registry_by_name))
    missing = sorted(set(registry_by_name) - set(fixture_by_name))
    if unknown:
        problems.append("advertised capabilities are absent from the experimental registry: " + ", ".join(unknown))
    if missing:
        problems.append("registered capabilities absent from ServerInfoV3 fixture: " + ", ".join(missing))

    # Confirm the job type list advertised by the prototype is the same list enforced at submission.
    jobs_entry = registry_by_name.get("jobs")
    server_path = os.path.join(root, "Scripts", "genx_test_server.py")
    try:
        with open(server_path, encoding="utf-8") as handle:
            server_ast = ast.parse(handle.read(), filename=server_path)
        assigned = None
        for node in server_ast.body:
            if isinstance(node, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id == "SUPPORTED_JOB_TYPES"
                for target in node.targets
            ):
                assigned = ast.literal_eval(node.value)
                break
        if not isinstance(assigned, (tuple, list)) or not assigned or any(
            not isinstance(item, str) or not item.strip() for item in assigned
        ):
            problems.append("reference server SUPPORTED_JOB_TYPES must be a non-empty sequence of exact strings")
        elif len(assigned) != len(set(assigned)):
            problems.append("reference server SUPPORTED_JOB_TYPES contains duplicates")
        elif jobs_entry is not None and isinstance(jobs_entry.get("jobTypes"), list):
            registry_types = jobs_entry["jobTypes"]
            if all(isinstance(item, str) and item.strip() for item in registry_types) and set(assigned) != set(registry_types):
                problems.append("reference server SUPPORTED_JOB_TYPES differs from the jobs capability registry")
    except Exception as exc:
        problems.append(f"cannot validate reference server supported job types: {type(exc).__name__}: {exc}")

    # Build a source-of-truth map from the actual GenX OpenAPI fragments.
    genx_dir = os.path.join(root, "Specification", "BrAPI-GenX")
    operation_catalog = {}
    for yaml_path in glob.glob(os.path.join(genx_dir, "**", "*.yaml"), recursive=True):
        try:
            document = load_yaml(yaml_path)
        except Exception as exc:
            problems.append(f"cannot parse GenX YAML {os.path.relpath(yaml_path, root)}: {exc}")
            continue
        if not isinstance(document, dict):
            continue
        paths = document.get("paths")
        if not isinstance(paths, dict):
            continue
        for route, path_item in paths.items():
            if not isinstance(path_item, dict):
                continue
            for method, operation in path_item.items():
                method_upper = str(method).upper()
                if method_upper not in OPENAPI_METHODS or not isinstance(operation, dict):
                    continue
                operation_id = operation.get("operationId")
                if not isinstance(operation_id, str) or not operation_id.strip():
                    continue
                full_route = "/genx/v1" + route
                if operation_id in operation_catalog:
                    old = operation_catalog[operation_id]
                    problems.append(
                        f"OpenAPI operationId '{operation_id}' is duplicated at "
                        f"{old['method']} {old['route']} and {method_upper} {full_route}"
                    )
                else:
                    operation_catalog[operation_id] = {
                        "method": method_upper,
                        "route": full_route,
                    }

    for name, cap in fixture_by_name.items():
        entry = registry_by_name.get(name)
        if entry is None:
            continue

        for label, value in (("versions", cap.get("versions")), ("methods", cap.get("methods"))):
            if not isinstance(value, list) or not value:
                problems.append(f"capability '{name}' {label} must be a non-empty array")
                continue
            if any(not isinstance(item, str) or not item.strip() for item in value):
                problems.append(f"capability '{name}' {label} must contain non-empty strings")
            string_items = [item for item in value if isinstance(item, str)]
            if len(string_items) != len(set(string_items)):
                problems.append(f"capability '{name}' {label} contains duplicates")

        versions = cap.get("versions") if isinstance(cap.get("versions"), list) else []
        entry_versions = entry.get("versions") if isinstance(entry.get("versions"), list) else []
        versions_are_strings = all(isinstance(value, str) and value.strip() for value in versions)
        entry_versions_are_strings = all(isinstance(value, str) and value.strip() for value in entry_versions)
        if not versions_are_strings:
            problems.append(f"capability '{name}' version values must be non-empty opaque strings")
        if not entry_versions_are_strings:
            problems.append(f"capability registry '{name}' version values must be non-empty opaque strings")
        if versions_are_strings and entry_versions_are_strings and set(versions) != set(entry_versions):
            problems.append(f"capability '{name}' versions differ from the experimental registry")

        methods = cap.get("methods") if isinstance(cap.get("methods"), list) else []
        entry_methods = entry.get("methods") if isinstance(entry.get("methods"), list) else []
        methods_are_strings = all(isinstance(method, str) for method in methods)
        entry_methods_are_strings = all(isinstance(method, str) for method in entry_methods)
        for method in methods + entry_methods:
            if not isinstance(method, str) or method not in HTTP_METHODS:
                problems.append(f"capability '{name}' uses unsupported method summary {method!r}")
        if methods_are_strings and entry_methods_are_strings and set(methods) != set(entry_methods):
            problems.append(f"capability '{name}' method summary differs from the experimental registry")

        advertised_job_types = cap.get("jobTypes")
        registered_job_types = entry.get("jobTypes")
        if name == "jobs":
            for label, values in (("ServerInfoV3", advertised_job_types), ("registry", registered_job_types)):
                if not isinstance(values, list) or not values:
                    problems.append(f"capability '{name}' {label} jobTypes must be a non-empty array in this experimental profile")
                    continue
                if any(not isinstance(item, str) or not item.strip() for item in values):
                    problems.append(f"capability '{name}' {label} jobTypes must contain non-empty exact tokens")
                elif len(values) != len(set(values)):
                    problems.append(f"capability '{name}' {label} jobTypes contains duplicates")
            if (
                isinstance(advertised_job_types, list)
                and isinstance(registered_job_types, list)
                and all(isinstance(item, str) and item.strip() for item in advertised_job_types)
                and all(isinstance(item, str) and item.strip() for item in registered_job_types)
                and set(advertised_job_types) != set(registered_job_types)
            ):
                problems.append("capability 'jobs' jobTypes differ from the experimental registry")
        else:
            if "jobTypes" in cap:
                problems.append(f"capability '{name}' must not advertise jobTypes; only the jobs capability can do so")
            if "jobTypes" in entry:
                problems.append(f"capability registry '{name}' must not declare jobTypes; only the jobs capability can do so")

        for label, source in (("ServerInfoV3", cap), ("registry", entry)):
            scopes = source.get("scopes")
            if scopes is None:
                continue
            if not isinstance(scopes, list):
                problems.append(f"capability '{name}' {label} scopes must be an array when present")
            elif any(not isinstance(scope, str) or not scope.strip() for scope in scopes):
                problems.append(f"capability '{name}' {label} scopes must contain non-empty strings")
            elif len(scopes) != len(set(scopes)):
                problems.append(f"capability '{name}' {label} scopes contains duplicates")

        advertised_ops = cap.get("operations")
        registered_ops = entry.get("operations")
        if not isinstance(advertised_ops, list) or not advertised_ops:
            problems.append(f"capability '{name}' must advertise a non-empty operations array in this experimental profile")
            continue
        if not isinstance(registered_ops, list) or not registered_ops:
            problems.append(f"capability registry '{name}' must contain a non-empty operations array")
            continue

        def normalize_ops(items, label):
            normalized = []
            seen = set()
            for operation in items:
                if not isinstance(operation, dict):
                    problems.append(f"capability '{name}' {label} contains a non-object operation")
                    continue
                method = operation.get("method")
                route = operation.get("route")
                operation_id = operation.get("operationId")
                valid = True
                if not isinstance(method, str) or method not in HTTP_METHODS:
                    problems.append(f"capability '{name}' {label} has unsupported operation method {method!r}")
                    valid = False
                if not isinstance(route, str) or not route.startswith("/genx/v1/") or "?" in route or "#" in route:
                    problems.append(f"capability '{name}' {label} route must be a full /genx/v1 route template, got {route!r}")
                    valid = False
                if not isinstance(operation_id, str) or not operation_id.strip():
                    problems.append(f"capability '{name}' {label} has missing/blank operationId")
                    valid = False
                if not valid:
                    continue
                key = (method, route, operation_id)
                if key in seen:
                    problems.append(f"capability '{name}' {label} has a duplicate operation reference {key!r}")
                seen.add(key)
                normalized.append(key)
                actual = operation_catalog.get(operation_id)
                if actual is None:
                    problems.append(f"capability '{name}' {label} references unknown operationId {operation_id!r}")
                elif actual.get("method") != method or actual.get("route") != route:
                    problems.append(
                        f"capability '{name}' {label} operation {operation_id!r} advertises "
                        f"{method} {route}, but OpenAPI defines {actual.get('method')} {actual.get('route')}"
                    )
            return normalized

        normalized_advertised = normalize_ops(advertised_ops, "advertised operations")
        normalized_registered = normalize_ops(registered_ops, "registry operations")
        if set(normalized_advertised) != set(normalized_registered):
            problems.append(f"capability '{name}' operation mapping differs from the experimental registry")

        methods_from_ops = {method for method, _, _ in normalized_advertised}
        if methods_from_ops != set(methods):
            problems.append(
                f"capability '{name}' methods must equal its operations' method union; "
                f"got {sorted(set(methods))}, expected {sorted(methods_from_ops)}"
            )

    auth_profiles = result.get("authProfiles", [])
    if not isinstance(auth_profiles, list):
        problems.append("authProfiles must be an array when present")
    else:
        seen_profiles = set()
        for profile in auth_profiles:
            if not isinstance(profile, dict):
                problems.append("authProfiles contains a non-object entry")
                continue
            name = profile.get("name")
            if not isinstance(name, str) or not name.strip():
                problems.append("auth profile has a missing/blank name")
                continue
            if name in seen_profiles:
                problems.append(f"authProfiles contains duplicate profile name '{name}'")
            seen_profiles.add(name)
            scopes = profile.get("scopes")
            if scopes is not None and (
                not isinstance(scopes, list)
                or any(not isinstance(scope, str) or not scope.strip() for scope in scopes)
                or (isinstance(scopes, list) and len(scopes) != len(set(scopes)))
            ):
                problems.append(f"auth profile '{name}' scopes must be an array of unique non-empty strings when present")

    return problems


def check_capability_contract(root, probe, ctx, results):
    genx = os.path.join(root, "Specification", "BrAPI-GenX")
    info_path = os.path.join(genx, "Conformance", "fixtures", "serverinfov3.json")
    registry_path = ctx.get(
        "capability_registry_path",
        os.path.join(genx, "Conformance", "capability-registry.json"),
    )
    try:
        info = load_json(info_path)
        problems = capability_contract_problems(root, info, registry_path)
    except Exception as exc:
        problems = [f"{type(exc).__name__}: {exc}"]
    if problems:
        results.report(probe["id"], probe["title"], "FAIL", "; ".join(problems))
    else:
        results.report(probe["id"], probe["title"], "PASS",
                       "capability names, version/method summaries, and operation routes match the registry")


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
        os.path.join(root, "Specification", "BrAPI-GenX", "Research", "Models",
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
        os.path.join(root, "Specification", "BrAPI-GenX", "Genotyping", "Genomics",
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
        os.path.join(root, "Specification", "BrAPI-GenX", "Interoperability", "FAIR",
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
        os.path.join(root, "Specification", "BrAPI-GenX", "Instrumentation", "Telemetry",
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


def v21_fallback_calls_problems(document):
    """Minimum usable legacy server-info shape, not full version 2.1 certification."""
    if not isinstance(document, dict):
        return ["server-info response is not an object"]
    result = document.get("result")
    if not isinstance(result, dict):
        return ["server-info result is not an object"]
    calls = result.get("calls")
    if not isinstance(calls, list) or not calls:
        return ["server-info calls must be a nonempty array"]
    problems = []
    for index, call in enumerate(calls):
        if not isinstance(call, dict):
            problems.append(f"call {index}: not an object")
            continue
        service = call.get("service")
        if not isinstance(service, str) or not service.strip():
            problems.append(f"call {index}: missing usable service")
        for field in ("versions", "methods"):
            values = call.get(field)
            if (not isinstance(values, list) or not values
                    or any(not isinstance(v, str) or not v.strip() for v in values)):
                problems.append(f"call {index}: {field} must be a nonempty string array")
    return problems


def check_v21_fallback_shape(root, probe, ctx, results):
    doc = load_json(
        os.path.join(
            root, "Specification", "BrAPI-GenX", "Conformance",
            "fixtures", "serverinfo_v21_only.json",
        )
    )
    problems = v21_fallback_calls_problems(doc)
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
            if not cells[0].startswith("/genx/v1/"):
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
            if not re.fullmatch(r"/genx/v1/.+", full_route):
                problems.append(f"catalogue route is not generation-qualified: {full_route}")
                continue
            if method not in OPENAPI_METHODS:
                problems.append(f"catalogue route {full_route} has invalid method '{method}'")
                continue
            if not re.fullmatch(r"genx[A-Z][A-Za-z0-9]*", op_id):
                problems.append(f"catalogue route {method} {full_route} has invalid/missing operationId '{op_id}'")
                continue
            triple = (method, normalize_operation_path(full_route[len("/genx/v1"):]), op_id)
            if triple in catalogue_rows_seen:
                print(f'DEBUG: DUPLICATE: {method} {full_route} ({op_id})', file=sys.stderr)
                print(f'DEBUG: Already seen from one of {len(catalogue_rows_seen)} entries', file=sys.stderr)
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
    if register.get("api_base_paths", {}).get("genx") != "/genx/v1":
        problems.append("overlap register must identify the GenX base path as /genx/v1")
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
    "capability_contract": check_capability_contract,
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
        # Preserve text errors for confidentiality assertions: silently
        # replacing a non-JSON 403 body with {} can hide leaked values.
        raw = exc.read().decode("utf-8", errors="replace")
        if not raw:
            return exc.code, {}
        try:
            return exc.code, json.loads(raw)
        except ValueError:
            return exc.code, {"error": raw}


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
            # A terminal-looking body on a failed GET is not evidence that
            # the accepted job completed. Propagate the transport failure to
            # the live probe's fail-closed exception handler.
            raise ValueError(
                f"terminal job polling GET returned HTTP {status}"
            )
        returned = last.get("result") if isinstance(last, dict) else None
        if (not isinstance(returned, dict)
                or returned.get("jobDbId") != job_id):
            # A successful GET for one accepted job must not use the
            # terminal state of a different job as completion evidence.
            raise ValueError(
                f"terminal job polling GET did not return requested job {job_id}"
            )
        if returned.get("status") in TERMINAL:
            return last
        time.sleep(1)
    return last


def immutable_job_snapshot(status, payload):
    """Return (job identity map, diagnostic) for a complete jobs collection."""
    result = payload.get("result") if isinstance(payload, dict) else None
    rows = result.get("data") if isinstance(result, dict) else None
    metadata = payload.get("metadata") if isinstance(payload, dict) else None
    page = metadata.get("pagination") if isinstance(metadata, dict) else None
    if (status != 200 or not isinstance(rows, list)
            or not isinstance(page, dict)
            or any(type(page.get(field)) is not int
                   for field in ("totalCount", "pageSize", "totalPages", "currentPage"))
            or page["totalCount"] != len(rows)
            or page["pageSize"] < len(rows)
            or page["totalPages"] != 1 or page["currentPage"] != 0):
        return None, "incomplete jobs collection or pagination"
    snapshot = {}
    for row in rows:
        if (not isinstance(row, dict)
                or not isinstance(row.get("jobDbId"), str)
                or not row["jobDbId"]
                or not isinstance(row.get("jobType"), str)
                or not row["jobType"]
                or not valid_job_wire_fields(row)
                or ("idempotencyKey" in row
                    and not isinstance(row["idempotencyKey"], str))
                or row["jobDbId"] in snapshot):
            return None, "malformed or duplicated job identity/status in collection"
        snapshot[row["jobDbId"]] = (
            row["jobType"], row.get("idempotencyKey")
        )
    return snapshot, None


def published_record_problem(status, payload, original, expected_id, identity_field):
    """Return a diagnostic if a rejected rewrite changed the submitted record."""
    stored = payload.get("result") if isinstance(payload, dict) else None
    if (status != 200 or not isinstance(original, dict)
            or not isinstance(expected_id, str) or not expected_id
            or original.get(identity_field) != expected_id
            or not isinstance(stored, dict)
            or stored.get(identity_field) != expected_id):
        return "published record or original identity unavailable"
    if any(key not in stored or stored[key] != value
           for key, value in original.items()):
        return "published record fields changed after rejected conflict"
    return None


def submitted_record_problem(payload, submitted):
    """Return a diagnostic when a publish response changes source fields.

    Additional server metadata is allowed, but every originally submitted
    scientific and nested provenance value must survive unchanged.
    """
    returned = payload.get("result") if isinstance(payload, dict) else None
    if not isinstance(submitted, dict) or not isinstance(returned, dict):
        return "replay response or original submission is not an object"
    for field, value in submitted.items():
        if field not in returned or returned[field] != value:
            return f"replay response changed or dropped submitted field {field!r}"
    return None


def replay_collection_problem(status, payload, original, expected_id, identity_field):
    """Return a diagnostic when a replay's complete collection lacks one original."""
    result = payload.get("result") if isinstance(payload, dict) else None
    rows = result.get("data") if isinstance(result, dict) else None
    metadata = payload.get("metadata") if isinstance(payload, dict) else None
    pagination = metadata.get("pagination") if isinstance(metadata, dict) else None
    if (status != 200 or not isinstance(original, dict)
            or not isinstance(expected_id, str) or not expected_id
            or original.get(identity_field) != expected_id
            or not isinstance(rows, list) or not rows
            or not all(isinstance(row, dict) for row in rows)
            or not isinstance(pagination, dict)
            or any(type(pagination.get(k)) is not int
                   for k in ("totalCount", "pageSize", "totalPages", "currentPage"))
            or pagination["totalCount"] != len(rows)
            or pagination["pageSize"] < len(rows)
            or pagination["totalPages"] != 1
            or pagination["currentPage"] != 0):
        return "replay collection malformed, incomplete, or unavailable"
    matches = [row for row in rows if row.get(identity_field) == expected_id]
    if (len(matches) != 1
            or any(key not in matches[0] or matches[0][key] != value
                   for key, value in original.items())):
        return "original record missing, duplicated, or modified after replay"
    return None


def run_live_probe(server, probe, ctx, results, token, expired_job):
    conformance_dir = ctx["conformance_dir"]
    calls = probe.get("calls", [])
    if any(isinstance(s.get("assert"), dict)
           and s["assert"].get("capture_job_collection")
           for s in calls):
        ctx["live_job_conflict_baseline"] = None
    if any(isinstance(s.get("assert"), dict)
           and s["assert"].get("terminal_state_unchanged")
           for s in calls):
        ctx["live_terminal_before_cancel"] = None
    if any(s.get("capture_term") for s in calls):
        ctx["live_term_id"] = None
        ctx["live_term"] = None
        ctx["live_term_baseline"] = None
    if any(s.get("capture_ledger") for s in calls):
        ctx["live_lot"] = None
        ctx["live_ledger"] = None
        ctx["live_ledger_body"] = None
    if any(s.get("capture_model") for s in calls):
        ctx["live_model_id"] = None
        ctx["live_model"] = None
        ctx["live_model_baseline"] = None
        ctx["live_model_original"] = None
    if any(s.get("body_fixture") == "live_submit_unknown_type" for s in calls):
        ctx["live_unknown_type_request"] = None
    if any(s.get("body_fixture") in ("live_inference_unknown",
                                        "live_inference_revoked") for s in calls):
        ctx["live_rejected_inference"] = {}
    if any(s.get("capture_model_revoked") for s in calls):
        ctx["live_model_revoked_id"] = None
        ctx["live_model_revoked"] = None
        ctx["live_model_revoked_original"] = None
    if any(s.get("capture_model_deprecated") for s in calls):
        ctx["live_model_deprecated_id"] = None
        ctx["live_model_deprecated"] = None
        ctx["live_model_deprecated_original"] = None
        ctx["live_deprecated_inference_request"] = None
    if any(s.get("capture_matrix") for s in calls):
        ctx["live_matrix_id"] = None
        ctx["live_matrix"] = None
        ctx["live_matrix_baseline"] = None
        ctx["live_matrix_original"] = None
    if any(s.get("capture_package") for s in calls):
        ctx["live_package_id"] = None
        ctx["live_package"] = None
        ctx["live_package_baseline"] = None
        ctx["live_package_original"] = None
    if any(s.get("capture_telemetry") for s in calls):
        ctx["live_device"] = None
        ctx["live_batch"] = None
    if any(s.get("body_fixture") == "live_telemetry_conflict" for s in calls):
        ctx["live_telemetry_conflict_submitted"] = None
    if any("concurrent_posts" in s for s in calls):
        ctx["live_concurrent_job"] = None
        ctx["live_concurrent_key"] = None
        ctx["live_concurrent_type"] = None
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
                ctx["live_unknown_type_request"] = copy.deepcopy(body)
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
                ctx["live_telemetry_conflict_submitted"] = copy.deepcopy(body)
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
            if fixture == "live_inference_deprecated":
                ctx["live_deprecated_inference_request"] = copy.deepcopy(body)
            if fixture in ("live_inference_unknown", "live_inference_revoked"):
                # Retain the exact rejected request keys and model identities,
                # rather than deriving them from the server's error response.
                rejected = ctx.get("live_rejected_inference")
                if not isinstance(rejected, dict):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "missing rejected inference capture context"
                    )
                rejected[fixture] = {
                    "key": body["idempotencyKey"],
                    "modelDbId": body["parameters"]["modelDbId"],
                }
            path = step["path"]
            if "{variableDbId}" in path or "{termVersion}" in path:
                baseline = ctx.get("live_term_baseline")
                if (not isinstance(baseline, dict)
                        or not isinstance(baseline.get("variableDbId"), str)
                        or not baseline["variableDbId"]
                        or not isinstance(baseline.get("version"), str)
                        or not baseline["version"]):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "no original variable-term identity captured"
                    )
                path = path.replace("{variableDbId}",
                                    quote(baseline["variableDbId"], safe=":"))
                path = path.replace("{termVersion}",
                                    quote(baseline["version"], safe=""))
            if "{modelDbId}" in path or "{modelVersion}" in path:
                baseline = ctx.get("live_model_baseline")
                if (not baseline or len(baseline) != 3
                        or not all(isinstance(value, str) and value for value in baseline)):
                    return results.report(probe["id"], probe["title"], "FAIL",
                                          "no complete model baseline captured")
                path = path.replace("{modelDbId}", quote(baseline[0], safe=":"))
                path = path.replace("{modelVersion}", quote(baseline[1], safe=""))
            if "{revokedModelDbId}" in path or "{revokedModelVersion}" in path:
                original = ctx.get("live_model_revoked_original")
                if (not isinstance(original, dict)
                        or not isinstance(original.get("modelDbId"), str)
                        or not original["modelDbId"]
                        or not isinstance(original.get("modelVersion"), str)
                        or not original["modelVersion"]):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "no original revoked model identity captured"
                    )
                path = path.replace("{revokedModelDbId}",
                                    quote(original["modelDbId"], safe=":"))
                path = path.replace("{revokedModelVersion}",
                                    quote(original["modelVersion"], safe=""))
            if "{deprecatedModelDbId}" in path or "{deprecatedModelVersion}" in path:
                original = ctx.get("live_model_deprecated_original")
                if (not isinstance(original, dict)
                        or not isinstance(original.get("modelDbId"), str)
                        or not original["modelDbId"]
                        or not isinstance(original.get("modelVersion"), str)
                        or not original["modelVersion"]):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "no original deprecated model identity captured"
                    )
                path = path.replace("{deprecatedModelDbId}",
                                    quote(original["modelDbId"], safe=":"))
                path = path.replace("{deprecatedModelVersion}",
                                    quote(original["modelVersion"], safe=""))
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
            if "{matrixDbId}" in path:
                baseline = ctx.get("live_matrix_baseline")
                if not baseline or not baseline[0]:
                    return results.report(probe["id"], probe["title"], "FAIL",
                                          "no matrix baseline captured")
                path = path.replace("{matrixDbId}", quote(baseline[0], safe=":"))
            if "{packageDbId}" in path:
                if ctx.get("live_package_id") is None:
                    return results.report(probe["id"], probe["title"], "FAIL", "no captured package")
                path = path.replace("{packageDbId}", ctx["live_package_id"])
            if "{telemetry_device}" in path:
                if ctx.get("live_device") is None:
                    return results.report(probe["id"], probe["title"], "FAIL", "no captured device")
                path = path.replace("{telemetry_device}", ctx["live_device"])
            if step.get("replay_capture"):
                # A matching jobDbId alone cannot prove that the replay
                # acknowledged the original job type and idempotency key.
                # L-01 explicitly permits HTTP 200 or 202, not every 2xx.
                original = ctx.get("live_body")
                status, payload = http_call(
                    server, "POST", "/jobs", body=original, token=token)
                returned = (payload.get("result")
                            if isinstance(payload, dict) else None)
                if (status in (200, 202)
                        and isinstance(original, dict)
                        and valid_job_wire_fields(returned)
                        and isinstance(ctx.get("live_job"), str)
                        and ctx["live_job"]
                        and returned.get("jobDbId") == ctx["live_job"]
                        and isinstance(original.get("jobType"), str)
                        and returned.get("jobType") == original["jobType"]
                        and isinstance(original.get("idempotencyKey"), str)
                        and original["idempotencyKey"]
                        and returned.get("idempotencyKey")
                            == original["idempotencyKey"]):
                    continue
                return results.report(
                    probe["id"], probe["title"], "FAIL",
                    "job replay HTTP status, Job lifecycle status or original "
                    "identity/type/key not preserved in response"
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
                returned = [
                    response.get("result")
                    if isinstance(response, dict) else None
                    for _, response in outcomes
                ]
                ids = [
                    record.get("jobDbId") if isinstance(record, dict) else None
                    for record in returned
                ]
                if (not isinstance(body, dict)
                        or not isinstance(body.get("idempotencyKey"), str)
                        or not body["idempotencyKey"].strip()
                        or not isinstance(body.get("jobType"), str)
                        or not body["jobType"]):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "concurrent request lacks original identity and job type")
                if (len(outcomes) != count
                        or any(type(code) is not int or not (200 <= code < 300)
                               for code in statuses)
                        or not ids or not isinstance(ids[0], str) or not ids[0]
                        or any(job_id != ids[0] for job_id in ids)
                        or any(
                            not valid_job_wire_fields(record)
                            or record.get("jobType") != body["jobType"]
                            or record.get("idempotencyKey")
                                != body["idempotencyKey"]
                            for record in returned
                        )):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "concurrent job acknowledgments changed original "
                        f"identity/type/key or Job status "
                        f"(HTTP statuses={statuses}, jobDbIds={ids})"
                    )
                if not step.get("assert", {}).get("single_effect"):
                    return results.report(
                        probe["id"], probe["title"], "FAIL", "no assertion for concurrent step")
                ctx["live_concurrent_job"] = ids[0]
                ctx["live_concurrent_key"] = body["idempotencyKey"]
                ctx["live_concurrent_type"] = body["jobType"]
                continue
            status, payload = http_call(server, step["method"], path, body=body, token=token)
            if step.get("capture_job"):
                accepted = (payload.get("result")
                            if isinstance(payload, dict) else None)
                if (status not in (200, 202)
                        or not isinstance(accepted, dict)
                        or not isinstance(body, dict)
                        or not isinstance(accepted.get("jobDbId"), str)
                        or not accepted["jobDbId"]
                        or not valid_job_wire_fields(accepted)
                        or not isinstance(body.get("jobType"), str)
                        or not body["jobType"]
                        or accepted.get("jobType") != body["jobType"]
                        or not isinstance(body.get("idempotencyKey"), str)
                        or not body["idempotencyKey"]
                        or accepted.get("idempotencyKey")
                            != body["idempotencyKey"]):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "initial job acceptance missing or changing original "
                        "identifier, type, idempotency key or Job status"
                    )
                ctx["live_job"] = accepted["jobDbId"]
                ctx["live_body"] = body
                if step.get("wait_terminal"):
                    payload = wait_terminal(server, ctx["live_job"], token)
                    if "live_terminal_before_cancel" in ctx:
                        ctx["live_terminal_before_cancel"] = copy.deepcopy(
                            payload.get("result") if isinstance(payload, dict) else None
                        )
            if step.get("capture_term"):
                if status not in (200, 202):
                    return results.report(
                        probe["id"], probe["title"], "FAIL", f"submit returned {status}")
                problem = submitted_record_problem(payload, body)
                if problem:
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "initial term publication: " + problem
                    )
                seen = payload["result"]
                ctx["live_term"] = (seen.get("variableDbId"), seen.get("version"))
                ctx["live_term_baseline"] = copy.deepcopy(body)
            if step.get("capture_ledger"):
                if status not in (200, 202):
                    return results.report(
                        probe["id"], probe["title"], "FAIL", f"submit returned {status}")
                problem = submitted_record_problem(payload, body)
                if problem:
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "initial ledger publication: " + problem
                    )
                seen = payload["result"]
                ctx["live_ledger"] = (seen.get("seedLotDbId"), seen.get("entryDbId"))
            if step.get("capture_model"):
                if status not in (200, 202):
                    return results.report(
                        probe["id"], probe["title"], "FAIL", f"submit returned {status}")
                problem = submitted_record_problem(payload, body)
                if problem:
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "initial model publication: " + problem
                    )
                seen = payload["result"]
                ctx["live_model"] = (seen.get("modelDbId"), seen.get("modelVersion"))
                ctx["live_model_baseline"] = (
                    body.get("modelDbId"), body.get("modelVersion"),
                    body.get("artifactDigest"),
                )
                ctx["live_model_original"] = copy.deepcopy(body)
            if step.get("capture_model_revoked"):
                if status not in (200, 202):
                    return results.report(
                        probe["id"], probe["title"], "FAIL", f"submit returned {status}")
                # A later rejected inference or completed result does not
                # validate the initial model-registration acknowledgment.
                problem = submitted_record_problem(payload, body)
                if problem:
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "initial revoked model publication: " + problem
                    )
                seen = payload["result"]
                ctx["live_model_revoked"] = (seen.get("modelDbId"), seen.get("modelVersion"))
                ctx["live_model_revoked_original"] = copy.deepcopy(body)
            if step.get("capture_model_deprecated"):
                if status not in (200, 202):
                    return results.report(
                        probe["id"], probe["title"], "FAIL", f"submit returned {status}")
                # A later rejected inference or completed result does not
                # validate the initial model-registration acknowledgment.
                problem = submitted_record_problem(payload, body)
                if problem:
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "initial deprecated model publication: " + problem
                    )
                seen = payload["result"]
                ctx["live_model_deprecated"] = (seen.get("modelDbId"), seen.get("modelVersion"))
                ctx["live_model_deprecated_original"] = copy.deepcopy(body)
            if step.get("capture_matrix"):
                if status not in (200, 202):
                    return results.report(
                        probe["id"], probe["title"], "FAIL", f"submit returned {status}")
                problem = submitted_record_problem(payload, body)
                if problem:
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "initial matrix publication: " + problem
                    )
                seen = payload["result"]
                ctx["live_matrix"] = seen.get("matrixDbId")
                ctx["live_matrix_baseline"] = (body.get("matrixDbId"), body.get("fileDigest"))
                ctx["live_matrix_original"] = copy.deepcopy(body)
            if step.get("capture_package"):
                if status not in (200, 202):
                    return results.report(
                        probe["id"], probe["title"], "FAIL", f"submit returned {status}")
                problem = submitted_record_problem(payload, body)
                if problem:
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "initial package publication: " + problem
                    )
                seen = payload["result"]
                ctx["live_package"] = seen.get("packageDbId")
                ctx["live_package_baseline"] = (body.get("packageDbId"), body.get("license"))
                ctx["live_package_original"] = copy.deepcopy(body)
            if step.get("capture_telemetry"):
                if status not in (200, 202):
                    return results.report(
                        probe["id"], probe["title"], "FAIL", f"submit returned {status}")
            assertion = step.get("assert", {})
            if assertion.get("rejected") and not (
                    type(status) is int and 400 <= status < 500):
                # An HTTP 5xx response is a server failure, not evidence
                # that a conflicting or terminal-state operation was rejected.
                # The precise 4xx conflict code remains an open proposal
                # decision; do not silently select one here.
                return results.report(
                    probe["id"], probe["title"], "FAIL",
                    f"expected client-side rejection (4xx), got {status}")
            if "status" in assertion and status != assertion["status"]:
                return results.report(
                    probe["id"], probe["title"], "FAIL",
                    f"expected {assertion['status']}, got {status}")
            if assertion.get("deprecated_inference_completed"):
                accepted = payload.get("result") if isinstance(payload, dict) else None
                job_id = (accepted.get("jobDbId") if isinstance(accepted, dict)
                          else None)
                # The terminal readback cannot repair a corrupted
                # initial acknowledgment. Bind the accepted job's type
                # and idempotency key to the original inference request
                # before any polling occurs.
                submitted = ctx.get("live_deprecated_inference_request")
                if (status != 202 or not isinstance(job_id, str) or not job_id
                        or not isinstance(submitted, dict)
                        or submitted.get("jobType") != "inference"
                        or not isinstance(submitted.get("idempotencyKey"), str)
                        or not submitted["idempotencyKey"]
                        or not valid_job_wire_fields(accepted)
                        or accepted.get("jobType") != submitted["jobType"]
                        or accepted.get("idempotencyKey")
                            != submitted["idempotencyKey"]):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "deprecated inference initial acknowledgment missing or "
                        "changing original job identifier, type, key or status"
                    )
                terminal_payload = wait_terminal(server, job_id, token)
                terminal_job = (terminal_payload.get("result")
                                if isinstance(terminal_payload, dict) else None)
                original_model = ctx.get("live_model_deprecated_original")
                expected_model = ctx.get("live_model_deprecated")
                submitted = ctx.get("live_deprecated_inference_request")
                parameters = (submitted.get("parameters")
                              if isinstance(submitted, dict) else None)
                completed = (terminal_job.get("result")
                             if isinstance(terminal_job, dict) else None)
                rows = completed.get("data") if isinstance(completed, dict) else None
                expected_digest = (
                    hashlib.sha256(canonical(parameters["inputs"]).encode("utf-8"))
                    .hexdigest()
                    if isinstance(parameters, dict) and "inputs" in parameters
                    else None
                )
                if (not isinstance(original_model, dict)
                        or original_model.get("status") != "deprecated"
                        or not isinstance(expected_model, tuple)
                        or len(expected_model) != 2
                        or expected_model != (
                            original_model.get("modelDbId"),
                            original_model.get("modelVersion"))
                        or not isinstance(submitted, dict)
                        or submitted.get("jobType") != "inference"
                        or not isinstance(submitted.get("idempotencyKey"), str)
                        or not submitted["idempotencyKey"]
                        or not isinstance(parameters, dict)
                        or (parameters.get("modelDbId"),
                            parameters.get("modelVersion")) != expected_model
                        or not isinstance(terminal_job, dict)
                        or terminal_job.get("jobDbId") != job_id
                        or terminal_job.get("jobType") != "inference"
                        or terminal_job.get("idempotencyKey")
                            != submitted["idempotencyKey"]
                        or terminal_job.get("status") != "COMPLETED"
                        or not isinstance(rows, list) or len(rows) != 1
                        or not isinstance(rows[0], dict)
                        or (rows[0].get("modelDbId"),
                            rows[0].get("modelVersion")) != expected_model
                        or rows[0].get("inputsDigest") != expected_digest):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "deprecated inference completed without original model, "
                        "request key, version or canonical input digest binding"
                    )
            if assertion.get("embargo_denial_no_payload"):
                # A 403 can still echo a whole protected record, including
                # in plain-text errors. Compare against the original request.
                original = ctx.get("live_package_original")
                captured_id = ctx.get("live_package")
                if (status != 403 or not isinstance(original, dict)
                        or not isinstance(captured_id, str) or not captured_id
                        or original.get("packageDbId") != captured_id
                        or not isinstance(payload, dict)
                        or "result" in payload or "data" in payload):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "embargo denial missing or contains a package data envelope"
                    )
                serialized = json.dumps(payload, ensure_ascii=False, sort_keys=True)
                protected = [original.get("title"), original.get("license"),
                             original.get("publisher"),
                             original.get("embargoUntil")]
                protected.extend(
                    entry.get("value") for entry in original.get("identifiers", [])
                    if isinstance(entry, dict)
                )
                protected.extend(
                    value for value in original.get("creators", [])
                    if isinstance(value, str)
                )
                for item in original.get("payloadRefs", []):
                    if isinstance(item, dict):
                        protected.extend(item.get(field) for field in (
                            "endpoint", "responseDigest", "queryDigest"
                        ))
                if ("payloadRefs" in serialized
                        or any(isinstance(value, str) and len(value) >= 5
                               and value in serialized for value in protected)):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "embargo denial leaks protected package metadata or evidence"
                    )
            if assertion.get("expired_result_withheld"):
                # A visible EXPIRED status does not prove the result data
                # was actually withheld from this expired job response.
                expired = payload.get("result") if isinstance(payload, dict) else None
                if (status != 200 or not isinstance(expired, dict)
                        or not isinstance(expired_job, str) or not expired_job
                        or expired.get("jobDbId") != expired_job
                        or expired.get("status") != "EXPIRED"
                        or ("result" in expired and expired["result"] is not None)):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "expired job identity/status invalid or result still exposed"
                    )
            if assertion.get("unknown_job_type_not_stored"):
                original = ctx.get("live_unknown_type_request")
                # The absence of one rejected key/type is not trustworthy
                # evidence if unrelated collection rows have missing or
                # duplicated identities. Reuse the existing complete
                # collection validator rather than trusting only row counts.
                snapshot, problem = immutable_job_snapshot(status, payload)
                if (problem or not isinstance(original, dict)
                        or not isinstance(original.get("idempotencyKey"), str)
                        or not original["idempotencyKey"]
                        or not isinstance(original.get("jobType"), str)
                        or not original["jobType"]):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "unknown job-type rejection lacks valid complete jobs "
                        "readback: " + (problem or "original rejected request unavailable")
                    )
                if any(
                        job_type == original["jobType"]
                        or key == original["idempotencyKey"]
                        for job_type, key in snapshot.values()
                ):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "unknown job type created a stored job despite HTTP 400"
                    )
            if assertion.get("terminal_state_unchanged"):
                baseline = ctx.get("live_terminal_before_cancel")
                saved = payload.get("result") if isinstance(payload, dict) else None
                original = ctx.get("live_body")
                terminal = {"COMPLETED", "FAILED", "CANCELLED", "EXPIRED"}
                if (status != 200 or not isinstance(baseline, dict)
                        or not isinstance(saved, dict)
                        or not isinstance(original, dict)
                        or not isinstance(ctx.get("live_job"), str)
                        or not ctx["live_job"]
                        or baseline.get("jobDbId") != ctx["live_job"]
                        or saved.get("jobDbId") != ctx["live_job"]
                        or baseline.get("status") not in terminal
                        or saved.get("status") != baseline["status"]
                        or any(
                            not isinstance(original.get(field), str)
                            or not original[field]
                            or baseline.get(field) != original[field]
                            or saved.get(field) != original[field]
                            for field in ("jobType", "idempotencyKey")
                        )
                        or ("result" in baseline) != ("result" in saved)
                        or (("result" in baseline)
                            and saved["result"] != baseline["result"])):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "terminal job original identity, status or result changed "
                        "after rejected DELETE"
                    )
            if assertion.get("capture_job_collection"):
                snapshot, problem = immutable_job_snapshot(status, payload)
                original = ctx.get("live_body")
                original_id = ctx.get("live_job")
                if (problem or not isinstance(original, dict)
                        or not isinstance(original_id, str) or not original_id
                        or not isinstance(snapshot, dict)
                        or snapshot.get(original_id) != (
                            original.get("jobType"), original.get("idempotencyKey"))):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "original job absent from pre-conflict collection: " +
                        (problem or "identity or request mismatch")
                    )
                ctx["live_job_conflict_baseline"] = snapshot
            if assertion.get("job_conflict_collection_unchanged"):
                snapshot, problem = immutable_job_snapshot(status, payload)
                baseline = ctx.get("live_job_conflict_baseline")
                if (problem or not isinstance(baseline, dict)
                        or snapshot != baseline):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "conflict changed job collection immutable identities: " +
                        (problem or "stored jobs added, removed, or rewritten")
                    )
            if assertion.get("job_replay_single_stored"):
                # All visible jobs must have valid, distinct identifiers:
                # a correct original row in a malformed collection is not
                # reliable evidence that the identical replay had one effect.
                snapshot, problem = immutable_job_snapshot(status, payload)
                expected_id = ctx.get("live_job")
                submitted = ctx.get("live_body")
                expected_key = ctx.get("live_key")
                if (problem or not isinstance(expected_id, str)
                        or not expected_id
                        or not isinstance(expected_key, str) or not expected_key
                        or not isinstance(submitted, dict)
                        or submitted.get("idempotencyKey") != expected_key
                        or not isinstance(submitted.get("jobType"), str)
                        or not submitted["jobType"]
                        or not snapshot):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "job replay readback lacks valid, unique complete jobs: "
                        + (problem or "original job identity unavailable")
                    )
                matched_key = [
                    job_id for job_id, (_, key) in snapshot.items()
                    if key == expected_key
                ]
                if (matched_key != [expected_id]
                        or snapshot.get(expected_id)
                            != (submitted["jobType"], expected_key)):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "job replay missing, duplicated, or changed stored identity"
                    )
            if assertion.get("deprecated_model_persisted"):
                original = ctx.get("live_model_deprecated_original")
                identity = ctx.get("live_model_deprecated")
                expected_id = (identity[0] if isinstance(identity, tuple)
                               and len(identity) == 2 else None)
                problem = published_record_problem(
                    status, payload, original, expected_id, "modelDbId"
                )
                if (problem or not isinstance(original, dict)
                        or original.get("status") != "deprecated"
                        or not isinstance(identity, tuple) or len(identity) != 2
                        or identity != (original.get("modelDbId"),
                                        original.get("modelVersion"))):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "registered deprecated model not persisted intact: " +
                        (problem or "original deprecated model version/status mismatch")
                    )
            if assertion.get("revoked_model_persisted"):
                original = ctx.get("live_model_revoked_original")
                identity = ctx.get("live_model_revoked")
                expected_id = (identity[0] if isinstance(identity, tuple)
                               and len(identity) == 2 else None)
                problem = published_record_problem(
                    status, payload, original, expected_id, "modelDbId"
                )
                if (problem or not isinstance(original, dict)
                        or original.get("status") != "revoked"
                        or not isinstance(identity, tuple) or len(identity) != 2
                        or identity != (original.get("modelDbId"),
                                        original.get("modelVersion"))):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "registered revoked model not persisted intact: " +
                        (problem or "original revoked model version/status mismatch")
                    )
            if assertion.get("rejected_inference_not_stored"):
                # Rejected inference is not proved absent by a collection
                # with duplicate or malformed identities, even when its
                # page counters are internally consistent.
                snapshot, problem = immutable_job_snapshot(status, payload)
                result = payload.get("result") if isinstance(payload, dict) else None
                rows = result.get("data") if isinstance(result, dict) else None
                denied = ctx.get("live_rejected_inference")
                if (problem
                        or not isinstance(denied, dict)
                        or set(denied) != {"live_inference_unknown",
                                          "live_inference_revoked"}
                        or any(not isinstance(item, dict)
                               or not isinstance(item.get("key"), str)
                               or not item["key"]
                               or not isinstance(item.get("modelDbId"), str)
                               or not item["modelDbId"]
                               for item in denied.values())
                        or len({item["key"] for item in denied.values()}) != 2):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "rejected inference readback lacks valid, complete jobs "
                        "evidence: " + (problem or "rejected input unavailable")
                    )
                denied_keys = {item["key"] for item in denied.values()}
                denied_models = {item["modelDbId"] for item in denied.values()}
                if (any(key in denied_keys for _, key in snapshot.values())
                        or any(
                            row["jobType"] == "inference"
                            and isinstance(row.get("parameters"), dict)
                            and row["parameters"].get("modelDbId") in denied_models
                            for row in rows
                        )):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "rejected inference created a stored job despite HTTP 400"
                    )
            if assertion.get("concurrent_single_stored_job"):
                snapshot, problem = immutable_job_snapshot(status, payload)
                expected_key = ctx.get("live_concurrent_key")
                expected_id = ctx.get("live_concurrent_job")
                expected_type = ctx.get("live_concurrent_type")
                if (problem or not isinstance(expected_key, str)
                        or not expected_key
                        or not isinstance(expected_id, str) or not expected_id
                        or not isinstance(expected_type, str)
                        or not expected_type or not snapshot):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "concurrent job readback lacks valid, unique complete "
                        "jobs: " + (problem or "original concurrent identity unavailable")
                    )
                matched_key = [
                    job_id for job_id, (_, key) in snapshot.items()
                    if key == expected_key
                ]
                if (matched_key != [expected_id]
                        or snapshot.get(expected_id)
                            != (expected_type, expected_key)):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "concurrent submissions created missing, duplicate, "
                        "or mismatched stored jobs"
                    )
            if "collection_contains_created" in assertion:
                kind = assertion["collection_contains_created"]
                result = payload.get("result") if isinstance(payload, dict) else None
                rows = result.get("data") if isinstance(result, dict) else None
                metadata = payload.get("metadata") if isinstance(payload, dict) else None
                pagination = (metadata.get("pagination")
                              if isinstance(metadata, dict) else None)
                if (status != 200 or not isinstance(rows, list) or not rows
                        or not isinstance(pagination, dict)
                        or not all(isinstance(row, dict) for row in rows)):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        f"{kind} collection missing data or pagination"
                    )
                fields = ("totalCount", "pageSize", "totalPages", "currentPage")
                if (any(type(pagination.get(k)) is not int for k in fields)
                        or pagination["totalCount"] < len(rows)
                        or pagination["pageSize"] < len(rows)
                        or pagination["pageSize"] < 1
                        or pagination["currentPage"] < 0
                        or pagination["totalPages"] < 1
                        or pagination["currentPage"] >= pagination["totalPages"]
                        or pagination["currentPage"] != 0
                        or pagination["totalPages"] != (
                            pagination["totalCount"] + pagination["pageSize"] - 1
                        ) // pagination["pageSize"]
                        or len(rows) != min(
                            pagination["pageSize"], pagination["totalCount"])):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        f"{kind} pagination counts/shape invalid: {pagination!r}"
                    )
                if kind == "jobs":
                    # The stored job must be the exact accepted job and
                    # retain the original submitted type/idempotency key.
                    # Two rows with the same key but distinct IDs are not a
                    # single created resource, even with valid pagination.
                    expected_id = ctx.get("live_job")
                    original = ctx.get("live_body")
                    if (not isinstance(expected_id, str) or not expected_id
                            or not isinstance(original, dict)
                            or not isinstance(original.get("jobType"), str)
                            or not isinstance(original.get("idempotencyKey"), str)
                            or not original["idempotencyKey"]):
                        return results.report(
                            probe["id"], probe["title"], "FAIL",
                            "jobs original submission or accepted identity missing"
                        )
                    # L-25 checks one first page, not necessarily the
                    # complete collection. Validate every visible job's
                    # schema identity without requiring totalPages == 1.
                    visible_job_ids = set()
                    for row in rows:
                        job_id = row.get("jobDbId")
                        if (not isinstance(job_id, str) or not job_id
                                or not isinstance(row.get("jobType"), str)
                                or not row["jobType"]
                                or not valid_job_wire_fields(row)
                                or ("idempotencyKey" in row
                                    and not isinstance(row["idempotencyKey"], str))
                                or job_id in visible_job_ids):
                            return results.report(
                                probe["id"], probe["title"], "FAIL",
                                "jobs first page contains malformed or duplicated "
                                "job identities/statuses"
                            )
                        visible_job_ids.add(job_id)
                    same_id = [
                        row for row in rows if row.get("jobDbId") == expected_id
                    ]
                    same_key = [
                        row for row in rows
                        if row.get("idempotencyKey") == original["idempotencyKey"]
                    ]
                    if (len(same_id) != 1 or len(same_key) != 1
                            or same_id[0] is not same_key[0]
                            or same_id[0].get("jobType") != original["jobType"]):
                        return results.report(
                            probe["id"], probe["title"], "FAIL",
                            "jobs collection does not retain one original "
                            "job identity, idempotency key and type"
                        )
                else:
                    # The accepted version and the stored record must match
                    # the original model submission, not just one another.
                    original = ctx.get("live_model_original")
                    expected_model = ctx.get("live_model")
                    if (not isinstance(original, dict)
                            or not isinstance(expected_model, tuple)
                            or len(expected_model) != 2
                            or expected_model != (
                                original.get("modelDbId"),
                                original.get("modelVersion"))):
                        return results.report(
                            probe["id"], probe["title"], "FAIL",
                            "models original submission or accepted version missing"
                        )
                    # A correct newly published version does not prove
                    # that unrelated visible model versions have unique,
                    # well-formed identities. Do not require all pages.
                    visible_model_versions = set()
                    for row in rows:
                        model_id = row.get("modelDbId")
                        model_version = row.get("modelVersion")
                        version_key = (model_id, model_version)
                        if (not isinstance(model_id, str) or not model_id
                                or not isinstance(model_version, str)
                                or not model_version
                                or version_key in visible_model_versions):
                            return results.report(
                                probe["id"], probe["title"], "FAIL",
                                "models first page contains malformed or "
                                "duplicated model-version identities"
                            )
                        visible_model_versions.add(version_key)
                    same_version = [
                        row for row in rows
                        if (row.get("modelDbId"), row.get("modelVersion"))
                        == expected_model
                    ]
                    if (len(same_version) != 1
                            or any(k not in same_version[0]
                                   or same_version[0][k] != v
                                   for k, v in original.items())):
                        return results.report(
                            probe["id"], probe["title"], "FAIL",
                            "models collection does not retain one unchanged "
                            "original model version"
                        )
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
            if assertion.get("term_replay_single_version"):
                # L-08 must inspect all published versions for its fresh term,
                # not just trust two identical response identifiers.
                result = payload.get("result") if isinstance(payload, dict) else None
                rows = result.get("data") if isinstance(result, dict) else None
                metadata = payload.get("metadata") if isinstance(payload, dict) else None
                page = metadata.get("pagination") if isinstance(metadata, dict) else None
                baseline = ctx.get("live_term_baseline")
                published_id = ctx.get("live_term")
                if (status != 200 or not isinstance(baseline, dict)
                        or not isinstance(published_id, tuple)
                        or published_id != (baseline.get("variableDbId"),
                                            baseline.get("version"))
                        or not isinstance(rows, list) or len(rows) != 1
                        or not isinstance(rows[0], dict)
                        or not isinstance(page, dict)
                        or any(type(page.get(k)) is not int
                               for k in ("totalCount", "totalPages",
                                         "currentPage", "pageSize"))
                        or page["totalCount"] != 1 or page["totalPages"] != 1
                        or page["currentPage"] != 0 or page["pageSize"] < 1):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "term replay did not expose a complete one-version collection"
                    )
                row = rows[0]
                if (row.get("variableDbId") != baseline["variableDbId"]
                        or row.get("version") != baseline["version"]
                        or any(k not in row or row[k] != value
                               for k, value in baseline.items())):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "original term version or content changed after replay"
                    )
            if assertion.get("unchanged_term_record"):
                # Verify the stored version against the original submitted
                # content, never the potentially tampered conflict response.
                baseline = ctx.get("live_term_baseline")
                stored = payload.get("result") if isinstance(payload, dict) else None
                if (status != 200 or not isinstance(baseline, dict)
                        or not isinstance(stored, dict)
                        or any(field not in stored or stored[field] != expected
                               for field, expected in baseline.items())):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "stored variable-term version changed after conflict"
                    )
            if assertion.get("same_term"):
                seen = payload.get("result") if isinstance(payload, dict) else None
                problem = submitted_record_problem(payload, ctx.get("live_term_baseline"))
                identity = ((seen.get("variableDbId"), seen.get("version"))) if isinstance(seen, dict) else None
                expected = ctx.get("live_term")
                if problem or identity != expected:
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        problem or f"term replay returned {identity}, expected {expected}"
                    )
            if assertion.get("same_ledger"):
                seen = payload.get("result") if isinstance(payload, dict) else None
                problem = submitted_record_problem(payload, ctx.get("live_ledger_body"))
                identity = ((seen.get("seedLotDbId"), seen.get("entryDbId"))) if isinstance(seen, dict) else None
                expected = ctx.get("live_ledger")
                if problem or identity != expected:
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        problem or f"ledger replay returned {identity}, expected {expected}"
                    )
            if assertion.get("unchanged_model_digest"):
                original = ctx.get("live_model_original")
                identity = ctx.get("live_model")
                expected_id = (identity[0] if isinstance(identity, tuple)
                               and len(identity) == 2 else None)
                problem = published_record_problem(
                    status, payload, original, expected_id, "modelDbId"
                )
                if (problem or not isinstance(identity, tuple) or len(identity) != 2
                        or not isinstance(original, dict)
                        or original.get("modelVersion") != identity[1]):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "model: " + (problem or "original model version mismatch")
                    )
            if assertion.get("same_model"):
                seen = payload.get("result") if isinstance(payload, dict) else None
                problem = submitted_record_problem(payload, ctx.get("live_model_original"))
                identity = ((seen.get("modelDbId"), seen.get("modelVersion"))) if isinstance(seen, dict) else None
                expected = ctx.get("live_model")
                if problem or identity != expected:
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        problem or f"model replay returned {identity}, expected {expected}"
                    )
            if assertion.get("unchanged_matrix_digest"):
                problem = published_record_problem(
                    status, payload, ctx.get("live_matrix_original"),
                    ctx.get("live_matrix"), "matrixDbId"
                )
                if problem:
                    return results.report(
                        probe["id"], probe["title"], "FAIL", "matrix: " + problem
                    )
            if assertion.get("unchanged_package_license"):
                problem = published_record_problem(
                    status, payload, ctx.get("live_package_original"),
                    ctx.get("live_package"), "packageDbId"
                )
                if problem:
                    return results.report(
                        probe["id"], probe["title"], "FAIL", "package: " + problem
                    )
            if assertion.get("model_replay_single_version"):
                original = ctx.get("live_model_original")
                expected = ctx.get("live_model")
                expected_id = expected[0] if isinstance(expected, tuple) and len(expected) == 2 else None
                result = payload.get("result") if isinstance(payload, dict) else None
                rows = result.get("data") if isinstance(result, dict) else None
                problem = replay_collection_problem(
                    status, payload, original, expected_id, "modelDbId"
                )
                if (problem or not isinstance(rows, list) or len(rows) != 1
                        or not isinstance(expected, tuple) or len(expected) != 2
                        or not isinstance(original, dict)
                        or expected != (original.get("modelDbId"),
                                        original.get("modelVersion"))):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "model replay version integrity failed: " +
                        (problem or "filtered model versions incomplete or mismatched")
                    )
            if assertion.get("matrix_replay_single_record"):
                problem = replay_collection_problem(
                    status, payload, ctx.get("live_matrix_original"),
                    ctx.get("live_matrix"), "matrixDbId"
                )
                if problem:
                    return results.report(
                        probe["id"], probe["title"], "FAIL", "matrix: " + problem
                    )
            if assertion.get("package_replay_single_record"):
                problem = replay_collection_problem(
                    status, payload, ctx.get("live_package_original"),
                    ctx.get("live_package"), "packageDbId"
                )
                if problem:
                    return results.report(
                        probe["id"], probe["title"], "FAIL", "package: " + problem
                    )
            if assertion.get("same_matrix"):
                seen = payload.get("result") if isinstance(payload, dict) else None
                problem = submitted_record_problem(payload, ctx.get("live_matrix_original"))
                identity = (seen.get("matrixDbId")) if isinstance(seen, dict) else None
                expected = ctx.get("live_matrix")
                if problem or identity != expected:
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        problem or f"matrix replay returned {identity}, expected {expected}"
                    )
            if assertion.get("same_package"):
                seen = payload.get("result") if isinstance(payload, dict) else None
                problem = submitted_record_problem(payload, ctx.get("live_package_original"))
                identity = (seen.get("packageDbId")) if isinstance(seen, dict) else None
                expected = ctx.get("live_package")
                if problem or identity != expected:
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        problem or f"package replay returned {identity}, expected {expected}"
                    )
            if assertion.get("telemetry_original_intact"):
                original = ctx.get("live_batch")
                result = payload.get("result") if isinstance(payload, dict) else None
                rows = result.get("data") if isinstance(result, dict) else None
                if (status != 200 or not isinstance(original, list)
                        or not isinstance(rows, list)
                        or not all(isinstance(point, dict) for point in original)):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "original telemetry unavailable after replay or rejected conflict"
                    )
                identity = lambda point: (
                    point.get("deviceDbId"), point.get("sensorDbId"),
                    point.get("timestamp")
                )
                expected = {identity(point): point for point in original}
                if len(expected) != len(original):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "original telemetry contains duplicate source identities"
                    )
                actual = {}
                for point in rows:
                    if not isinstance(point, dict):
                        return results.report(
                            probe["id"], probe["title"], "FAIL",
                            "malformed telemetry row after replay or rejected conflict"
                        )
                    key = identity(point)
                    if key in actual:
                        return results.report(
                            probe["id"], probe["title"], "FAIL",
                            f"duplicate telemetry identity after replay or conflict: {key!r}"
                        )
                    actual[key] = point
                if set(actual) != set(expected) or len(rows) != len(original):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "stored telemetry identities were added, removed or reassigned"
                    )
                for key, source in expected.items():
                    stored = actual[key]
                    if any(field not in stored or stored[field] != value
                           for field, value in source.items()):
                        return results.report(
                            probe["id"], probe["title"], "FAIL",
                            f"original telemetry field or nested provenance changed: {key!r}"
                        )
            if "telemetry_counts" in assertion:
                # JSON booleans must not pass integer-count checks: in
                # Python, False == 0 and True == 1.
                result = payload.get("result") if isinstance(payload, dict) else None
                want = assertion["telemetry_counts"]
                if (status != 200 or not isinstance(result, dict)
                        or any(type(result.get(name)) is not int
                               or result[name] < 0 for name in ("appended", "replayed"))
                        or (result["appended"], result["replayed"]) != (
                            want["appended"], want["replayed"])):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "telemetry counts must be nonnegative integers "
                        "matching original append/replay expectations"
                    )
            if assertion.get("telemetry_no_conflicts"):
                # Clean append and identical replay cannot report rejected
                # natural keys; counts alone would miss fabricated conflicts.
                result = payload.get("result") if isinstance(payload, dict) else None
                conflicts = result.get("conflicts") if isinstance(result, dict) else None
                if status != 200 or conflicts != []:
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "successful append or identical replay reported telemetry conflicts"
                    )
            if "telemetry_conflicts" in assertion:
                result = payload.get("result") if isinstance(payload, dict) else None
                seen = result.get("conflicts") if isinstance(result, dict) else None
                submitted = ctx.get("live_telemetry_conflict_submitted")
                original = ctx.get("live_batch")
                if (status != 200 or not isinstance(seen, list)
                        or not isinstance(submitted, list)
                        or len(submitted) != 1
                        or not isinstance(submitted[0], dict)
                        or not isinstance(original, list)
                        or not all(isinstance(point, dict) for point in original)
                        or len(seen) != assertion["telemetry_conflicts"]):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "telemetry conflict response or original request unavailable"
                    )
                rejected = submitted[0]
                identity = (
                    rejected.get("deviceDbId"), rejected.get("sensorDbId"),
                    rejected.get("timestamp"),
                )
                original_points = [
                    point for point in original
                    if (point.get("deviceDbId"), point.get("sensorDbId"),
                        point.get("timestamp")) == identity
                ]
                if (len(original_points) != 1
                        or original_points[0].get("value") == rejected.get("value")
                        or any(not isinstance(value, str) or not value
                               for value in identity)
                        or seen != ["/".join(identity)]):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "telemetry conflict did not name the actual rejected natural key"
                    )
            if assertion.get("telemetry_window_partitions"):
                # L-26 must verify that each minute retains its own reading,
                # not merely that an arbitrary three rows were returned.
                result = payload.get("result") if isinstance(payload, dict) else None
                rows = result.get("data") if isinstance(result, dict) else None
                original = ctx.get("live_batch")
                if (status != 200 or not isinstance(rows, list)
                        or not isinstance(original, list) or not original
                        or len(rows) != len(original)):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "windowed telemetry has missing or invalid buckets"
                    )
                expected = {}
                for point in original:
                    if (not isinstance(point, dict)
                            or not isinstance(point.get("timestamp"), str)
                            or type(point.get("value")) not in (int, float)
                            or point["timestamp"] in expected):
                        return results.report(
                            probe["id"], probe["title"], "FAIL",
                            "submitted telemetry cannot establish unique window expectations"
                        )
                    expected[point["timestamp"]] = point["value"]
                seen = set()
                for row in rows:
                    if not isinstance(row, dict):
                        return results.report(
                            probe["id"], probe["title"], "FAIL",
                            "windowed telemetry contains a malformed bucket"
                        )
                    stamp = row.get("windowStart")
                    value = row.get("value")
                    if (not isinstance(stamp, str) or stamp not in expected
                            or stamp in seen
                            or row.get("aggregation") != "mean"
                            or type(row.get("sampleCount")) is not int
                            or row["sampleCount"] != 1
                            or type(value) not in (int, float)
                            or not (-float("inf") < value < float("inf"))
                            or abs(value - expected[stamp]) > 1e-9):
                        return results.report(
                            probe["id"], probe["title"], "FAIL",
                            f"incorrect telemetry window bucket: {row!r}"
                        )
                    seen.add(stamp)
                if seen != set(expected):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "telemetry window partition omitted a submitted minute"
                    )
            if assertion.get("telemetry_page_slice"):
                # L-28 must traverse both pages, retaining every submitted field.
                # Derive the expected slice from the actual requested page.
                requested = parse_qs(urlsplit(path).query)
                page_parts = requested.get("page")
                size_parts = requested.get("pageSize")
                if page_parts not in (["0"], ["1"]) or size_parts != ["2"]:
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "telemetry page slice requested unexpected page or page size"
                    )
                page_index = int(page_parts[0])
                result = payload.get("result") if isinstance(payload, dict) else None
                rows = result.get("data") if isinstance(result, dict) else None
                metadata = payload.get("metadata") if isinstance(payload, dict) else None
                pagination = (metadata.get("pagination")
                              if isinstance(metadata, dict) else None)
                original = ctx.get("live_batch")
                if (status != 200 or not isinstance(rows, list)
                        or not isinstance(original, list) or len(original) != 3
                        or not all(isinstance(point, dict) for point in original)
                        or len({(p.get("deviceDbId"), p.get("sensorDbId"),
                                 p.get("timestamp")) for p in original}) != 3
                        or not isinstance(pagination, dict)
                        or any(type(pagination.get(k)) is not int
                               for k in ("currentPage", "pageSize",
                                         "totalCount", "totalPages"))
                        or (pagination["currentPage"], pagination["pageSize"],
                            pagination["totalCount"], pagination["totalPages"])
                            != (page_index, 2, 3, 2)):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "telemetry pagination envelope or original source incorrect"
                    )
                expected = sorted(original, key=lambda point: point["timestamp"])
                expected = expected[page_index * 2:(page_index + 1) * 2]
                if len(rows) != len(expected):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "telemetry page slice has incorrect row count"
                    )
                for index, (point, wanted) in enumerate(zip(rows, expected)):
                    value = point.get("value") if isinstance(point, dict) else None
                    if (not isinstance(point, dict)
                            or type(value) not in (int, float)
                            or not math.isfinite(value)
                            or any(k not in point or point[k] != v
                                   for k, v in wanted.items())):
                        return results.report(
                            probe["id"], probe["title"], "FAIL",
                            f"telemetry page {page_index} source mismatch "
                            f"at row {index}: {point!r}"
                        )
            if "telemetry_mean" in assertion:
                original = ctx.get("live_batch")
                values = ([point.get("value") for point in original]
                          if isinstance(original, list)
                          and all(isinstance(point, dict) for point in original)
                          else None)
                result = payload.get("result") if isinstance(payload, dict) else None
                rows = result.get("data") if isinstance(result, dict) else None
                metadata = payload.get("metadata") if isinstance(payload, dict) else None
                page = metadata.get("pagination") if isinstance(metadata, dict) else None
                if (status != 200 or not isinstance(values, list) or not values
                        or any(type(v) not in (int, float) or not math.isfinite(v)
                               for v in values)
                        or not isinstance(rows, list) or len(rows) != 1
                        or not isinstance(rows[0], dict)
                        or not isinstance(page, dict)
                        or any(type(page.get(k)) is not int
                               for k in ("totalCount", "totalPages", "pageSize",
                                         "currentPage"))
                        or page["totalCount"] != 1
                        or page["totalPages"] != 1
                        or page["pageSize"] < 1
                        or page["currentPage"] != 0):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "telemetry mean unavailable or incomplete aggregation envelope"
                    )
                expected_mean = sum(values) / len(values)
                bucket = rows[0]
                got_mean = bucket.get("value")
                if (bucket.get("aggregation") != "mean"
                        or bucket.get("windowStart") != original[0].get("timestamp")
                        or type(bucket.get("sampleCount")) is not int
                        or bucket["sampleCount"] != len(values)
                        or bucket["sampleCount"] != assertion.get("telemetry_samples")
                        or type(got_mean) not in (int, float)
                        or not math.isfinite(got_mean)
                        or abs(got_mean - expected_mean) > 1e-9
                        or abs(got_mean - assertion["telemetry_mean"]) > 1e-9):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "mean bucket does not recompute from captured source samples"
                    )
            if assertion.get("inference_intact"):
                original_model = ctx.get("live_model_original")
                expected_model = ctx.get("live_model")
                request_body = ctx.get("live_body")
                params = (request_body.get("parameters")
                          if isinstance(request_body, dict) else None)
                job = payload.get("result") if isinstance(payload, dict) else None
                completed = job.get("result") if isinstance(job, dict) else None
                rows = completed.get("data") if isinstance(completed, dict) else None
                inputs = params.get("inputs") if isinstance(params, dict) else None
                want_digest = (
                    hashlib.sha256(canonical(inputs).encode("utf-8")).hexdigest()
                    if isinstance(params, dict) and "inputs" in params else None
                )
                if (status != 200 or not isinstance(original_model, dict)
                        or not isinstance(expected_model, tuple)
                        or len(expected_model) != 2
                        or expected_model != (
                            original_model.get("modelDbId"),
                            original_model.get("modelVersion"))
                        or not isinstance(request_body, dict)
                        or request_body.get("jobType") != "inference"
                        or not isinstance(request_body.get("idempotencyKey"), str)
                        or not request_body["idempotencyKey"]
                        or not isinstance(params, dict)
                        or (params.get("modelDbId"), params.get("modelVersion"))
                            != expected_model
                        or inputs != ctx.get("live_inference_inputs")
                        or not isinstance(job, dict)
                        or job.get("jobDbId") != ctx.get("live_job")
                        or job.get("jobType") != "inference"
                        or job.get("idempotencyKey")
                            != request_body["idempotencyKey"]
                        or job.get("status") != "COMPLETED"
                        or not isinstance(rows, list) or len(rows) != 1
                        or not isinstance(rows[0], dict)
                        or (rows[0].get("modelDbId"),
                            rows[0].get("modelVersion")) != expected_model
                        or rows[0].get("inputsDigest") != want_digest):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "inference result not bound to original completed job, "
                        "registered model version or canonical input digest"
                    )
            if assertion.get("ledger_original_intact"):
                # L-11 must prove the original entry survived rejection,
                # not just that the ledger still has one record.
                result = payload.get("result") if isinstance(payload, dict) else None
                rows = result.get("data") if isinstance(result, dict) else None
                metadata = payload.get("metadata") if isinstance(payload, dict) else None
                page = metadata.get("pagination") if isinstance(metadata, dict) else None
                original = ctx.get("live_ledger_body")
                identity = ctx.get("live_ledger")
                lot_id = ctx.get("live_lot")
                if (status != 200 or not isinstance(original, dict)
                        or not isinstance(identity, tuple) or len(identity) != 2
                        or not isinstance(lot_id, str) or not lot_id
                        or identity[0] != lot_id
                        or not isinstance(identity[1], str) or not identity[1]
                        or not isinstance(rows, list) or len(rows) != 1
                        or not isinstance(rows[0], dict)
                        or not isinstance(page, dict)
                        or any(type(page.get(k)) is not int
                               for k in ("totalCount", "totalPages",
                                         "currentPage", "pageSize"))
                        or page["totalCount"] != 1 or page["totalPages"] != 1
                        or page["currentPage"] != 0 or page["pageSize"] < 1):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "ledger replay/conflict readback or pagination incomplete"
                    )
                row = rows[0]
                if (row.get("seedLotDbId") != lot_id
                        or row.get("entryDbId") != identity[1]
                        or any(k not in row or row[k] != value
                               for k, value in original.items())):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "original ledger entry changed after replay or rejected conflict"
                    )
            if "ledger_count" in assertion:
                rows = payload.get("result", {}).get("data", [])
                if len(rows) != assertion["ledger_count"]:
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        f"ledger holds {len(rows)} entries, "
                        f"expected {assertion['ledger_count']}")
            if assertion.get("negotiable"):
                problems = (v21_fallback_calls_problems(payload)
                            if status == 200 else [f"unexpected HTTP status {status}"])
                if not problems:
                    continue
                return results.report(
                    probe["id"], probe["title"], "FAIL",
                    "serverinfo not negotiable: " + "; ".join(problems))

            if assertion.get("capability_registry_match"):
                registry_path = ctx.get("capability_registry_path")
                problems = capability_contract_problems(
                    ctx.get("root", "."), payload, registry_path
                )
                if problems:
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "live ServerInfoV3 does not match the capability registry: " +
                        "; ".join(problems)
                    )
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
                # L-07 exercises the analysis echo reference workflow.
                # Comparing only provenance would accept a changed
                # observation value or scientific identity with the original
                # provenance copied onto an unrelated returned observation.
                request_body = ctx.get("live_body")
                parameters = (request_body.get("parameters")
                              if isinstance(request_body, dict) else None)
                submitted = (parameters.get("observation")
                             if isinstance(parameters, dict) else None)
                want = submitted.get("provenance") if isinstance(submitted, dict) else None
                job = payload.get("result") if isinstance(payload, dict) else None
                completed = job.get("result") if isinstance(job, dict) else None
                observations = completed.get("data") if isinstance(completed, dict) else None
                if (status != 200 or not isinstance(want, dict)
                        or not isinstance(request_body, dict)
                        or not isinstance(job, dict)
                        or job.get("jobDbId") != ctx.get("live_job")
                        or job.get("jobType") != request_body.get("jobType")
                        or job.get("idempotencyKey") != request_body.get("idempotencyKey")
                        or job.get("status") != "COMPLETED"
                        or not isinstance(observations, list)
                        or len(observations) != 1
                        or not isinstance(observations[0], dict)):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "completed job or original observation identity missing"
                    )
                returned = observations[0]
                if (returned.get("provenance") != want
                        or any(field not in returned or returned[field] != value
                               for field, value in submitted.items())):
                    return results.report(
                        probe["id"], probe["title"], "FAIL",
                        "original observation value, identity or nested provenance changed"
                    )
        results.report(probe["id"], probe["title"], "PASS")
    except Exception as exc:
        results.report(probe["id"], probe["title"], "FAIL", f"{type(exc).__name__}: {exc}")




# The manifest is the authority for currently registered probes. Preserve the
# accepted verification baseline while allowing future new probe identifiers.
REQUIRED_REGISTERED_PROBES = (
    {f"S-{number:02d}" for number in range(1, 22)}
    | {f"L-{number:02d}" for number in range(1, 29)}
)




# The live probe runner formerly ignored unrecognized call directives and
# unknown fixture names. Both could silently change which request was sent.
LIVE_BOOLEAN_DIRECTIVES = frozenset({
    "capture_job", "capture_term", "capture_ledger", "capture_model",
    "capture_model_revoked", "capture_model_deprecated",
    "capture_matrix", "capture_package", "capture_telemetry",
    "wait_terminal", "replay_capture",
})
LIVE_CALL_FIELDS = (LIVE_BOOLEAN_DIRECTIVES |
                    {"method", "path", "assert", "body_fixture",
                     "concurrent_posts"})
LIVE_BODY_FIXTURES = frozenset({
    "live_submit", "live_submit_conflict", "live_submit_unknown_type",
    "live_provenanced_submit", "live_term_submit", "live_term_conflict",
    "live_ledger_submit", "live_ledger_conflict", "live_model_submit",
    "live_model_conflict", "live_model_revoked", "live_model_deprecated",
    "live_matrix_submit", "live_matrix_conflict", "live_package_submit",
    "live_package_conflict", "live_package_embargoed",
    "live_telemetry_batch", "live_telemetry_conflict",
    "live_inference_submit", "live_inference_revoked",
    "live_inference_unknown", "live_inference_deprecated",
})


def validate_live_step_directives(probe_id, index, call):
    """Reject directives the runner would otherwise silently disregard."""
    unknown = set(call) - LIVE_CALL_FIELDS
    if unknown:
        raise ValueError(
            f"probe {probe_id} call {index}: unknown live call directive(s): "
            + ", ".join(sorted(map(str, unknown)))
        )
    for key in LIVE_BOOLEAN_DIRECTIVES & call.keys():
        if call[key] is not True:
            raise ValueError(
                f"probe {probe_id} call {index}: {key} must be true"
            )
    method = call["method"]
    fixture = call.get("body_fixture")
    if "body_fixture" in call:
        if not isinstance(fixture, str) or fixture not in LIVE_BODY_FIXTURES:
            raise ValueError(
                f"probe {probe_id} call {index}: unknown body_fixture {fixture!r}"
            )
        if method != "POST":
            raise ValueError(
                f"probe {probe_id} call {index}: body_fixture requires POST"
            )
    if method == "POST" and fixture is None and not call.get("replay_capture"):
        raise ValueError(
            f"probe {probe_id} call {index}: POST requires a known "
            "body_fixture or replay_capture"
        )
    if call.get("replay_capture") and (fixture is not None or method != "POST"):
        raise ValueError(
            f"probe {probe_id} call {index}: replay_capture needs a "
            "POST without an additional body_fixture"
        )
    if call.get("wait_terminal") and not call.get("capture_job"):
        raise ValueError(
            f"probe {probe_id} call {index}: wait_terminal requires capture_job"
        )
    if method != "POST" and (
            any(call.get(flag) for flag in LIVE_BOOLEAN_DIRECTIVES
                if flag.startswith("capture_"))
            or "concurrent_posts" in call):
        raise ValueError(
            f"probe {probe_id} call {index}: capture/concurrent directives need POST"
        )


# A misspelled live assertion must not be silently ignored by the probe runner.
# Keep this vocabulary synchronized with the registered conformance executor.
LIVE_BOOLEAN_ASSERTIONS = frozenset({
    "same_jobDbId", "rejected", "negotiable", "provenance_intact",
    "same_term", "same_ledger", "same_model", "same_matrix",
    "same_package", "unchanged_model_digest", "unchanged_matrix_digest",
    "telemetry_original_intact", "telemetry_window_partitions",
    "telemetry_page_slice", "telemetry_no_conflicts",
    "deprecated_inference_completed",
    "unchanged_package_license", "unchanged_term_record", "ledger_original_intact",
    "term_replay_single_version", "matrix_replay_single_record",
    "package_replay_single_record", "model_replay_single_version",
    "inference_intact", "single_effect",
    "concurrent_single_stored_job", "rejected_inference_not_stored",
    "revoked_model_persisted", "deprecated_model_persisted",
    "job_replay_single_stored", "capture_job_collection",
    "job_conflict_collection_unchanged", "terminal_state_unchanged",
    "unknown_job_type_not_stored", "expired_result_withheld",
    "embargo_denial_no_payload",
    "capability_registry_match",
})
LIVE_COUNT_ASSERTIONS = frozenset({
    "data_length", "total_count", "ledger_count", "telemetry_conflicts",
    "telemetry_samples",
})
LIVE_ASSERTIONS = (LIVE_BOOLEAN_ASSERTIONS | LIVE_COUNT_ASSERTIONS |
                   {"status", "status_message", "telemetry_counts",
                    "telemetry_mean", "body", "collection_contains_created"})


def validate_live_step_assertions(probe_id, index, call):
    """Validate assertions as executable evidence, not ignored metadata."""
    assertion = call.get("assert")
    if assertion is None and "assert" not in call:
        assertion = {}
    elif not isinstance(assertion, dict) or not assertion:
        raise ValueError(
            f"probe {probe_id} call {index}: assert must be a nonempty mapping"
        )
    unknown = set(assertion) - LIVE_ASSERTIONS
    if unknown:
        raise ValueError(
            f"probe {probe_id} call {index}: unknown live assertion(s): "
            + ", ".join(sorted(map(str, unknown)))
        )
    for name in LIVE_BOOLEAN_ASSERTIONS & assertion.keys():
        if assertion[name] is not True:
            raise ValueError(
                f"probe {probe_id} call {index}: {name} must be true"
            )
    for name in LIVE_COUNT_ASSERTIONS & assertion.keys():
        value = assertion[name]
        if type(value) is not int or value < 0:
            raise ValueError(
                f"probe {probe_id} call {index}: {name} must be a nonnegative integer"
            )
    if "status" in assertion:
        status = assertion["status"]
        if type(status) is not int or not (100 <= status <= 599):
            raise ValueError(
                f"probe {probe_id} call {index}: status must be an HTTP status integer"
            )
    if "status_message" in assertion:
        message = assertion["status_message"]
        if not isinstance(message, str) or not message.strip():
            raise ValueError(
                f"probe {probe_id} call {index}: status_message must be a string"
            )
    if "body" in assertion:
        body = assertion["body"]
        if (not isinstance(body, dict) or not body
                or any(not isinstance(key, str) or not key.strip()
                       for key in body)):
            raise ValueError(
                f"probe {probe_id} call {index}: body must be a nonempty path mapping"
            )
    if "collection_contains_created" in assertion:
        if assertion["collection_contains_created"] not in ("jobs", "models"):
            raise ValueError(
                f"probe {probe_id} call {index}: "
                "collection_contains_created must be jobs or models"
            )
    if "telemetry_counts" in assertion:
        counts = assertion["telemetry_counts"]
        if (not isinstance(counts, dict)
                or set(counts) != {"appended", "replayed"}
                or any(type(value) is not int or value < 0
                       for value in counts.values())):
            raise ValueError(
                f"probe {probe_id} call {index}: telemetry_counts needs "
                "nonnegative appended and replayed integers"
            )
    if "telemetry_mean" in assertion:
        mean = assertion["telemetry_mean"]
        if type(mean) not in (int, float) or not (-float("inf") < mean < float("inf")):
            raise ValueError(
                f"probe {probe_id} call {index}: telemetry_mean must be finite"
            )
    if ("telemetry_mean" in assertion) != ("telemetry_samples" in assertion):
        raise ValueError(
            f"probe {probe_id} call {index}: telemetry_mean and "
            "telemetry_samples must be paired"
        )
    if "model_replay_single_version" in assertion and (
            call.get("method") != "GET"
            or call.get("path") != "/models?modelDbId={modelDbId}"):
        raise ValueError(
            f"probe {probe_id} call {index}: "
            "model_replay_single_version requires filtered model collection GET"
        )
    if "package_replay_single_record" in assertion and (
            call.get("method") != "GET"
            or call.get("path") != "/fair-packages"):
        raise ValueError(
            f"probe {probe_id} call {index}: "
            "package_replay_single_record requires GET /fair-packages"
        )
    if "matrix_replay_single_record" in assertion and (
            call.get("method") != "GET"
            or call.get("path") != "/variantmatrices"):
        raise ValueError(
            f"probe {probe_id} call {index}: "
            "matrix_replay_single_record requires GET /variantmatrices"
        )
    if "term_replay_single_version" in assertion and (
            call.get("method") != "GET"
            or call.get("path") != "/variable-terms?variableDbId={variableDbId}"):
        raise ValueError(
            f"probe {probe_id} call {index}: "
            "term_replay_single_version requires filtered term collection GET"
        )
    if "ledger_original_intact" in assertion and (
            call.get("method") != "GET"
            or call.get("path") != "/seedlots/{lotDbId}/ledger"):
        raise ValueError(
            f"probe {probe_id} call {index}: "
            "ledger_original_intact requires GET on captured seed lot"
        )
    if "unchanged_term_record" in assertion and (
            call.get("method") != "GET"
            or call.get("path") != "/variable-terms/{variableDbId}?version={termVersion}"):
        raise ValueError(
            f"probe {probe_id} call {index}: "
            "unchanged_term_record requires versioned term GET"
        )
    if "embargo_denial_no_payload" in assertion and (
            call.get("method") != "GET"
            or call.get("path") != "/fair-packages/{packageDbId}"):
        raise ValueError(
            f"probe {probe_id} call {index}: "
            "embargo_denial_no_payload requires embargoed package GET"
        )
    if "expired_result_withheld" in assertion and (
            call.get("method") != "GET"
            or call.get("path") != "/jobs/{expiredJobDbId}"):
        raise ValueError(
            f"probe {probe_id} call {index}: "
            "expired_result_withheld requires known-expired job GET"
        )
    if "unknown_job_type_not_stored" in assertion and (
            call.get("method") != "GET"
            or call.get("path") != "/jobs"):
        raise ValueError(
            f"probe {probe_id} call {index}: "
            "unknown_job_type_not_stored requires GET /jobs"
        )
    if "terminal_state_unchanged" in assertion and (
            call.get("method") != "GET"
            or call.get("path") != "/jobs/{jobDbId}"):
        raise ValueError(
            f"probe {probe_id} call {index}: "
            "terminal_state_unchanged requires captured job GET"
        )
    if ("capture_job_collection" in assertion
            or "job_conflict_collection_unchanged" in assertion) and (
            call.get("method") != "GET" or call.get("path") != "/jobs"):
        raise ValueError(
            f"probe {probe_id} call {index}: "
            "job conflict collection assertions require GET /jobs"
        )
    if "job_replay_single_stored" in assertion and (
            call.get("method") != "GET" or call.get("path") != "/jobs"):
        raise ValueError(
            f"probe {probe_id} call {index}: "
            "job_replay_single_stored requires GET /jobs"
        )
    if "rejected_inference_not_stored" in assertion and (
            call.get("method") != "GET" or call.get("path") != "/jobs"):
        raise ValueError(
            f"probe {probe_id} call {index}: "
            "rejected_inference_not_stored requires GET /jobs"
        )
    if "concurrent_single_stored_job" in assertion and (
            call.get("method") != "GET" or call.get("path") != "/jobs"):
        raise ValueError(
            f"probe {probe_id} call {index}: "
            "concurrent_single_stored_job requires GET /jobs"
        )
    if bool(call.get("replay_capture")) != ("same_jobDbId" in assertion):
        raise ValueError(
            f"probe {probe_id} call {index}: replay_capture requires "
            "same_jobDbId assertion and vice versa"
        )
    if "concurrent_posts" in call:
        count = call["concurrent_posts"]
        if type(count) is not int or count < 2:
            raise ValueError(
                f"probe {probe_id} call {index}: concurrent_posts must be >= 2"
            )
    if ("concurrent_posts" in call) != ("single_effect" in assertion):
        raise ValueError(
            f"probe {probe_id} call {index}: concurrent_posts requires "
            "single_effect assertion and vice versa"
        )


def validate_probe_manifest(probes):
    """Reject silently dropped, duplicated or unexecutable registered probes."""
    if not isinstance(probes, list):
        raise ValueError("conformance probe registry is not an array")
    observed = set()
    for position, probe in enumerate(probes):
        if not isinstance(probe, dict):
            raise ValueError(f"probe {position}: expected mapping")
        probe_id = probe.get("id")
        if not isinstance(probe_id, str) or not re.fullmatch(r"[SL]-[0-9]{2,}", probe_id):
            raise ValueError(f"probe {position}: invalid identifier {probe_id!r}")
        if probe_id in observed:
            raise ValueError(f"duplicate registered probe identifier: {probe_id}")
        observed.add(probe_id)
        tier = probe.get("tier")
        if tier not in ("static", "live"):
            raise ValueError(f"probe {probe_id}: unrecognized tier {tier!r}")
        if (probe_id.startswith("S-") and tier != "static"
                or probe_id.startswith("L-") and tier != "live"):
            raise ValueError(f"probe {probe_id}: identifier and tier disagree")
        if tier == "static" and probe.get("check") not in STATIC:
            raise ValueError(f"probe {probe_id}: unknown static check {probe.get('check')!r}")
        if tier == "live":
            calls = probe.get("calls")
            if not isinstance(calls, list) or not calls:
                raise ValueError(f"probe {probe_id}: missing executable live calls")
            for index, call in enumerate(calls):
                if (not isinstance(call, dict)
                        or call.get("method") not in HTTP_METHODS
                        or not isinstance(call.get("path"), str)
                        or not call["path"].startswith("/")):
                    raise ValueError(f"probe {probe_id}: invalid live call {index}")
                validate_live_step_directives(probe_id, index, call)
                validate_live_step_assertions(probe_id, index, call)
            if probe_id == "L-21":
                if (len(calls) != 3
                        or calls[0].get("method") != "POST"
                        or calls[0].get("path") != "/telemetry"
                        or calls[0].get("body_fixture") != "live_telemetry_batch"
                        or calls[0].get("capture_telemetry") is not True
                        or calls[0].get("assert", {}).get("telemetry_counts") != {
                            "appended": 3, "replayed": 0}
                        or calls[0].get("assert", {}).get("telemetry_no_conflicts")
                            is not True
                        or calls[1].get("method") != "POST"
                        or calls[1].get("path") != "/telemetry"
                        or calls[1].get("body_fixture") != "live_telemetry_batch"
                        or calls[1].get("assert", {}).get("telemetry_counts") != {
                            "appended": 0, "replayed": 3}
                        or calls[1].get("assert", {}).get("telemetry_no_conflicts")
                            is not True):
                    raise ValueError(
                        "probe L-21: clean append and replay conflict arrays required"
                    )
            if probe_id == "L-22":
                if (len(calls) != 3
                        or calls[0].get("method") != "POST"
                        or calls[0].get("path") != "/telemetry"
                        or calls[0].get("body_fixture") != "live_telemetry_batch"
                        or calls[0].get("capture_telemetry") is not True
                        or calls[0].get("assert") != {
                            "telemetry_counts": {"appended": 3, "replayed": 0},
                            "telemetry_no_conflicts": True,
                        }
                        or calls[1].get("method") != "POST"
                        or calls[1].get("path") != "/telemetry"
                        or calls[1].get("body_fixture") != "live_telemetry_conflict"
                        or calls[1].get("assert", {}).get("telemetry_conflicts") != 1
                        or calls[1].get("assert", {}).get("telemetry_counts") != {
                            "appended": 0, "replayed": 0}
                        or calls[2].get("method") != "GET"
                        or calls[2].get("path") !=
                            "/telemetry?deviceDbId={telemetry_device}&sensorDbId=air-temp-01&aggregation=none"
                        or calls[2].get("assert", {}).get("telemetry_original_intact")
                            is not True):
                    raise ValueError(
                        "probe L-22: rejected telemetry natural key and retained source required"
                    )
            if probe_id == "L-23":
                if (len(calls) != 3
                        or calls[0].get("method") != "POST"
                        or calls[0].get("path") != "/telemetry"
                        or calls[0].get("body_fixture") != "live_telemetry_batch"
                        or calls[0].get("capture_telemetry") is not True
                        or calls[0].get("assert") != {
                            "telemetry_counts": {"appended": 3, "replayed": 0},
                            "telemetry_no_conflicts": True,
                        }
                        or calls[1].get("method") != "GET"
                        or calls[1].get("path") !=
                            "/telemetry?deviceDbId={telemetry_device}&sensorDbId=air-temp-01&from=2026-09-07T08:00:00Z&to=2026-09-07T08:03:00Z&aggregation=none"
                        or calls[1].get("assert", {}).get("telemetry_original_intact")
                            is not True
                        or calls[2].get("method") != "GET"
                        or calls[2].get("path") !=
                            "/telemetry?deviceDbId={telemetry_device}&sensorDbId=air-temp-01&from=2026-09-07T08:00:00Z&to=2026-09-07T08:03:00Z&aggregation=mean"
                        or calls[2].get("assert", {}).get("telemetry_mean") != 21.7
                        or calls[2].get("assert", {}).get("telemetry_samples") != 3):
                    raise ValueError(
                        "probe L-23: source telemetry GET and mean recomputation required"
                    )
            if probe_id == "L-14":
                if (len(calls) != 3
                        or calls[0].get("method") != "POST"
                        or calls[0].get("path") != "/models"
                        or calls[0].get("body_fixture") != "live_model_submit"
                        or calls[0].get("capture_model") is not True
                        or calls[1].get("method") != "POST"
                        or calls[1].get("path") != "/jobs"
                        or calls[1].get("body_fixture") != "live_inference_submit"
                        or calls[1].get("capture_job") is not True
                        or calls[1].get("wait_terminal") is not True
                        or calls[2].get("method") != "GET"
                        or calls[2].get("path") != "/jobs/{jobDbId}"
                        or calls[2].get("assert", {}).get("inference_intact")
                            is not True):
                    raise ValueError(
                        "probe L-14: bound inference result and completion GET required"
                    )
            if probe_id == "L-27":
                if (len(calls) != 3
                        or calls[0].get("method") != "POST"
                        or calls[0].get("path") != "/models"
                        or calls[0].get("body_fixture") != "live_model_deprecated"
                        or calls[0].get("capture_model_deprecated") is not True
                        or calls[2].get("method") != "POST"
                        or calls[2].get("path") != "/jobs"
                        or calls[2].get("body_fixture") != "live_inference_deprecated"
                        or calls[2].get("assert", {}).get("status") != 202
                        or calls[2].get("assert", {}).get("status_message") != "WARNING"
                        or calls[2].get("assert", {}).get("deprecated_inference_completed")
                            is not True):
                    raise ValueError(
                        "probe L-27: bound deprecated inference completion and warning required"
                    )
                if (calls[1].get("method") != "GET"
                        or calls[1].get("path") !=
                            "/models/{deprecatedModelDbId}?version={deprecatedModelVersion}"
                        or calls[1].get("assert", {}).get("status") != 200
                        or calls[1].get("assert", {}).get("deprecated_model_persisted")
                            is not True):
                    raise ValueError(
                        "probe L-27: deprecated_model_persisted GET before inference required"
                    )
            if probe_id == "L-07":
                if (len(calls) != 2
                        or calls[0].get("method") != "POST"
                        or calls[0].get("path") != "/jobs"
                        or calls[0].get("body_fixture") != "live_provenanced_submit"
                        or calls[0].get("capture_job") is not True
                        or calls[0].get("wait_terminal") is not True
                        or calls[1].get("method") != "GET"
                        or calls[1].get("path") != "/jobs/{jobDbId}"
                        or calls[1].get("assert", {}).get("provenance_intact") is not True):
                    raise ValueError(
                        "probe L-07: original observation and provenance round-trip required"
                    )
            if probe_id == "L-25":
                if (len(calls) != 4
                        or calls[0].get("method") != "POST"
                        or calls[0].get("path") != "/jobs"
                        or calls[0].get("body_fixture") != "live_submit"
                        or calls[0].get("capture_job") is not True
                        or calls[1].get("method") != "POST"
                        or calls[1].get("path") != "/models"
                        or calls[1].get("body_fixture") != "live_model_submit"
                        or calls[1].get("capture_model") is not True
                        or calls[2].get("method") != "GET"
                        or calls[2].get("path") != "/jobs"
                        or calls[2].get("assert", {}).get(
                            "collection_contains_created") != "jobs"
                        or calls[3].get("method") != "GET"
                        or calls[3].get("path") != "/models"
                        or calls[3].get("assert", {}).get(
                            "collection_contains_created") != "models"):
                    raise ValueError(
                        "probe L-25: paged job and model collection evidence required"
                    )
            if probe_id == "L-20":
                if (len(calls) != 2
                        or calls[0].get("method") != "POST"
                        or calls[0].get("path") != "/fair-packages"
                        or calls[0].get("body_fixture") != "live_package_embargoed"
                        or calls[0].get("capture_package") is not True
                        or calls[1].get("method") != "GET"
                        or calls[1].get("path") != "/fair-packages/{packageDbId}"
                        or calls[1].get("assert", {}).get("status") != 403
                        or calls[1].get("assert", {}).get("embargo_denial_no_payload")
                            is not True):
                    raise ValueError(
                        "probe L-20: embargo_denial_no_payload on rejected package GET required"
                    )
            if probe_id == "L-05":
                if (len(calls) != 1
                        or calls[0].get("method") != "GET"
                        or calls[0].get("path") != "/jobs/{expiredJobDbId}"
                        or calls[0].get("assert", {}).get("expired_result_withheld")
                            is not True
                        or calls[0].get("assert", {}).get("body", {}).get(
                            "result.status") != "EXPIRED"):
                    raise ValueError(
                        "probe L-05: expired_result_withheld on known-expired job required"
                    )
            if probe_id == "L-04":
                if (len(calls) != 2
                        or calls[0].get("method") != "POST"
                        or calls[0].get("path") != "/jobs"
                        or calls[0].get("body_fixture") != "live_submit_unknown_type"
                        or calls[0].get("assert", {}).get("status") != 400
                        or calls[1].get("method") != "GET"
                        or calls[1].get("path") != "/jobs"
                        or calls[1].get("assert", {}).get("unknown_job_type_not_stored")
                            is not True):
                    raise ValueError(
                        "probe L-04: unknown_job_type_not_stored GET after rejection required"
                    )
            if probe_id == "L-03":
                if (len(calls) != 3
                        or calls[0].get("method") != "POST"
                        or calls[0].get("path") != "/jobs"
                        or calls[0].get("body_fixture") != "live_submit"
                        or calls[0].get("capture_job") is not True
                        or calls[0].get("wait_terminal") is not True
                        or calls[1].get("method") != "DELETE"
                        or calls[1].get("path") != "/jobs/{jobDbId}"
                        or calls[1].get("assert", {}).get("rejected") is not True
                        or calls[2].get("method") != "GET"
                        or calls[2].get("path") != "/jobs/{jobDbId}"
                        or calls[2].get("assert", {}).get("terminal_state_unchanged")
                            is not True):
                    raise ValueError(
                        "probe L-03: terminal_state_unchanged GET after rejected cancellation required"
                    )
            if probe_id == "L-02":
                if (len(calls) != 4
                        or calls[0].get("method") != "POST"
                        or calls[0].get("path") != "/jobs"
                        or calls[0].get("body_fixture") != "live_submit"
                        or calls[0].get("capture_job") is not True
                        or calls[1].get("method") != "GET"
                        or calls[1].get("path") != "/jobs"
                        or calls[1].get("assert", {}).get("capture_job_collection")
                            is not True
                        or calls[2].get("method") != "POST"
                        or calls[2].get("path") != "/jobs"
                        or calls[2].get("body_fixture") != "live_submit_conflict"
                        or calls[2].get("assert", {}).get("rejected") is not True
                        or calls[3].get("method") != "GET"
                        or calls[3].get("path") != "/jobs"
                        or calls[3].get("assert", {}).get("job_conflict_collection_unchanged")
                            is not True):
                    raise ValueError(
                        "probe L-02: complete job collection before and after conflict required"
                    )
            if probe_id == "L-01":
                if (len(calls) != 3
                        or calls[0].get("method") != "POST"
                        or calls[0].get("path") != "/jobs"
                        or calls[0].get("body_fixture") != "live_submit"
                        or calls[0].get("capture_job") is not True
                        or calls[1].get("method") != "POST"
                        or calls[1].get("path") != "/jobs"
                        or calls[1].get("replay_capture") is not True
                        or calls[1].get("assert", {}).get("same_jobDbId") is not True
                        or calls[2].get("method") != "GET"
                        or calls[2].get("path") != "/jobs"
                        or calls[2].get("assert", {}).get("job_replay_single_stored")
                            is not True):
                    raise ValueError(
                        "probe L-01: job_replay_single_stored GET after replay required"
                    )
            if probe_id == "L-15":
                if (len(calls) != 5
                        or calls[0].get("method") != "POST"
                        or calls[0].get("path") != "/jobs"
                        or calls[0].get("body_fixture") != "live_inference_unknown"
                        or calls[0].get("assert", {}).get("status") != 400
                        or calls[1].get("method") != "POST"
                        or calls[1].get("path") != "/models"
                        or calls[1].get("body_fixture") != "live_model_revoked"
                        or calls[1].get("capture_model_revoked") is not True
                        or calls[3].get("method") != "POST"
                        or calls[3].get("path") != "/jobs"
                        or calls[3].get("body_fixture") != "live_inference_revoked"
                        or calls[3].get("assert", {}).get("status") != 400
                        or calls[4].get("method") != "GET"
                        or calls[4].get("path") != "/jobs"
                        or calls[4].get("assert", {}).get("rejected_inference_not_stored")
                            is not True):
                    raise ValueError(
                        "probe L-15: rejected_inference_not_stored GET after both rejections required"
                    )
                if (calls[2].get("method") != "GET"
                        or calls[2].get("path") !=
                            "/models/{revokedModelDbId}?version={revokedModelVersion}"
                        or calls[2].get("assert", {}).get("status") != 200
                        or calls[2].get("assert", {}).get("revoked_model_persisted")
                            is not True):
                    raise ValueError(
                        "probe L-15: revoked_model_persisted GET before rejected inference required"
                    )
            if probe_id == "L-13":
                if (len(calls) != 3
                        or calls[0].get("method") != "POST"
                        or calls[0].get("path") != "/models"
                        or calls[0].get("body_fixture") != "live_model_submit"
                        or calls[0].get("capture_model") is not True
                        or calls[1].get("method") != "POST"
                        or calls[1].get("path") != "/models"
                        or calls[1].get("body_fixture") != "live_model_conflict"
                        or calls[1].get("assert", {}).get("status") != 409
                        or calls[2].get("method") != "GET"
                        or calls[2].get("path")
                            != "/models/{modelDbId}?version={modelVersion}"
                        or calls[2].get("assert", {}).get("unchanged_model_digest")
                            is not True):
                    raise ValueError(
                        "probe L-13: full model original readback after conflict required"
                    )
            if probe_id == "L-19":
                if (len(calls) != 3
                        or calls[0].get("body_fixture") != "live_package_submit"
                        or calls[0].get("capture_package") is not True
                        or calls[1].get("body_fixture") != "live_package_conflict"
                        or calls[1].get("assert", {}).get("status") != 409
                        or calls[2].get("method") != "GET"
                        or calls[2].get("path") != "/fair-packages/{packageDbId}"
                        or calls[2].get("assert", {}).get("unchanged_package_license")
                            is not True):
                    raise ValueError(
                        "probe L-19: full package original readback after conflict required"
                    )
            if probe_id == "L-17":
                if (len(calls) != 3
                        or calls[0].get("body_fixture") != "live_matrix_submit"
                        or calls[0].get("capture_matrix") is not True
                        or calls[1].get("body_fixture") != "live_matrix_conflict"
                        or calls[1].get("assert", {}).get("status") != 409
                        or calls[2].get("method") != "GET"
                        or calls[2].get("path") != "/variantmatrices/{matrixDbId}"
                        or calls[2].get("assert", {}).get("unchanged_matrix_digest")
                            is not True):
                    raise ValueError(
                        "probe L-17: full matrix original readback after conflict required"
                    )
            if probe_id == "L-12":
                if (len(calls) != 3
                        or calls[0].get("body_fixture") != "live_model_submit"
                        or calls[0].get("capture_model") is not True
                        or calls[1].get("body_fixture") != "live_model_submit"
                        or calls[1].get("assert", {}).get("status") != 200
                        or calls[1].get("assert", {}).get("same_model") is not True
                        or calls[2].get("method") != "GET"
                        or calls[2].get("path") != "/models?modelDbId={modelDbId}"
                        or calls[2].get("assert", {}).get("model_replay_single_version")
                            is not True):
                    raise ValueError(
                        "probe L-12: model_replay_single_version GET after replay required"
                    )
            if probe_id == "L-18":
                if (len(calls) != 3
                        or calls[0].get("body_fixture") != "live_package_submit"
                        or calls[0].get("capture_package") is not True
                        or calls[1].get("body_fixture") != "live_package_submit"
                        or calls[1].get("assert", {}).get("status") != 200
                        or calls[1].get("assert", {}).get("same_package") is not True
                        or calls[2].get("method") != "GET"
                        or calls[2].get("path") != "/fair-packages"
                        or calls[2].get("assert", {}).get("package_replay_single_record")
                            is not True):
                    raise ValueError(
                        "probe L-18: package_replay_single_record GET after replay required"
                    )
            if probe_id == "L-16":
                if (len(calls) != 3
                        or calls[0].get("body_fixture") != "live_matrix_submit"
                        or calls[0].get("capture_matrix") is not True
                        or calls[1].get("body_fixture") != "live_matrix_submit"
                        or calls[1].get("assert", {}).get("status") != 200
                        or calls[1].get("assert", {}).get("same_matrix") is not True
                        or calls[2].get("method") != "GET"
                        or calls[2].get("path") != "/variantmatrices"
                        or calls[2].get("assert", {}).get("matrix_replay_single_record")
                            is not True):
                    raise ValueError(
                        "probe L-16: matrix_replay_single_record GET after replay required"
                    )
            if probe_id == "L-08":
                if (len(calls) != 3
                        or calls[0].get("body_fixture") != "live_term_submit"
                        or calls[0].get("capture_term") is not True
                        or calls[1].get("body_fixture") != "live_term_submit"
                        or calls[1].get("assert", {}).get("status") != 200
                        or calls[1].get("assert", {}).get("same_term") is not True
                        or calls[2].get("method") != "GET"
                        or calls[2].get("path")
                            != "/variable-terms?variableDbId={variableDbId}"
                        or calls[2].get("assert", {}).get("term_replay_single_version")
                            is not True):
                    raise ValueError(
                        "probe L-08: term_replay_single_version GET after replay required"
                    )
            if probe_id == "L-10":
                if (len(calls) != 3
                        or calls[0].get("body_fixture") != "live_ledger_submit"
                        or calls[0].get("capture_ledger") is not True
                        or calls[1].get("body_fixture") != "live_ledger_submit"
                        or calls[1].get("assert", {}).get("status") != 200
                        or calls[1].get("assert", {}).get("same_ledger") is not True
                        or calls[2].get("method") != "GET"
                        or calls[2].get("path") != "/seedlots/{lotDbId}/ledger"
                        or calls[2].get("assert", {}).get("ledger_original_intact")
                            is not True):
                    raise ValueError(
                        "probe L-10: ledger_original_intact GET after replay required"
                    )
            if probe_id == "L-11":
                if (len(calls) != 3
                        or calls[0].get("body_fixture") != "live_ledger_submit"
                        or calls[0].get("capture_ledger") is not True
                        or calls[1].get("body_fixture") != "live_ledger_conflict"
                        or calls[2].get("method") != "GET"
                        or calls[2].get("path") != "/seedlots/{lotDbId}/ledger"
                        or calls[2].get("assert", {}).get("ledger_original_intact")
                            is not True):
                    raise ValueError(
                        "probe L-11: ledger_original_intact GET after conflict required"
                    )
            if probe_id == "L-09":
                if (len(calls) != 3
                        or calls[0].get("body_fixture") != "live_term_submit"
                        or calls[0].get("capture_term") is not True
                        or calls[1].get("body_fixture") != "live_term_conflict"
                        or calls[2].get("method") != "GET"
                        or calls[2].get("path")
                            != "/variable-terms/{variableDbId}?version={termVersion}"
                        or calls[2].get("assert", {}).get("unchanged_term_record")
                            is not True):
                    raise ValueError(
                        "probe L-09: unchanged_term_record GET after conflict required"
                    )
            if probe_id == "L-24":
                if not any(
                        call.get("concurrent_posts") == 8
                        and isinstance(call.get("assert"), dict)
                        and call["assert"].get("single_effect") is True
                        for call in calls):
                    raise ValueError(
                        "probe L-24: eight concurrent submissions required")
                if not any(
                        call.get("method") == "GET"
                        and call.get("path") == "/jobs"
                        and isinstance(call.get("assert"), dict)
                        and call["assert"].get("concurrent_single_stored_job") is True
                        for call in calls):
                    raise ValueError(
                        "probe L-24: concurrent_single_stored_job GET assertion required")
            if probe_id == "L-21" and not any(
                    call.get("method") == "GET"
                    and isinstance(call.get("assert"), dict)
                    and call["assert"].get("telemetry_original_intact") is True
                    for call in calls):
                raise ValueError(
                    "probe L-21: telemetry_original_intact GET assertion required"
                )
            if probe_id == "L-28":
                expected_pages = (
                    "/telemetry?deviceDbId={telemetry_device}&page=0&pageSize=2",
                    "/telemetry?deviceDbId={telemetry_device}&page=1&pageSize=2",
                )
                if (len(calls) != 3
                        or calls[0].get("method") != "POST"
                        or calls[0].get("path") != "/telemetry"
                        or calls[0].get("body_fixture") != "live_telemetry_batch"
                        or calls[0].get("capture_telemetry") is not True
                        or calls[0].get("assert") != {
                            "telemetry_counts": {"appended": 3, "replayed": 0},
                            "telemetry_no_conflicts": True,
                        }
                        or any(
                            calls[idx].get("method") != "GET"
                            or calls[idx].get("path") != expected_pages[idx - 1]
                            or calls[idx].get("assert") != {
                                "data_length": 2 if idx == 1 else 1,
                                "total_count": 3,
                                "telemetry_page_slice": True,
                            }
                            for idx in (1, 2)
                        )):
                    raise ValueError(
                        "probe L-28: two-page telemetry slice and source integrity required"
                    )
            if probe_id == "L-26":
                if (len(calls) != 3
                        or calls[0].get("method") != "POST"
                        or calls[0].get("path") != "/telemetry"
                        or calls[0].get("body_fixture") != "live_telemetry_batch"
                        or calls[0].get("capture_telemetry") is not True
                        or calls[0].get("assert") != {
                            "telemetry_counts": {"appended": 3, "replayed": 0},
                            "telemetry_no_conflicts": True,
                        }
                        or calls[1].get("method") != "GET"
                        or calls[1].get("path") !=
                            "/telemetry?deviceDbId={telemetry_device}&sensorDbId=air-temp-01&aggregation=none"
                        or calls[1].get("assert") != {
                            "status": 200, "telemetry_original_intact": True}
                        or calls[2].get("method") != "GET"
                        or calls[2].get("path") !=
                            "/telemetry?deviceDbId={telemetry_device}&sensorDbId=air-temp-01&aggregation=mean&windowSeconds=60"
                        or calls[2].get("assert") != {
                            "data_length": 3, "telemetry_window_partitions": True}):
                    raise ValueError(
                        "probe L-26: original telemetry source before window aggregation required"
                    )
            if probe_id == "L-26" and not any(
                    call.get("method") == "GET"
                    and isinstance(call.get("assert"), dict)
                    and call["assert"].get("telemetry_window_partitions") is True
                    for call in calls):
                raise ValueError(
                    "probe L-26: telemetry_window_partitions GET assertion required"
                )
    missing = sorted(REQUIRED_REGISTERED_PROBES - observed)
    if missing:
        raise ValueError(
            "missing baseline conformance probes: " + ", ".join(missing)
        )


def select_probes(probes, only=None, server=None):
    """Fail closed for explicit single-probe execution.

    An unfiltered static run retains its established SKIP semantics for live
    probes when no server is supplied.
    """
    if only is None:
        return probes
    matches = [probe for probe in probes if probe.get("id") == only]
    if len(matches) != 1:
        raise ValueError(
            f"--only {only!r}: expected exactly one registered probe, found {len(matches)}"
        )
    tier = matches[0].get("tier")
    if tier not in ("static", "live"):
        raise ValueError(f"--only {only!r}: invalid probe tier {tier!r}")
    if tier == "live" and not server:
        raise ValueError(f"--only {only!r}: live probe requires --server")
    return matches


def selected_probe_exit_code(failures, skips, explicit_selection):
    """An explicit single-probe SKIP must fail even if no assertion failed."""
    return 1 if failures or (explicit_selection and skips) else 0


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
    try:
        validate_probe_manifest(spec.get("probes"))
        selected = select_probes(spec["probes"], args.only, args.server)
    except ValueError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    ctx = {
        "required_map": spec.get("required_map", {}),
        "genx_object_names": spec.get("genx_object_names", []),
        "capability_dirs": spec.get("capability_dirs", {}),
        "capability_registry_path": os.path.join(conf, spec.get("capability_registry", "capability-registry.json")),
        "conformance_dir": conf,
        "root": root,
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
    for probe in selected:
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
    # Explicitly requested probes must actually execute; a SKIP is not a pass.
    # Unfiltered static-only runs retain their established live-SKIP behavior.
    return selected_probe_exit_code(results.failures, results.skips, args.only is not None)


if __name__ == "__main__":
    sys.exit(main())
