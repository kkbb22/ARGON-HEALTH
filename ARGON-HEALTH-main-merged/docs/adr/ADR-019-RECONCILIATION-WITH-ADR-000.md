# ADR — Reconciliation of the 2026-08-27 v2/v3 Target Architecture with ADR-000

STATUS: PROPOSED
EVIDENCE CLASS: DESIGN (reconciles two existing documented decisions; introduces no new unverified technical claim)

## ADR ID
ADR-019 (log entry: `docs/master/19-MASTER-ARCHITECTURAL-DECISIONS.md`). This
file is the full-detail standalone record.

## Title
Formal reconciliation between the 2026-08-27 v2/v3 "Master Foundation" /
"Architecture Normalization" documentation set (this entire `docs/`
tree) and **ADR-000: ARGON Platform Target Architecture & Migration
Strategy** (dated 2026-08-22, status: *Accepted as North Star; execution
is staged, not immediate*).

## Status
PROPOSED — this is a reconciliation of documentation consistency, not a
new speculative technology pick, but it still follows the same discipline
as every other ADR here: it does not self-approve.

## Context

**ADR-000 already existed before this documentation pass began.** It
reconciled an earlier full-rebuild recommendation (PostgreSQL, NestJS,
React, Keycloak/Auth0, event-driven modular monolith, FHIR/DICOM/SMART,
hospital-department modules) against `argon-governance`'s core principle
— **"reality over ambition."** Its resolution separated **what** (the
long-term target is correct) from **when/how** (staged evolution,
triggered only by real client signals, never a big-bang rewrite of the
live 5-clinic Firebase system). It includes a concrete **Staged Trigger
Table**, a **"build now" list** of zero-rewrite-risk steps achievable
inside the current Firebase schema today, and explicit **AI Agent
Rules**: *"DO NOT propose migrating a subsystem off Firebase, adopting
Postgres/NestJS/Kubernetes, or building a hospital-tier module without
first checking whether its trigger signal in this table has actually
occurred."*

**Five days later (2026-08-27), this entire `docs/` tree was produced**
by a sequence of independently-authored mega-prompts ("Master
Foundation," "Architecture Normalization," "Autonomous Execution
Contract"). Each was explicit that it describes a TARGET/PROPOSED
architecture, not an authorization to implement — but the originating
"Master Foundation" prompt specifically instructed treating the
repository as **"Repository Unknown"** and did not reference, incorporate,
or check itself against ADR-000's trigger table, "build now" list, or AI
Agent Rules at any point during its authoring. `ADR-014`
(`docs/master/19`) already flagged this gap: *"this document set uses the
Java 25/Spring Boot baseline throughout... reconciling this baseline
against any earlier stated preference, if one exists, is future work."*
This ADR is that future work.

**Separately, and more concretely than any documentation gap:** a real
rebuild attempt on **2026-08-23** — three days before this v2/v3 pass,
using an earlier Java 21/Spring Boot target — was found **BLOCKED**: no
functional Gradle/Gradle Wrapper, Java 11 installed where Java 21 was
required, no PostgreSQL/Docker/git available in the build environment.
Its own forensic self-audit found real defects in the code that *was*
generated: medication/RxNorm codes mishandled as UUIDs, allergy checks
that didn't match allergen to drug, and FHIR ingest methods returning
random UUIDs without persisting any data. This is not a hypothetical
risk — it is a first-hand, dated failure of exactly the kind of rewrite
this new v2/v3 documentation set describes, on this same project, days
before this pass began.

## Problem
Does the v2/v3 documentation set conflict with ADR-000, and if so, how
should the two be reconciled without discarding the genuinely
higher-quality work in either?

## Options

**A — Discard the v2/v3 set, defer to ADR-000 as-is.** Rejected: this
throws away real, dated (2026-08-27), independently-verified technology
research — current Java LTS status, current Spring Boot/PostgreSQL
releases, a real evidence-based messaging comparison (Pub/Sub vs.
RabbitMQ vs. Kafka), a real IaC licensing comparison (OpenTofu vs.
Terraform), and a material correction to the FHIR version claim (R4/R4B,
not R5) — none of which existed when ADR-000 inherited its stack
reference (NestJS) from an even earlier, less-verified document.

**B — Discard ADR-000, treat the v2/v3 set as the new authoritative plan
and begin implementing it.** Rejected outright: this is precisely the
big-bang-rewrite failure pattern ADR-000 already diagnosed — made
concretely worse by the fact that the most recent real attempt at
exactly this kind of rewrite, three days before this pass, failed at the
build-environment level and produced verified-defective code.

**C — Layer the two: ADR-000 governs *whether/when*; the v2/v3 set
becomes the updated *what*, fully subordinate to ADR-000's trigger table
and AI Agent Rules.** Chosen.

## Decision

1. **ADR-000 remains the governing document, unchanged.** Its Staged
   Trigger Table, "build now" list, and AI Agent Rules continue to bind
   every future architecture or implementation decision for ARGON,
   including everything in this `docs/` tree, without exception.

2. **The v2/v3 technology baseline
   (`docs/governance/TECHNOLOGY-BASELINE.md`,
   `docs/master/14-MASTER-TECHNOLOGY-STACK.md`) formally supersedes
   ADR-000's inherited stack reference (NestJS)** as the more current,
   more rigorously verified statement of "what the target stack should
   be, *if and when* a row in ADR-000's trigger table fires." This is a
   narrow, stack-specifics-only supersession — it does not touch ADR-000's
   governance mechanism.

3. **Every phase in `docs/master/20-MASTER-IMPLEMENTATION-ROADMAP.md` is
   re-gated by ADR-000's Staged Trigger Table**, not by the roadmap's own
   generic phase language alone:
   - **Phase 1 (Foundational Domains)** has **no fired trigger** in
     ADR-000's table today. Per ADR-000's "build now" list, the
     equivalent real value — `license_tier`/`enabled_modules` fields,
     server-side module gating, an optional Organization→Facility layer
     — is achievable **today, inside the current Firebase schema, at
     near-zero risk**. That is the actual next step toward the vision,
     not starting Phase 1 of the new stack.
   - **Phase 3 (Pharmacy/Laboratory/Radiology), Phase 4 (Hospital
     Operations), Phase 6 (Interoperability/Government)** remain gated
     by ADR-000's corresponding trigger rows (a hospital-tier client, an
     external FHIR/PACS consumer, a licensed hospital-tier module
     requirement) — unchanged, now explicitly cross-referenced instead of
     living in two disconnected documents.
   - **Phase 5 (Billing/Insurance)** — if/when billing/insurance
     reporting genuinely needs multi-way joins RTDB can't serve well,
     ADR-000's answer is a **Postgres reporting read-replica fed by
     Firebase events**, not a full Billing-domain rewrite. This is the
     correct-scale current answer, not Phase 5 of the new stack.

