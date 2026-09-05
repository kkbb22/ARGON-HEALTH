# 17 — MASTER DISASTER RECOVERY

STATUS: PROPOSED
EVIDENCE CLASS: DESIGN

## Status
TARGET ARCHITECTURE / PROPOSED.

## Purpose
Define, per stateful component, the backup/restore/failover discipline —
and enforce the rule that a backup is not "done" until a restore has
actually been tested successfully.

## Scope
Covers every stateful component in the Data Plane (`04`) plus
platform-critical state (OpenTofu state, configuration, secrets). Full
mechanics of the Disaster Recovery *workflow* (the human/operational
sequence when a real incident occurs) are defined in `05-MASTER-WORKFLOW-MAP.md`
Tier 2; this document defines the per-component targets that workflow
executes against.

## Current Assumptions
RPO/RTO **numeric targets** require business continuity sign-off and are
not invented in this pass — this document records the recovery
**mechanism** available per component and marks numeric targets as
pending definition where no measured or agreed figure exists.

## Evidence
UNKNOWN — REQUIRES EVIDENCE (see `01`).

## Decision

### Per-Component DR Register

| Component | Backup mechanism | RPO capability | RTO target | Restore test cadence | Failover | Owner |
|---|---|---|---|---|---|---|
| PostgreSQL (Cloud SQL) | Continuous WAL archiving + PITR + scheduled full backups | Near-zero via PITR (exact target TBD — requires business continuity sign-off) | TBD — requires sign-off | Scheduled restore drill (frequency TBD) | Managed HA failover (`13`) | Platform-ops / DBA role |
| Keycloak DB | Same PostgreSQL mechanism as above (if co-located) or its own PITR-backed instance | Near-zero via PITR | TBD | Same cadence as PostgreSQL | Managed HA failover | Platform-ops |
| Google Cloud Pub/Sub (primary messaging) | Provider-managed durability + dead-letter topics; message retention up to 31 days provides a natural short-window replay buffer | Provider-managed (no self-hosted broker to fail) | TBD | N/A — no broker to restore; subscription/topic config restore drill still applies | Provider-managed, multi-zone by default | Platform-ops |
| RabbitMQ (conditional, adapter-specific only — see ADR-016) | Mirrored/quorum queues + periodic definition export | Depends on queue durability config — REQUIRES definition | TBD | Scheduled failover drill | Cluster-level failover | Platform-ops |
| Object Storage (Cloud Storage) | Multi-region replication + versioning/lifecycle policy | Near-zero (provider-managed durability) | TBD | Scheduled retrieval-integrity drill | Provider-managed | Platform-ops |
| OpenTofu State (was Terraform State — see ADR-017) | Remote state backend with versioning + locking; native state encryption (OpenTofu-specific improvement over the prior Terraform target) | N/A (config, not runtime data) | TBD | State-restore drill before any major infra change | N/A | Infrastructure lead |
| Configuration (`Platform` domain, `03`) | Versioned in the Configuration Hierarchy itself (`04`) + exported snapshots | Near-zero (every change already versioned) | TBD | Config-restore drill | N/A | Platform-ops |
| Critical Secrets (Secret Manager / KMS) | Provider-managed replication + documented recovery procedure | Near-zero (provider-managed) | TBD | Secret-recovery drill (access-path test, not secret-value exposure) | Provider-managed | Security lead |

### The Restore-Test Rule
**A backup is not complete until its restore has been tested.** Every row
above requires a scheduled, logged restore drill with a pass/fail result
(`Disaster Recovery` domain, `03`); "a backup job ran successfully" is
never treated as equivalent to "this data is recoverable."

### DR Workflow Trigger
When a real incident occurs, the Disaster Recovery workflow (`05` Tier 2)
executes against the targets in this register: assess scope → select
recovery point → restore from a **previously drill-tested** backup →
verify integrity → resume service → postmortem.

