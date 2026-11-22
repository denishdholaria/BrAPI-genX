#!/usr/bin/env python3
"""Fail closed when GenX CI no longer watches shared specification dependencies."""
from __future__ import annotations

import copy
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/genx-static-conformance.yml"
REQUIRED_PATHS = {
    "Specification/**",
    ".github/workflows/genx-static-conformance.yml",
    "Scripts/checkGenXConformance.py",
    "Scripts/checkGenXEndpointCatalog.py",
    "Scripts/checkEndpointRegistry.py",
    "Scripts/generateEndpointArtifacts.py",
    "Scripts/specification_structure.py",
    "Scripts/test_specification_structure.py",
    "Scripts/test_conformance_workflow_scope.py",
    "Scripts/auditEndpointRegistrySourceConsistency.py",
}
REQUIRED_COMMANDS = {
    "python Scripts/specification_structure.py",
    "python Scripts/test_specification_structure.py",
    "python Scripts/checkGenXConformance.py",
    "python Scripts/checkEndpointRegistry.py",
    "python Scripts/generateEndpointArtifacts.py --check",
}


def scope_errors(document: dict) -> list[str]:
    errors: list[str] = []
    # PyYAML's YAML 1.1 resolver interprets 'on:' as the boolean True.
    triggers = document.get("on", document.get(True))
    if not isinstance(triggers, dict):
        return ["Missing pull_request/push workflow trigger mapping"]
    for event in ("pull_request", "push"):
        options = triggers.get(event)
        paths = set((options or {}).get("paths") or [])
        for dep in sorted(REQUIRED_PATHS - paths):
            errors.append(f"{event} trigger missing dependency: {dep}")
    jobs = document.get("jobs") or {}
    job = jobs.get("static-conformance") or {}
    commands = "\n".join(str(s.get("run", "")) for s in job.get("steps", []) if isinstance(s, dict))
    for command in sorted(REQUIRED_COMMANDS):
        if command not in commands:
            errors.append(f"static-conformance job missing command: {command}")
    return errors


class WorkflowScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))

    def test_complete_scope_and_required_commands(self):
        self.assertEqual([], scope_errors(self.workflow))

    def test_missing_shared_specification_dependency_is_detected(self):
        damaged = copy.deepcopy(self.workflow)
        triggers = damaged.get("on", damaged.get(True))
        triggers["pull_request"]["paths"].remove("Specification/**")
        self.assertTrue(any("pull_request trigger missing dependency: Specification/**" in x
                            for x in scope_errors(damaged)))

    def test_missing_validator_execution_is_detected(self):
        damaged = copy.deepcopy(self.workflow)
        steps = damaged["jobs"]["static-conformance"]["steps"]
        step = next(s for s in steps if s.get("run") == "python Scripts/specification_structure.py")
        step["run"] = "echo skipped"
        self.assertTrue(any("job missing command: python Scripts/specification_structure.py" in x
                            for x in scope_errors(damaged)))


if __name__ == "__main__":
    unittest.main()
