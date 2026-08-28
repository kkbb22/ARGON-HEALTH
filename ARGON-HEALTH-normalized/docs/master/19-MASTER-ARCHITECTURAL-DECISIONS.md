# 19 — MASTER ARCHITECTURAL DECISIONS

STATUS: PROPOSED
EVIDENCE CLASS: DESIGN

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

---

### Full-Format ADRs (2026-08-27 Architecture Normalization Pass)
*The three entries below follow the fuller ADR template required by the
Architecture Normalization task (ADR ID, Title, Status, Date, Context,
Problem, Options, Evidence, Decision, Rationale, Consequences, Security/
Operational/Compliance Impact, Revisit Trigger, Rollback/Exit Strategy).
ADR-001–ADR-015 above remain in the lightweight format pending a full
reformat pass — tracked as open work, not silently upgraded.*

**ADR-016 — Internal event backbone: Google Cloud Pub/Sub (primary),
RabbitMQ (conditional), Kafka (rejected)**
- Status: **PROPOSED** (not Approved — requires sign-off per ADR-009's
  discipline applied to itself)
- Date: 2026-08-27
- Context: `06`'s original target named RabbitMQ as the sole internal
  event backbone. The Architecture Normalization task required a fresh,
  non-popularity-based comparison against Google Cloud Pub/Sub and Apache
  Kafka.
- Problem: Which messaging technology should back the Transactional
  Outbox pattern for a single-team-operated, GCP-native platform at its
  current stage?
- Options: RabbitMQ (self/managed), Google Cloud Pub/Sub (managed),
  Apache Kafka (self-managed or Confluent).
- Evidence: `docs/evidence/TECHNOLOGY-BASELINE-VERIFICATION.md` §5 (live
  research, 2026-08-27).
- Decision: Pub/Sub primary; RabbitMQ conditional (AMQP-only external
  adapters only); Kafka rejected for the current stage.
- Rationale: Pub/Sub eliminates broker/partition operational burden
  entirely on a platform that is already GCP-first end to end (`13`);
  no evidenced requirement justifies Kafka's added operational
  complexity; RabbitMQ remains available where a specific external
  system requires AMQP.
- Consequences: `06`'s Internal Event Backbone section and `14`'s Data
  table are both updated; the domain layer depends on a messaging
  abstraction, not a broker SDK, keeping this reversible.
- Security Impact: Pub/Sub inherits GCP IAM scoping natively; no new
  broker-credential surface to manage versus a self-hosted RabbitMQ.
- Operational Impact: Removes cluster/broker management from the
  platform-ops workload entirely for the primary path.
- Compliance Impact: None identified; data-residency implications of
  Pub/Sub (regional topic placement) should be checked per country
  during Phase 6 (`20`) alongside the Government Country Adapter work.
- Revisit Trigger: A measured requirement for cross-partition ordering
  at platform scale, or a real long-window event-replay/event-sourcing
  need beyond Pub/Sub's 31-day maximum retention.
- Rollback/Exit Strategy: Because domain code depends on the messaging
  abstraction rather than the Pub/Sub SDK, swapping the underlying
  transport (including back to RabbitMQ or to Kafka) is an
  infrastructure-and-adapter change, not a domain-code rewrite.

**ADR-017 — Infrastructure as Code: OpenTofu (replacing Terraform)**
- Status: **PROPOSED**
- Date: 2026-08-27
- Context: `13`/`14`'s original target named Terraform. The Architecture
  Normalization task explicitly listed "Terraform vs OpenTofu" as a
  drift category to verify with fresh evidence.
- Problem: Which IaC tool should the platform standardize on, given
  Terraform's 2023 relicensing to BSL 1.1 and IBM's 2024 acquisition of
  HashiCorp?
- Options: Terraform (BSL 1.1, IBM-owned), OpenTofu (MPL 2.0, Linux
  Foundation-governed fork).
- Evidence: `docs/evidence/TECHNOLOGY-BASELINE-VERIFICATION.md` §6 (live
  research, 2026-08-27).
- Decision: OpenTofu adopted as the IaC baseline.
- Rationale: OSI-approved MPL 2.0 licensing reduces legal-review friction
  for a healthcare platform expecting ongoing compliance/legal review
  (`08`); native state/plan encryption is a concrete security
  improvement over Terraform's open CLI; HCL syntax and provider
  ecosystem are near-identical, keeping migration risk low; no
  Terraform-exclusive feature (e.g., HCP Terraform Stacks) is required
  by anything in this architecture today.
- Consequences: `13`'s Infrastructure Diagram section and `14`'s
  Observability & Infrastructure table both updated; Terraform state
  language throughout `13`/`17` updated to OpenTofu state.
- Security Impact: Native state encryption directly strengthens the
  Terraform-state DR/security posture already tracked in `17`.
- Operational Impact: Near-zero — CLI and workflow are effectively a
  binary swap (`terraform` → `tofu`).
- Compliance Impact: Improves license-review posture for regulated
  jurisdictions (`08`).
- Revisit Trigger: A specific need for an HCP-Terraform-exclusive
  capability, or evidence of GCP-provider compatibility regression in
  OpenTofu.
- Rollback/Exit Strategy: Both tools read the same state format as of
  this writing; a "dual-engine" fallback (Terraform CLI against the same
  state) remains available without a state migration if ever needed.

**ADR-018 — FHIR production baseline corrected to R4/R4B (was R5)**
- Status: **PROPOSED** (correction, not yet independently reviewed)
- Date: 2026-08-27
- Context: The original `06`/`14` target stated FHIR R5 as the
  production baseline with R4/R4B as a compatibility layer. The
  Architecture Normalization task required re-verifying this against
  current official/authoritative sources rather than carrying it forward
  unverified.
- Problem: Is R5 actually the correct production target for near-term
  real-world interoperability (government systems, payers, external
  labs)?
- Options: R4/R4B as baseline (R5 optional), R5 as baseline (R4/R4B
  compatibility), R6 as baseline (rejected outright — still in ballot).
- Evidence: `docs/evidence/TECHNOLOGY-BASELINE-VERIFICATION.md` §10 (live
  research, 2026-08-27): US Core (the dominant regulatory FHIR baseline)
  remains on R4 and is not planning to move to R5; R5 is independently
  described as having limited real-world adoption; R6 is still in ballot
  (first full ballot dated May 2026), with production-grade adoption not
  expected before late 2027 per HL7's own guidance.
- Decision: FHIR R4/R4B is now the stated production target; R5 is
  transitional/optional (adopted only per specific partner requirement);
  R6 is tracked, not adopted.
- Rationale: Matches the regulatory and ecosystem reality found in fresh
  research rather than an earlier, unverified assumption that R5 was the
  more "current" and therefore preferable choice.
- Consequences: This is a **documentation correction**, not a scope
  change — no domain/workflow document required rewriting beyond the
  `06`/`14` version labels, since the canonical internal clinical model
  (`Clinical` domain, `03`) was never FHIR-native in the first place.
- Security Impact: None identified.
- Operational Impact: None identified at this design stage.
- Compliance Impact: Directly improves alignment with the dominant
  regulatory FHIR baseline (US Core / ONC Cures Act / CMS), reducing
  future integration-conformance risk.
- Revisit Trigger: FHIR R6 reaching final/normative publication.
- Rollback/Exit Strategy: N/A — this is itself the correction of an
  earlier, unverified claim; there is no prior "implementation" to roll
  back.

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
