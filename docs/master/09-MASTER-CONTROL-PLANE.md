# 09 — MASTER CONTROL PLANE

STATUS: PROPOSED
EVIDENCE CLASS: DESIGN

## Status
TARGET ARCHITECTURE / PROPOSED.

## Purpose
Define the functional surface of the Global Control Plane — what an
operator can do to the platform itself, distinct from anything a clinical
or operational user does. The security separation between this surface
and clinical data access is defined in `07-MASTER-SECURITY-MAP.md` and is
not repeated here.

## Scope
Covers Control Plane capability areas and the Organization lifecycle state
machine. The step-by-step provisioning saga is fully specified in
`11-MASTER-ORGANIZATION-PROVISIONING.md` — this document defines the
lifecycle states that saga moves an Organization through, not the saga
mechanics themselves.

## Current Assumptions
The Control Plane never touches clinical content — its entire domain is
platform state (who exists, what they're licensed for, what version
they're on, whether they're healthy).

## Evidence
UNKNOWN — REQUIRES EVIDENCE (see `01`).

## Decision

### Control Plane Capability Areas
```
GLOBAL COMMAND CENTER
 ├─ Dashboard / Organizations / Facilities / Users & Roles
 ├─ Licensing & Module Entitlements
 ├─ Feature Flags
 ├─ Maintenance & Release Management
 ├─ Incident Management
 ├─ Configuration (hierarchical — see 04, Platform domain in 03)
 ├─ Security Ops (privileged access, break-glass review)
 ├─ Compliance Evidence (feeds 08-MASTER-COMPLIANCE-MAP.md)
 ├─ Audit (platform-wide, read-restricted)
 └─ Bulk Operations
```

### Organization Lifecycle State Machine
```
CREATED → PROVISIONING → ACTIVE ⇄ MAINTENANCE
                             |
                          SUSPENDED
                             |
                          ARCHIVED → DECOMMISSIONED
```
- **CREATED** — record exists, provisioning saga not yet started.
- **PROVISIONING** — saga in flight (full detail in `11`); not yet usable
  by clinical/operational users.
- **ACTIVE** — normal operating state.
- **MAINTENANCE** — Application Plane degrades gracefully for this tenant;
  Control Plane remains available (see Maintenance workflow, `05`).
- **SUSPENDED** — access blocked platform-side, typically for billing or
  compliance reasons; data retained, reversible.
- **ARCHIVED** — read-only retention state, no active operational use.
- **DECOMMISSIONED** — terminal state; retention/deletion follows the
  data-retention policy defined per jurisdiction in `08`.

Every transition is a Control Plane command (`03` Control Plane domain:
Activate, Suspend, Maintenance, Archive, Decommission), fully audited, and
— for Suspend/Decommission specifically — treated as a high-risk operation
under `07`'s step-up-MFA/reason/approval rules.

### Bulk Operations
Any operation applied across multiple organizations (e.g., a policy
rollout) is itself modeled as a batch of individually-audited,
individually-reversible single-organization operations — never a single
opaque "apply to all" action with no per-tenant trace.

### Licensing & Module Entitlements
A license tier (defined per Organization in `03`) determines which
modules (Clinical, Pharmacy, Laboratory, Radiology, Hospital Ops, Billing,
Insurance, etc.) are entitled. Module access is enforced at the
Authorization layer (`07`) using the entitlement as an ABAC attribute —
a user with a clinical role but no Pharmacy entitlement on their
Organization cannot reach Pharmacy endpoints regardless of role.

### Licensing Lifecycle
*(closes the architectural half of GAP-004 in
`docs/audit/FINAL-GAP-ANALYSIS.md`; exact durations are explicitly left
open, not invented — see below)*
```
ACTIVE → (payment lapses) → GRACE PERIOD → (unresolved) → SUSPENDED
                                  |
                          (resolved) → ACTIVE
SUSPENDED → (unresolved past a defined window) → ARCHIVED
SUSPENDED → (resolved) → ACTIVE
Any state → (renewal) → ACTIVE (tier unchanged)
Any state → (upgrade/downgrade request, approved) → ACTIVE (new tier)
```
- **Grace Period** — data remains fully intact and exportable; clinical
  read access continues (patient safety takes precedence over a billing
  lapse); new-record creation and non-clinical modules (e.g., new
  bookings) may be restricted — exact scope of restriction is a business
  decision, not fixed here.
