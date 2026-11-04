"""JCS (RFC 8785) canonical JSON serialization for BrAPI-GenX.

This module provides the canonicalization primitive that produces deterministic
UTF-8 bytes from valid JSON input, following the JSON Canonicalization Scheme
defined in RFC 8785.

The canonicalizer:
- Rejects duplicate JSON object property names (at any nesting depth).
- Rejects non-finite numbers (NaN, Infinity, -Infinity).
- Rejects lone Unicode surrogates.
- Rejects integers outside the IEEE 754 safe integer range.
- Produces canonical UTF-8 bytes with sorted object keys, compact separators,
  and JCS-compliant number serialization.
- Does NOT perform Unicode normalization (NFC/NFD).
- Does NOT convert scientific decimal strings to numbers.

This module is independent of cryptographic hashing, digest envelopes,
and request fingerprint construction.
"""

from __future__ import annotations

import json
import re
from typing import Any

try:
    import rfc8785
except ImportError as exc:
    raise SystemExit(
        "Missing dependency: python -m pip install rfc8785==0.1.4"
    ) from exc

# Regex to detect non-finite JSON numbers that should be rejected
_NON_FINITE_NUMBER_RE = re.compile(r"^-?(?:Infinity|NaN)$", re.IGNORECASE)

# IEEE 754 binary64 safe integer range: -(2^53 - 1) to 2^53 - 1
_MAX_SAFE_INTEGER = 2**53 - 1
_MIN_SAFE_INTEGER = -(2**53 - 1)


class JCSError(ValueError):
    """Base exception for JCS canonicalization errors."""
    pass


class DuplicatePropertyError(JCSError):
    """Raised when a JSON object contains duplicate property names."""
    pass


class NonFiniteNumberError(JCSError):
    """Raised when a non-finite number (NaN, Infinity) is encountered."""
    pass


class LoneSurrogateError(JCSError):
    """Raised when a lone Unicode surrogate is encountered."""
    pass


class UnsafeIntegerError(JCSError):
    """Raised when an integer exceeds the IEEE 754 safe integer range."""
    pass


def _check_lone_surrogates(value: Any) -> None:
    """Recursively check for lone Unicode surrogates in strings.

    A lone high surrogate (0xD800-0xDBFF) not followed by a low surrogate,
    or a lone low surrogate (0xDC00-0xDFFF), is invalid per JCS.
    """
    if isinstance(value, str):
        i = 0
        while i < len(value):
            code = ord(value[i])
            if 0xD800 <= code <= 0xDBFF:  # High surrogate
                if i + 1 >= len(value):
                    raise LoneSurrogateError("lone high surrogate at end of string")
                next_code = ord(value[i + 1])
                if not (0xDC00 <= next_code <= 0xDFFF):
                    raise LoneSurrogateError(
                        f"lone high surrogate U+{code:04X} not followed by low surrogate"
                    )
                i += 2
            elif 0xDC00 <= code <= 0xDFFF:  # Low surrogate without preceding high
                raise LoneSurrogateError(f"lone low surrogate U+{code:04X}")
            else:
                i += 1
    elif isinstance(value, list):
        for item in value:
            _check_lone_surrogates(item)
    elif isinstance(value, dict):
        for k, v in value.items():
            _check_lone_surrogates(k)
            _check_lone_surrogates(v)


def _check_safe_integers(value: Any) -> None:
    """Recursively check that integers are within IEEE 754 safe range.

    JCS requires that integers be representable exactly in IEEE 754 binary64,
    which means they must be within [-(2^53 - 1), 2^53 - 1].
    """
    if isinstance(value, int):
        if value > _MAX_SAFE_INTEGER or value < _MIN_SAFE_INTEGER:
            raise UnsafeIntegerError(
                f"integer {value} outside IEEE 754 safe range "
                f"[{_MIN_SAFE_INTEGER}, {_MAX_SAFE_INTEGER}]"
            )
    elif isinstance(value, list):
        for item in value:
            _check_safe_integers(item)
    elif isinstance(value, dict):
        for k, v in value.items():
            _check_safe_integers(v)


