# 14 — MASTER TECHNOLOGY STACK

STATUS: PROPOSED
EVIDENCE CLASS: DESIGN

## Status
TARGET ARCHITECTURE / PROPOSED. Every version below is a baseline target,
not a frozen pin — see the Managed Upgrade Policy.

## Purpose
Record the specific technology baseline this master foundation targets,
so every other document references consistent names and versions.

## Scope
Covers language/framework/database/frontend/interoperability/observability/
infrastructure choices. Rationale for the higher-level architectural
decisions each of these serves lives in the respective master document
(e.g., why PostgreSQL is source-of-truth is in `01`/`04`, not repeated
here).

## Current Assumptions
A version is a target, evaluated against a managed upgrade policy — it is
never treated as evidence that any implementation matching it exists.

## Evidence
UNKNOWN — REQUIRES EVIDENCE for repository/implementation state (see
`01`). **Updated 2026-08-27**: every version/technology below has now
been through a fresh verification pass against live sources — see
`docs/evidence/TECHNOLOGY-BASELINE-VERIFICATION.md`. The `Status` column
in each table below records the outcome (ADOPT / RETAIN / CONDITIONAL /
DEFERRED / REJECTED) per that verification; it is a documentation
finding, not a claim that any implementation exists.

## Decision

### Backend
| Component | Target | Status | Notes |
|---|---|---|---|
| Language runtime | Java 25 LTS (OpenJDK distribution) | ADOPT | Confirmed current LTS; use Temurin/Corretto, not Oracle JDK, to avoid NFTC licensing window exposure — verification §1 |
| Application framework | Spring Boot 4.1.x | ADOPT | Confirmed current; Spring Boot 3.x is now EOL-adjacent — verification §2 |
| Core framework | Spring Framework 7 | ADOPT | Paired with Spring Boot 4.1 |
| Modularity | Spring Modulith 2.1.x | ADOPT | Enforces the modular-monolith boundary from `13` at the code level — module boundaries mirror `03`'s domain boundaries |
| Build tool | Gradle 9.x | ADOPT | Unchanged |

### Data
| Component | Target | Status | Notes |
|---|---|---|---|
| Primary datastore | PostgreSQL 18.x | ADOPT | Confirmed current major, patch 18.6 — verification §3 |
| Migrations | Flyway | ADOPT | Every schema change versioned, `07` |
| Cache / queue backing | Redis | ADOPT | Never source of truth, `04` |
| Messaging (primary) | **Google Cloud Pub/Sub** | **ADOPT (changed 2026-08-27)** | Primary internal event backbone, `06`; domain layer depends on an abstraction, not the Pub/Sub SDK directly — verification §5 |
| Messaging (conditional) | RabbitMQ | CONDITIONAL | AMQP-only external adapters only, not the internal backbone — verification §5 |
| Messaging (rejected) | Apache Kafka | REJECTED (current stage) | No evidenced need for log-scale replay/throughput — verification §5 |
| Identity provider | Keycloak (on Cloud Run) | ADOPT | OIDC/OAuth2 baseline, `07`; hosting clarified as a Cloud Run container, not GKE — verification §8 |

### Frontend
| Component | Target | Status | Notes |
|---|---|---|---|
| Web framework | Next.js 16.x (16.3 line) | ADOPT | `12`; verification §4 |
| UI library | React | ADOPT | `12` |
| Mobile | React Native (0.87.x, tracked line) | ADOPT | `12`; version made explicit — verification §4 |
| Language | TypeScript | ADOPT | Web + mobile |

### Interoperability & Terminology
| Component | Target | Status | Notes |
|---|---|---|---|
| FHIR (production) | **R4/R4B** | **ADOPT (corrected 2026-08-27)** | Regulatory-baseline-aligned; was previously stated as R5-primary — this was a documentation error, corrected per verification §10 |
| FHIR (transitional) | R5 | CONDITIONAL | Adopted only where a specific integration partner requires it — verification §10 |
| FHIR (future) | R6 | DEFERRED | Tracked only; still in ballot as of this verification, not production-adoptable — verification §10 |
| SMART on FHIR | 2.2 | ADOPT | `06` |
| Clinical decision support | CDS Hooks | ADOPT | Advisory only, `AI` domain in `03` |
| Structured capture | FHIR SDC | ADOPT | `06` |
| Legacy messaging | HL7 v2 | ADOPT | `06` |
| Imaging | DICOM, DICOMweb | ADOPT | `06` |
| Cross-community | IHE profiles | ADOPT | `06` |
| Terminology | SNOMED CT, ICD, LOINC, UCUM, ATC | ADOPT | `Terminology` domain, `03`; licensing REQUIRES LEGAL VERIFICATION per source |

