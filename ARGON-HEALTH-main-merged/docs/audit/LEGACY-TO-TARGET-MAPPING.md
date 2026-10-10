# LEGACY TO TARGET MAPPING

STATUS: PROPOSED
EVIDENCE CLASS: DESIGN

> New document, added during repository consolidation (2026-09-05).
> Structural, not exhaustive: it maps concepts, not fields or
> collections, because no field-level LEGACY ARGON schema is available
> to this consolidation (see `LEGACY-VS-TARGET-BOUNDARY.md`).

## Purpose
Show, concept by concept, how a LEGACY ARGON (Firebase) construct
relates to its TARGET ARGON-HEALTH (Java/Spring/PostgreSQL) counterpart
— so a future migration, *if a trigger ever fires*, has a starting map
instead of starting from zero.

## Mapping Table

| LEGACY ARGON (Firebase, today) | TARGET ARGON-HEALTH (`docs/master/`) | Migration posture |
|---|---|---|
| `clinic_id`-scoped data isolation (RTDB paths + Rules) | Organization → Facility → Department hierarchy, three-layer authorization incl. PostgreSQL RLS (`07`) | ADR-000 "build now" list: an *optional* Organization→Facility layer can sit above existing `clinic_id` scoping with a 1:1 mapping for today's single-clinic case — additive, no rewrite |
| Firebase custom claims (`setClinicClaim.js`) for role/clinic assignment | Keycloak-based Identity domain, OIDC/OAuth, service-identity/M2M pattern (`07`, GAP-001) | Not migrated until a trigger fires; today's claims model is the only production auth mechanism |
| Firebase Security Rules (declarative, single layer + app logic + UI) | Three-layer authorization: application + Authorization Service + PostgreSQL RLS (ADR-007) | TARGET adds two enforcement layers LEGACY does not have; this is a target improvement, not a claim about LEGACY's current state |
| Firebase Realtime Database (single logical tree) | PostgreSQL 18 as sole structural source of truth (ADR-004) | Migration trigger: "a measured write-contention or query-complexity bottleneck on RTDB" (ADR-000 Staged Trigger Table) — not fired today |
| No formal licensing/module-gating field on a clinic record | `license_tier` / `enabled_modules` per Organization, server-side gated (`09`, GAP-004 architecture) | ADR-000 "build now": additive field on the *existing* Firebase schema, zero-rewrite-risk, does not require any of the rest of this column |
| No FHIR/DICOM boundary — LEGACY ARGON's data model is internal-only | Single Interoperability Layer, FHIR R4/R4B, DICOM/DICOMweb (`06`, ADR-006, ADR-018) | Migration trigger: "an external hospital, insurer, or PACS system needs to consume ARGON data" — no such consumer exists yet |
| Ad hoc reporting against RTDB | Postgres reporting read-replica fed by Firebase events (ADR-000 "build now" candidate once justified) | Narrower than a full Billing rewrite — the correct-scale answer per ADR-019 §3 |
| Single Firebase project, no formal DR runbooks beyond incident response | Named Scenario Runbooks — ransomware, regional outage, identity-provider outage (`17`, GAP-010) | TARGET-only content; LEGACY's actual DR posture is UNKNOWN/REQUIRES EVIDENCE at this consolidation |

## What This Table Is Not
Not a migration plan, not a schema-mapping specification, and not
authorization to build any TARGET-side item against LEGACY data. Per
ADR-000 and ADR-019, every row above stays PROPOSED/reference material
until its named trigger fires and a real decision authority reviews the
resulting ADR.

## Dependencies
`docs/audit/LEGACY-VS-TARGET-BOUNDARY.md`, `argon-platform-target-architecture`
skill (source of the Staged Trigger Table and "build now" list),
`docs/audit/LEGACY-LESSONS-AND-REQUIREMENTS.md`.

## Unknowns
UNKNOWN: LEGACY ARGON's actual current RTDB schema, data volumes, or
whether any of the "build now" list items have already been implemented
in production since `argon-platform-target-architecture`'s 2026-08-22
context date. This consolidation has no way to check LEGACY ARGON's
actual current state and does not assume it is unchanged.