def _check_non_finite_numbers(value: Any) -> None:
    """Recursively check for non-finite numbers that JCS rejects.

    JCS does not permit NaN, Infinity, or -Infinity.
    """
    if isinstance(value, float):
        if value != value or value == float("inf") or value == float("-inf"):
            raise NonFiniteNumberError(f"non-finite number: {value}")
    elif isinstance(value, list):
        for item in value:
            _check_non_finite_numbers(item)
    elif isinstance(value, dict):
        for k, v in value.items():
            _check_non_finite_numbers(v)


class _DuplicateDetector:
    """JSON object_pairs_hook that detects duplicate property names."""

    def __init__(self) -> None:
        self.duplicates: list[str] = []

    def __call__(self, pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, val in pairs:
            if key in result:
                self.duplicates.append(key)
            result[key] = val
        return result


def parse_strict_json(json_bytes: bytes) -> Any:
    """Parse JSON bytes with strict validation.

    Args:
        json_bytes: Raw JSON input as UTF-8 bytes.

    Returns:
        Parsed Python object.

    Raises:
        JCSError: If the input is invalid JSON or violates JCS constraints
            (duplicate properties, non-finite numbers, lone surrogates,
            unsafe integers).
    """
    if not isinstance(json_bytes, (bytes, bytearray)):
        raise JCSError("input must be bytes")

    # Decode UTF-8
    try:
        text = json_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise JCSError(f"invalid UTF-8: {exc}") from exc

    # Detect duplicate properties using object_pairs_hook
    detector = _DuplicateDetector()
    try:
        value = json.loads(text, object_pairs_hook=detector)
    except json.JSONDecodeError as exc:
        raise JCSError(f"invalid JSON: {exc}") from exc

    if detector.duplicates:
        # Report the first duplicate found
        raise DuplicatePropertyError(
            f"duplicate JSON property name: {detector.duplicates[0]!r}"
        )

    # Validate JCS constraints
    _check_non_finite_numbers(value)
    _check_lone_surrogates(value)
    _check_safe_integers(value)

    return value


def jcs_canonicalize(json_bytes: bytes) -> bytes:
    """Canonicalize JSON input according to JCS (RFC 8785).

    This is the primary canonicalization function. It:
    1. Parses the input JSON with strict validation.
    2. Validates JCS constraints (no duplicates, no non-finite numbers,
       no lone surrogates, safe integers only).
    3. Produces JCS canonical UTF-8 bytes using rfc8785.

    Args:
        json_bytes: Raw JSON input as UTF-8 bytes.

    Returns:
        Canonical UTF-8 bytes as defined by RFC 8785.

    Raises:
        JCSError: If the input is invalid or violates JCS constraints.
    """
    # Parse and validate
    value = parse_strict_json(json_bytes)

    # Canonicalize using rfc8785 (returns bytes)
    canonical_bytes = rfc8785.dumps(value)

    # rfc8785.dumps returns bytes; ensure it's valid UTF-8
    canonical_bytes.decode("utf-8")

    return canonical_bytes


def jcs_canonicalize_text(json_text: str) -> str:
    """Canonicalize JSON text input according to JCS (RFC 8785).

    Convenience function for text input. Returns canonical text (str).
    """
    canonical_bytes = jcs_canonicalize(json_text.encode("utf-8"))
    return canonical_bytes.decode("utf-8")


# Re-export the exception classes for external use
__all__ = [
    "jcs_canonicalize",
    "jcs_canonicalize_text",
    "parse_strict_json",
    "JCSError",
    "DuplicatePropertyError",
    "NonFiniteNumberError",
    "LoneSurrogateError",
    "UnsafeIntegerError",
]