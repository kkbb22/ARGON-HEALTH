# 19 — MASTER ARCHITECTURAL DECISIONS

## Status
TARGET ARCHITECTURE / PROPOSED. This document is an index of decisions
already made (and justified) inline across `01`–`18`; it does not
introduce new decisions.

## Purpose
Consolidate every major architectural decision made across this
foundation into one browsable ADR log, in standard lightweight ADR format
(Title, Status, Context, Decision, Consequences), so a future contributor
doesn't have to re-derive *why* by reading every document in full.

## Scope
Covers decisions with platform-wide consequence. Domain-local choices
(e.g., a specific field on a specific entity) are not elevated to ADR
status.

## Current Assumptions
An ADR here is Proposed until independently reviewed/accepted by whoever
owns that decision authority for the project — this document does not
self-approve its own entries.

## Evidence
UNKNOWN — REQUIRES EVIDENCE (see `01`).

## Decision — The ADR Log

**ADR-001 — Three-plane model (Control / Application / Data)**
Status: Proposed. Context: needed a top-level decomposition that keeps
platform-management privilege structurally separate from clinical access.
Decision: adopt Control/Application/Data planes + Interoperability
boundary (`01`). Consequences: every subsequent domain/workflow must
declare its plane; enables independent scaling and independent
maintenance windows per plane.

**ADR-002 — Modular monolith first, not microservices-per-domain**
Status: Proposed. Context: no evidence yet of independent-scaling need
per domain. Decision: Spring Modulith-enforced module boundaries within a
small number of Cloud Run services (`13`, `14`). Consequences: lower
initial operational complexity; a future service split is possible
because domain boundaries (`03`) are already drawn correctly.

**ADR-003 — Cloud Run over Kubernetes**
Status: Proposed. Context: no measured load pattern justifies cluster
management overhead. Decision: Cloud Run for both planes (`13`).
Consequences: revisit only on measured autoscaling-ceiling evidence.

**ADR-004 — PostgreSQL as sole structural source of truth**
Status: Proposed. Context: needed one unambiguous system of record.
Decision: PostgreSQL for all structured data; Redis/object storage/search/
warehouse are all derived or binary-only (`04`). Consequences: any
future "let's just read from cache" shortcut is a documented anti-pattern.

**ADR-005 — DICOM/large binaries never in PostgreSQL**
Status: Proposed. Context: relational stores degrade badly under large
binary load. Decision: object storage only for DICOM instances and
documents (`04`, `13`). Consequences: Radiology domain's report/metadata
stays relational; image bytes never touch backup/restore paths meant for
OLTP data.

**ADR-006 — Single Interoperability Layer for all external integration**
Status: Proposed. Context: avoids N duplicated protocol handlers across
domains. Decision: FHIR/HL7/DICOM/IHE/Government/Payer integration all
route through one layer (`06`). Consequences: adding a country or payer
is a plugin, never a Core-domain code change.

**ADR-007 — Three-layer authorization enforcement**
Status: Proposed. Context: a single-layer permission check is a single
point of failure. Decision: application + Authorization Service +
PostgreSQL RLS, all three enforced simultaneously (`07`). Consequences:
an application bug alone cannot cause a cross-tenant data leak if RLS is
correctly configured.

**ADR-008 — Structural separation of Control Plane and Clinical Data
access**
Status: Proposed. Context: platform operators must be able to manage
tenants without implicit PHI access. Decision: distinct privilege
domains, break-glass-only PHI access for Control Plane actors (`07`,
`09`). Consequences: every "support needs to see patient data" request
becomes an audited, time-boxed exception, never a standing permission.

**ADR-009 — Compliance status can never skip IMPLEMENTED → APPROVED**
Status: Proposed. Context: prevents "we built it" from being read as "an
auditor approved it." Decision: mandatory TESTED/EVIDENCED gates (`08`).
Consequences: every compliance claim in any pitch/CV/portfolio context
must be traceable to an EVIDENCED-or-higher register row, never inferred
from DESIGNED/IMPLEMENTED status.

