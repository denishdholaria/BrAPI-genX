#!/usr/bin/env bun
/** Shared golden vectors for an RFC 8785 candidate. Does not ratify BrAPI D-02. */
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import canonicalize from "canonicalize";

type Vector = { id: string; inputJson: string; expectedCanonicalUtf8: string; expectedSha256: string };
type Corpus = {
  structuredJsonVectors: Vector[];
  exactByteVectors: Array<{ id: string; inputUtf8: string; expectedSha256: string }>;
  rejectionVectors: Array<{ id: string; inputJson: string; reasonClass: string; reason: string }>;
  legacyDiagnostics: Array<{ id: string; inputJson: string; typescriptLegacyCanonicalUtf8: string; pythonLegacyCanonicalUtf8: string }>;
};

const defaultCorpusPath = new URL("../../Specification/BrAPI-GenX/Conformance/digest-vectors.json", import.meta.url);
const corpusOverride = Bun.argv.slice(2).find((arg) => arg.startsWith("--corpus="))?.slice("--corpus=".length);
const corpusText = readFileSync(corpusOverride ?? defaultCorpusPath, "utf8");
const corpus = JSON.parse(corpusText) as Corpus;
const failures: string[] = [];
const SHA256_PATTERN = /^[0-9a-f]{64}$/;
const REQUIRED_VECTOR_IDS: Array<{ section: keyof Corpus; ids: string[] }> = [
  { section: "structuredJsonVectors", ids: [
    "object-key-order-and-whitespace", "unicode-escaped-input-canonical-unescaped-output",
    "nested-objects-arrays-null-booleans", "string-escaping", "utf16-property-order",
    "number-serialization-and-negative-zero", "exact-scientific-decimal-represented-as-string",
    "unicode-composed-form-preserved", "unicode-decomposed-form-preserved-without-normalization",
    "empty-object", "empty-array", "safe-integer-interoperability-boundary",
  ] },
  { section: "exactByteVectors", ids: ["http-body-whitespace-preserved", "http-body-key-order-preserved"] },
  { section: "rejectionVectors", ids: [
    "duplicate-property-name", "duplicate-property-name-after-unescaping", "non-json-nan-token",
    "lone-unicode-surrogate", "integer-outside-safe-interoperability-range",
  ] },
  { section: "legacyDiagnostics", ids: ["non-ascii-escaping", "unicode-property-order"] },
];
for (const entry of REQUIRED_VECTOR_IDS) {
  const vectors = corpus[entry.section] as Array<{ id: string }>;
  const present = new Set(vectors.map((vector) => vector.id));
  for (const requiredId of entry.ids) {
    if (!present.has(requiredId)) failures.push(entry.section + ": missing required vector " + requiredId);
  }
  if (present.size !== vectors.length) failures.push(entry.section + ": duplicate vector IDs");
}
const allIds = [
  ...corpus.structuredJsonVectors, ...corpus.exactByteVectors,
  ...corpus.rejectionVectors, ...corpus.legacyDiagnostics,
].map((vector) => vector.id);
if (new Set(allIds).size !== allIds.length) failures.push("vector IDs must be unique across the whole corpus");
for (const vector of [...corpus.structuredJsonVectors, ...corpus.exactByteVectors]) {
  if (!SHA256_PATTERN.test(vector.expectedSha256)) failures.push(vector.id + ": malformed lowercase SHA-256 value");
}
for (const vector of corpus.rejectionVectors) {
  if (!["jcs-input-constraint", "invalid-json-syntax", "candidate-profile-hardening"].includes(vector.reasonClass)) {
    failures.push(vector.id + ": unknown rejection reasonClass");
  }
  if (typeof vector.reason !== "string" || !vector.reason.trim()) failures.push(vector.id + ": missing rejection rationale");
}

