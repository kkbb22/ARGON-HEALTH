# 14 — MASTER TECHNOLOGY STACK

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
UNKNOWN — REQUIRES EVIDENCE (see `01`). This target stack's specific
versions have not been cross-checked against any prior ARGON technology
decision; reconciling this document against any earlier stack choice is
explicitly the job of `19-MASTER-ARCHITECTURAL-DECISIONS.md`; it is not
resolved here.

## Decision

### Backend
| Component | Target | Notes |
|---|---|---|
| Language runtime | Java 25 LTS | LTS baseline for long-term support |
| Application framework | Spring Boot 4.1.x | |
| Core framework | Spring Framework 7 | |
| Modularity | Spring Modulith 2.1.x | Enforces the modular-monolith boundary from `13` at the code level — module boundaries mirror `03`'s domain boundaries |
| Build tool | Gradle 9.x | |

### Data
| Component | Target | Notes |
|---|---|---|
| Primary datastore | PostgreSQL 18.x | Source of truth, `04` |
| Migrations | Flyway | Every schema change versioned, `07` |
| Cache / queue backing | Redis | Never source of truth, `04` |
| Messaging | RabbitMQ | Event backbone, `06` |
| Identity provider | Keycloak | OIDC/OAuth2 baseline, `07` |

### Frontend
| Component | Target | Notes |
|---|---|---|
| Web framework | Next.js 16.x | `12` |
| UI library | React | `12` |
| Mobile | React Native | `12` |
| Language | TypeScript | Web + mobile |

### Interoperability & Terminology
| Component | Target | Notes |
|---|---|---|
| FHIR | R5 baseline, R4/R4B compatibility | `06` |
| SMART on FHIR | 2.2 | `06` |
| Clinical decision support | CDS Hooks | Advisory only, `AI` domain in `03` |
| Structured capture | FHIR SDC | `06` |
| Legacy messaging | HL7 v2 | `06` |
| Imaging | DICOM, DICOMweb | `06` |
| Cross-community | IHE profiles | `06` |
| Terminology | SNOMED CT, ICD, LOINC, UCUM, ATC | `Terminology` domain, `03` |

### Observability & Infrastructure
| Component | Target | Notes |
|---|---|---|
| Telemetry | OpenTelemetry | `28`-equivalent, `Observability` domain in `03` |
| IaC | Terraform | `13` |
| Containers | Docker | `13` |
| CI/CD | GitHub Actions | `05` Release workflow |
| Cloud | GCP | `13` |
| Compute | Cloud Run | `13` |
| Managed DB | Cloud SQL (PostgreSQL) | `13` |
| Managed cache | Memorystore (Redis) | `13` |
| Object storage | Cloud Storage | `13` |
| Secrets | Secret Manager, Cloud KMS | `13` |
| Edge | Cloud Armor, Cloudflare (where justified) | `13` |

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
