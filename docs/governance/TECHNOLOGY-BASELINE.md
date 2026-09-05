# TECHNOLOGY BASELINE (GOVERNANCE)

STATUS: PROPOSED
EVIDENCE CLASS: EXTERNAL STANDARD (live-researched vendor/standards sources, 2026-08-27, for the items marked "verified"; DESIGN for items carried forward without independent re-verification this pass)

## Purpose
Single authoritative governance-level decision table for every
technology named across the repository, using the
ADOPT / CONDITIONAL / DEFERRED / REJECTED / SUPERSEDED vocabulary. This
document is the governance-layer counterpart to
`docs/master/14-MASTER-TECHNOLOGY-STACK.md` (architecture-narrative form)
and is backed by `docs/evidence/TECHNOLOGY-BASELINE-VERIFICATION.md`
(full research detail). Where the three documents could drift, this one
and `14` are kept in lockstep; `docs/evidence/` is the append-only
research log neither is meant to duplicate in full.

## Status Vocabulary
- **ADOPT** — current baseline, use for new work.
- **CONDITIONAL** — usable only in a specifically scoped circumstance,
  named per row.
- **DEFERRED** — consciously not adopted yet; a revisit trigger is named.
- **REJECTED** — evaluated and explicitly not adopted, with reason.
- **SUPERSEDED** — was previously ADOPT, replaced by a later decision;
  kept in the table for history, never deleted.

*(2026-08-27, second pass: the "Continuous Improvement" governance task
uses a parallel vocabulary — RETAIN/UPGRADE/CONDITIONAL/DEFER/REJECT/
REQUIRES BENCHMARK. These map directly onto the vocabulary above:
RETAIN=ADOPT-unchanged, UPGRADE=ADOPT-with-a-version-bump,
DEFER=DEFERRED, REJECT=REJECTED, REQUIRES BENCHMARK=CONDITIONAL pending
a performance-governance measurement per
`docs/governance/PERFORMANCE-GOVERNANCE.md`. One vocabulary is used
throughout this document rather than mixing both.)*

## Backend

