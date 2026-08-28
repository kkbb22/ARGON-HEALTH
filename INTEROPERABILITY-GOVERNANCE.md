# INTEROPERABILITY GOVERNANCE

STATUS: PROPOSED
EVIDENCE CLASS: EXTERNAL STANDARD (FHIR version guidance per `docs/evidence/TECHNOLOGY-BASELINE-VERIFICATION.md` §10, live-researched 2026-08-27; remaining protocol detail is DESIGN)

## Purpose
For every interoperability protocol named in
`docs/master/06-MASTER-INTEGRATION-MAP.md`, define Version, Scope,
Profile, Validation, Transport, Security, Error handling, Retry, Audit,
Conformance test, and External integration rules — the operational
detail one level below `06`'s architectural summary.

## Scope
Covers FHIR, HL7 v2, DICOM/DICOMweb, IHE, SMART on FHIR, CDS Hooks, and
Terminology. Government/payer adapter-specific detail stays in `06` and
`docs/compliance/COMPLIANCE-TRACEABILITY-MATRIX.md`.

## FHIR

| Field | Value |
|---|---|
| Version | **R4/R4B — production baseline** (corrected 2026-08-27, was R5 — see ADR-018, `docs/master/19`). R5 — conditional, partner-specific only. R6 — deferred, tracked only, currently in ballot. |
| Scope | Patient, Encounter, Observation, MedicationRequest, DiagnosticReport, ImagingStudy, Claim resources at minimum, mapped from the canonical internal Clinical model (`03`) — **ARGON does not claim "ARGON uses FHIR" unqualified; FHIR is a mapping/exchange layer, not the internal source of truth.** |
| Profile | ARGON-specific FHIR profiles/extensions — not yet authored; TARGET only. |
| Validation | Every inbound/outbound FHIR resource validated against its declared profile before acceptance/transmission (`06` malformed-message quarantine rule). |
| Transport | REST (FHIR RESTful API) at the Interoperability Layer boundary (`06`). |
| Security | SMART on FHIR scopes for app-launch contexts; OAuth2/OIDC token validation shared with the platform's general Identity baseline (`07`). |
| Error handling | RFC 9457 Problem Details, consistent with `06`'s general API error convention — FHIR OperationOutcome resources used for FHIR-specific error detail within that shape. |
| Retry | Outbound FHIR submissions follow the general Interoperability Layer retry/backoff/DLQ policy (`06`). |
| Audit | Every FHIR resource access logged with correlation ID, consistent with `07`'s audit requirements for PHI access. |
| Conformance test | **Not performed.** No CapabilityStatement has been published; no conformance test suite exists. Status: TARGET/PROPOSED only. |
| External integration rules | No domain calls a FHIR API directly outside the Interoperability Layer's FHIR Gateway (`06`, `02`). |

## HL7 v2

| Field | Value |
|---|---|
| Version | HL7 v2.x (specific minor version TBD per integration partner — v2 is not centrally versioned the way FHIR is; each trading-partner interface specifies its own supported v2 version, typically 2.3–2.5.1 in practice) |
| Scope | ADT (admit/discharge/transfer), ORM (orders), ORU (results), MDM (documents) message types — `06` |
| Profile | Per-partner interface specification (a "trading partner agreement"), not a single ARGON-wide profile — this is normal for HL7 v2 and differs from FHIR's IG-based approach. |
| Validation | Message structure and required-segment validation before internal translation. |
| Transport | MLLP (Minimal Lower Layer Protocol) is the conventional v2 transport; confirmed as the assumed transport here, not yet implemented. |
| Security | Transport-level encryption (TLS) for MLLP where the partner supports it; VPN/private-network fallback where a partner requires plain MLLP (common in legacy lab/analyzer integrations). |
| Error handling | HL7 v2 ACK/NAK messages at the protocol level, mapped internally to the same quarantine/DLQ pattern as any other Interoperability Layer failure (`06`). |
| Retry | Same general retry/backoff/DLQ policy as `06`. |
| Audit | Same as FHIR row above. |
| Conformance test | Not performed — no live analyzer/lab integration exists yet. |
| External integration rules | Same single-choke-point rule as FHIR — no domain speaks raw HL7 v2 outside the Interoperability Layer's HL7 v2 Adapter. |

## DICOM / DICOMweb

| Field | Value |
|---|---|
| Version | Current DICOM standard (rolling-release, no single "version number" the way FHIR has — conformance is tracked per DICOM Conformance Statement, not a version string) |
| Scope | Modality Worklist, study/series/instance transfer, DICOMweb (WADO-RS/QIDO-RS/STOW-RS) for web-based access |
| Profile | A DICOM Conformance Statement is required before any PACS integration claim — **not yet authored, TARGET only.** |
| Validation | DICOM object structure/tag validation on ingest. |
| Transport | DICOM (C-STORE/C-FIND/C-MOVE) for classic PACS; DICOMweb (HTTP-based) for modern/cloud PACS — both supported per `06`. |
| Security | TLS for DICOMweb; DICOM-native security profiles (or VPN/private network) for classic DICOM transport. |
| Error handling | Same quarantine pattern as `06` — a failed/incomplete study transfer keeps the imaging order open rather than falsely marking it complete (`05` §8 Radiology workflow). |
| Retry | Same general Interoperability Layer policy. |
| Audit | Study access audited per `07`; image binaries never in PostgreSQL (`04`, ADR-005). |
| Conformance test | Not performed — no PACS integration exists yet. |
| External integration rules | Radiology domain (`03`) never talks to PACS directly — only through the DICOM/DICOMweb Gateway (`06`). |