4. **A new permanent gate is added**, sourced directly from the
   2026-08-23 forensic-audit failure: no phase, at any future point, may
   be marked IMPLEMENTED without first (a) an independently verified,
   actually-functional build environment (correct runtime version,
   working dependency manager, working local database) confirmed
   *before* any code-completion claim, and (b) an adversarial/forensic
   audit of the generated code against its own claims — never a
   self-reported "tests passed" summary alone. Recorded as Rule L15 in
   `docs/governance/ARCHITECTURE-LINT-RULES.md`. This directly closes the
   exact failure mode already observed once on this project.

5. **The live Firebase-based ARGON system, serving real clinics today,
   remains the sole production system.** Nothing in this repository
   authorizes touching it. The entire `docs/` tree is reference material
   for a future, trigger-gated evolution — exactly the role ADR-000
   already assigned to the earlier "council" document, now updated with
   more current research.

6. **ADR-014's status is updated**: was "explicitly unreconciled"; now
   **RESOLVED by this ADR (ADR-019)** — see
   `docs/master/19-MASTER-ARCHITECTURAL-DECISIONS.md`.

## Rationale
Neither discarding the new research nor discarding ADR-000's governance
principle serves the project. The new pass's technology verification is
genuinely better than what it's replacing; ADR-000's staged, evidence-gated
philosophy is genuinely correct and, as of 2026-08-23, has fresh
first-hand evidence (the blocked/defective rebuild attempt) proving why
it exists. Layering them — new *what*, old *when/how* — keeps both.

## Consequences
- No implementation work starts as a result of this reconciliation — it
  changes documentation consistency and governance clarity, not
  authorization to build.
- The next real, concrete, low-risk step toward the platform vision is
  ADR-000's own "build now" list — additive fields inside the existing
  Firebase schema — not anything in the v2/v3 Java/Spring Boot stack.
- Future architecture passes on this repository must check ADR-000's
  trigger table first, per its own AI Agent Rules — this reconciliation
  makes that check explicit and binding on the entire v2/v3 tree
  specifically, closing the gap that let this whole pass be authored
  without ever consulting it.
- `docs/master/20-MASTER-IMPLEMENTATION-ROADMAP.md` gets explicit
  trigger cross-references added per phase (tracked as a direct edit
  alongside this ADR, not left as a future task).

## Security / Operational / Compliance Impact
None beyond what ADR-000 and the v2/v3 set already state individually —
this ADR reconciles documentation and governance, not technical scope.

## Revisit Trigger
Any row in ADR-000's Staged Trigger Table firing for the first time; or a
future technology-verification pass that supersedes this pass's Java
25/Spring Boot 4.1 findings the same way this pass superseded the NestJS
reference.

## Rollback / Exit Strategy
N/A — this ADR reconciles existing documents; it deploys nothing and
authorizes no implementation to roll back.

## Related
- `argon-platform-target-architecture` skill (ADR-000 itself)
- `docs/master/19-MASTER-ARCHITECTURAL-DECISIONS.md` — ADR-014 (now
  resolved by this document), ADR-016/017/018 (the technology
  corrections this ADR builds on)
- `docs/master/20-MASTER-IMPLEMENTATION-ROADMAP.md` — phase-level
  trigger cross-references
- `docs/governance/ARCHITECTURE-LINT-RULES.md` — new Rule L15
