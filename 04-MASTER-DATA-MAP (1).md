# 04 — MASTER DATA MAP

## Status
TARGET ARCHITECTURE / PROPOSED.

## Purpose
Answer, for every domain in `03-MASTER-DOMAIN-MAP.md`: where does this
domain's data physically live, at what classification, with what
encryption/retention/residency rules — so no domain improvises its own
storage decision.

## Scope
Covers data-at-rest placement and classification. Data-in-motion (events)
is covered in `06-MASTER-INTEGRATION-MAP.md`; access control is covered in
`07-MASTER-SECURITY-MAP.md`.

## Current Assumptions
PostgreSQL is the single source of structural truth for the platform.
Every other store (Redis, object storage, search, warehouse) is either a
cache, a binary blob store, or a derived read model — never a second
source of truth for the same fact.

## Evidence
UNKNOWN — REQUIRES EVIDENCE (see `01`).

## Decision

### Data Location Matrix

| Domain cluster | Primary store (source of truth) | Cache (Redis) | Object storage | Analytics feed |
|---|---|---|---|---|
| Platform, Identity, Organization | PostgreSQL | Session/config cache | — | Config-change events only |
| Patient, MPI, Consent | PostgreSQL (RLS-scoped per tenant) | Read-through cache for Patient 360 assembly | Uploaded ID scans (via Documents) | De-identified aggregate only |
| Clinical, Specialties | PostgreSQL, versioned/append-only for finalized notes | Active-encounter working cache | Scanned paper records (via Documents) | Coded diagnoses/procedures (de-identified) |
| Pharmacy | PostgreSQL | Stock-level hot cache | — | Dispensing volume, stockouts |
| Laboratory | PostgreSQL | Pending-result queue | Instrument raw output archive (optional) | Turnaround-time metrics |
| Radiology | PostgreSQL (report/metadata only) | Worklist cache | **DICOM instances — object storage only, never PostgreSQL** | Report-turnaround metrics |
| Hospital Ops | PostgreSQL | Bed-state lock/cache | — | Occupancy, LOS metrics |
| Billing, Payments | PostgreSQL (NUMERIC, never float) | Invoice-render cache | Generated PDF invoices | Revenue, aging metrics |
| Insurance, Claims | PostgreSQL | Eligibility-check cache | Payer response archives | Denial-rate metrics |
| Documents | Metadata in PostgreSQL | — | Binary content — object storage | Storage-volume metrics |
| Notifications, Communications | PostgreSQL (delivery log) | Send-queue | — | Delivery-rate metrics |
| Compliance, Audit | PostgreSQL, append-only | — | Long-term audit archive (cold storage) | Compliance-status dashboards |
| Control Plane | PostgreSQL (platform-operational) | Provisioning-job state | — | Platform health dashboards |
| Analytics / Warehouse | — (derived only) | — | — | **Read side — populated by events, never written to directly by any domain** |

### Data Classification Tiers
1. **PHI** — patient-identifiable clinical data. Encrypted at rest and in
   transit, RLS-enforced per tenant, access-audited on every read.
2. **Financial** — billing/payment/claims data. NUMERIC/exact
   representation mandatory; append-only with correcting entries.
3. **Operational** — inventory, scheduling, staffing. Tenant-isolated,
   standard encryption, no elevated audit requirement beyond normal.
4. **Reference** — terminology, configuration. Not tenant-scoped in most
   cases; versioned, not encrypted beyond platform baseline.
5. **Telemetry** — must be PHI-free by construction (enforced by
   `Observability` domain in `03`).

### Cross-Cutting Data Rules
- No domain's application role can bypass tenant isolation — enforced at
  both the application layer and PostgreSQL Row-Level Security (see `01`
  Decision diagram: JWT → Tenant Context → Authorization → RLS).
- Redis holds no fact that would cause harm if lost — every Redis-resident
  value must be reconstructable from PostgreSQL or the event log.
- DICOM instances and other large binaries never transit through or land
  in PostgreSQL.
- Monetary values use PostgreSQL `NUMERIC`, never `FLOAT`/`DOUBLE`.
- Backups follow the schedule and restore-testing regime owned by the
  `Disaster Recovery` domain (`03`) and detailed in `17-MASTER-DISASTER-RECOVERY.md`.

## Alternatives Considered
- **Redis as a secondary source of truth for hot paths** (e.g., bed
  allocation) — rejected; race-condition-safety and durability both
  require a single authoritative store with proper locking, not a
  cache promoted to truth under load.
- **Storing DICOM/document binaries inline in PostgreSQL (bytea)** —
  rejected per the originating prompt's explicit constraint and standard
  practice; large binaries degrade OLTP performance and backup size.

## Security Impact
This matrix is the primary input to encryption-at-rest scoping and to
`07-MASTER-SECURITY-MAP.md`'s per-store threat model.

## Operational Impact
Backup/restore procedures differ per store (transactional PITR for
PostgreSQL vs. object-storage versioning/lifecycle rules) — both must be
defined before any store is considered production-eligible.

## Performance Impact
No numbers asserted. REQUIRES MEASUREMENT once implemented — see `29`
performance-budget principle in the originating prompt.

## Compliance Impact
Data classification tiers above feed directly into `08-MASTER-COMPLIANCE-MAP.md`'s
per-control applicability (e.g., PHI tier triggers stricter controls than
Reference tier).

## Failure Modes
- Cache-store outage must degrade to direct-store reads, never to stale
  data presented as current without a staleness indicator.
- Object-storage outage must block operations depending on that binary
  (e.g., can't finalize a radiology report without the study existing),
  not silently proceed without it.

## Dependencies
Depends on `01`, `02`, `03`. Feeds `07`, `13`, `17`.

## Unknowns
UNKNOWN — REQUIRES EVIDENCE whether any existing data currently lives
outside this matrix's intended placement.

## Validation
Every domain in `03` must map to at least one row in the Data Location
Matrix above. Confirmed at time of writing.

## Rollback
N/A at design stage. For implementation: any store migration must be
additive (dual-write/backfill/cutover) — never a destructive first step.

## Definition of Done
Every domain's data has exactly one declared source of truth, and every
non-source-of-truth store for that data is explicitly labeled as
cache/derived/binary rather than left ambiguous.
