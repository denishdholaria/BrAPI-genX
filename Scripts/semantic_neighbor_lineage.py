#!/usr/bin/env python3
"""Distinguish historical neighbor retirement from genuinely new relationships.

Pure provenance classification. The canonical ledger validator separately checks
status transitions, maintainer authorization, evidence and registry consistency.
"""
from __future__ import annotations

from typing import Any


def noncurrent_lineage_errors(
    entry: dict[str, Any],
    current_inherited: set[tuple[str, str]],
    baseline_ids: frozenset[str],
) -> list[str]:
    """Inspect ledger records absent from the *current* inherited registry set.

    Historical IDs remain historical after their registry reference is removed.
    Removal is only permitted with a terminal disposition; new records cannot
    borrow inherited-registry-only provenance to bypass scientific review.
    """
    pair = (entry.get("sourceCatalogId"), entry.get("targetOperationId"))
    if pair in current_inherited:
        return []

    identity = entry.get("id", "<missing id>")
    status = entry.get("reviewStatus")
    if identity in baseline_ids:
        if status in {"rejected", "superseded"}:
            return []  # Authorization and successor checks live in the canonical validator.
        return [
            f"{identity}: historical inherited neighbor absent from registry requires "
            "an authorized terminal disposition (rejected or superseded)."
        ]

    errors = []
    if status == "inherited-unreviewed":
        errors.append(f"{identity}: a non-inherited relationship cannot be 'inherited-unreviewed'.")
    if entry.get("provenance") == "inherited-registry-only":
        errors.append(
            f"{identity}: a non-inherited relationship requires traceable provenance "
            "beyond inherited-registry-only."
        )
    rationale = entry.get("rationale")
    if not isinstance(rationale, str) or not rationale.strip():
        errors.append(f"{identity}: a non-inherited relationship requires a non-empty rationale.")
    return errors
