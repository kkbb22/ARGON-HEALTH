# Technology Baseline — Governance Layer

**STATUS:** ACTIVE (governance index, not itself a new decision)
**EVIDENCE CLASS:** DESIGN

## Purpose
This file is the **governance-level entry point** into ARGON's
technology baseline. It does not repeat the full decision tables — those
live in `docs/master/14-MASTER-TECHNOLOGY-STACK.md` — or the underlying
research — that lives in
`docs/evidence/TECHNOLOGY-BASELINE-VERIFICATION.md`. This file exists so
"what's the current baseline and who decided it" has one short answer
before drilling into either of those.

## Authority Chain
```
docs/governance/TECHNOLOGY-BASELINE.md   (you are here — index/policy)
        ↓ points to
docs/master/14-MASTER-TECHNOLOGY-STACK.md (the decision: ADOPT/CONDITIONAL/DEFERRED/REJECTED)
        ↓ backed by
docs/evidence/TECHNOLOGY-BASELINE-VERIFICATION.md (the live research behind each decision)
        ↓ formalized as
docs/master/19-MASTER-ARCHITECTURAL-DECISIONS.md + docs/adr/ (ADR log)
```

## Status Categories (as used throughout `14`)
| Category | Meaning |
|---|---|
| **ADOPT** | Current target baseline; use this unless an ADR supersedes it |
| **RETAIN** | Re-confirmed against an alternative; no change |
| **CONDITIONAL** | Adopted only for a specific, named circumstance — not the default path |
| **DEFERRED** | Tracked, not adopted; revisit when its trigger condition occurs |
| **REJECTED** | Actively decided against for the current stage, with a stated reason |
| **SUPERSEDED** | Was previously ADOPT/RETAIN; a later ADR changed the decision |

## Current Baseline Summary (see `14` for full tables + rationale)
- **Backend:** Java 25 LTS, Spring Boot 4.1.x, Spring Framework 7, Spring
  Modulith 2.1.x, Gradle 9.x — all ADOPT.
- **Database:** PostgreSQL 18.x — ADOPT.
- **Messaging:** Google Cloud Pub/Sub — ADOPT (primary, ADR-016);
  RabbitMQ — CONDITIONAL (AMQP adapters only); Kafka — REJECTED (current
  stage).
- **IaC:** OpenTofu — ADOPT (ADR-017, replaces Terraform).
- **Interoperability:** FHIR R4/R4B — ADOPT (production baseline,
  ADR-018); FHIR R5 — CONDITIONAL (specific partner requirement only);
  FHIR R6 — DEFERRED (still in ballot).
- **Identity:** Keycloak on Cloud Run — ADOPT.
- **Cloud:** GCP, Cloud Run, Cloud SQL, Memorystore, Cloud Storage,
  Secret Manager, Cloud KMS — ADOPT. GKE — not adopted, re-confirmed
  against Cloud Run. Cloud Armor / Cloudflare — CONDITIONAL.
- **Observability:** OpenTelemetry — ADOPT. Grafana Cloud (managed) —
  CONDITIONAL, lower confidence, flagged for a dedicated research pass.
- **Web/Mobile:** Next.js 16.x, React, TypeScript, React Native 0.87.x —
  ADOPT.
- **Security standards:** governed by `docs/master/07-MASTER-SECURITY-MAP.md`
  (OWASP ASVS/API Security Top 10, NIST CSF, ISO 27001/27002/27799,
  IEC 81001-5-1, ISO 14971/IEC 62304 where applicable) — not duplicated
  here.
- **Accessibility:** WCAG 2.2 AA, ISO 9241-210 — governed by
  `docs/master/15-MASTER-TESTING-STRATEGY.md` and
  `docs/master/12-MASTER-APPLICATION-ARCHITECTURE.md`.
- **API standards:** OpenAPI, RFC 9457 Problem Details — governed by
  `docs/master/06-MASTER-INTEGRATION-MAP.md`.
- **Payments:** PCI DSS applicable baseline, tokenization/PSP strategy —
  **UNKNOWN — REQUIRES EVIDENCE**; not yet given a dedicated decision
  record. Tracked as a governance gap, not silently assumed.

## Version Pinning Policy
A target baseline (e.g., "Java 25 LTS") is not a frozen pin. Exact patch
versions are pinned only at implementation time, per
`docs/governance/VERSION-MANAGEMENT-POLICY.md`. Nothing in this
repository should ever be read as "implementation must use exactly
version X.Y.Z" — that specificity belongs to a build file, not an
architecture document.

## Open Item
The backend language/framework choice (Java/Spring Boot) is **recorded
as unreconciled** against a separate, earlier architecture consultation
for this same project (ADR-014, `docs/master/19`). This governance
document does not resolve that — see
`docs/audit/ARCHITECTURE-CONSISTENCY-AUDIT.md` Finding AUDIT-001.
