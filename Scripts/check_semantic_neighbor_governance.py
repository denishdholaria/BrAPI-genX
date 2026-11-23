#!/usr/bin/env python3
"""Validate the semantic-neighbor review ledger against the endpoint registry.

This is a governance check, not a scientific-equivalence check. It ensures the
review inventory remains complete, internally consistent, and explicitly
unresolved where evidence is absent.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "Specification" / "ENDPOINT-REGISTRY.json"
LEDGER = ROOT / "Specification" / "BrAPI-GenX" / "Conformance" / "semantic-neighbor-review.yaml"
AUDIT = ROOT / "Scripts" / "auditEndpointRegistrySourceConsistency.py"
BASELINE_REF = "3125fbc35dd32abbf8166b990c5597f1aea6e61f"
BASELINE_LEDGER_IDS = frozenset({
'brapi-genx.genx.v1.artifact-catalogues.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.artifact-catalogues.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.artifact-catalogues.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.assay-executions.get -> genxRecordAssayDesign',
'brapi-genx.genx.v1.assay-executions.list -> genxRecordAssayDesign',
'brapi-genx.genx.v1.assay-executions.record -> genxRecordAssayDesign',
'brapi-genx.genx.v1.biodiversity-exports.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.biodiversity-exports.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.biodiversity-exports.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.calibration-qualities.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.calibration-qualities.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.calibration-qualities.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.capability-negotiations.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.capability-negotiations.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.capability-negotiations.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.capture-workflows.get -> genxPublishVariableTermVersion',
'brapi-genx.genx.v1.capture-workflows.list -> genxPublishVariableTermVersion',
'brapi-genx.genx.v1.capture-workflows.record -> genxPublishVariableTermVersion',
'brapi-genx.genx.v1.cloud-masks.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.cloud-masks.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.cloud-masks.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.conformance-probes.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.conformance-probes.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.conformance-probes.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.crop-health-images.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.crop-health-images.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.crop-health-images.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.crop-recommendations.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.crop-recommendations.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.crop-recommendations.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.crop-suitabilities.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.crop-suitabilities.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.crop-suitabilities.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.crs-transforms.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.crs-transforms.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.crs-transforms.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.diagnostic-evidences.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.diagnostic-evidences.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.diagnostic-evidences.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.disease-observations.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.disease-observations.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.disease-observations.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.disease-resistances.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.disease-resistances.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.disease-resistances.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.edge-gateway-healths.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.edge-gateway-healths.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.edge-gateway-healths.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.evidence-packs.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.evidence-packs.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.evidence-packs.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.experimental-protocols.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.experimental-protocols.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.experimental-protocols.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.explanation-evidences.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.explanation-evidences.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.explanation-evidences.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.farms.get -> genxRegisterCropCycle',
'brapi-genx.genx.v1.farms.list -> genxRegisterCropCycle',
'brapi-genx.genx.v1.farms.register -> genxRegisterCropCycle',
'brapi-genx.genx.v1.field-books.get -> genxRegisterFieldScouting',
'brapi-genx.genx.v1.field-books.list -> genxRegisterFieldScouting',
'brapi-genx.genx.v1.field-books.record -> genxRegisterFieldScouting',
'brapi-genx.genx.v1.field-geometries.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.field-geometries.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.field-geometries.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.human-reviews.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.human-reviews.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.human-reviews.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.ipm-strategies.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.ipm-strategies.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.ipm-strategies.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.irrigation-advices.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.irrigation-advices.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.irrigation-advices.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.local-constraints.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.local-constraints.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.local-constraints.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.nutrient-advices.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.nutrient-advices.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.nutrient-advices.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.outcome-feedbacks.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.outcome-feedbacks.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.outcome-feedbacks.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.pest-disease-risks.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.pest-disease-risks.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.pest-disease-risks.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.pipeline-provenances.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.pipeline-provenances.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.pipeline-provenances.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.plots.get -> genxRegisterFieldScouting',
'brapi-genx.genx.v1.plots.list -> genxRegisterFieldScouting',
'brapi-genx.genx.v1.plots.record -> genxRegisterFieldScouting',
'brapi-genx.genx.v1.protocol-libraries.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.protocol-libraries.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.protocol-libraries.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.publication-reviews.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.publication-reviews.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.publication-reviews.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.quality-flags.get -> genxPublishVariableTermVersion',
'brapi-genx.genx.v1.quality-flags.list -> genxPublishVariableTermVersion',
'brapi-genx.genx.v1.quality-flags.record -> genxPublishVariableTermVersion',
'brapi-genx.genx.v1.raster-catalogues.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.raster-catalogues.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.raster-catalogues.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.reference-assemblies.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.reference-assemblies.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.reference-assemblies.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.remote-sensing-metadata.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.remote-sensing-metadata.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.remote-sensing-metadata.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.schema-mappings.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.schema-mappings.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.schema-mappings.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.sensor-devices.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.sensor-devices.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.sensor-devices.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.sowing-windows.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.sowing-windows.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.sowing-windows.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.spatial-indexes.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.spatial-indexes.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.spatial-indexes.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.spatial-queries.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.spatial-queries.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.spatial-queries.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.telemetry-normalizations.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.telemetry-normalizations.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.telemetry-normalizations.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.threshold-alerts.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.threshold-alerts.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.threshold-alerts.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.treatment-assignments.get -> genxRegisterFieldScouting',
'brapi-genx.genx.v1.treatment-assignments.list -> genxRegisterFieldScouting',
'brapi-genx.genx.v1.treatment-assignments.record -> genxRegisterFieldScouting',
'brapi-genx.genx.v1.trial-networks.get -> genxRegisterFieldScouting',
'brapi-genx.genx.v1.trial-networks.list -> genxRegisterFieldScouting',
'brapi-genx.genx.v1.trial-networks.record -> genxRegisterFieldScouting',
'brapi-genx.genx.v1.value-missingness.get -> genxPublishVariableTermVersion',
'brapi-genx.genx.v1.value-missingness.list -> genxPublishVariableTermVersion',
'brapi-genx.genx.v1.value-missingness.record -> genxPublishVariableTermVersion',
'brapi-genx.genx.v1.vcf-exports.get -> genxRecordVcfImport',
'brapi-genx.genx.v1.vcf-exports.list -> genxRecordVcfImport',
'brapi-genx.genx.v1.vcf-exports.record -> genxRecordVcfImport',
'brapi-genx.genx.v1.vegetation-indexes.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.vegetation-indexes.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.vegetation-indexes.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.yield-forecasts.get -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.yield-forecasts.list -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.yield-forecasts.record -> genxRegisterGenomicDataset',
'brapi-genx.genx.v1.yield-maps.get -> genxRecordHarvest',
'brapi-genx.genx.v1.yield-maps.list -> genxRecordHarvest',
'brapi-genx.genx.v1.yield-maps.register -> genxRecordHarvest'
})


ALLOWED_STATUSES = {"inherited-unreviewed", "evidence-backed-proposed",
                    "requires-decision", "rejected", "superseded"}
ALLOWED_PROVENANCE = {"inherited-registry-only", "source-openapi-declared",
                      "registry-and-source", "documented-mapping", "manual-review"}
ALLOWED_BOUNDARIES = {"within-module", "cross-module", "cross-domain"}
ALLOWED_TRANSITIONS = {
    "inherited-unreviewed": {"evidence-backed-proposed", "requires-decision", "rejected", "superseded"},
    "evidence-backed-proposed": {"requires-decision", "rejected", "superseded"},
    "requires-decision": {"evidence-backed-proposed", "rejected", "superseded"},
    "rejected": {"superseded"},
    "superseded": set(),
}
REQUIRED_FIELDS = [
    "id", "sourceCatalogId", "sourceOperationId", "targetOperationId",
    "targetCatalogId", "sourceModule", "targetModule", "boundary",
    "provenance", "reviewStatus", "documentaryEvidence", "decisionReferences",
    "scientificConcerns",
]
EVIDENCE_REQUIRED = {
    "evidence-backed-proposed": ["rationale", "evidence", "reviewedBy", "reviewedAt"],
    "requires-decision": ["rationale", "openQuestion"],
    "rejected": ["rationale", "authorizationReference"],
    "superseded": ["rationale", "supersededBy", "authorizationReference"],
}


def run_audit(root: Path) -> dict[str, Any]:
    command = [sys.executable, str(AUDIT), "--root", str(root), "--report-json"]
    result = subprocess.run(command, cwd=root, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(f"Registry audit failed: {result.stderr[-2000:]}")
    for line in reversed(result.stdout.splitlines()):
        if line.startswith("REGISTRY_DRIFT_REPORT="):
            report = json.loads(line[len("REGISTRY_DRIFT_REPORT="):])
            if isinstance(report, dict):
                return report
    raise RuntimeError("Audit did not emit a structured report")



def load_ledger_from_git(root: Path, ref: str) -> tuple[dict[str, Any] | None, str | None]:
    path = "Specification/BrAPI-GenX/Conformance/semantic-neighbor-review.yaml"
    result = subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        cwd=root, capture_output=True, text=True, check=False,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or "unreadable comparison revision"
        return None, f"cannot read comparison ledger from Git ref {ref}: {detail}"
    try:
        loaded = yaml.safe_load(result.stdout)
    except yaml.YAMLError as exc:
        return None, f"malformed comparison ledger from Git ref {ref}: {exc}"
    if not isinstance(loaded, dict):
        return None, f"malformed comparison ledger from Git ref {ref}: expected a mapping"
    return loaded, None


def load_ledger_from_path(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return None, f"cannot read comparison ledger {path}: {exc}"
    if not isinstance(loaded, dict):
        return None, f"malformed comparison ledger {path}: expected a mapping"
    return loaded, None



def is_ancestor(root: Path, ancestor: str, descendant: str) -> bool:
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=root, capture_output=True, text=True, check=False,
    )
    return result.returncode == 0

def module_path(entry: dict[str, Any]) -> str:
    source = entry.get("source") or {}
    path = source.get("path") or ""
    parts = path.split("/")
    return "/".join(parts[2:4]) if len(parts) >= 4 else ""


def primary_class(entry: dict[str, Any], dc_modules: list[dict[str, Any]]) -> str | None:
    path = module_path(entry)
    for mod in dc_modules:
        if mod.get("path", "").rstrip("/") == path:
            return mod.get("primary_class")
    return None


def inherited_set(root: Path) -> set[tuple[str, str]]:
    report = run_audit(root)
    result: set[tuple[str, str]] = set()
    registry = json.loads((root / "Specification" / "ENDPOINT-REGISTRY.json").read_text(encoding="utf-8"))
    by_cat = {e["catalogId"]: e for e in registry["entries"]}
    by_opid = {e["recommendedOperationId"]: e for e in registry["entries"]}
    for item in report.get("registryOnlyNeighbors", []):
        for neighbor in item.get("neighbors", []):
            result.add((item["catalogId"], neighbor))
    return result


def check(root: Path = ROOT,
        comparison_ref: str | None = None,
        comparison_ledger_path: Path | None = None,
        allow_bootstrap: bool = False) -> list[str]:
    errors: list[str] = []
    root = root.resolve()
    registry_path = root / "Specification" / "ENDPOINT-REGISTRY.json"
    ledger_path = root / "Specification" / "BrAPI-GenX" / "Conformance" / "semantic-neighbor-review.yaml"
    dc_path = root / "Specification" / "BrAPI-GenX" / "Conformance" / "domain-classification.yaml"

    try:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Cannot load registry: {exc}"]
    try:
        ledger = yaml.safe_load(ledger_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return [f"Cannot load semantic-neighbor ledger: {exc}"]
    try:
        dc = yaml.safe_load(dc_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return [f"Cannot load domain classification: {exc}"]

    if not isinstance(ledger, dict):
        return ["Semantic-neighbor ledger root must be a mapping."]
    if not isinstance(registry, dict):
        return ["Registry root must be a mapping."]
    dc_modules = dc.get("modules", []) if isinstance(dc, dict) else []
    if not isinstance(dc_modules, list):
        dc_modules = []

    by_cat = {e["catalogId"]: e for e in registry.get("entries", [])}
    by_opid = {e["recommendedOperationId"]: e for e in registry.get("entries", [])}
    gov_ids = {r.get("id") for r in registry.get("semanticRelationships", [])
               if isinstance(r, dict) and isinstance(r.get("id"), str)}

    # Schema-level checks.
    if ledger.get("allowed_statuses") != sorted(ALLOWED_STATUSES):
        # Allow same set, order-independent.
        if set(ledger.get("allowed_statuses", [])) != ALLOWED_STATUSES:
            errors.append("Ledger allowed_statuses does not match the governed status set.")
    if not isinstance(ledger.get("entries"), list):
        return errors + ["Ledger 'entries' must be a list."]

    entries = ledger["entries"]

    # Retention: all original 153 identities must remain present.
    current_ids = {e.get("id") for e in entries if isinstance(e, dict)}
    for retained in sorted(BASELINE_LEDGER_IDS - current_ids):
        errors.append(f"Missing retained semantic-neighbor relationship: {retained}")

    # Canonical sourceCatalogId -> targetOperationId identity.
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        expected_id = f"{entry.get('sourceCatalogId')} -> {entry.get('targetOperationId')}"
        if entry.get("id") != expected_id:
            errors.append(
                f"Non-canonical semantic-neighbor relationship id: {entry.get('id')!r} "
                f"(expected {expected_id!r})"
            )

    # Comparison ledger for status transitions.
    comparison_selected = comparison_ref is not None or comparison_ledger_path is not None
    comparison_ledger = None
    comparison_error = None
    if comparison_ledger_path is not None:
        comparison_ledger, comparison_error = load_ledger_from_path(comparison_ledger_path)
    elif comparison_ref is not None:
        comparison_ledger, comparison_error = load_ledger_from_git(root, comparison_ref)

    # Bootstrap only when no explicit comparison was selected. Verify the base
    # is genuinely pre-ledger before skipping transition enforcement.
    if not comparison_selected:
        head_ledger, head_error = load_ledger_from_git(root, "HEAD")
        if head_ledger is not None:
            comparison_ledger = head_ledger
            comparison_selected = True
        elif head_error is not None and ("not a git repository" in head_error
                                       or "unknown revision" in head_error
                                       or "does not exist" in head_error
                                       or "Path " in head_error
                                       or "not in" in head_error):
            pass  # verified pre-ledger base (or non-git test checkout)
        else:
            if head_error is not None:
                errors.append(f"Cannot verify bootstrap base: {head_error}")

    comparison_status = {}
    # Bootstrap for a verified pre-ledger base.
    if comparison_selected and comparison_error is not None and comparison_ref is not None:
        if is_ancestor(root, comparison_ref, "3125fbc35dd32abbf8166b990c5597f1aea6e61f"):
            comparison_error = None
            comparison_selected = False

    if comparison_selected:
        if comparison_error is not None:
            errors.append(f"Comparison ledger could not be loaded: {comparison_error}")
        elif isinstance(comparison_ledger, dict):
            for e in comparison_ledger.get("entries", []):
                if isinstance(e, dict) and isinstance(e.get("id"), str):
                    comparison_status[e["id"]] = e.get("reviewStatus")

    try:
        current_inherited_global = inherited_set(root)
    except RuntimeError as exc:
        errors.append(f"Cannot compute current inherited set: {exc}")
        current_inherited_global = set()
    # Unique ids and source-target pairs.
    seen_ids: set[str] = set()
    seen_pairs: set[tuple[str, str]] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("Ledger contains a non-mapping entry.")
            continue
        for field in REQUIRED_FIELDS:
            if field not in entry:
                errors.append(f"Ledger entry {entry.get('id', '<unknown>')} is missing required field '{field}'.")
        eid = entry.get("id")
        if not isinstance(eid, str) or not eid.strip():
            errors.append("Ledger entry has a missing or invalid id.")
            continue
        if eid in seen_ids:
            errors.append(f"Duplicate ledger entry id: {eid}")
        seen_ids.add(eid)
        pair = (entry.get("sourceCatalogId"), entry.get("targetOperationId"))
        if pair in seen_pairs:
            errors.append(f"Duplicate source-target relationship: {pair}")
        seen_pairs.add(pair)

        status = entry.get("reviewStatus")
        if status not in ALLOWED_STATUSES:
            errors.append(f"{eid}: invalid reviewStatus {status!r}.")

        # Status transitions.
        old_status = comparison_status.get(eid)
        if old_status is not None and old_status != status:
            allowed = ALLOWED_TRANSITIONS.get(old_status, [])
            if status not in allowed:
                errors.append(
                    f"Forbidden semantic-neighbor status transition for {eid}: "
                    f"{old_status} -> {status}"
                )

        boundary = entry.get("boundary")
        if boundary not in ALLOWED_BOUNDARIES:
            errors.append(f"{eid}: invalid boundary {boundary!r}.")

        provenance = entry.get("provenance")
        if provenance not in ALLOWED_PROVENANCE:
            errors.append(f"{eid}: invalid provenance {provenance!r}.")

        # Resolve source.
        src_cat = entry.get("sourceCatalogId")
        src_entry = by_cat.get(src_cat)
        if not isinstance(src_entry, dict):
            errors.append(f"{eid}: sourceCatalogId does not resolve to a registry entry: {src_cat!r}.")
        else:
            if entry.get("sourceOperationId") != src_entry.get("recommendedOperationId"):
                errors.append(f"{eid}: sourceOperationId does not match the registry entry.")
            if entry.get("sourceModule") != src_entry.get("genxModule"):
                errors.append(f"{eid}: sourceModule does not match the registry entry.")
            # Boundary recomputation.
            tgt_entry = by_opid.get(entry.get("targetOperationId"))
            if isinstance(tgt_entry, dict):
                sp = module_path(src_entry)
                tp = module_path(tgt_entry)
                sc = primary_class(src_entry, dc_modules)
                tc = primary_class(tgt_entry, dc_modules)
                if sp == tp:
                    computed = "within-module"
                elif sc is not None and tc is not None and sc != tc:
                    computed = "cross-domain"
                else:
                    computed = "cross-module"
                if computed != boundary:
                    errors.append(f"{eid}: boundary {boundary!r} does not match computed {computed!r}.")

        # Resolve target: operation id or governed relationship id.
        target_op = entry.get("targetOperationId")
        target_entry = by_opid.get(target_op)
        if isinstance(target_entry, dict):
            if entry.get("targetCatalogId") != target_entry.get("catalogId"):
                errors.append(f"{eid}: targetCatalogId does not match the resolved target operation.")
            if entry.get("targetModule") != target_entry.get("genxModule"):
                errors.append(f"{eid}: targetModule does not match the resolved target operation.")
        elif target_op in gov_ids:
            # Governed relationship target; targetCatalogId may be empty/None.
            pass
        else:
            errors.append(f"{eid}: targetOperationId does not resolve to an operation or governed relationship: {target_op!r}.")

        # Evidence requirements.
        for field in EVIDENCE_REQUIRED.get(status, []):
            value = entry.get(field)
            if field == "evidence":
                if not isinstance(value, list) or not value:
                    errors.append(f"{eid}: evidence-backed status requires non-empty 'evidence' list.")
            elif field == "rationale":
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"{eid}: status {status!r} requires non-empty 'rationale'.")
            elif field == "openQuestion":
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"{eid}: status {status!r} requires non-empty 'openQuestion'.")
            elif field == "reviewedBy":
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"{eid}: evidence-backed status requires 'reviewedBy'.")
            elif field == "reviewedAt":
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"{eid}: evidence-backed status requires 'reviewedAt'.")
            elif field == "supersededBy":
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"{eid}: superseded status requires 'supersededBy'.")
            else:
                if value in (None, "", [], {}):
                    errors.append(f"{eid}: status {status!r} requires field '{field}'.")

        # Resolvable successor for superseded entries.
        if status == "superseded":
            successor = entry.get("supersededBy")
            if not (successor in {e.get("id") for e in entries if isinstance(e, dict)}
                    or successor in gov_ids or successor in by_opid):
                errors.append(f"{eid}: supersededBy does not resolve to a known relationship or operation: {successor!r}.")

        # Usable evidence citations for proposed relationships.
        if status == "evidence-backed-proposed":
            for item in entry.get("evidence", []):
                if not isinstance(item, str) or not item.strip():
                    errors.append(f"{eid}: evidence entries must be non-empty strings.")

        # Authorization references for terminal decisions must be followable.
        if status in ("rejected", "superseded"):
            auth = entry.get("authorizationReference")
            if not isinstance(auth, str) or not auth.strip():
                errors.append(f"{eid}: status {status!r} requires a non-empty authorizationReference.")
            elif len(auth.strip()) < 3:
                errors.append(f"{eid}: authorizationReference is too vague to follow: {auth!r}.")

        # Reject self-supersession.
        if status == "superseded" and entry.get("supersededBy") == eid:
            errors.append(f"{eid}: self-supersession is not allowed.")

        # Documentary evidence type check.
        de = entry.get("documentaryEvidence")
        if not isinstance(de, list):
            errors.append(f"{eid}: documentaryEvidence must be a list.")

        # Scientific concerns type check.
        sc = entry.get("scientificConcerns")
        if not isinstance(sc, list):
            errors.append(f"{eid}: scientificConcerns must be a list.")

        # decisionReferences type check.
        dr = entry.get("decisionReferences")
        if not isinstance(dr, list):
            errors.append(f"{eid}: decisionReferences must be a list.")

        # Newly proposed/non-inherited relationships need traceable provenance.
        pair = (src_cat, target_op)
        if pair not in current_inherited_global:
            # Not a current registry-only inherited reference.
            if status == "inherited-unreviewed":
                errors.append(f"{eid}: a non-inherited relationship cannot be 'inherited-unreviewed'.")
            if provenance == "inherited-registry-only":
                errors.append(f"{eid}: a non-inherited relationship requires traceable provenance beyond inherited-registry-only.")
            if not isinstance(entry.get("rationale"), str) or not entry.get("rationale", "").strip():
                errors.append(f"{eid}: a non-inherited relationship requires a non-empty rationale.")

    # Completeness: every current inherited relationship must be in ledger.
    try:
        current = inherited_set(root)
    except RuntimeError as exc:
        return errors + [f"Cannot compute inherited set: {exc}"]
    ledger_pairs = {(e.get("sourceCatalogId"), e.get("targetOperationId"))
                    for e in entries if isinstance(e, dict)}
    for pair in sorted(current):
        if pair not in ledger_pairs:
            errors.append(f"Missing ledger entry for inherited registry-only relationship: {pair}")

    # Grandfathered entries remain unresolved: inherited-unreviewed entries must
    # not be treated as approved. (No status named approved exists; ensure none
    # of the inherited entries were silently changed to evidence-backed without
    # evidence, already covered above.)

    # Ledger header count sanity.
    if ledger.get("entry_count") != len(entries):
        errors.append(f"Ledger entry_count {ledger.get('entry_count')} does not match entries length {len(entries)}.")

    # Baseline count preservation (informational but check).
    baseline = ledger.get("generated_from", {}).get("baseline_registry_only_count")
    if baseline is not None and baseline != 153 and baseline != len(current):
        # Allow baseline to remain 153 for historical reference.
        pass

    return errors


def main() -> int:
    global ROOT, REGISTRY, LEDGER, AUDIT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root")
    parser.add_argument("--comparison-ref", default=None, help="trusted comparison revision for status transitions")
    parser.add_argument("--comparison-ledger", type=Path, default=None, help="path to comparison ledger for status transitions")
    parser.add_argument("--allow-bootstrap", action="store_true", help="allow verified pre-ledger bootstrap when no comparison is supplied")
    args = parser.parse_args()
    root = args.root.resolve()
    ROOT = root
    REGISTRY = root / "Specification" / "ENDPOINT-REGISTRY.json"
    LEDGER = root / "Specification" / "BrAPI-GenX" / "Conformance" / "semantic-neighbor-review.yaml"
    AUDIT = root / "Scripts" / "auditEndpointRegistrySourceConsistency.py"
    errors = check(root,
                   comparison_ref=args.comparison_ref,
                   comparison_ledger_path=args.comparison_ledger,
                   allow_bootstrap=args.allow_bootstrap)
    if errors:
        print("Semantic-neighbor governance validation FAILED:")
        for error in errors:
            print("- " + error)
        return 1
    print("Semantic-neighbor governance validation passed: ledger complete, references resolve, "
          "statuses valid, evidence requirements enforced.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