function sha256(text: string): string {
  return createHash("sha256").update(text, "utf8").digest("hex");
}
function skipWhitespace(raw: string, position: { value: number }): void {
  while (position.value < raw.length && /\s/.test(raw[position.value])) position.value++;
}
function parseStringToken(raw: string, position: { value: number }): string {
  const start = position.value;
  if (raw[position.value] !== '"') throw new Error("expected JSON string");
  position.value++;
  while (position.value < raw.length) {
    const char = raw[position.value++];
    if (char === "\\") {
      if (position.value >= raw.length) throw new Error("unterminated escape");
      position.value++;
    } else if (char === '"') {
      return JSON.parse(raw.slice(start, position.value)) as string;
    }
  }
  throw new Error("unterminated JSON string");
}
/** Detect duplicate keys before JSON.parse discards that information. */
function assertNoDuplicateKeys(raw: string): void {
  const p = { value: 0 };
  function value(): void {
    skipWhitespace(raw, p);
    const char = raw[p.value];
    if (char === '"') {
      parseStringToken(raw, p);
      return;
    }
    if (char === "{") {
      p.value++;
      skipWhitespace(raw, p);
      const keys = new Set<string>();
      if (raw[p.value] === "}") { p.value++; return; }
      while (p.value < raw.length) {
        skipWhitespace(raw, p);
        const key = parseStringToken(raw, p);
        if (keys.has(key)) throw new Error("duplicate JSON property: " + key);
        keys.add(key);
        skipWhitespace(raw, p);
        if (raw[p.value++] !== ":") throw new Error("expected colon");
        value();
        skipWhitespace(raw, p);
        const separator = raw[p.value++];
        if (separator === "}") return;
        if (separator !== ",") throw new Error("expected comma or object close");
      }
      throw new Error("unterminated JSON object");
    }
    if (char === "[") {
      p.value++;
      skipWhitespace(raw, p);
      if (raw[p.value] === "]") { p.value++; return; }
      while (p.value < raw.length) {
        value();
        skipWhitespace(raw, p);
        const separator = raw[p.value++];
        if (separator === "]") return;
        if (separator !== ",") throw new Error("expected comma or array close");
      }
      throw new Error("unterminated JSON array");
    }
    const start = p.value;
    while (p.value < raw.length && !/[\s,\]}]/.test(raw[p.value])) p.value++;
    if (p.value === start) throw new Error("expected JSON value");
    const token = raw.slice(start, p.value);
    if (token === "true" || token === "false" || token === "null") return;
    if (!/^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?$/.test(token)) {
      throw new Error("invalid JSON primitive token");
    }
    // Reject plain integer tokens that JavaScript would silently round during JSON.parse.
    if (/^-?(?:0|[1-9]\d*)$/.test(token)) {
      const integer = BigInt(token);
      const maxSafeInteger = 9007199254740991n;
      if (integer > maxSafeInteger || integer < -maxSafeInteger) {
        throw new Error("integer outside I-JSON safe interoperability range");
      }
    }
  }
  value();
  skipWhitespace(raw, p);
  if (p.value !== raw.length) throw new Error("trailing content after JSON value");
}
function rejectLoneSurrogates(value: unknown): void {
  function checkString(text: string): void {
    for (let index = 0; index < text.length; index++) {
      const code = text.charCodeAt(index);
      if (code >= 0xd800 && code <= 0xdbff) {
        const next = text.charCodeAt(index + 1);
        if (!(next >= 0xdc00 && next <= 0xdfff)) throw new Error("lone high surrogate");
        index++;
      } else if (code >= 0xdc00 && code <= 0xdfff) {
        throw new Error("lone low surrogate");
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
function parseStrict(raw: string): unknown {
  assertNoDuplicateKeys(raw);
  const value: unknown = JSON.parse(raw);
  rejectLoneSurrogates(value);
  return value;
}
function legacyTsCanonical(value: unknown): string {
  if (value === null || typeof value !== "object") return JSON.stringify(value);
  if (Array.isArray(value)) return "[" + value.map(legacyTsCanonical).join(",") + "]";
  const record = value as Record<string, unknown>;
  const fields = Object.keys(record).sort().map((key) => JSON.stringify(key) + ":" + legacyTsCanonical(record[key]));
  return "{" + fields.join(",") + "}";
}
let structuredCount = 0;
let exactCount = 0;
let rejectionCount = 0;
let legacyCount = 0;

for (const vector of corpus.structuredJsonVectors) {
  try {
    const canonicalText = canonicalize(parseStrict(vector.inputJson));
    if (typeof canonicalText !== "string") throw new Error("canonicalizer returned no string");
    if (canonicalText !== vector.expectedCanonicalUtf8) failures.push(vector.id + ": canonical UTF-8 differs");
    const digest = sha256(canonicalText);
    if (digest !== vector.expectedSha256) failures.push(vector.id + ": SHA-256 differs (" + digest + ")");
    structuredCount++;
  } catch (error) {
    failures.push(vector.id + ": unexpected rejection/error: " + String(error));
  }
}
for (const vector of corpus.exactByteVectors) {
  const digest = sha256(vector.inputUtf8);
  if (digest !== vector.expectedSha256) failures.push(vector.id + ": exact-byte SHA-256 differs (" + digest + ")");
  exactCount++;
}
for (const vector of corpus.rejectionVectors) {
  try {
    const canonicalText = canonicalize(parseStrict(vector.inputJson));
    if (typeof canonicalText !== "string") throw new Error("canonicalizer returned no string");
  } catch {
    rejectionCount++;
    continue;
  }
  failures.push(vector.id + ": rejection-policy input was accepted");
}
for (const vector of corpus.legacyDiagnostics) {
  try {
    const actual = legacyTsCanonical(parseStrict(vector.inputJson));
    if (actual !== vector.typescriptLegacyCanonicalUtf8) failures.push(vector.id + ": TypeScript legacy diagnostic changed: " + actual);
    if (actual === vector.pythonLegacyCanonicalUtf8) failures.push(vector.id + ": expected legacy divergence disappeared");
    legacyCount++;
  } catch (error) {
    failures.push(vector.id + ": legacy diagnostic error: " + String(error));
  }
}
if (failures.length) {
  console.error("FAIL digest interoperability vectors");
  failures.forEach((failure) => console.error(" - " + failure));
  process.exit(1);
}
console.log("PASS digest interoperability vectors: " + structuredCount + " structured JCS candidates, " +
  exactCount + " exact-byte cases, " + rejectionCount + " rejection-policy cases, " + legacyCount + " known legacy divergences");
console.log("NOTE: RFC 8785 is evaluated as a candidate only; BrAPI decision D-02 remains open.");
