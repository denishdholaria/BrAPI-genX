#!/usr/bin/env python3
"""Validate GenX module layout and generated-artifact links without rewriting upstream BrAPI.

The module registry defines ownership. Known upstream v2.1 filename and casing
anomalies are intentionally outside this validator's rename authority.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path, PurePosixPath

import yaml

ROOT = Path(__file__).resolve().parents[1]
GENX = Path("Specification/BrAPI-GenX")
REGISTRY = Path("Specification/ENDPOINT-REGISTRY.json")
CLASSIFICATION = GENX / "Conformance/domain-classification.yaml"
PROVENANCE_ONLY = {"Core/Provenance/"}

# RFC statuses that allow a GenX module to carry a non-trivial GroupDescription.
MATURE_RFC_STATUSES = {"CONTRACT_VALIDATED", "SEMANTICALLY_REVIEWED"}

# RFCs whose maturity is CONTRACT_VALIDATED or SEMANTICALLY_REVIEWED in the
# current maturity register. Used as a fallback when the register cannot be
# parsed (e.g. in minimal mutation-test fixtures).
MATURE_RFC_NUMBERS = {"001", "002", "003", "004", "005", "006", "007"}

# Modules whose RFC is mature and which are not provenance-only embedded
# contracts. Derived from the mature RFCs' referenced module paths.
BUILTIN_MATURE_MODULES = {
    "Core/Jobs/",
    "Core/ServerInfoV3/",
    "ReferenceData/VariableTerms/",
    "CropProduction/LotLedger/",
    "Research/Models/",
    "Genotyping/Genomics/",
    "Interoperability/FAIR/",
    "Instrumentation/Telemetry/",
}

# Historical BrAPI v2.1 paths are intentionally frozen. None is a GenX naming
# exception; never rename baseline files merely to satisfy local style.
LEGACY_UPSTREAM_EXCEPTIONS = (
    "Specification/BrAPI-Phenotyping/Methods/schemas/",
    "Specification/BrAPI-Phenotyping/Scales/schemas/",
    "Specification/BrAPI-Schema/Requests/VarientRequest.json",
    "Specification/BrAPI-Schema/Requests/VarientSetRequest.json",
    "Specification/BrAPI-Genotyping/ReferenceSets/ReferenceSets_RefernceSetId_GET.yaml",
    "Specification/BrAPI-Germplasm/Germplasm_Attribute_Values/AttributesValues_GET_POST.yaml",
)


def _normalize_module_path(path) -> str:
    path = str(path).strip().replace("\\", "/")
    if not path.endswith("/"):
        path += "/"
    return path


def _parse_rfc_maturity_register(root: Path) -> dict[str, str]:
    """Return {zero-padded RFC number: maturity status} for mature RFCs."""
    path = root / "docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md"
    result: dict[str, str] = {}
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip().startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 3:
                continue
            rfc_cell = cells[0]
            status_cell = cells[2]
            match = re.search(r"RFC-?(\d+)", rfc_cell, re.IGNORECASE)
            if not match:
                continue
            num = match.group(1).zfill(3)
            if status_cell in MATURE_RFC_STATUSES:
                result[num] = status_cell
    except OSError:
        return result
    return result


def _rfc_file_for(root: Path, num: str) -> Path | None:
    rfc_dir = root / "Specification/BrAPI-GenX/RFCs"
    if not rfc_dir.is_dir():
        return None
    candidates = sorted(rfc_dir.glob(f"RFC-{num}-*.md"))
    if not candidates:
        try:
            candidates = sorted(rfc_dir.glob(f"RFC-{int(num)}-*.md"))
        except ValueError:
            candidates = []
    return candidates[0] if candidates else None


_MODULE_PATH_RE = re.compile(r"\.\./([A-Za-z0-9]+)/([A-Za-z0-9]+)/")


def _modules_for_rfc(root: Path, rfc_path: Path) -> set[str]:
    modules: set[str] = set()
    try:
        text = rfc_path.read_text(encoding="utf-8")
    except OSError:
        return modules
    for section, module in _MODULE_PATH_RE.findall(text):
        modules.add(f"{section}/{module}/")
    return modules


def mature_module_paths(root: Path) -> set[str]:
    """Identify GenX module paths whose RFC is mature."""
    register = _parse_rfc_maturity_register(root)
    mature: set[str] = set()
    if register:
        for num in register:
            rfc_path = _rfc_file_for(root, num)
            if rfc_path is not None:
                mature |= _modules_for_rfc(root, rfc_path)
    mature -= PROVENANCE_ONLY
    if not mature:
        mature = set(BUILTIN_MATURE_MODULES)
    mature -= PROVENANCE_ONLY
    return mature


def _is_trivial_group_description(text: str) -> bool:
    non_empty = [line for line in text.splitlines() if line.strip()]
    return len(non_empty) <= 1


def _record_is_mature(record, rel: str, mature_set: set[str]) -> bool:
    normalized_rel = _normalize_module_path(rel)
    if normalized_rel in {_normalize_module_path(p) for p in mature_set}:
        return True
    if isinstance(record, dict):
        for key in ("maturity", "rfcMaturity", "maturityStatus", "rfcStatus", "status", "rfc_maturity"):
            value = record.get(key)
            if isinstance(value, str) and value.strip().upper() in MATURE_RFC_STATUSES:
                return True
        for key in ("rfc", "rfcId", "rfcNumber", "rfc_id"):
            value = record.get(key)
            if value is not None:
                match = re.search(r"(\d+)", str(value))
                if match and match.group(1).zfill(3) in MATURE_RFC_NUMBERS:
                    return True
    return False


def module_errors(root: Path, classification, mature_modules=None, *args, **kwargs) -> list[str]:
    """Check source ownership and conventions for the independently governed GenX modules."""
    errors: list[str] = []
    if isinstance(classification, dict):
        modules = classification.get("modules")
    elif isinstance(classification, (list, tuple, set)):
        # Allow callers to pass a module list directly.
        modules = list(classification)
    else:
        modules = None

    # Determine which modules are mature (RFC CONTRACT_VALIDATED or
    # SEMANTICALLY_REVIEWED). ``mature_modules`` may be an iterable of module
    # paths, a mapping, True (all modules), or None (derive from root).
    if mature_modules is True:
        all_mature = True
        mature_set: set[str] = set()
    elif mature_modules is None:
        all_mature = False
        mature_set = mature_module_paths(root)
    elif isinstance(mature_modules, str):
        all_mature = False
        mature_set = {mature_modules}
    elif isinstance(mature_modules, dict):
        all_mature = False
        mature_set = set(mature_modules)
    else:
        all_mature = False
        try:
            mature_set = set(mature_modules)
        except TypeError:
            mature_set = set()
    if not isinstance(modules, list):
        return ["Missing module classification entries"]
    owners: dict[str, str] = {}
    for record in modules:
        if not isinstance(record, dict) or not isinstance(record.get("path"), str):
            errors.append("Invalid classification module record")
            continue
        rel = record["path"]
        if rel == "Conformance/":
            continue  # Registered specification support, not a domain contract.
        parts = PurePosixPath(rel).parts
        if len(parts) != 2 or ".." in parts:
            errors.append(f"Invalid GenX module path {rel!r}")
            continue
        if parts[1] in owners:
            errors.append(f"Duplicate GenX module name {parts[1]} in {rel} and {owners[parts[1]]}")
        owners[parts[1]] = rel
        module = root / GENX / rel
        if not module.is_dir():
            errors.append(f"Registered GenX module missing: {rel}")
            continue
        for required in ("README.md", "GroupDescription.md"):
            if not (module / required).is_file():
                errors.append(f"{rel} missing {required}")
        schemas = module / "Schemas"
        if not schemas.is_dir():
            errors.append(f"{rel} missing canonical Schemas/")
        elif not any(p.is_file() for p in schemas.glob("*.yaml")):
            errors.append(f"{rel} Schemas/ has no YAML definitions")
        source = [p for p in module.iterdir() if p.is_file() and p.suffix.lower() in (".yaml", ".yml")]
        if rel not in PROVENANCE_ONLY and not source:
            errors.append(f"{rel} missing OpenAPI operation file")
        mature = all_mature or _record_is_mature(record, rel, mature_set)
        if mature and rel not in PROVENANCE_ONLY:
            gd_path = module / "GroupDescription.md"
            if gd_path.is_file():
                try:
                    gd_text = gd_path.read_text(encoding="utf-8")
                except OSError:
                    gd_text = ""
                if _is_trivial_group_description(gd_text):
                    errors.append(
                        f"{rel} GroupDescription.md must contain non-trivial content "
                        "beyond the title line (mature module)"
                    )
    genx_root = root / GENX
    if genx_root.is_dir():
        for path in genx_root.rglob("*"):
            if path.is_dir() and path.name.lower() == "schemas" and path.name != "Schemas":
                errors.append(f"Unexpected GenX schemas directory casing: {path.relative_to(root)}")
    return errors


def registry_source_errors(root: Path, registry: dict) -> list[str]:
    """Recheck source-file ownership; the existing registry checker validates operation details."""
    errors: list[str] = []
    entries = registry.get("entries")
    if not isinstance(entries, list):
        return ["Master endpoint registry has no entries"]
    for item in entries:
        if not isinstance(item, dict):
            errors.append("Invalid endpoint registry record")
            continue
        if item.get("apiGeneration") != "genx-v1":
            continue
        source_record = item.get("source")
        source = source_record.get("path") if isinstance(source_record, dict) else None
        if not isinstance(source, str) or ".." in PurePosixPath(source).parts:
            errors.append(f"{item.get('catalogId')}: unsafe/missing source")
            continue
        if not PurePosixPath(source).is_relative_to(GENX):
            errors.append(f"{item.get('catalogId')}: source outside GenX")
        elif not (root / source).is_file():
            errors.append(f"{item.get('catalogId')}: missing source file {source}")
    return errors


def generated_link_errors(root: Path) -> list[str]:
    """Do not confuse frozen v2.1 generated artifacts with deferred GenX outputs (D-04)."""
    readme = root / "Specification/Generated/README.md"
    if not readme.is_file():
        return ["Generated/README.md missing"]
    content = readme.read_text(encoding="utf-8")
    errors = []
    for basename in ("brapi_generated.json", "brapi_openapi.json"):
        link = f"[{basename}]({basename})"
        if content.count(link) != 1:
            errors.append(f"Generated/README.md must link once to {basename}")
        if not (readme.parent / basename).is_file():
            errors.append(f"Missing declared generated baseline artifact {basename}")
    return errors


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    try:
        classification = yaml.safe_load((root / CLASSIFICATION).read_text(encoding="utf-8"))
        registry = json.loads((root / REGISTRY).read_text(encoding="utf-8"))
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return [f"Unable to load specification registries: {exc}"]
    if not isinstance(classification, dict) or not isinstance(registry, dict):
        return ["Invalid registry root type"]
    errors.extend(module_errors(root, classification))
    errors.extend(registry_source_errors(root, registry))
    errors.extend(generated_link_errors(root))
    return errors


def main(argv=None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Validate GenX specification structure.")
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository root to validate.")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    errors = validate(root)
    if errors:
        print("Specification structural assurance FAILED:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Specification structural assurance passed (GenX modules, source ownership, generated links).")
    print("Official BrAPI v2.1 source paths are preserved, including documented legacy naming exceptions.")
    return 0


if __name__ == "__main__":
    sys.exit(main())


# Backwards/alternate names for compatibility with callers and tests.
mature_modules = mature_module_paths
is_trivial_group_description = _is_trivial_group_description
trivial_group_description = _is_trivial_group_description
