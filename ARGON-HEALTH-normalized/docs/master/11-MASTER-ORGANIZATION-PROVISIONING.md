# 11 — MASTER ORGANIZATION PROVISIONING

STATUS: PROPOSED
EVIDENCE CLASS: DESIGN

## Status
TARGET ARCHITECTURE / PROPOSED.

## Purpose
Fully specify the provisioning saga that moves an Organization from
CREATED to ACTIVE (state machine owned by `09-MASTER-CONTROL-PLANE.md`),
so a hospital, clinic, or any other facility type can be provisioned in
minutes without a bespoke script per customer.

## Scope
Covers the saga steps, their idempotency/retry/compensation behavior, and
the facility-type-specific structural output (e.g., what "provisioned"
means concretely for a Hospital vs. a Clinic). Legal licensing and
regulatory approval are explicitly out of scope — they happen outside the
software and are never implied by a digital Organization record reaching
ACTIVE.

## Current Assumptions
Provisioning is a saga, not a single transaction — it spans multiple
domains (Organization, Identity, Platform/Config, Control Plane) and must
be resumable and compensable at every step.

## Evidence
UNKNOWN — REQUIRES EVIDENCE (see `01`).

## Decision

### Provisioning Saga
```
CREATE
  → VALIDATE
  → COUNTRY PROFILE
  → TEMPLATE
  → STRUCTURE
  → MODULES
  → LICENSE
  → POLICIES
  → ADMINS
  → INTEGRATIONS
  → SECURITY BASELINE
  → PROVISIONING
  → VALIDATION
  → HEALTH CHECK
  → READY
  → ACTIVATE
```

| Step | What happens | Owning domain |
|---|---|---|
| CREATE | Organization record created, lifecycle = CREATED | Organization (`03`) |
| VALIDATE | Input completeness/consistency check | Control Plane |
| COUNTRY PROFILE | Attach country adapter context (residency, e-invoicing format, local codes) | Government Integrations (`03`), `06` |
| TEMPLATE | Select facility-type template (Clinic / Medical Center / Complex / Hospital / Pharmacy / Laboratory / Radiology Center / Network) | Organization |
| STRUCTURE | Instantiate facility structure per template — see Hospital example below | Organization, Hospital (`03`) |
| MODULES | Attach entitled modules per license tier | Organization, Control Plane |
| LICENSE | Set license tier, seat/usage limits | Organization |
| POLICIES | Apply security/retention/compliance policy defaults | Compliance, Security (`07`, `08`) |
| ADMINS | Provision initial admin user(s) | Identity, Membership (`03`) |
| INTEGRATIONS | Configure entitled integrations (payer, government, notification channels) | Interoperability (`06`) |
| SECURITY BASELINE | Apply RLS policies, default roles, MFA requirement | Security (`07`) |
| PROVISIONING | Execute all of the above as tracked, resumable steps | Control Plane |
| VALIDATION | Re-check the fully provisioned state against the template | Control Plane |
| HEALTH CHECK | Confirm every entitled module responds healthy for this tenant | Observability (`03`) |
| READY | All checks passed, lifecycle = PROVISIONING complete | Control Plane |
| ACTIVATE | Lifecycle = ACTIVE, tenant becomes usable | Control Plane, Organization |

### Saga Guarantees
- **Idempotency** — re-running any step with the same input produces the
  same result, never a duplicate side effect.
- **Retry** — transient failures (e.g., a downstream service timeout)
  retry with backoff before escalating.
- **Provisioning Jobs & Step Tracking** — every saga instance is a
  queryable job with per-step status, visible on the Control Plane
  dashboard (`09`).
- **Failure Recovery / Compensation** — a failed step triggers
  compensation for every already-completed step in that saga instance,
  never leaves a half-created Organization silently active.
- **Audit** — every step transition logged with actor (usually a Control
  Plane operator or an automated pipeline) and timestamp.
- **Preview Before Execution** — the fully resolved plan (which modules,
  which policies, which structure) is previewable before PROVISIONING
  actually runs.
