# 02 — MASTER SYSTEM MAP

STATUS: PROPOSED
EVIDENCE CLASS: DESIGN

## Status
TARGET ARCHITECTURE / PROPOSED.

## Purpose
Enumerate every service/capability that exists inside each of the three
planes defined in `01-MASTER-SYSTEM-ARCHITECTURE.md`, so no capability is
designed twice under different names in later documents.

## Scope
A flat inventory, one line per service, grouped by plane. Behavior detail
lives in `03-MASTER-DOMAIN-MAP.md`; this document is the index.

## Current Assumptions
Every service listed below is a logical capability, not necessarily a
separate deployable unit — deployment granularity is decided in
`13-MASTER-INFRASTRUCTURE-ARCHITECTURE.md`, staged per
`20-MASTER-IMPLEMENTATION-ROADMAP.md`.

## Evidence
UNKNOWN — REQUIRES EVIDENCE (see `01`).

## Decision — The Map

```
CONTROL PLANE
 ├─ Global Command Center (dashboard, incidents, health)
 ├─ Organization Lifecycle (create/activate/suspend/archive/decommission)
 ├─ Provisioning Engine (saga-based facility/module setup)
 ├─ Configuration Hierarchy (global→country→org→facility→dept→module)
 ├─ Release Management (canary, waves, rollback)
 └─ Security & Compliance Ops (IAM, privileged access, incidents, evidence)

APPLICATION PLANE
 ├─ Patient Domain        (Patient 360 / MPI / Consent)
 ├─ Clinical Domain       (Encounters, Notes, Orders, Diagnoses)
 ├─ Specialty Extensions  (Cardiology, Peds, Derm, ... — on Clinical Core)
 ├─ Scheduling & Queue    (Appointments, waitlists, check-in)
 ├─ Pharmacy Domain       (Drug master, dispensing, inventory)
 ├─ Laboratory Domain     (Orders, specimens, results, QC)
 ├─ Radiology Domain      (Orders, DICOM studies, reports)
 ├─ Hospital Ops Domain   (ADT, beds, ICU, OR, nursing)
 ├─ Billing Domain        (Charge capture, invoices, payments)
 ├─ Insurance Domain      (Eligibility, claims, remittance)
 ├─ Documents & Comms     (Files, notifications, messaging)
 └─ Analytics & AI        (Dashboards, forecasting, CDS)

DATA PLANE
 ├─ PostgreSQL (system of record — OLTP)
 ├─ Redis (cache, session, queue — never source of truth)
 ├─ Object Storage (documents, DICOM instances, backups)
 ├─ Messaging / Pub/Sub primary, RabbitMQ conditional (event backbone, outbox relay — corrected 2026-08-27, see ADR-016)
 ├─ Search Index (operational search, not clinical truth)
 └─ Analytics Warehouse (read-optimized, fed by events — never written to directly)

INTEROPERABILITY LAYER
 ├─ FHIR Gateway (R4/R4B production baseline, R5 optional — corrected 2026-08-27)
 ├─ HL7 v2 Adapter (ADT/ORM/ORU/MDM)
 ├─ DICOM / DICOMweb Gateway
 ├─ IHE Profile Adapters (XDS, PIX/PDQ, XCA, XCPD)
 ├─ Government Country Adapters (isolated per country)
 ├─ Payer Adapter Framework
 └─ Patient/Clinician App Edge (mobile + web API surface)
```

## Alternatives Considered
- A single undifferentiated "services" list without plane grouping — rejected
  because it re-creates the ambiguity `01` was written to remove.

## Security Impact
This map is the authoritative source for "which plane owns which service" —
used by `07-MASTER-SECURITY-MAP.md` to assign authorization boundaries per
service rather than per ad-hoc grouping.

## Operational Impact
Each bullet above becomes exactly one entry in the eventual service catalog
and on-call ownership table (target of `20-MASTER-IMPLEMENTATION-ROADMAP.md`).

## Performance Impact
N/A — inventory document.

## Compliance Impact
N/A directly; used by `08-MASTER-COMPLIANCE-MAP.md` to ensure every
data-classification requirement has a home.

## Failure Modes
A service appearing in a workflow (`05`) but missing from this map is a
documentation defect and must be treated as blocking for that workflow's
Definition of Done.

## Dependencies
Depends on `01`. Feeds `03`, `05`, `06`, `07`, `13`.

## Unknowns
UNKNOWN whether any of these logical services already exist in any form —
REQUIRES EVIDENCE before this map can be reconciled against reality.

## Validation
Cross-check: every domain in `03-MASTER-DOMAIN-MAP.md` must appear
somewhere in this map, and every service here must have a corresponding
domain entry. No orphans in either direction.

## Rollback
N/A at design stage.

## Definition of Done
Zero orphaned services (present here, absent from `03`) and zero orphaned
domains (present in `03`, absent from here).
