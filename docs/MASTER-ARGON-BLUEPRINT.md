ARGON HEALTH PLATFORM
MASTER BLUEPRINT

STATUS: PROPOSED
EVIDENCE CLASS: DESIGN

## Status
TARGET ARCHITECTURE / PROPOSED. This is a synthesis index over
`docs/master/01`–`20`. It introduces no new decisions — every claim below
points to the document that owns it. STATUS AT END OF DOCUMENT:
**TARGET ARCHITECTURE COMPLETE** — not PRODUCTION READY, not a claim of
compliance or certification, not the start of implementation.

---

## 1. Vision
ARGON HEALTH PLATFORM is a healthcare operating system designed to scale
from a single clinic to hospital networks, spanning EMR, pharmacy,
laboratory, radiology, hospital operations, billing, insurance, and
government/interoperability integration, under one control plane and one
role-aware application design.

## 2. System Scope
Clinic → Medical Center → Medical Complex → Hospital → Hospital Network,
plus standalone Pharmacy, Laboratory, and Radiology Center facility
types — all provisionable from a central Control Plane (`09`, `11`).

## 3. Principles
No plane collapses into another (`01`). No domain owns another domain's
identity data (`03`, `10`). No country-specific rule leaks into Global
Core (`06`). No compliance status skips its evidence gate (`08`). No
numeric claim is invented (`17`, `18`). No implementation starts from
this foundation pass alone (`20`).

## 4. System Map
Full inventory in `02-MASTER-SYSTEM-MAP.md`: Control Plane, Application
Plane (12 domain groups), Data Plane, Interoperability Layer.

## 5. Control Plane
Organization lifecycle, licensing, release management, security/
compliance ops — fully specified in `09-MASTER-CONTROL-PLANE.md`,
structurally separated from clinical access per `07-MASTER-SECURITY-MAP.md`.

## 6. Organization Provisioning
CREATE→...→ACTIVATE saga, compensable and resumable, with a worked Hospital
example — `11-MASTER-ORGANIZATION-PROVISIONING.md`. Digital provisioning
is explicitly not legal/regulatory approval (ADR-015, `19`).

## 7. Domain Map
40 domains, 15-field profiles, tiered by blast radius —
`03-MASTER-DOMAIN-MAP.md`.

## 8. Patient 360
One identity, one assembled longitudinal view, no duplicate patient
records across modules — `10-MASTER-PATIENT-JOURNEY.md`.

## 9. Clinical Core
Encounters, notes, diagnoses, orders, amendments — versioned,
auditable, original-preserving — `CLINICAL` domain in `03`.

## 10. Specialty Framework
Clinical Core + Specialty Extensions, not per-specialty forks —
`SPECIALTIES` domain in `03`.

## 11. Pharmacy
Drug master, interaction/allergy/dose checking, dispensing, controlled-
substance ledger — `PHARMACY` domain in `03`; workflow in `05` §6.

## 12. Laboratory
Order-to-result LIS with barcode-linked specimen chain-of-custody and
critical-result escalation — `LABORATORY` domain in `03`; workflow in `05` §7.

## 13. Radiology
Order-to-report RIS with DICOM/DICOMweb PACS integration; images never
in PostgreSQL — `RADIOLOGY` domain in `03`; workflow in `05` §8.

## 14. Hospital
ADT, race-safe bed allocation, ICU, OR, nursing, wrong-patient
prevention — `HOSPITAL`/`ICU`/`OPERATING ROOM`/`NURSING` domains in `03`;
workflow in `05` §5.

## 15. Billing
Charge capture through immutable, NUMERIC-typed financial ledger —
`BILLING` domain in `03`; workflow in `05` §9.

## 16. Insurance
Payer-agnostic eligibility/authorization/claims via the Payer Adapter
Framework — `INSURANCE`/`CLAIMS` domains in `03`; workflow in `05` §10.

## 17. Revenue Cycle
Orchestration sequence over Billing + Insurance — `REVENUE CYCLE` domain
in `03`; workflow in `05` Tier 2.

## 18. Government
Per-country adapters isolating e-invoicing and national-system
integration from Global Core — `06-MASTER-INTEGRATION-MAP.md`,
`GOVERNMENT INTEGRATIONS` domain in `03`.

