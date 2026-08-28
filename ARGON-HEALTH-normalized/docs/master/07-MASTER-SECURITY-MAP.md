# 07 — MASTER SECURITY MAP

**STATUS:** TARGET ARCHITECTURE / PROPOSED
**EVIDENCE CLASS:** DESIGN

## Status
TARGET ARCHITECTURE / PROPOSED.

## Purpose
Define the platform's authentication, authorization, and security-control
baseline, and the structural separation between platform-management access
and clinical-data access.

## Scope
Covers identity, authorization enforcement, the security-standard
baseline, and Control Plane security specifically. Data-at-rest
classification is covered in `04-MASTER-DATA-MAP.md`; compliance-status
tracking against named standards is covered in `08-MASTER-COMPLIANCE-MAP.md`.

## Current Assumptions
No permission decision is ever made in the UI layer alone — UI hiding a
button is a convenience, never a security control.

## Evidence
UNKNOWN — REQUIRES EVIDENCE (see `01`).

## Decision

### Identity & Session Baseline
- OIDC/OAuth2 on top of an identity provider (Keycloak baseline) —
  central credential/session management, not per-domain auth.
- MFA mandatory for any role with PHI access; WebAuthn/passkeys supported
  where justified by device/user population.
- Sessions are short-lived tokens with server-side revocation — revoking a
  session takes effect immediately, not at next token expiry.

### Authorization Model
```
JWT  →  Tenant Context  →  Authorization Service  →  PostgreSQL RLS
```
- **RBAC** — coarse role-based grants (clinician, pharmacist, billing
  staff, Control Plane operator, etc.).
- **ABAC** — attribute-based refinement (facility scope, department scope,
  active-care-relationship requirement).
- **Relationship-based** — some decisions depend on a relationship record
  (e.g., "assigned nurse for this patient today"), not just a role.
- **Purpose of use** — sensitive reads (e.g., a Control Plane operator
  viewing PHI) require a declared purpose, logged alongside the access.
- **Break-glass** — emergency access override exists, but is itself
  authenticated, time-boxed, reason-required, and always audited — never
  a silent bypass.
- Enforcement happens at **three layers simultaneously**: the requesting
  application, a dedicated Authorization Service (see `AUTHORIZATION`
  domain in `03`), and PostgreSQL Row-Level Security as the last line of
  defense. A bug in application logic must not be sufficient to leak
  cross-tenant data if RLS is correctly configured.

### Security Standard Baseline
| Standard | Role |
|---|---|
| OWASP ASVS 5 | Application security verification baseline |
| OWASP API Security Top 10 | API-specific control checklist |
| OWASP Top 10 | General web application risk checklist |
| NIST CSF 2.0 | Organizational security function framework |
| ISO/IEC 27001:2022 / 27002:2022 | Information security management system |
| ISO 27799:2025 | Health-sector-specific application of ISO 27002 |
| IEC 81001-5-1 | Health software security lifecycle |
| ISO 14971 / IEC 62304 | Applicable only where final product classification makes them relevant (e.g., certain AI/CDS features) — applicability is UNKNOWN pending feature-level review, see `AI` domain in `03` |

Adoption of a standard as a *baseline* is a design decision, not a
compliance claim — see `08` for how each control gets evidenced.

### Security Architecture Components
Encryption (at rest and in transit) · Secrets Management/KMS · IAM ·
MFA · WAF · DDoS protection · Rate Limiting · Input Validation · API
Security (per `06`) · Supply Chain Security (SAST, DAST, dependency
scanning, secret scanning, container scanning, SBOM) · Incident Response
(see the Incident workflow in `05-MASTER-WORKFLOW-MAP.md`).

### Control Plane Security — Structural Separation
Platform Management Access and Clinical Data Access are **structurally
different privilege domains**, not just different roles under one
umbrella:
- A Control Plane operator can suspend, license, or configure a tenant
  **without** any implicit ability to read that tenant's PHI.
- High-risk Control Plane operations (global shutdown, mass organization
  change, mass PHI export, global security-policy change, production
  credential rotation) require: step-up MFA, an approval step where
  defined, a documented reason, full audit, and a rollback plan.
- Any Control Plane access to PHI (e.g., for a support ticket) happens
  only via the same break-glass mechanism used elsewhere — authenticated,
  time-boxed, reason-required, audited.

### Data Security (PostgreSQL)
RLS enforced on every tenant-scoped table · transactions for every
multi-step write · constraints/indexes reviewed per domain ·
partitioning applied only where measured need exists (not speculative) ·
PITR enabled · HA configuration for the primary OLTP store · connection
pooling to prevent connection exhaustion under load · every schema
migration versioned (Flyway or equivalent) — see `14-MASTER-TECHNOLOGY-STACK.md`.
The normal application database role can never bypass tenant isolation,
even under a bug — RLS is the backstop regardless of application-layer
correctness.

## Alternatives Considered
- **Application-layer-only authorization** (rejected) — a single bug
  becomes a cross-tenant data breach; the three-layer model (`06`
  Alternatives-style reasoning) exists specifically to avoid a single
  point of authorization failure.
- **Shared Control-Plane/Clinical role** (rejected) — collapses two
  privilege domains that must remain independently auditable per `27` in
  the originating prompt.

## Security Impact
This document IS the security impact statement for the rest of the
platform; every other master document's "Security Impact" section defers
to the model defined here.

## Operational Impact
Break-glass and step-up-MFA flows require an on-call operational process,
not just a technical capability — owned jointly by Control Plane and
Incident Response (`05` Incident workflow).

## Performance Impact
Three-layer authorization (app + service + RLS) adds latency versus a
single-layer check. No numbers asserted — REQUIRES MEASUREMENT once
implemented.

## Compliance Impact
This model is a prerequisite for most controls in `08-MASTER-COMPLIANCE-MAP.md`,
but implementing it does not itself constitute compliance with any named
standard — status tracking lives exclusively in `08`.

## Failure Modes
- Authorization Service outage must fail closed (deny), never fail open.
- A break-glass invocation with no follow-up audit review within a
  defined window is itself treated as a security incident.
- RLS misconfiguration on a new table is a release-blocking defect, not a
  follow-up ticket (see `31` Release workflow gating).

## Dependencies
Depends on `01`, `02`, `03`, `04`. Feeds `08`, `09` (Control Plane
document), `27`-equivalent detail already summarized above, `15`
(security test cases).

## Unknowns
UNKNOWN — REQUIRES EVIDENCE whether any existing identity/authorization
implementation exists to reconcile against this model.

## Validation
Every domain's "Permissions" field in `03-MASTER-DOMAIN-MAP.md` must be
expressible in terms of the RBAC/ABAC/relationship/purpose-of-use/
break-glass model defined here. Confirmed consistent at time of writing.

## Rollback
N/A at design stage. For implementation: authorization changes are always
introduced as an additive, feature-flagged tightening — a stricter rule
must never accidentally lock out an entire tenant with no rollback path.

## Definition of Done
Every sensitive operation named anywhere in `03` or `05` has an explicit
ALLOW and DENY test case defined against this model (tracked fully in
`15-MASTER-TESTING-STRATEGY.md`).