## IHE Profiles (XDS, PIX/PDQ, XCA, XCPD)

| Field | Value |
|---|---|
| Version | Current IHE Technical Framework — adopted per specific interoperability need, not by default (`06`). |
| Scope | XDS (document sharing), PIX/PDQ (patient identity cross-referencing), XCA/XCPD (cross-community access) — used only where a specific external requirement (e.g., a national health information exchange) demands it. |
| Profile | Per-IHE-Actor conformance, TARGET only — not yet authored. |
| Validation | Per IHE Technical Framework transaction validation rules. |
| Transport | SOAP/HTTP per the specific IHE profile's transaction spec. |
| Security | IHE ATNA (Audit Trail and Node Authentication) profile — TARGET, not yet adopted in any implementation. |
| Error handling | Same general pattern as other protocols. |
| Retry | Same general policy. |
| Audit | ATNA-aligned audit trail, once adopted — currently just the general `07` audit baseline. |
| Conformance test | Not performed. |
| External integration rules | Adopted only when a real government/HIE integration requires it (Phase 6 trigger, `docs/master/20`) — never adopted speculatively. |

## SMART on FHIR

| Field | Value |
|---|---|
| Version | SMART App Launch 2.2 (`docs/master/14`) |
| Scope | App-launch authorization flow for third-party or first-party clinical apps needing scoped FHIR access. |
| Profile | Standard SMART scopes (`patient/*.read`, etc.), refined per ARGON's Authorization model (`07`). |
| Validation | OAuth2 token/scope validation at launch. |
| Transport | HTTPS, standard OAuth2 redirect flow. |
| Security | Shares the platform's Identity baseline (`07`) — SMART tokens are scoped, time-limited, revocable via the same session-revocation mechanism as any other session. |
| Error handling | Standard OAuth2 error responses. |
| Retry | N/A — interactive auth flow, not a retryable batch operation. |
| Audit | App-launch events audited like any authentication event (`07`). |
| Conformance test | Not performed. |
| External integration rules | Only third-party apps explicitly entitled via the Organization's module/integration configuration (`09`, `11`) may SMART-launch against a tenant's data. |

## CDS Hooks

| Field | Value |
|---|---|
| Version | CDS Hooks 2.0.1 (`docs/master/14`) |
| Scope | Advisory clinical decision support only — never autonomous action (`AI` domain, `03`; `docs/master/16` hazard-model discipline). |
| Profile | Hook-specific (e.g., `patient-view`, `order-select`) per CDS Hooks spec. |
| Validation | Card-response structure validation. |
| Transport | HTTPS REST. |
| Security | Same Identity/session baseline as the rest of the platform. |
| Error handling | A CDS Hooks service failure must degrade to "no advisory shown," never block the underlying clinical workflow (`AI` domain failure-mode rule, `03`). |
| Retry | Not retried if it would delay clinical workflow — CDS Hooks calls are advisory and time-boxed; a slow/failed call is simply skipped for that interaction. |
| Audit | Every recommendation issued is logged with model/service version (`AI` domain, `03`). |
| Conformance test | Not performed. |
| External integration rules | CDS services are entitled per Organization like any other integration (`09`). |

## Terminology (SNOMED CT, ICD, LOINC, UCUM, ATC)

| Field | Value |
|---|---|
| Version | Tracked per CodeSystem, versioned explicitly — no single "terminology version" (`Terminology` domain, `03`). |
| Scope | Diagnosis coding (SNOMED CT/ICD), lab result coding (LOINC), units (UCUM), drug coding (ATC) — `03`. |
| Profile | ValueSets/ConceptMaps authored per ARGON's actual clinical scope — not yet authored, TARGET only. |
| Validation | Code validated against its declared CodeSystem version before acceptance into a finalized clinical record (`Terminology` domain DoD, `03`). |
| Transport | N/A — internal reference data service, not an external protocol. |
| Security | Reference data, not PHI — standard platform data-classification handling (`04`). |
| Error handling | An unrecognized/unpublished code is rejected at entry, not silently accepted (`03` Terminology domain Failure Modes). |
| Retry | N/A. |
| Audit | CodeSystem import/publish events logged (`03`). |
| Conformance test | Not performed. |
| External integration rules | Licensing for each terminology source (especially SNOMED CT) **REQUIRES LEGAL VERIFICATION** before use — ARGON does not redistribute proprietary datasets without valid rights (`03` Terminology domain, `docs/master/06` original constraint). |

## Alternatives Considered
- **One combined table for all protocols** (rejected) — the fields mean
  materially different things per protocol (e.g., "Version" for FHIR is a
  clean single string; for HL7 v2 and DICOM it's fundamentally
  per-partner/per-conformance-statement) — collapsing them would either
  be misleading or force artificial uniformity.

## Dependencies
Depends on `docs/master/06`, `docs/master/03` (`Terminology`, `AI`
domains), `docs/master/07`, `docs/master/14`,
`docs/evidence/TECHNOLOGY-BASELINE-VERIFICATION.md` §10. Feeds
`docs/compliance/COMPLIANCE-TRACEABILITY-MATRIX.md` (terminology
licensing row) and `docs/governance/ARCHITECTURE-STATUS.md`.

## Unknowns
UNKNOWN — no conformance test has been performed for any protocol above;
every "Conformance test: Not performed" line is the accurate current
state, not a gap hidden by this document.

## Definition of Done
Every protocol named in `docs/master/06-MASTER-INTEGRATION-MAP.md`'s
Protocol Standards section has a full row-set above with no field left
blank; conformance testing itself is explicitly deferred to
implementation phases (`docs/master/20`), not claimed here.