| Technology | Status | Reason / Revisit Trigger | Verified 2026-08-27? |
|---|---|---|---|
| Java 25 LTS (OpenJDK distribution) | ADOPT | Current LTS; OpenJDK avoids Oracle NFTC licensing exposure | Yes |
| Java 21 LTS | CONDITIONAL | Fallback only if a specific dependency hasn't certified Java 25 | Yes |
| Spring Boot 4.1.x | ADOPT | Current OSS-supported line; 3.x is EOL-adjacent | Yes |
| Spring Boot 3.x | SUPERSEDED | Progressively reaching EOL (3.4 EOL'd Dec 2025) | Yes |
| Spring Framework 7.x | ADOPT | Paired with Spring Boot 4.1 | Yes |
| Spring Modulith 2.1.x | ADOPT | Enforces domain-module boundaries at build time | No — carried forward |
| Gradle 9.x | ADOPT | No change | No — carried forward |

## Database

| Technology | Status | Reason / Revisit Trigger | Verified 2026-08-27? |
|---|---|---|---|
| PostgreSQL 18.x | ADOPT | Current major, patch 18.6; AIO, OAuth auth, `uuidv7()` all directly useful | Yes |
| PostgreSQL 16 / 17 | SUPERSEDED | Not the current major; PostgreSQL 14 reaches end-of-fixes Nov 12, 2026 (unrelated version, cited as a concrete EOL example) | Yes |
| PostgreSQL 19 | DEFERRED | In Beta as of Aug 2026 — revisit after GA + one patch cycle | Yes |

## Identity

| Technology | Status | Reason / Revisit Trigger | Verified 2026-08-27? |
|---|---|---|---|
| Keycloak (containerized on Cloud Run) | ADOPT | No Kubernetes-exclusive feature required; runs statelessly against external Cloud SQL | Partial — hosting model reasoned, not independently deep-researched |
| OIDC / OAuth2 | ADOPT | Baseline protocol | No — carried forward |
| MFA | ADOPT | Mandatory for any PHI-access role | No — carried forward |
| WebAuthn / Passkeys | CONDITIONAL | Where device/user population justifies it | No — carried forward |

## Data

| Technology | Status | Reason / Revisit Trigger | Verified 2026-08-27? |
|---|---|---|---|
| Redis (Memorystore) | ADOPT | Cache/queue backing only, never source of truth | No — carried forward |
| Cloud Storage | ADOPT | Object storage for documents/DICOM/backups | No — carried forward |

## Messaging

| Technology | Status | Reason / Revisit Trigger | Verified 2026-08-27? |
|---|---|---|---|
| Google Cloud Pub/Sub | **ADOPT (primary)** | GCP-native, zero broker ops, no evidenced need for RabbitMQ/Kafka-class ordering/replay — full detail `docs/adr/ADR-MESSAGING-PLATFORM.md` | Yes |
| RabbitMQ | **CONDITIONAL** | AMQP-only external adapters only, never the internal domain backbone | Yes |
| Apache Kafka | **REJECTED (current stage)** | No evidenced log-scale replay/throughput requirement | Yes |

## Cloud

| Technology | Status | Reason / Revisit Trigger | Verified 2026-08-27? |
|---|---|---|---|
| GCP | ADOPT | Primary cloud provider | No — carried forward |
| Cloud Run | **ADOPT (re-confirmed)** | Modular-monolith-first; no measured autoscaling ceiling reached | Yes (re-confirmed, not changed) |
| GKE | **CONDITIONAL/REJECTED (current stage)** | Not adopted merely because "enterprise systems use Kubernetes"; requires an evidence-backed ADR to activate | Yes (re-confirmed) |
| Cloud SQL | ADOPT | Managed PostgreSQL | No — carried forward |
| Memorystore | ADOPT | Managed Redis | No — carried forward |
| Cloud Storage | ADOPT | Object storage | No — carried forward |
| Secret Manager, KMS | ADOPT | Secrets/encryption | No — carried forward |
| Cloud Armor | ADOPT | Edge WAF/DDoS | No — carried forward |
| Cloudflare | CONDITIONAL | Where justified over Cloud Armor alone (e.g., global edge caching) — not independently re-verified this pass | No — carried forward |
| Terraform | **SUPERSEDED** | BSL 1.1 license (not OSI), IBM-owned since Dec 2024 | Yes |
| OpenTofu | **ADOPT (replaces Terraform)** | OSI-approved MPL 2.0, native state encryption, Linux Foundation governance — full detail `docs/evidence/TECHNOLOGY-BASELINE-VERIFICATION.md` §6 | Yes |

## Observability

| Technology | Status | Reason / Revisit Trigger | Verified 2026-08-27? |
|---|---|---|---|
| OpenTelemetry / OTLP | ADOPT | Vendor-neutral telemetry standard | No — carried forward |
| Grafana Cloud (managed) | **CONDITIONAL — lower confidence** | Leans ADOPT on single-team-operability grounds but not independently re-verified to the same depth as other items this pass; do not promote to ADOPT without a dedicated research pass | Partial (reasoned, not deep-researched) |
| Self-hosted Grafana/Loki/Tempo/Prometheus | CONDITIONAL | Fallback if managed cost-at-scale evidence disfavors Grafana Cloud once real telemetry volume exists | Partial |

## Web

| Technology | Status | Reason / Revisit Trigger | Verified 2026-08-27? |
|---|---|---|---|
| Next.js 16.x (16.3 line) | ADOPT | Current stable, 16.3.3 security-patched as of Aug 25, 2026 | Yes |
| React | ADOPT | Paired with Next.js | No — carried forward |
| TypeScript | ADOPT | Web + mobile | No — carried forward |

## Mobile

| Technology | Status | Reason / Revisit Trigger | Verified 2026-08-27? |
|---|---|---|---|
| React Native (0.87.x, tracked line) | ADOPT | Current as of Aug 2026; platform tracks a *line*, not a frozen patch, per the Managed Upgrade Policy | Yes |
| React Native 1.0 (future) | DEFERRED | Revisit the whole mobile-stack stability assumption at 1.0 GA | Yes (as a named trigger) |

## Healthcare Interoperability

| Technology | Status | Reason / Revisit Trigger | Verified 2026-08-27? |
|---|---|---|---|
| **FHIR R4/R4B** | **ADOPT (corrected — was R5)** | Regulatory-baseline-aligned (US Core remains R4); full detail `docs/adr/` cross-reference to ADR-018 in `19` | Yes |
| **FHIR R5** | **CONDITIONAL (corrected — was baseline)** | Adopted only per specific partner requirement; independently described as having limited real-world adoption | Yes |
| FHIR R6 | DEFERRED | Still in ballot (first full ballot May 2026); not production-adoptable until final stable | Yes |
| SMART on FHIR 2.2 | ADOPT | App-launch/scopes standard | No — carried forward |
| CDS Hooks 2.0.1 | ADOPT | Advisory-only decision support | No — carried forward |
| FHIR SDC 4.0 | ADOPT | Structured data capture | No — carried forward |
| HL7 v2 | ADOPT | Legacy ADT/ORM/ORU/MDM messaging | No — carried forward |
| DICOM / DICOMweb | ADOPT | Imaging interchange | No — carried forward |
| IHE profiles | ADOPT | Adopted per specific interoperability need, not by default | No — carried forward |
| SNOMED CT, ICD, LOINC, UCUM, ATC | ADOPT | Terminology; licensing per source REQUIRES LEGAL VERIFICATION | No — carried forward |

## Security Standards

| Standard | Status | Reason / Revisit Trigger | Verified 2026-08-27? |
|---|---|---|---|
| OWASP ASVS 5 | ADOPT (baseline reference) | Application security verification checklist — adoption of a standard as baseline is not a compliance claim | No — carried forward |
| OWASP API Security Top 10 | ADOPT (baseline reference) | | No — carried forward |
| NIST CSF 2.0 | ADOPT (baseline reference) | | No — carried forward |
| ISO/IEC 27001:2022 / 27002:2022 | ADOPT (baseline reference) | | No — carried forward |
| ISO 27799:2025 | ADOPT (baseline reference) | Health-sector overlay | No — carried forward |
| IEC 81001-5-1 | ADOPT (baseline reference) | Health software security lifecycle | No — carried forward |
| ISO 14971 / IEC 62304 | CONDITIONAL | Applicable only where final product/feature classification requires it — UNKNOWN pending that classification | No — carried forward |

## Accessibility

| Standard | Status | Reason / Revisit Trigger | Verified 2026-08-27? |
|---|---|---|---|
| WCAG 2.2 AA | **ADOPT (re-verified 2026-08-27)** | Confirmed current W3C Recommendation; WCAG 3.0 remains a Working Draft only, final Recommendation not expected before 2028-2030 — no change needed | **Yes** |
| ISO 9241-210 | ADOPT (process principle) | Human-centered design process, not a deliverable | No — carried forward |

## API Standards

| Standard | Status | Reason / Revisit Trigger | Verified 2026-08-27? |
|---|---|---|---|
| OpenAPI | ADOPT | Contract format for internal APIs | No — carried forward |
| RFC 9457 (Problem Details) | ADOPT | Error response shape | No — carried forward |
| OAuth2 security practices | ADOPT | Baseline | No — carried forward |

## Payments

| Standard | Status | Reason / Revisit Trigger | Verified 2026-08-27? |
|---|---|---|---|
| PCI DSS (current applicable baseline) | **CONDITIONAL — version now specific: PCI DSS 4.0.1** (re-verified 2026-08-27; 4.0.1 is the only active version, all future-dated requirements mandatory since March 31, 2025) | Payments domain design already tokenizes/avoids raw card storage; PCI scope assessment against v4.0.1 REQUIRES an independent review not performed in this pass | **Yes (version), No (scope assessment itself)** |
| Tokenization / PSP integration | ADOPT (design principle) | No raw card data touches ARGON's own data plane | No — carried forward |

## Dependencies
Backed by `docs/evidence/TECHNOLOGY-BASELINE-VERIFICATION.md` (research
detail) and `docs/adr/ADR-MESSAGING-PLATFORM.md` (messaging full ADR).
Mirrored in narrative form in `docs/master/14-MASTER-TECHNOLOGY-STACK.md`.
Feeds `docs/governance/ARCHITECTURE-STATUS.md`'s Technology Component
Status Board and `docs/governance/VERSION-MANAGEMENT-POLICY.md`.

## Unknowns
Every row marked "No — carried forward" or "Partial" was not
independently re-verified against live sources during the 2026-08-27
pass — these remain at their prior confidence level, not elevated by
this document's existence. Grafana Cloud and Cloudflare rows are
explicitly flagged CONDITIONAL/lower-confidence for this reason and
should not be read as equivalent in rigor to the Messaging, FHIR,
OpenTofu, Java, Spring Boot, PostgreSQL, Next.js, or React Native rows.

## Definition of Done
Every technology named anywhere in `docs/master/14` or elsewhere in the
repository appears in exactly one table above with a real status — no
technology is left undecided without an explicit DEFERRED/CONDITIONAL
marking and a stated revisit trigger.
