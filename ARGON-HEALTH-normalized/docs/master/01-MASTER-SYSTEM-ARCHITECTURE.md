# 01 — MASTER SYSTEM ARCHITECTURE

STATUS: PROPOSED
EVIDENCE CLASS: DESIGN

## Status
TARGET ARCHITECTURE / PROPOSED. Not implemented. Not production. No repository
evidence was reviewed to produce this document — see `19-MASTER-ARCHITECTURAL-DECISIONS.md`
for how this target relates to any existing codebase.

## Purpose
Define the single top-level shape of ARGON HEALTH PLATFORM — the three-plane
model every other master document, domain, and workflow must stay consistent
with.

## Scope
Covers the platform's highest-level decomposition only: Control Plane,
Application Plane, Data Plane, and the Interoperability boundary between the
platform and the outside world (government systems, payers, external
labs/PACS, patient-facing apps). Does not cover individual domain internals
(see `03-MASTER-DOMAIN-MAP.md`) or workflow steps (see `05-MASTER-WORKFLOW-MAP.md`).

## Current Assumptions
- ARGON is being designed to scale from a single clinic to hospital networks
  across multiple countries.
- Multi-tenancy is mandatory at every layer, not bolted on later.
- The platform must support both a digital control layer (this document) and
  physical/legal facility onboarding that happens outside the software
  (licensing, inspections, ministry approvals) — the two are related but not
  the same process.

## Evidence
UNKNOWN — REQUIRES EVIDENCE. No existing repository, infrastructure, or
production system was inspected in the construction of this document. Any
resemblance to a live system is coincidental unless explicitly cross-referenced
in an ADR.

## Decision

ARGON is decomposed into three planes plus one cross-cutting boundary:

```
                         ARGON HEALTH PLATFORM
                                  |
        +-------------------------+-------------------------+
        |                         |                         |
        v                         v                         v
  CONTROL PLANE           APPLICATION PLANE            DATA PLANE
        |                         |                         |
  Org Provisioning          Clinical                   PostgreSQL (OLTP)
  Licensing                 Pharmacy                    Redis (cache/queue)
  Releases                  Laboratory                  Object Storage (docs/DICOM)
  Maintenance                Radiology                   Messaging (RabbitMQ)
  Configuration              Hospital Ops                Search
  Security Ops               Billing                     Analytics / Warehouse
  Compliance Evidence        Insurance
  Global Audit               Scheduling
                              Patient
        |                         |                         |
        +-------------------------+-------------------------+
                                  |
                          INTEROPERABILITY LAYER
                                  |
              FHIR / HL7 / DICOM / Government APIs / Payers / Patient Apps
```

**Control Plane** — owns the platform itself: who exists, what they're
licensed for, what version they're running, whether they're healthy. It
never touches clinical content directly (see `27` in the security map for
the Control-Plane-vs-Clinical-Access separation).

**Application Plane** — owns clinical and operational behavior: every domain
a clinician, pharmacist, biller, or patient actually interacts with.

**Data Plane** — owns durability and truth. PostgreSQL is the system of
record for structured clinical/financial data; Redis is disposable cache and
queue state, never source of truth; object storage holds large binary
content (documents, DICOM instances) that must never live in the relational
store; messaging carries events between plane boundaries.

**Interoperability Layer** — the only sanctioned path in or out of the
platform for external systems. No domain integrates with an external payer,
government system, lab analyzer, or PACS directly; it goes through this
layer so a single choke point can be audited, rate-limited, and versioned.

## Alternatives Considered
- **Single monolithic plane** (rejected) — collapses platform-management
  concerns into clinical code paths, making it impossible to reason about
  who can see PHI vs who can just suspend a tenant.
- **Full microservices per domain from day one** (rejected at this stage) —
  multiplies operational surfaces before there is evidence of independent
  scaling needs; see `13-MASTER-INFRASTRUCTURE-ARCHITECTURE.md` for the
  modular-monolith-first stance.
- **Direct external integrations per domain** (rejected) — without a single
  Interoperability Layer, every domain would need its own FHIR/HL7/DICOM
  handling, duplicating validation and creating inconsistent external
  contracts.

## Security Impact
Three-plane separation is itself a security control: it makes "platform
administrator" and "clinical data access" structurally different privilege
domains (elaborated in `07-MASTER-SECURITY-MAP.md` and `27` Control Plane
Security). A design that merges the planes would make privilege escalation
from platform-ops to PHI-access a single-role problem instead of a two-step,
auditable one.

## Operational Impact
Each plane can be deployed, scaled, and put into maintenance mode
independently. Control Plane maintenance must never require Application
Plane downtime, and vice versa — this constrains release architecture (see
`31` Update/Release Architecture, formalized in `20-MASTER-IMPLEMENTATION-ROADMAP.md`).

## Performance Impact
No performance numbers are asserted. Plane separation implies at least one
network hop between Control Plane provisioning actions and Application Plane
tenant activation; this must be measured once a real implementation exists.
REQUIRES MEASUREMENT.

## Compliance Impact
Separating planes materially helps compliance posture (data classification
boundaries, least-privilege enforcement) but implementing this diagram does
not itself satisfy any named standard. See `08-MASTER-COMPLIANCE-MAP.md` —
status for every control stays at DESIGNED until independently evidenced.

## Failure Modes
- Control Plane outage must degrade to "no new provisioning/licensing
  changes," never to "existing clinics lose clinical access."
- Data Plane partial outage (e.g., search or analytics down) must degrade
  gracefully without blocking OLTP clinical writes.
- Interoperability Layer outage must queue/retry rather than silently drop
  outbound government/payer submissions.

## Dependencies
This document is the parent of every other master document. All other
documents must reference planes using the names defined here.

## Unknowns
- UNKNOWN — REQUIRES EVIDENCE: whether any existing ARGON system maps onto
  this model today, partially or not at all.
- UNKNOWN: real multi-region requirements (which countries, what data
  residency rules) — see `06-MASTER-INTEGRATION-MAP.md` government section.

## Validation
No validation performed. This is a design document. Validation criteria for
an eventual implementation: each plane must be independently deployable, and
a Control-Plane-only outage drill must demonstrate zero clinical-write
impact.

## Rollback
N/A at design stage. For implementation: plane boundaries must be
introduced additively (new boundary drawn around existing capability)
rather than by first tearing down a working system — see
`19-MASTER-ARCHITECTURAL-DECISIONS.md` and the non-destructive-change
principle it inherits.

## Definition of Done
This document is done when: (a) every subsequent master document places
its subject matter in exactly one plane without ambiguity, (b) the ASCII
diagram above is reused unmodified everywhere the three-plane model is
referenced, (c) no domain is left unassigned to a plane in
`03-MASTER-DOMAIN-MAP.md`.