### Observability & Infrastructure
| Component | Target | Status | Notes |
|---|---|---|---|
| Telemetry | OpenTelemetry | ADOPT | `Observability` domain in `03` |
| Telemetry backend | Grafana Cloud (managed) | CONDITIONAL, lower confidence | Leans toward managed over self-hosted Grafana/Loki/Tempo on operability grounds; **flagged for a dedicated research pass before promotion to ADOPT** — verification §9 |
| IaC | **OpenTofu** | **ADOPT (changed 2026-08-27)** | Replaces Terraform — OSI-licensed (MPL 2.0), native state encryption, Linux Foundation governance; near-identical CLI/HCL to Terraform — verification §6 |
| Containers | Docker | ADOPT | `13` |
| CI/CD | GitHub Actions | ADOPT | `05` Release workflow |
| Cloud | GCP | ADOPT | `13` |
| Compute | Cloud Run | RETAIN | Re-confirmed against GKE — verification §7 |
| Managed DB | Cloud SQL (PostgreSQL) | ADOPT | `13` |
| Managed cache | Memorystore (Redis) | ADOPT | `13` |
| Object storage | Cloud Storage | ADOPT | `13` |
| Secrets | Secret Manager, Cloud KMS | ADOPT | `13` |
| Edge | Cloud Armor, Cloudflare (where justified) | CONDITIONAL | Not independently re-verified in this pass — no change from prior target |

### Managed Upgrade Policy
Dependency **patch** versions are never frozen blindly — they track
upstream security releases on a defined cadence. **Minor/major** version
upgrades go through the same compatibility-validation step as any other
release change (`05` §12 Release workflow) before rollout. This document
records the current target baseline, not a permanently pinned set of
version numbers.

## Alternatives Considered
- **NestJS/Node.js backend instead of Spring Boot** — a viable
  alternative stack considered in earlier architecture consultations;
  not adopted in this target because this document's baseline specifies
  the JVM/Spring stack. Reconciling this choice against any other
  previously-stated preference is an ADR-level decision, tracked in `19`,
  not settled by this document alone.
- **Kubernetes-based container orchestration instead of Cloud Run** —
  see `13` Alternatives; rejected for this target absent measured need.
- **RabbitMQ as the sole/primary messaging technology** (superseded
  2026-08-27) — re-evaluated with fresh evidence against Pub/Sub and
  Kafka; changed to Pub/Sub-primary, RabbitMQ-conditional — verification
  §5.
- **Terraform instead of OpenTofu** (superseded 2026-08-27) — re-evaluated
  on licensing (BSL vs. MPL/OSI) and state-encryption grounds; changed to
  OpenTofu — verification §6. A "dual-engine" approach (OpenTofu for new
  work, Terraform only if an HCP-exclusive feature is later required) is
  the documented fallback, not a rejected option.
- **FHIR R5 as production baseline** (superseded 2026-08-27) — corrected
  to R4/R4B after evidence of limited R5 real-world adoption and US
  Core's continued R4 baseline — verification §10.

## Security Impact
Keycloak, Cloud KMS, and Secret Manager together implement the
credential/secrets handling required by `07`.

## Operational Impact
Spring Modulith's module boundaries give a mechanical way to verify that
code doesn't cross the domain boundaries defined in `03` — a build-time
check, not just a documentation convention.

## Performance Impact
No numbers asserted for any component. REQUIRES MEASUREMENT once
implemented.

## Compliance Impact
Terminology licensing (SNOMED CT, ICD, LOINC, etc.) REQUIRES LEGAL
VERIFICATION per the `Terminology` domain profile in `03` before any
redistribution or embedding claim.

## Failure Modes
A dependency upgrade that breaks compatibility is caught by the
compatibility-validation gate in the Release workflow (`05` §12) before
reaching any wave — never discovered first in production.

## Dependencies
Depends on `01` through `13`. Feeds `19` (ADRs formalizing each major
choice above), `20` (roadmap sequencing of stack adoption).

## Unknowns
UNKNOWN — REQUIRES EVIDENCE whether any existing codebase currently uses
this stack, an earlier variant of it, or an entirely different one.

## Validation
Every technology named in any other master document (e.g., `04`'s
PostgreSQL/Redis, `06`'s RabbitMQ, `07`'s Keycloak) appears in this
document's tables with a specific target version. Confirmed at time of
writing.

## Rollback
N/A at design stage. For implementation: version upgrades follow the
Release workflow's canary/wave/rollback mechanics (`05` §12), never a
direct production version bump.

## Definition of Done
No other master document names a technology absent from this stack
without an explicit note that it's a deferred/future consideration.