- **Dependency Validation** — e.g., MODULES cannot exceed what LICENSE
  permits; STRUCTURE cannot reference a department type not in the
  selected TEMPLATE.
- **Bulk Provisioning** — multiple Organizations can be provisioned from
  the same template in a batch, each still an independently tracked,
  independently compensable saga instance (see `09` Bulk Operations).

### Example — Create Hospital
Selecting the Hospital template during STRUCTURE instantiates:
```
Hospital
 ├─ Campus
 │   └─ Buildings
 │       └─ Departments
 │           └─ Units
 │               └─ Wards
 │                   └─ Rooms
 │                       └─ Beds
 ├─ ICU
 ├─ Emergency
 ├─ Operating Room(s)
 ├─ Pharmacy (facility-scoped)
 ├─ Laboratory (facility-scoped)
 ├─ Radiology (facility-scoped)
 ├─ Billing configuration
 ├─ Insurance configuration
 ├─ Initial Users & Roles
 ├─ Policies
 └─ Integrations
```
A Clinic template instantiates the same MODULES/LICENSE/POLICIES/ADMINS/
INTEGRATIONS/SECURITY BASELINE steps but a minimal STRUCTURE (no
Campus/Wards/ICU/OR) — see `05-MASTER-WORKFLOW-MAP.md` Tier 2 entries for
Hospital Provisioning and Clinic Provisioning, which point back here for
full mechanics.

### Explicit Non-Scope
Reaching ACTIVATE means the **digital** organization is provisioned and
usable. It does not mean: legal business licensing is complete, physical
facility inspection has passed, or any government regulatory approval has
been granted. Those are separate, externally-tracked processes and must
never be inferred from software state.

## Alternatives Considered
- **Manual per-customer setup** (rejected) — cannot meet the "minutes, not
  weeks" provisioning goal and produces undetectable drift between
  organizations over time.
- **Single non-resumable transaction spanning every step** (rejected) —
  a failure partway through a dozen-domain operation would either lock
  the whole operation (poor availability) or risk partial commits across
  domains that don't share a database transaction boundary; the saga
  pattern with compensation is the standard answer to this class of
  problem.

## Security Impact
POLICIES and SECURITY BASELINE steps must apply the strictest applicable
default (deny-by-default entitlements, MFA required) — a newly
provisioned Organization must never start in a looser security posture
than an existing one of the same type.

## Operational Impact
Every provisioning job is visible and resumable from the Control Plane
dashboard (`09`) — no provisioning step should ever require direct
database intervention to recover from a failure.

## Performance Impact
No numbers asserted for saga completion time. "Minutes" is a target
stated in the originating prompt, not a measured figure — REQUIRES
MEASUREMENT.

## Compliance Impact
The COUNTRY PROFILE step is where jurisdiction-specific compliance
posture (`08`) starts applying to a tenant — an Organization must not
reach ACTIVE without a resolved country profile.

## Failure Modes
A saga stuck in PROVISIONING past a defined timeout is surfaced as an
Incident (`05` Incident workflow), not left silently pending
indefinitely.

## Dependencies
Depends on `01`, `02`, `03`, `06`, `07`, `08`, `09`. Referenced by `05`
(Organization Creation / Hospital Provisioning / Clinic Provisioning
workflows).

## Unknowns
UNKNOWN — REQUIRES EVIDENCE whether any provisioning automation exists
today in any form.

## Validation
Every step above maps to exactly one owning domain in `03`; no step is
left without a clear owner. Confirmed at time of writing.

## Rollback
Compensation is the rollback mechanism for an in-flight saga (see Saga
Guarantees above). For a fully ACTIVE organization that must be
reversed, the Organization Lifecycle's Suspend/Archive/Decommission
states (`09`) are the correct mechanism — not a re-run of this saga in
reverse.

## Definition of Done
An Organization cannot reach ACTIVE with any saga step in a failed or
skipped state; every ACTIVE organization has a complete, auditable saga
history from CREATE through ACTIVATE.