- **Suspended** — access blocked platform-side (mirrors the `Organization`
  Lifecycle's existing SUSPENDED state, `09` above — this is the same
  state machine, triggered by a billing event rather than a manual
  Control Plane action); data retained, fully reversible.
- **Archived** — same terminal-but-reversible-by-reactivation state as
  the general Organization Lifecycle; follows the same data-retention
  policy as any other Archived organization (`04`'s Retention, Legal
  Hold, and Deletion section).
- **Upgrade/Downgrade** — a mid-lifecycle tier change is a Control Plane
  command (`GrantLicense` with a new tier, `03`), audited identically to
  the initial grant; a downgrade that would remove entitlement to a
  module currently holding data does not delete that data — it becomes
  read-only until re-entitled, never silently purged.
- **Exact durations left open:** how many days of Grace Period, how long
  Suspended persists before Archival, and the specific restricted-scope
  list during Grace Period are **business decisions requiring input
  from whoever owns commercial/billing policy** — not architectural
  facts this document can assert. The state machine and data-safety
  guarantees above hold regardless of what those numbers turn out to be.

### Release & Incident Management
Full mechanics owned by the Release and Incident workflows in
`05-MASTER-WORKFLOW-MAP.md`. This document's role is only to confirm both
are Control-Plane-operated capabilities, visible on the Global Command
Center dashboard.

## Alternatives Considered
- **Per-organization custom provisioning scripts** (rejected) — defeats
  the goal of provisioning "in minutes" (originating prompt, section 1)
  and makes drift between organizations undetectable; see `11` for the
  templated-saga alternative adopted instead.

## Security Impact
Every capability listed above is subject to the Platform-Management vs.
Clinical-Data separation defined in `07`; this document does not grant any
additional access beyond what `07` allows.

## Operational Impact
The Global Command Center dashboard is the primary operational surface
for platform-ops/SRE — its health-monitoring view aggregates signals
defined in the `Observability` domain (`03`).

## Performance Impact
No numbers asserted. REQUIRES MEASUREMENT once implemented.

## Compliance Impact
Compliance Evidence capability here is a UI/workflow surface over the
register defined in `08` — it does not itself change any compliance
status.

## Failure Modes
An Organization stuck mid-lifecycle-transition (e.g., a Suspend that
partially applies) must be resumable to a known state, never left
ambiguous — same principle as the provisioning saga in `11`.

## Dependencies
Depends on `01`, `02`, `03`, `07`. Feeds `11`, and is referenced by `05`
(Release/Incident/Maintenance workflows).

## Related ADRs
None — the GAP-004 Licensing Lifecycle closure (2026-09-02, under
ADR-020) elaborates the existing Organization Lifecycle state machine;
no new technology or architecture decision required.

## Unknowns
UNKNOWN — REQUIRES EVIDENCE whether any Control Plane capability exists
today in any form. UNKNOWN — REQUIRES BUSINESS DECISION: exact Grace
Period / Suspended-to-Archived durations and Grace Period restriction
scope (see Licensing Lifecycle, above).

## Validation
Every Control Plane command named in `03`'s Control Plane domain profile
appears in this document's capability map. Confirmed at time of writing.

## Rollback
Every lifecycle transition above has a defined reverse or compensating
transition (e.g., Suspend → Activate) except the terminal
Decommissioned state, which follows data-retention policy rather than a
software rollback.

## Definition of Done
Every Organization in the system is, at all times, in exactly one of the
states in the lifecycle diagram above, with no undefined intermediate
state persisting beyond an in-flight saga.
