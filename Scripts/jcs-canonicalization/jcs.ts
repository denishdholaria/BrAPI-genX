// JCS (RFC 8785) canonicalization for BrAPI-GenX — TypeScript/Bun implementation.
//
// Independent implementation mirroring the Python primitive in
// src/brapi_genx/canonicalization.py. Uses the maintained `canonicalize`
// package (erdtman/canonicalize, JCS reference implementation) for the
// canonical serialization step, with BrAPI-GenX strict input validation
// layered on top.
//
// Interface:
//   jcsCanonicalize(input: Uint8Array): Uint8Array
//
// Does NOT compute SHA-256.

import canonicalize from "canonicalize";

export class JCSError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "JCSError";
  }
}
export class DuplicatePropertyError extends JCSError {
  constructor(message: string) {
    super(message);
    this.name = "DuplicatePropertyError";
  }
}
export class NonFiniteNumberError extends JCSError {
  constructor(message: string) {
    super(message);
    this.name = "NonFiniteNumberError";
  }
}
export class LoneSurrogateError extends JCSError {
  constructor(message: string) {
    super(message);
    this.name = "LoneSurrogateError";
  }
}
export class UnsafeIntegerError extends JCSError {
  constructor(message: string) {
    super(message);
    this.name = "UnsafeIntegerError";
  }
}

const MAX_SAFE_INTEGER = 9007199254740991; // 2^53 - 1
const MIN_SAFE_INTEGER = -9007199254740991;

function decodeUtf8Strict(bytes: Uint8Array): string {
  const decoder = new TextDecoder("utf-8", { fatal: true });
  try {
    return decoder.decode(bytes);
  } catch (e) {
    throw new JCSError(`invalid UTF-8: ${String(e)}`);
  }
}

// Duplicate-key detection that runs on the raw text BEFORE JSON.parse,
// so duplicate information is not lost. Decodes JSON string escapes so that
// "a" and "\u0061" are compared after unescaping.
function assertNoDuplicateKeys(raw: string): void {
  const p = { value: 0 };
  function skipWs(): void {
    while (p.value < raw.length && /\s/.test(raw[p.value])) p.value++;
  }
  function parseStringToken(): string {
    const start = p.value;
    if (raw[p.value] !== '"') throw new JCSError("expected JSON string");
    p.value++;
    while (p.value < raw.length) {
      const ch = raw[p.value++];
      if (ch === "\\") {
        if (p.value >= raw.length) throw new JCSError("unterminated escape");
        p.value++;
      } else if (ch === '"') {
        return JSON.parse(raw.slice(start, p.value)) as string;
      }
    }
    throw new JCSError("unterminated JSON string");
  }
  function value(): void {
    skipWs();
    const ch = raw[p.value];
    if (ch === '"') {
      parseStringToken();
      return;
    }
    if (ch === "{") {
      p.value++;
      skipWs();
      const keys = new Set<string>();
      if (raw[p.value] === "}") {
        p.value++;
        return;
      }
      while (p.value < raw.length) {
        skipWs();
        const key = parseStringToken();
        if (keys.has(key)) throw new DuplicatePropertyError("duplicate JSON property name: " + key);
        keys.add(key);
        skipWs();
        if (raw[p.value++] !== ":") throw new JCSError("expected colon");
        value();
        skipWs();
        const sep = raw[p.value++];
        if (sep === "}") return;
        if (sep !== ",") throw new JCSError("expected comma or object close");
      }
      throw new JCSError("unterminated JSON object");
    }
    if (ch === "[") {
      p.value++;
      skipWs();
      if (raw[p.value] === "]") {
        p.value++;
        return;
      }
      while (p.value < raw.length) {
        value();
        skipWs();
        const sep = raw[p.value++];
        if (sep === "]") return;
        if (sep !== ",") throw new JCSError("expected comma or array close");
      }
      throw new JCSError("unterminated JSON array");
    }
    const start = p.value;
    while (p.value < raw.length && !/[\s,\]}]/.test(raw[p.value])) p.value++;
    if (p.value === start) throw new JCSError("expected JSON value");
    const token = raw.slice(start, p.value);
    if (token === "true" || token === "false" || token === "null") return;
    if (!/^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?$/.test(token)) {
      throw new JCSError("invalid JSON primitive token");
    }
    // Reject plain integer tokens outside the safe interoperability range,
    // before JavaScript parsing can round them.
    if (/^-?(?:0|[1-9]\d*)$/.test(token)) {
      const integer = BigInt(token);
      if (integer > BigInt(MAX_SAFE_INTEGER) || integer < BigInt(MIN_SAFE_INTEGER)) {
        throw new UnsafeIntegerError("integer outside safe interoperability range: " + token);
      }
    }
  }
  value();
  skipWs();
  if (p.value !== raw.length) throw new JCSError("trailing content after JSON value");
}

function rejectLoneSurrogates(value: unknown): void {
  function checkString(text: string): void {
    for (let i = 0; i < text.length; i++) {
      const code = text.charCodeAt(i);
      if (code >= 0xd800 && code <= 0xdbff) {
        const next = text.charCodeAt(i + 1);
        if (!(next >= 0xdc00 && next <= 0xdfff)) throw new LoneSurrogateError("lone high surrogate");
        i++;
      } else if (code >= 0xdc00 && code <= 0xdfff) {
        throw new LoneSurrogateError("lone low surrogate");
      }
    }
  }
  if (typeof value === "string") checkString(value);
  else if (Array.isArray(value)) value.forEach(rejectLoneSurrogates);
  else if (value !== null && typeof value === "object") {
    for (const entry of Object.entries(value as Record<string, unknown>)) {
      checkString(entry[0]);
      rejectLoneSurrogates(entry[1]);
    }
  }
}

function checkSafeIntegers(value: unknown): void {
  // Safe-integer enforcement for *plain integer tokens* is performed on the
  // raw text in assertNoDuplicateKeys, mirroring Python's isinstance-int
  // check (Python parses 1e30 as float, so it is not range-checked). Here we
  // only reject non-finite values defensively.
  if (typeof value === "number") {
    if (!Number.isFinite(value)) throw new NonFiniteNumberError("non-finite number");
  } else if (Array.isArray(value)) {
    value.forEach(checkSafeIntegers);
  } else if (value !== null && typeof value === "object") {
    for (const v of Object.values(value as Record<string, unknown>)) checkSafeIntegers(v);
  }
}

export function parseStrictJson(input: Uint8Array): unknown {
  const raw = decodeUtf8Strict(input);
  assertNoDuplicateKeys(raw);
  let value: unknown;
  try {
    value = JSON.parse(raw);
  } catch (e) {
    throw new JCSError(`invalid JSON: ${String(e)}`);
  }
  rejectLoneSurrogates(value);
  checkSafeIntegers(value);
  return value;
}

export function jcsCanonicalize(input: Uint8Array): Uint8Array {
  const value = parseStrictJson(input);
  const canonicalText = canonicalize(value);
  if (typeof canonicalText !== "string") throw new JCSError("canonicalizer returned no string");
  return new TextEncoder().encode(canonicalText);
}