### Named Scenario Runbooks
*(closes GAP-010 in `docs/audit/FINAL-GAP-ANALYSIS.md` — the register
above is organized per-component; these three scenarios walk the same
register end-to-end for named, higher-likelihood catastrophic cases,
surfacing cross-component interactions a per-component table doesn't)*

**Scenario 1 — Ransomware / mass-delete incident**
1. Detect (anomalous deletion/encryption volume — `Observability` domain,
   `03`) → declare Incident (`05` §11) at highest severity.
2. Immediately suspend further writes to the affected store(s) — do not
   let a compromised credential keep destroying data while response
   organizes.
3. Identify the last known-good restore point **before** the attack
   began (requires PITR/versioned backups, per the per-component
   register above — this is why continuous PITR, not just periodic
   snapshots, matters here specifically).
4. Restore from that point per the per-component procedure (PostgreSQL
   PITR, Object Storage versioning, etc.).
5. Rotate every credential with write access to the affected store
   before resuming normal operation — a ransomware event is treated as
   a confirmed credential compromise, not just a data-loss event.
6. Resume service → postmortem, feeding `08`'s compliance evidence
   (breach-notification obligations are jurisdiction-specific, `08`).

**Scenario 2 — Full regional GCP outage**
1. Detect (multi-service, region-wide health-check failure —
   distinguishes this from a single-component outage).
2. Control Plane's own health monitoring (`09`) is the first thing that
   must survive this — if the Control Plane is single-region and down,
   no one can *initiate* a coordinated recovery response, which is
   itself a finding this scenario exists to surface (current
   architecture, `13`, is explicitly single-region; multi-region is
   Phase 8+ evidence-gated, not assumed here).
3. Communicate a known-outage status through whatever channel doesn't
   depend on the affected region (this is an operational/runbook
   detail, not an architectural one — flagged as a gap in the
   *operational* runbook, not the DR *architecture*).
4. Recovery follows GCP's own regional-recovery timeline for managed
   services (Cloud SQL, Cloud Run, etc.) — ARGON's part is verifying
   data integrity and resuming service once the region recovers, not
   an independent multi-region failover (not built, per `13`'s
   Cloud-Run-first, single-region-until-evidenced stance).

**Scenario 3 — Identity provider (Keycloak) outage**
1. Detect — distinguishes itself from other outages because its
   symptom is "no one, including responders, can authenticate,"
   including to *start* the recovery workflow.
2. This is why Keycloak's own DR entry (per-component register above)
   has the shortest acceptable RTO of any component in practice, even
   though a specific number isn't fixed here (REQUIRES business
   sign-off, same as every other RTO in this document) — every other
   recovery scenario assumes responders can log in; this one can't
   assume that.
3. Break-glass access (`07`) — a pre-provisioned, out-of-band
   credential path that does not depend on Keycloak being up — is the
   explicit answer to "how does anyone authenticate to fix
   authentication." This must exist and be drill-tested with the same
   rigor as any other restore-test in this document, not assumed as a
   theoretical escape hatch.
4. Restore Keycloak from its own DB backup (per-component register) →
   verify → resume normal-path authentication → retire the break-glass
   session used during the incident, fully audited (`07`).

## Alternatives Considered
- **Publishing invented numeric RPO/RTO targets to look complete**
  (rejected) — violates the Zero Fabrication principle (originating
  prompt, section 40); a wrong number is worse than an honestly marked
  TBD, because it creates false confidence during an actual incident.

## Security Impact
Secret-recovery drills must verify the recovery *procedure* without
exposing secret values during the drill itself — a drill design
requirement, not an afterthought.

## Operational Impact
Every component above needs a named Owner before this document can be
considered actionable — several rows above are marked with role
placeholders pending real assignment.

## Performance Impact
N/A directly; RTO targets, once defined, become inputs to `18`'s
availability SLOs.

## Compliance Impact
Restore-drill evidence is exactly the kind of artifact `08-MASTER-COMPLIANCE-MAP.md`
needs in its Evidence column for any control claiming resilience/backup
compliance.

## Failure Modes
A restore drill that fails must block any claim of DR-readiness for that
component — never quietly noted and moved past.

## Dependencies
Depends on `01`, `04`, `13`. Feeds `05` (DR workflow execution target),
`08` (evidence), `18` (RTO feeds availability SLOs once defined).

## Related ADRs
None — the GAP-010 Named Scenario Runbooks (2026-09-02, under ADR-020)
synthesize the existing per-component register into scenario form; no
new technology decision required. Scenario 2 makes explicit a known
consequence of the existing single-region stance (`13`) rather than
introducing a new one.

## Unknowns
UNKNOWN — every RTO target in the register above pending business
continuity sign-off. UNKNOWN — REQUIRES EVIDENCE whether any backup or
restore capability currently exists for any component. UNKNOWN —
REQUIRES EVIDENCE whether break-glass Keycloak-outage access (Scenario 3)
has ever been drill-tested.

## Validation
Every Data Plane component in `04-MASTER-DATA-MAP.md`'s matrix appears in
this register. Confirmed at time of writing.

## Rollback
This document's subject *is* the platform's rollback/recovery mechanism
for data loss — see the Restore-Test Rule above.

## Definition of Done
Every component has an assigned Owner, a defined (not TBD) RTO target,
and at least one passed restore drill on record before that component is
considered DR-ready.
