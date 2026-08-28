# Traceability Matrix

**STATUS:** ACTIVE (governance register) — **Tier 1 complete, Tier 2 backfill open**
**EVIDENCE CLASS:** DESIGN

## Purpose
Map Requirement → Domain → Workflow → API → Data → Security Control →
Compliance Requirement → Test → Evidence → Release, so a reviewer can
follow any critical capability end-to-end across the document set
without re-deriving the connections by reading all 20 master documents.

## Scope Decision (stated up front, not hidden)
`docs/master/03-MASTER-DOMAIN-MAP.md` documents **39 domains** and
`docs/master/05-MASTER-WORKFLOW-MAP.md` documents **30 workflows**, each
already split into Tier 1 (full depth) and Tier 2 (compact depth) per
**ADR-011**. This matrix follows that same, already-established
precedent rather than inventing a new one: **Tier 1's 12 workflows and
their directly-owning domains are traced at full depth below. Tier 2's
15 workflows are listed with their domain/data links only, with
Security/Compliance/Test/Evidence columns marked `NOT YET TRACED` rather
than filled with invented content.** Backfilling Tier 2 to the same
depth is future work, tracked here as an open item — the same honesty
discipline ADR-011 already applies to documentation depth applies to
this matrix too.

## Tier 1 — Full Traceability

| # | Workflow (`05`) | Owning Domain(s) (`03`) | API surface (`06`) | Data (`04`) | Security Control (`07`) | Compliance Requirement (`08`) | Test Coverage (`15`) | Evidence | Release Gate (`05` §12) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Patient Registration | PATIENT, MPI, CONSENT | Interoperability Layer (patient search/create) | PostgreSQL (patient identity, RLS-scoped) | 3-layer authZ; consent capture at intake | Data protection / personal-data processing (per jurisdiction) | Unit, Integration, Security ALLOW+DENY, E2E | UNKNOWN — REQUIRES EVIDENCE (no implementation yet) | Canary → wave rollout |
| 2 | Appointment & Check-in | SCHEDULING, QUEUE, PATIENT | Scheduling API | PostgreSQL (appointment, queue state) | Tenant-scoped RLS; role-based check-in permission | N/A (operational, not a compliance-register item) | Unit, Integration, E2E | UNKNOWN — REQUIRES EVIDENCE | Canary → wave rollout |
| 3 | Outpatient Encounter | CLINICAL, SPECIALTIES | Clinical API | PostgreSQL (encounter, notes, orders — versioned/append-only) | 3-layer authZ; audit on every clinical mutation (L4, lint rules) | Application security baseline (OWASP ASVS/API Top 10) | Unit, Integration, Security ALLOW+DENY, E2E | UNKNOWN — REQUIRES EVIDENCE | Canary → wave rollout |
| 4 | Emergency | EMERGENCY, CLINICAL, PATIENT | Clinical API (urgent path) | PostgreSQL | Break-glass access path for unidentified/unconscious patients | Clinical Safety — Wrong Patient hazard (`16`) | Unit, Integration, Clinical Safety test, E2E | UNKNOWN — REQUIRES EVIDENCE | Canary → wave rollout |
| 5 | Admission → Inpatient | HOSPITAL, ICU (extension), NURSING | Hospital API | PostgreSQL (bed allocation — race-safe lock) | Positive-ID enforcement (MAR execution) | Clinical Safety — Wrong Patient/Wrong Medication hazards | Unit, Integration, Clinical Safety test, Concurrency/race test, E2E | UNKNOWN — REQUIRES EVIDENCE | Canary → wave rollout |
| 6 | Pharmacy (Prescription → Dispense) | PHARMACY, CLINICAL | Pharmacy API | PostgreSQL (drug master, controlled-substance ledger — append-only) | Interaction/allergy/dose check gate; controlled-substance audit | Controlled-substance chain-of-custody (per country, `08`) | Unit, Integration, Clinical Safety test (Wrong Medication/Dose), E2E | UNKNOWN — REQUIRES EVIDENCE | Canary → wave rollout |
| 7 | Laboratory (Order → Result) | LABORATORY, CLINICAL | Lab API (LIS) | PostgreSQL (order/result); barcode specimen chain-of-custody | Critical-result escalation with mandatory acknowledgment | Clinical Safety — Critical Result Miss hazard | Unit, Integration, Clinical Safety test, E2E | UNKNOWN — REQUIRES EVIDENCE | Canary → wave rollout |
| 8 | Radiology (Order → Report) | RADIOLOGY, CLINICAL | Radiology API (RIS) + DICOM/DICOMweb PACS integration | Object Storage (DICOM images — never PostgreSQL, ADR-005); PostgreSQL (report/metadata only) | Critical-finding escalation; PACS-transfer retry-on-failure | PACS/imaging conformance — UNKNOWN, REQUIRES EVIDENCE (`08`) | Unit, Integration, DICOM interoperability test, Clinical Safety test, E2E | UNKNOWN — REQUIRES EVIDENCE | Canary → wave rollout |
| 9 | Billing (Charge → Payment) | BILLING, PAYMENTS | Billing API | PostgreSQL (immutable ledger, NUMERIC-typed — never floating point, L9) | Financial-integrity constraints; payment tokenization (no raw card storage) | PCI DSS applicable baseline — REQUIRES independent scope assessment (`08`) | Unit, Integration, Financial-integrity test, E2E | UNKNOWN — REQUIRES EVIDENCE | Canary → wave rollout |
| 10 | Insurance & Claims (Eligibility → Remittance) | INSURANCE, CLAIMS, REVENUE CYCLE | Payer Adapter Framework | PostgreSQL | Payer-adapter isolation (no payer-specific code in Global Core, L6) | National/payer-specific submission rules — per country, UNKNOWN | Unit, Integration, Contract test (per payer adapter), E2E | UNKNOWN — REQUIRES EVIDENCE | Canary → wave rollout |
| 11 | Incident (Platform Incident Response) | CONTROL PLANE, AUDIT | Control Plane console | PostgreSQL (audit log — append-only) | Security Operations, break-glass audit trail | N/A (operational) | Incident-response drill (tabletop, not yet run) | UNKNOWN — REQUIRES EVIDENCE | N/A — response process, not a release |
| 12 | Release (Deployment / Release Workflow) | CONTROL PLANE | Release Management API | Configuration Hierarchy (`04`) | Compatibility validation gate before canary | N/A (operational) | Compatibility validation, canary monitoring, rollback drill | UNKNOWN — REQUIRES EVIDENCE | Canary → Wave 1 → Wave 2 → Wave 3 → 100% |