## 19. Interoperability
FHIR R4/R4B production baseline, R5 conditional/transitional, R6
deferred (corrected 2026-08-27, see ADR-018) — HL7 v2, DICOM/DICOMweb,
IHE profiles, all behind one Interoperability Layer —
`06-MASTER-INTEGRATION-MAP.md`.

## 20. Patient App
Self-service booking, results, prescriptions, billing, consent
management — `12-MASTER-APPLICATION-ARCHITECTURE.md`.

## 21. Staff Apps
Clinician Experience, Administration, Pharmacy/Lab/Radiology consoles,
Hospital Ops console, Control Plane console — one shared design system,
RTL-first — `12-MASTER-APPLICATION-ARCHITECTURE.md`.

## 22. Security
OIDC/MFA identity, RBAC+ABAC+relationship+purpose-of-use+break-glass
authorization, three-layer enforcement (app + service + RLS), structural
Control-Plane/Clinical-access separation — `07-MASTER-SECURITY-MAP.md`.

## 23. Compliance
Requirement→Control→Implementation→Test→Evidence tracking with a
status lifecycle that never skips a gate — `08-MASTER-COMPLIANCE-MAP.md`.

## 24. Clinical Safety
Ten hazards (Wrong Patient/Medication/Dose/Procedure/Result, Duplicate
Orders, Critical Result Miss, Stale Data, Unavailable Integration,
Downtime) tracked Hazard→Risk→Mitigation→Verification→Evidence —
`16-MASTER-CLINICAL-SAFETY-MODEL.md`.

## 25. Data
PostgreSQL as sole source of structural truth; Redis/object storage/
search/warehouse all derived or binary-only; DICOM never in PostgreSQL;
money never as floating point — `04-MASTER-DATA-MAP.md`.

## 26. Infrastructure
GCP, Cloud Run (modular monolith first), Cloud SQL, Memorystore, Cloud
Storage, Secret Manager/KMS, Cloud Armor/Cloudflare, OpenTofu (replaces
Terraform, see ADR-017), GitHub Actions —
`13-MASTER-INFRASTRUCTURE-ARCHITECTURE.md`. Internal event backbone:
Google Cloud Pub/Sub primary, RabbitMQ conditional (see ADR-016).

## 27. Observability
OpenTelemetry metrics/logs/traces, PHI-scrubbed by construction —
`OBSERVABILITY` domain in `03`.

## 28. Disaster Recovery
Per-component backup/restore register; RTO/RPO numeric targets
explicitly deferred pending business sign-off rather than invented;
"backup is not complete until restore is tested" —
`17-MASTER-DISASTER-RECOVERY.md`.

## 29. Testing
Full pyramid with mandatory ALLOW+DENY security test pairs at every
authorization boundary — `15-MASTER-TESTING-STRATEGY.md`.

## 30. Technology Stack
Java 25 LTS / Spring Boot 4.1 / Spring Modulith / PostgreSQL 18 / Next.js
16 / React Native, with a managed (non-frozen) upgrade policy —
`14-MASTER-TECHNOLOGY-STACK.md`. Version drift against any earlier
ARGON stack decision is recorded, not resolved, in ADR-014 (`19`).

## 31. Dependencies
Document dependency chain: `01`→`02`→`03`→`04`/`05`→`06`/`07`/`08`→
`09`/`10`/`11`→`12`/`13`/`14`→`15`/`16`/`17`/`18`→`19`→`20`. Every later
document cites, never contradicts, an earlier one.

## 32. Roadmap
Trigger-based phases (not calendar dates): Foundation (done, this pass) →
Foundational Domains → Patient/Clinical Core → {Ancillary Clinical,
Hospital, Billing/Insurance in parallel, each independently triggered} →
Interoperability/Government (per-country trigger) → Analytics/AI, with
Production Hardening/Evidencing continuous throughout —
`20-MASTER-IMPLEMENTATION-ROADMAP.md`.

## 33. Risks
- No repository or existing implementation was evidenced against this
  target (`01`, applies platform-wide).
- *(Resolved 2026-08-27 — see below)* ~~Technology-stack version drift
  against any earlier ARGON decision~~
- All RPO/RTO and performance figures are unmeasured targets, not
  capacity claims (`17`, `18`).
- Jurisdiction-specific legal/compliance status defaults to UNKNOWN /
  REQUIRES LEGAL REVIEW for every country beyond the home jurisdiction,
  and even the home jurisdiction is not yet independently reviewed (`08`).
