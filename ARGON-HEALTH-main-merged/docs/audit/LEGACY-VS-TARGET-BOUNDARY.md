# LEGACY VS TARGET BOUNDARY

STATUS: PROPOSED
EVIDENCE CLASS: DESIGN (boundary statement) / RUNTIME EVIDENCE (legacy facts, sourced from `argon-governance`)

> New document, added during repository consolidation (2026-09-05).
> Neither source repository (`ARGON-HEALTH`, `system-ARGON-NEW`)
> describes the live legacy system in any detail — both are pure target-
> architecture documentation sets. This document draws its legacy-side
> facts from the `argon-governance` and `argon-platform-target-architecture`
> skill files available in this environment, which are the only source
> of legacy-system information accessible to this consolidation. Where
> those files don't state a fact, it is marked UNKNOWN below rather than
> inferred.

## Purpose
State plainly which system is which, so "target architecture" and
"current production" are never confused in conversation, a CV, an
interview, or a future document.

## LEGACY ARGON (current production)
- **What it is:** A live Firebase-based EMR system serving five paying
  clinics in Jordan today, built and operated by one developer.
- **Stack (per `argon-governance`):** Firebase (Realtime Database +
  Cloud Functions + Storage + Security Rules), a single Firebase
  project, `clinic_id`-scoped data isolation.
- **Role in this repository set:** production, business evidence (the
  proof that clinics will pay and trust it with patient data), proven
  workflow source, lessons-learned source, and eventual migration
  source — never a target to be rewritten wholesale.
- **Known incident history:** the `clinic_auth_map` privilege-escalation
  incident — a Firebase Security Rules change deployed before its
  supporting Cloud Function (`setClinicClaim.js`) was live and verified
  — caused a production outage and an emergency rollback. This is the
  concrete, dated origin of `argon-governance`'s core rule that a change
  spanning Rules + a Cloud Function is one atomic change, not two
  sequential ones.
- **A separate, later incident** (2026-08-23, per ADR-019 in this
  repository): an attempted rebuild onto an earlier Java/Spring Boot
  target was found blocked at the build-environment level (no working
  Gradle wrapper, wrong Java version, no PostgreSQL/Docker/git
  available) and a forensic self-audit of the code that *was* generated
  found real defects (medication codes mishandled as UUIDs, allergy
  checks not matching allergen to drug, FHIR ingest methods returning
  random UUIDs without persisting data). This is first-hand, dated
  evidence for why LEGACY ARGON is not rewritten speculatively.

## TARGET ARGON-HEALTH (this repository)
- **What it is:** A 40-domain, 30-workflow target platform architecture
  — Java 25 / Spring Boot 4.1 / Spring Modulith / PostgreSQL 18 /
  Keycloak / GCP / FHIR-R4/R4B / DICOM — designed to scale from a single
  clinic to hospital networks under one control plane and one
  role-aware application.
- **Status:** PROPOSED / NORTH STAR. Nothing in `docs/master/` has been
  implemented, reviewed, or approved (see
  `docs/governance/ARCHITECTURE-STATUS.md`,
  `docs/governance/DECISION-AUTHORITY.md`).
- **Governing constraint:** per ADR-000 (`argon-platform-target-architecture`
  skill) and ADR-019 (`docs/adr/ADR-019-RECONCILIATION-WITH-ADR-000.md`),
  this target is reached only by staged evolution triggered by real
  client signals — never by a big-bang rewrite of LEGACY ARGON. No phase
  of `docs/master/20-MASTER-IMPLEMENTATION-ROADMAP.md` is authorized to
  start merely because it is documented here.

## The Boundary Rule
**LEGACY ARGON and TARGET ARGON-HEALTH are never the same document, the
same status field, or the same claim.** A statement about one is never
evidence for the other:
- "The target architecture specifies three-layer authorization" is not
  evidence that LEGACY ARGON has three-layer authorization today (it has
  Rules + application logic + UI, per `argon-governance`; PostgreSQL RLS
  does not exist because there is no PostgreSQL).
- "LEGACY ARGON serves five real clinics" is not evidence that any part
  of TARGET ARGON-HEALTH has been built, deployed, or validated.

## What Is Genuinely UNKNOWN
This document does not have access to LEGACY ARGON's actual codebase,
data volumes, current feature set beyond what `argon-governance` and
`argon-platform-target-architecture` describe, or its current
compliance posture. Those are tracked, where relevant, as UNKNOWN /
REQUIRES EVIDENCE in `docs/compliance/COMPLIANCE-TRACEABILITY-MATRIX.md`
and `docs/audit/LEGACY-LESSONS-AND-REQUIREMENTS.md`, not invented here.

## Dependencies
`docs/audit/LEGACY-TO-TARGET-MAPPING.md` (structural mapping),
`docs/audit/LEGACY-LESSONS-AND-REQUIREMENTS.md` (what LEGACY ARGON's
history requires of the target), `argon-governance` and
`argon-platform-target-architecture` skills (source of every legacy-side
fact above).
