# 06 — MASTER INTEGRATION MAP

## Status
TARGET ARCHITECTURE / PROPOSED.

## Purpose
Define every sanctioned path in or out of the platform, and the API/event
standards every internal service must follow, so no domain grows its own
bespoke integration code.

## Scope
Covers the Interoperability Layer (external protocols), the Payer and
Government Country Adapter frameworks, internal API conventions, and the
internal event backbone. Domain-internal commands/queries are defined in
`03-MASTER-DOMAIN-MAP.md`; this document covers only boundary-crossing
traffic.

## Current Assumptions
No domain talks to an external system directly. Every external
integration — analyzer, PACS, payer, government system, patient app,
third-party notification channel — crosses through the Interoperability
Layer, which is the only place protocol translation and validation happen.

## Evidence
UNKNOWN — REQUIRES EVIDENCE (see `01`).

## Decision

### Integration Boundary Diagram

```
   EXTERNAL WORLD
   Analyzers · PACS · Payers · Government · Patient/Clinician Apps · SMS/Email
                              |
                              v
                 INTEROPERABILITY LAYER (single choke point)
   +------------+------------+------------+------------+------------+
   | FHIR       | HL7 v2     | DICOM/     | IHE        | Country/   |
   | Gateway    | Adapter    | DICOMweb   | Profiles   | Payer      |
   | R5 (R4/R4B | ADT/ORM/   | Gateway    | XDS/PIX/   | Adapters   |
   | compat)    | ORU/MDM    |            | PDQ/XCA/   |            |
   |            |            |            | XCPD       |            |
   +------------+------------+------------+------------+------------+
                              |
                        validate → translate → route
                              |
                              v
                     APPLICATION PLANE DOMAINS
      (Clinical, Pharmacy, Laboratory, Radiology, Billing, Insurance, ...)
```

### Protocol Standards
- **FHIR** — baseline **R5**; maintain **R4/R4B** compatibility for
  external systems that haven't upgraded. R6 is tracked but never used as
  a production baseline while still in ballot status. Includes SMART on
  FHIR (app launch/scopes), CDS Hooks (advisory decision support only —
  see `AI` domain in `03`), and FHIR Structured Data Capture (SDC) for
  structured questionnaires/forms.
- **HL7 v2** — ADT (admit/discharge/transfer), ORM (orders), ORU
  (results), MDM (documents) message types, primarily for
  Hospital/Laboratory/Radiology external interfaces.
- **DICOM / DICOMweb** — imaging interchange with PACS; modality worklist,
  study/series/instance transfer. Image binaries never transit into
  PostgreSQL (see `01`, `04`).
- **IHE Profiles** — XDS (document sharing), PIX/PDQ (patient
  identity cross-referencing/query), XCA/XCPD (cross-community access) —
  adopted where a specific interoperability requirement justifies the
  added complexity, not by default.

### Government Country Adapter Framework
Each country (Jordan, Saudi Arabia, UAE, Qatar, Kuwait, Bahrain, Oman, and
others as entitled) gets an isolated adapter that owns:
- E-invoicing format and submission mechanics.
- National health system / government API integration.
- Local payer and local coding-system quirks.
- Data residency constraints specific to that jurisdiction.

**Rule:** no country-specific logic is permitted in any Global Core
domain. Adding a country means adding an adapter, not modifying Clinical,
Billing, or any other core domain. Regulatory and legal approval status
for each country is tracked in `08-MASTER-COMPLIANCE-MAP.md` and is never
assumed from the existence of an adapter.

### Payer Adapter Framework
Mirrors the Country Adapter pattern: each payer integration is a plugin
implementing a common interface (eligibility, authorization, claim
submission, remittance) behind the `Insurance` domain (`03`). No payer
name or payer-specific rule appears in Clinical Core or Billing Core.

### Internal API Conventions
- REST + OpenAPI 3.1 contracts for every internal service boundary; FHIR
  resources exposed through the FHIR Gateway follow FHIR's own contract
  rules instead.
- Errors follow RFC 9457 (Problem Details for HTTP APIs).
- Every mutating request supports an `Idempotency-Key` header.
- Every request carries a `Correlation-ID` propagated across all
  downstream calls and into the event backbone, plus a `Request-ID` for
  the single hop.
- Versioning is explicit in the URL or media type; backward compatibility
  is enforced via contract tests before any breaking change ships (see
  `15-MASTER-TESTING-STRATEGY.md`).
- Pagination and filtering follow one consistent convention across every
  service — no per-domain reinvention.
- Rate limiting is enforced at the API gateway layer, tenant-scoped.

### Internal Event Backbone
```
Business Transaction → Database Commit → Outbox Table → Relay → RabbitMQ
      → Consumer(s) → Audit / Integration / Notification / Analytics
```
- **Transactional Outbox** — an event is only ever published after its
  originating database transaction commits; no dual-write race.
- **Idempotency** — every consumer is written to safely process the same
  event more than once.
- **Retry / Backoff / DLQ** — failed consumption retries with exponential
  backoff, then lands in a dead-letter queue for manual/automated
  remediation rather than being silently dropped.
- **Correlation IDs** — every event carries the originating request's
  Correlation-ID for end-to-end tracing.
- **Event Versioning** — event schemas are versioned; consumers must
  tolerate additive changes and explicitly opt into breaking ones.

## Alternatives Considered
- **Per-domain direct external integration** (rejected) — duplicates
  validation logic, multiplies the audit surface, and makes it impossible
  to rate-limit or version external contracts consistently (see `01`
  Alternatives).
- **Synchronous point-to-point calls instead of an event backbone for
  cross-domain effects** (rejected for most cases) — creates tight runtime
  coupling between domains that should fail independently; reserved only
  for read-time composition (e.g., Patient 360 assembly), not for
  side-effecting cross-domain workflows.

## Security Impact
The Interoperability Layer is a natural place to enforce
minimum-necessary-field filtering before data leaves the platform, and to
apply rate limiting/WAF rules against external actors specifically (see
`07-MASTER-SECURITY-MAP.md`).

## Operational Impact
Every external integration's health (analyzer link, PACS link, payer
gateway, government endpoint) is a distinct monitored dependency — see
`Observability` domain in `03`.

## Performance Impact
No numbers asserted. External integrations are the most likely source of
tail latency; SLOs for each protocol adapter are defined once real
integrations exist. REQUIRES MEASUREMENT.

## Compliance Impact
FHIR/HL7/DICOM/IHE conformance is TARGET, not evidenced. Government
adapter deployment for any country REQUIRES LEGAL VERIFICATION before any
compliance claim (see `08`).

## Failure Modes
- A malformed inbound message is quarantined whole — never partially
  applied to internal state.
- An external system outage degrades to queued-retry, never to silent
  data loss.
- A breaking event-schema change without consumer opt-in is treated as an
  incident, not a routine deploy.

## Dependencies
Depends on `01`, `02`, `03`, `04`. Feeds `07`, `08`, `17` (government
e-invoicing details), `19` (technology stack confirmation).

## Unknowns
UNKNOWN — REQUIRES EVIDENCE which, if any, of these integrations exist
today in any form.

## Validation
Every external touchpoint named in any domain's "External Integrations"
field in `03` must appear in this document's protocol/adapter breakdown.
Confirmed consistent at time of writing.

## Rollback
N/A at design stage. For implementation: a new integration adapter is
additive and feature-flagged, never a hard cutover from a working
integration.

## Definition of Done
No domain has direct external-network code; every external touchpoint
routes through the Interoperability Layer as mapped above.