**ADR-010 — Saga pattern (not a single distributed transaction) for
Organization Provisioning**
Status: Proposed. Context: provisioning spans many domains without a
shared transaction boundary. Decision: step-tracked, compensable saga
(`11`). Consequences: a failed provisioning run is always resumable or
fully compensable, never left in an ambiguous half-created state.

**ADR-011 — Tiered documentation depth for the Domain Map and Workflow
Map**
Status: Proposed. Context: full 15-field depth for all 39 domains and 30
workflows in one pass is a documentation-effort trade-off. Decision:
Tier 1 (highest blast-radius) gets full depth; Tier 2 gets
complete-but-compact depth, expandable on request (`03`, `05`).
Consequences: no domain or workflow is left with an empty field, but not
every one has been explored to maximum depth yet — expansion is a
tracked, not a hidden, gap.

**ADR-012 — RPO/RTO numeric targets deferred pending business
continuity sign-off**
Status: Proposed. Context: inventing specific numbers would violate Zero
Fabrication. Decision: record recovery *mechanism* per component now;
numeric targets marked TBD until sign-off (`17`). Consequences: this
document set is honest about an real open gap rather than papering over
it with plausible-looking numbers.

**ADR-013 — NFR targets sourced from the project's own vision material,
explicitly labeled unmeasured**
Status: Proposed. Context: the vision material already states
aspirational figures (99.95%+ availability, <2s p95, etc.). Decision:
record them as targets, not measurements (`18`). Consequences: any future
dashboard must visually distinguish target-vs-measured to avoid
Zero-Fabrication drift.

**ADR-014 — Java/Spring Boot/PostgreSQL stack baseline for this pass**
Status: Proposed — **explicitly unreconciled** against any earlier
ARGON technology decision. Context: this master foundation's own prompt
specifies Java 25 LTS / Spring Boot 4.1 / Spring Modulith / PostgreSQL 18
(`14`); a prior architecture consultation for this same project specified
a different Java version and left the Kotlin/Spring-Boot-vs-NestJS choice
open. Decision: this document set uses the Java 25/Spring Boot baseline
throughout, since that is what this pass's own instructions specify.
Consequences: reconciling this baseline against any earlier stated
preference, if one exists, is future work — this ADR records the
discrepancy rather than silently picking a winner.

**ADR-015 — Digital provisioning ≠ legal/regulatory approval**
Status: Proposed. Context: a Control Plane "Activate" action must never
be mistaken for a government license or inspection pass. Decision:
explicit non-scope statement in `11`; Organization ACTIVE state means
digital readiness only. Consequences: every pitch/customer-facing
description of "provision a hospital in minutes" must carry this caveat.

## Alternatives Considered
Each ADR above already documents its own alternative(s) inline — this
document does not duplicate them a second time.

## Security Impact
ADR-007 and ADR-008 are this document's most security-relevant entries;
both are fully elaborated in `07`.

## Operational Impact
ADR-002, ADR-003, ADR-010 are the entries with the largest day-to-day
operational consequence.

## Performance Impact
No new performance claims — ADR-013 explicitly defers to `18`.

## Compliance Impact
ADR-009 and ADR-015 are this document's compliance-critical entries.

## Failure Modes
An ADR marked Proposed being treated as Accepted without an actual review
step is itself the failure mode ADR-009's discipline exists to prevent,
applied reflexively to this document.

## Dependencies
Synthesizes `01` through `18`. Feeds `20` (roadmap sequencing reflects
these decisions).

## Unknowns
UNKNOWN whether any of these ADRs have been reviewed/accepted by an
actual decision authority — this log is a record of what was decided in
this pass, not a claim of sign-off.

## Validation
Every "Alternatives Considered" section in `01`–`18` has a corresponding
ADR entry above. Confirmed at time of writing.

## Rollback
Any ADR here can be superseded by a later ADR that explicitly says so —
ADRs are never silently edited; a changed decision gets a new numbered
entry referencing the one it supersedes.

## Definition of Done
Every platform-wide decision referenced across `01`–`18` has exactly one
ADR entry above; no decision is documented in two places with
inconsistent framing.
