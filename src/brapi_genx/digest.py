"""Digest primitives for BrAPI-GenX.

Provides SHA-256 based digest functions for the three approved digest purposes:
1. Raw-byte digest — exact byte sequence identification.
2. Canonical JSON digest — JCS-canonicalized JSON content identification.
3. Request fingerprint — composite request identity hashing.

This module uses SHA-256 as the approved algorithm (maintainer decision 2026-11-04).
The algorithm identifier is "sha256".

The external digest representation (envelope format, encoding) is NOT finalized
by this module. This module produces raw digest bytes and canonicalization
metadata for internal use.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from .canonicalization import jcs_canonicalize, JCSError


class DigestPurpose(str, Enum):
    """Approved digest purposes per D-02 resolution."""
    RAW_BYTE = "raw_byte"
    CANONICAL_JSON = "canonical_json"
    REQUEST_FINGERPRINT = "request_fingerprint"
    # Semantic fingerprint is domain-specific and not provided by this module


@dataclass(frozen=True)
class CanonicalizationProfile:
    """Identifies the canonicalization method and version."""
    name: str
    version: str = "v1"

    def __str__(self) -> str:
        return f"{self.name}:{self.version}"


# Approved canonicalization profiles
JCS_RFC8785_V1 = CanonicalizationProfile("jcs-rfc8785", "v1")


@dataclass(frozen=True)
class DigestResult:
    """Internal digest result — NOT the external API envelope.

    The external digest representation (hex, base64, multihash, JSON envelope)
    is a separate decision and not finalized by this module.

    This type is used for internal traceability and cross-language verification.
    """
    algorithm: str                  # e.g., "sha256"
    purpose: DigestPurpose
    value: bytes                    # raw digest bytes (32 bytes for SHA-256)
    canonicalization_profile: Optional[CanonicalizationProfile] = None

    def hex(self) -> str:
        """Return lowercase hexadecimal representation."""
        return self.value.hex()

    def __str__(self) -> str:
        parts = [f"algorithm={self.algorithm}", f"purpose={self.purpose.value}"]
        if self.canonicalization_profile:
            parts.append(f"profile={self.canonicalization_profile}")
        parts.append(f"digest={self.hex()}")
        return "DigestResult(" + ", ".join(parts) + ")"


# Algorithm constant
SHA256_ALGORITHM = "sha256"


def _sha256(data: bytes) -> bytes:
    """Compute SHA-256 digest of input bytes."""
    return hashlib.sha256(data).digest()


def raw_byte_digest(data: bytes) -> DigestResult:
    """Compute raw-byte digest (exact byte sequence identification).

    Purpose: File/artifact integrity, exact payload verification,
    byte-level provenance. No parsing, no canonicalization.

    Args:
        data: Exact byte sequence to hash.

    Returns:
        DigestResult with purpose=RAW_BYTE.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("raw_byte_digest requires bytes input")
    return DigestResult(
        algorithm=SHA256_ALGORITHM,
        purpose=DigestPurpose.RAW_BYTE,
        value=_sha256(bytes(data)),
    )


def canonical_json_digest(json_bytes: bytes) -> DigestResult:
    """Compute canonical JSON digest using JCS-RFC8785.

    Purpose: Provenance binding, mutation detection, interoperable
    request equivalence. Input is parsed, validated, JCS-canonicalized,
    then hashed.

    Args:
        json_bytes: JSON input as UTF-8 bytes.

    Returns:
        DigestResult with purpose=CANONICAL_JSON and JCS profile.

    Raises:
        JCSError: If input violates JCS constraints.
    """
    canonical_bytes = jcs_canonicalize(json_bytes)
    return DigestResult(
        algorithm=SHA256_ALGORITHM,
        purpose=DigestPurpose.CANONICAL_JSON,
        value=_sha256(canonical_bytes),
        canonicalization_profile=JCS_RFC8785_V1,
    )


def request_fingerprint_digest(
    operation_id: str,
    http_method: str,
    canonical_payload: bytes,
    query_params: Optional[dict[str, str]] = None,
    headers: Optional[dict[str, str]] = None,
    contract_version: str = "1",
) -> DigestResult:
    """Compute request fingerprint digest for idempotency.

    Purpose: Determine whether a new request is equivalent to a previous
    submission with the same idempotency key.

    The fingerprint is a SHA-256 hash of a JCS-canonicalized envelope
    containing the operation identity and relevant request context.

    Args:
        operation_id: Stable GenX operation identifier (e.g., "genxSubmitAsyncJob").
        http_method: HTTP method (GET, POST, PUT, DELETE).
        canonical_payload: JCS-canonicalized request body bytes.
        query_params: Relevant query parameters (operation-specific).
        headers: Relevant headers (operation-specific, e.g., Content-Type).
        contract_version: API/contract version for fingerprint versioning.

    Returns:
        DigestResult with purpose=REQUEST_FINGERPRINT.
    """
    import json

    # Validate raw payload bytes through JCS when available, so duplicate
    # properties and other JCS input constraints are rejected.
    if canonical_payload:
        canonical_payload = jcs_canonicalize(canonical_payload)

    envelope = {
        "v": 1,
        "op": operation_id,
        "method": http_method.upper(),
        "payload": json.loads(canonical_payload.decode("utf-8"))
                       if canonical_payload else None,
        "query": query_params or {},
        "headers": headers or {},
        "cv": contract_version,
    }

    # Authoritative JCS canonicalization of the envelope (RFC 8785).
    raw_envelope = json.dumps(envelope).encode("utf-8")
    envelope_bytes = jcs_canonicalize(raw_envelope)

    return DigestResult(
        algorithm=SHA256_ALGORITHM,
        purpose=DigestPurpose.REQUEST_FINGERPRINT,
        value=_sha256(envelope_bytes),
        canonicalization_profile=JCS_RFC8785_V1,
    )


__all__ = [
    "DigestPurpose",
    "CanonicalizationProfile",
    "JCS_RFC8785_V1",
    "DigestResult",
    "SHA256_ALGORITHM",
    "raw_byte_digest",
    "canonical_json_digest",
    "request_fingerprint_digest",
]