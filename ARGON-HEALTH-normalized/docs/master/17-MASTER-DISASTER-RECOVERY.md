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
platform-critical state (Terraform state, configuration, secrets). Full
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
| RabbitMQ | Mirrored/quorum queues + periodic definition export | Depends on queue durability config — REQUIRES definition | TBD | Scheduled failover drill | Cluster-level failover | Platform-ops |
| Object Storage (Cloud Storage) | Multi-region replication + versioning/lifecycle policy | Near-zero (provider-managed durability) | TBD | Scheduled retrieval-integrity drill | Provider-managed | Platform-ops |
| Terraform State | Remote state backend with versioning + locking | N/A (config, not runtime data) | TBD | State-restore drill before any major infra change | N/A | Infrastructure lead |
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

## Unknowns
UNKNOWN — every RTO target in the register above pending business
continuity sign-off. UNKNOWN — REQUIRES EVIDENCE whether any backup or
restore capability currently exists for any component.

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
