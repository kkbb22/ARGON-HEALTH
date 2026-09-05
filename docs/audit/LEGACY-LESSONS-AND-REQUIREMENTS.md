# LEGACY LESSONS AND REQUIREMENTS

STATUS: PROPOSED
EVIDENCE CLASS: RUNTIME EVIDENCE (both lessons below are dated, real incidents, not hypothetical risk scenarios)

> New document, added during repository consolidation (2026-09-05).
> Captures what LEGACY ARGON's actual history requires TARGET
> ARGON-HEALTH to account for — the opposite direction from
> `LEGACY-TO-TARGET-MAPPING.md`, which maps concepts forward.

## Lesson 1 — The `clinic_auth_map` Incident (LEGACY ARGON, dated)
**What happened:** a Firebase Security Rules change was deployed before
its supporting Cloud Function (`setClinicClaim.js`) was live and
verified, causing a production privilege-escalation exposure, an
outage, and an emergency rollback.

**Requirement this imposes on TARGET ARGON-HEALTH:** any future
migration step that spans two coupled layers (e.g., an Authorization
Service change plus a PostgreSQL RLS policy change) must treat that pair
as one atomic, jointly-verified deployment — never two sequential ones
verified separately. This is the same principle `argon-governance`
already states for LEGACY ARGON; this document records that it applies
identically, not just by analogy, to TARGET ARGON-HEALTH's three-layer
model (ADR-007) once any of it is ever implemented.

## Lesson 2 — The 2026-08-23 Blocked Rebuild (a real attempt at this exact migration)
**What happened** (per ADR-019, this repository): three days before the
2026-08-27 documentation pass that produced most of this target
architecture, a real rebuild attempt on an earlier Java 21/Spring Boot
target was found **blocked** — no functional Gradle/Gradle Wrapper, the
wrong Java version installed, no PostgreSQL/Docker/git available in the
build environment — and a forensic self-audit of the code that *was*
generated found real, dated defects: medication/RxNorm codes mishandled
as UUIDs, allergy checks that didn't match allergen to drug, and FHIR
ingest methods returning random UUIDs without persisting any data.

**Requirement this imposes on TARGET ARGON-HEALTH:** ADR-019 already
converts this into a permanent gate — recorded as **Rule L15** in
`docs/governance/ARCHITECTURE-LINT-RULES.md` — that no implementation
phase may be marked IMPLEMENTED without first (a) an independently
verified, actually-functional build environment confirmed *before* any
code-completion claim, and (b) an adversarial/forensic audit of the
generated code against its own claims, never a self-reported "tests
passed" summary alone. This consolidation carries that rule forward
unchanged; it is the single most concrete, evidence-backed requirement
in the entire target architecture, precisely because it is the one item
with a real, dated failure behind it rather than a hypothetical risk.

## What LEGACY ARGON Has Proven, Positively
Per `argon-governance` and `argon-platform-target-architecture`: five
paying clinics trust LEGACY ARGON with real patient data today. That is
explicitly named, in `argon-platform-target-architecture`, as ARGON's
single most valuable asset — more valuable than any code, including
everything in this target architecture. No TARGET ARGON-HEALTH document
may be read as implying otherwise.

## What Remains Genuinely Unverified About LEGACY ARGON
This consolidation has no access to LEGACY ARGON's current compliance
posture, data volumes, uptime history beyond the one named incident, or
whether any "build now" item from `argon-platform-target-architecture`
has since shipped. These are not filled in with plausible-sounding
detail; they remain open questions for whoever holds decision authority
(`docs/governance/DECISION-AUTHORITY.md`) to answer from the actual
production system, not from this document set.

## Dependencies
`docs/audit/LEGACY-VS-TARGET-BOUNDARY.md`,
`docs/audit/LEGACY-TO-TARGET-MAPPING.md`,
`docs/governance/ARCHITECTURE-LINT-RULES.md` (Rule L15),
`docs/adr/ADR-019-RECONCILIATION-WITH-ADR-000.md`.

## Definition of Done
Both lessons above are traceable to a real, dated, named incident — this
document contains zero hypothetical "what could go wrong" scenarios
invented for completeness.