- Scope is large — 40 domains, 30 workflows, 8+ target jurisdictions;
  the roadmap (`20`) exists specifically to prevent building all of it
  speculatively ahead of real demand.
- `origin/main`'s actual repository state remains unverified as of the
  last check — see `docs/audit/CONTINUOUS-IMPROVEMENT-FINAL-REPORT.md`
  §13/§16.

## 34. Open Decisions
- **RESOLVED 2026-08-27 (ADR-019):** this target's relationship to
  ARGON's pre-existing architecture strategy (ADR-000,
  `argon-platform-target-architecture`, dated 2026-08-22) is now
  explicit — ADR-000 governs *whether/when* (staged, trigger-gated);
  this document set is the updated *what*. **No phase of `20` is
  authorized to start without a fired ADR-000 trigger — Phase 1 has none
  today.** The real next step is ADR-000's "build now" list inside the
  live Firebase system. Full detail:
  `docs/adr/ADR-019-RECONCILIATION-WITH-ADR-000.md`.
- Actual RTO/RPO numeric targets — pending business continuity sign-off
  (`17`).
- Actual performance budgets — pending a measured baseline (`18`).
- Which countries beyond the home jurisdiction are real near-term
  targets — determines Phase 6 sequencing (`06`, `20`).
- Whether any AI/CDS feature's final classification triggers ISO 14971/
  IEC 62304 applicability — pending feature-level review (`07`, `16`).

---

## Appendix — Remaining Required Diagrams
*(completing the minimum diagram set from the originating prompt's
Visual Architecture section; all diagrams above and below are drawn
consistently with the three-plane model in `01`)*

### Pharmacy
```
OrderPlaced (Clinical)
   → Prescription received
   → Interaction/Allergy/Dose check ──fail──> blocked, override+reason required
   → pass
   → Pharmacist review → (Substitution?) → Dispense
   → Inventory deduction → Charge captured (Billing)
```

### Laboratory
```
LabOrder placed → Specimen collected (barcode) → Accessioned
   → Analyzer processing → QC check ──fail──> hold, re-run
   → pass → Result validated → Critical? ──yes──> escalate + ack required
   → Report to ordering clinician → Charge captured
```

### Radiology
```
ImagingOrder placed → Scheduled (modality worklist) → Acquisition (DICOM)
   → PACS transfer ──fail──> order stays open, retry
   → success → Radiologist reading → Preliminary (if urgent) → Final report
   → Critical finding? ──yes──> escalate + ack required → Charge captured
```

### Hospital
```
Admission request → Bed allocation (race-safe lock) ──contended──> next bed
   → Ward transfer → Nursing assessment → Physician orders
   → Daily review ⇄ MAR execution (positive-ID required)
   → Discharge planning (parallel) → Discharge order → Summary & follow-up
```

### Billing
```
Chargeable event (any domain) → Charge captured → Priced (contract/list)
   → Discounts/Taxes → Invoice generated
   → split: [Insurance portion → Insurance workflow]
            [Patient portion → Payment collection]
   → Reconciled → Statement (if balance remains)
```

### Insurance
```
Coverage on file → Eligibility check → (Prior auth if required)
   → Service rendered → Charge + Coding → Claim assembled → Submitted
   → Adjudicated ──denied──> Denial queue → Appeal/Resubmit
                ──paid──> Remittance posted → Reconciled
```

### Release Flow
```
Candidate ready → Compatibility validation ──fail──> blocked
   → pass → Canary → monitor ──breach──> auto-pause → rollback
   → healthy → Wave 1 → monitor → Wave 2 → monitor → Wave 3 → 100%
   → Post-release validation
```

### Disaster Recovery Flow
```
Incident declared (data loss / outage)
   → Assess scope → Select recovery point (from a PRE-TESTED backup only)
   → Restore → Verify integrity ──fail──> escalate as Tier-1 incident
   → pass → Resume service → Postmortem → Evidence recorded (`08`)
```

---

## Documentation Provenance
Every section above cites the master document that owns its full detail;
this file introduces no claim not already made in `01`–`20`. Consistent
with section 40 of the originating prompt: nothing here is fabricated —
where a figure or status is unknown, it is marked as such in the owning
document, not smoothed over here.