## Tier 2 — Domain/Data Links Only (NOT YET TRACED for Security/Compliance/Test/Evidence)

| Workflow (`05`) | Owning Domain(s) (`03`) | Data (`04`) | Security/Compliance/Test/Evidence |
|---|---|---|---|
| Organization Creation | ORGANIZATION, CONTROL PLANE | PostgreSQL | NOT YET TRACED |
| Hospital Provisioning | ORGANIZATION, CONTROL PLANE | PostgreSQL | NOT YET TRACED |
| Clinic Provisioning | ORGANIZATION, CONTROL PLANE | PostgreSQL | NOT YET TRACED |
| ICU (extends #5) | ICU | PostgreSQL | NOT YET TRACED |
| Surgery | OPERATING ROOM | PostgreSQL | NOT YET TRACED |
| Nursing | NURSING | PostgreSQL | NOT YET TRACED |
| Revenue Cycle (orchestration) | REVENUE CYCLE | PostgreSQL | NOT YET TRACED |
| Government E-Invoicing | GOVERNMENT INTEGRATIONS | Interoperability Layer | NOT YET TRACED |
| Patient Mobile App | PATIENT, COMMUNICATIONS | — (client-side) | NOT YET TRACED |
| Doctor Workflow | CLINICAL, SPECIALTIES | PostgreSQL | NOT YET TRACED |
| Notification Workflow | NOTIFICATIONS | Messaging (Pub/Sub) | NOT YET TRACED |
| Integration Workflow | INTEROPERABILITY | Interoperability Layer | NOT YET TRACED |
| Maintenance Workflow | CONTROL PLANE | Configuration Hierarchy | NOT YET TRACED |
| Release Rollback Workflow | CONTROL PLANE | Configuration Hierarchy | NOT YET TRACED |
| Disaster Recovery Workflow | DISASTER RECOVERY | All stateful components (`17`) | NOT YET TRACED |

## Domains With No Directly-Owned Tier 1/Tier 2 Workflow Row Above
The following domains from `03` are cross-cutting or support-role and
don't map to one specific workflow row; they support multiple rows
above instead: PLATFORM, IDENTITY, MEMBERSHIP, AUTHORIZATION, INVENTORY,
PROCUREMENT, DOCUMENTS, TERMINOLOGY, COMPLIANCE, ANALYTICS, AI,
OBSERVABILITY. This is expected, not a gap — a cross-cutting domain's
traceability lives in every row it supports rather than one row of its
own.

## Definition of Done for This Matrix
- [x] Every Tier 1 workflow has a full row.
- [x] Every Tier 2 workflow is listed with its domain/data link.
- [ ] Every Tier 2 workflow has Security/Compliance/Test/Evidence traced
      to the same depth as Tier 1 — **open, tracked here explicitly.**
- [ ] Every row's Evidence column has moved past `UNKNOWN — REQUIRES
      EVIDENCE` — **blocked on Foundation Implementation actually
      starting; not fabricated ahead of that.**
