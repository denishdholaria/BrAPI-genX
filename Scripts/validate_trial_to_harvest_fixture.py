#!/usr/bin/env python3
"""Validate the BrAPI-GenX trial-to-harvest fixture (FX-001 irrigation + FX-003 yield).

Standalone design-evidence checker. Uses only stdlib plus PyYAML/jsonschema.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import yaml
from jsonschema import validate, ValidationError

REPO = Path(__file__).resolve().parents[1]
JSON_PATH = REPO / "docs" / "assessment" / "BRAPI-GENX-TRIAL-TO-HARVEST-MAPPING.json"
EVENT_SCHEMA_PATH = REPO / "Specification" / "BrAPI-Phenotyping" / "Events" / "Schemas" / "Event.yaml"


def load_json():
    return json.loads(JSON_PATH.read_text())


def load_event_schema():
    spec = yaml.safe_load(EVENT_SCHEMA_PATH.read_text())
    return spec["components"]["schemas"]["Event"]


def is_dt(s):
    try:
        from datetime import datetime
        datetime.fromisoformat(str(s).replace("Z", "+00:00"))
        return True
    except Exception:
        return False


def schema_errors(payload, schema):
    try:
        validate(instance=payload, schema=schema)
    except ValidationError as e:
        return [str(e.message)]
    errs = []
    for dd in (payload.get("eventDateRange", {}).get("discreteDates") or []):
        if not is_dt(dd):
            errs.append(f"bad datetime {dd}")
    return errs


def recognizes_applied_depth(ep):
    def finite(v):
        try:
            f = float(v)
            return math.isfinite(f)
        except (TypeError, ValueError):
            return False
    return (ep.get("code") == "IRVAL" and ep.get("units") == "mm"
            and finite(ep.get("value")))


def main():
    d = load_json()
    fx = d["fixture"]
    event = fx["brapiEvent"]
    study_units = {u["observationUnitDbId"] for u in fx["observationUnits"]}
    foreign_units = {u["observationUnitDbId"] for u in fx.get("foreignStudyObservationUnits", [])}
    schema = load_event_schema()

    failures = []

    # --- Irrigation checks (FX-001) ---
    base_errors = schema_errors(event, schema)
    if base_errors:
        failures.append(f"irrigation base schema errors: {base_errors}")

    def resolve(refs):
        if refs is None:
            return sorted(study_units), []
        resolved = [r for r in refs if r in study_units]
        unknown = [r for r in refs if r not in study_units]
        return resolved, unknown

    case1_resolved, case1_unknown = resolve(event["observationUnitDbIds"])
    if not (case1_resolved == ["plot-a"] and case1_unknown == []):
        failures.append("irrigation case1 explicit plot-a")

    case2_resolved, case2_unknown = resolve(["plot-z"])
    if not (case2_resolved == [] and case2_unknown == ["plot-z"]):
        failures.append("irrigation case2 unknown plot")

    case3_resolved, case3_unknown = resolve(["plot-c"])
    if not (case3_resolved == [] and case3_unknown == ["plot-c"] and "plot-c" in foreign_units):
        failures.append("irrigation case3 foreign study plot")

    case4_resolved, case4_unknown = resolve(None)
    if not (case4_resolved == sorted(study_units) and case4_unknown == []):
        failures.append("irrigation case4 omitted -> all units")

    alt = json.loads(json.dumps(event))
    alt["observationUnitDbIds"] = ["plot-b"]
    case5_resolved, case5_unknown = resolve(alt["observationUnitDbIds"])
    if not (case5_resolved == ["plot-b"] and case5_unknown == [] and schema_errors(alt, schema) == []):
        failures.append("irrigation case5 substituted plot")

    wrong = json.loads(json.dumps(event))
    wrong["observationUnitDbIds"] = [123]
    if schema_errors(wrong, schema) == []:
        failures.append("irrigation case6 wrong-type mutation should fail")

    param = event["eventParameters"][0]
    if not recognizes_applied_depth(param):
        failures.append("irrigation case7 IRVAL 20 mm")
    if not recognizes_applied_depth({"code": "IRVAL", "units": "mm", "value": "17.5"}):
        failures.append("irrigation case8 IRVAL 17.5 mm")
    if recognizes_applied_depth({"code": "IRVAL", "units": "cm", "value": "20"}):
        failures.append("irrigation case9 cm should be rejected")
    if recognizes_applied_depth({"code": "IRADP", "units": "mm", "value": "20"}):
        failures.append("irrigation case10 IRADP should be rejected")
    if recognizes_applied_depth({"code": "XXXX", "units": "mm", "value": "20"}):
        failures.append("irrigation case11 unknown code should be rejected")

    field_log_plot = fx["independentFieldLog"]["plotDbId"]
    if not (event["observationUnitDbIds"] == ["plot-a"] and field_log_plot == "plot-a"):
        failures.append("irrigation case12 field-log agrees")
    if not (alt["observationUnitDbIds"] == ["plot-b"] and field_log_plot == "plot-a"):
        failures.append("irrigation case13 substituted field-log disagrees")

    # --- Yield checks (FX-003) ---
    yf = d.get("yieldFixture")
    if not yf:
        failures.append("missing yieldFixture")
    else:
        study_units_y = {u["observationUnitDbId"] for u in fx["observationUnits"]}
        obs = yf["observation"]
        ov = yf["observationVariable"]
        # plot resolves in study
        if obs["observationUnitDbId"] not in study_units_y:
            failures.append("yield plot does not resolve in study")
        # cultivar matches plot
        plot_unit = next((u for u in fx["observationUnits"] if u["observationUnitDbId"] == obs["observationUnitDbId"]), None)
        if plot_unit is None or plot_unit.get("germplasmDbId") != obs["germplasmDbId"]:
            failures.append("yield cultivar does not match plot")
        # study matches
        if obs["studyDbId"] != yf["studyDbId"]:
            failures.append("yield study mismatch")
        # variable resolves with trait/method/scale
        if not (ov.get("trait", {}).get("traitName") and ov.get("method", {}).get("methodName") and ov.get("scale", {}).get("scaleName")):
            failures.append("yield variable missing trait/method/scale")
        # moisture basis dry (HWAH)
        vocab = yf["vocabulary"]["entry"]
        if vocab.get("codeDisplay") != "HWAH":
            failures.append("yield vocabulary not HWAH")
        if vocab.get("unit") != "kg/ha":
            failures.append("yield vocabulary unit not kg/ha")
        # source measurement traceable
        sm = yf["sourceMeasurement"]
        calc = yf["calculation"]
        expected = sm["dryGrainMassKg"] / sm["harvestedAreaM2"] * 10000
        if abs(expected - calc["result"]) > 1e-9:
            failures.append("yield calculation mismatch")
        if str(calc["result"]) != obs["value"]:
            failures.append("yield reported value mismatch")
        # harvested vs full plot area
        if not (sm["harvestedAreaM2"] < sm["fullPlotAreaM2"]):
            failures.append("harvested area not distinct from plot area")
        # timestamp present
        if not obs.get("observationTimeStamp"):
            failures.append("yield missing harvest timing")
        # harvest event distinct
        he = yf["harvestEvent"]
        if he.get("eventType") != "harvest":
            failures.append("harvest event type not harvest")
        if obs["observationUnitDbId"] not in (he.get("observationUnitDbIds") or []):
            failures.append("harvest event does not affect plot")
        # negative cases presence
        ncs = yf.get("negativeCases", [])
        if len(ncs) < 4:
            failures.append("yield negative cases incomplete")

    # --- plot-b irrigation absence unknown vs zero ---
    # Ensure fixture does not record an irrigation Event for plot-b; absence is unknown.
    plot_b_events = [e for e in [event] if "plot-b" in (e.get("observationUnitDbIds") or [])]
    # base event affects plot-a only, so plot-b has no event -> unknown (not zero)
    if "plot-b" in (event.get("observationUnitDbIds") or []):
        failures.append("plot-b should not have irrigation event in base fixture")

    if failures:
        print("FAILURES:")
        for f in failures:
            print(" -", f)
        sys.exit(1)
    print("All irrigation and yield checks passed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
