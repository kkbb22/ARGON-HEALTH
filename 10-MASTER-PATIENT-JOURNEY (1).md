# 10 — MASTER PATIENT JOURNEY

## Status
TARGET ARCHITECTURE / PROPOSED.

## Purpose
Provide the patient-centric lens across every domain and workflow already
defined — one longitudinal view, and one journey map — so no module is
tempted to build a second patient identity or a competing "patient
timeline."

## Scope
Covers the Patient 360 assembled-view structure and the end-to-end
journey stage sequence. Each stage below cross-references the workflow
that owns its detailed mechanics in `05-MASTER-WORKFLOW-MAP.md` rather
than re-deriving it.

## Current Assumptions
Patient identity is owned exactly once, by the `Patient`/`MPI` domains in
`03-MASTER-DOMAIN-MAP.md`. Pharmacy, Laboratory, Radiology, and Hospital
Ops reference that identity; none of them store a second copy.

## Evidence
UNKNOWN — REQUIRES EVIDENCE (see `01`).

## Decision

### Patient 360 — Assembled View
```
PATIENT
 ├─ Identity & Demographics        (Patient, MPI domains)
 ├─ Contacts & Family
 ├─ Consent                        (Consent domain)
 ├─ Insurance / Coverage           (Insurance domain)
 ├─ Encounters                     (Clinical domain)
 ├─ Orders                         (Clinical → Pharmacy/Lab/Radiology)
 ├─ Results                        (Laboratory, Radiology domains)
 ├─ Medications                    (Pharmacy domain)
 ├─ Procedures                     (Clinical, Operating Room domains)
 ├─ Documents & Imaging            (Documents, Radiology domains)
 ├─ Claims & Payments              (Insurance, Billing domains)
 └─ Timeline                       (assembled read view — event-sourced,
                                     never a second write path)
```
The Timeline is a read-time composition over events already emitted by
every domain above — it is analytics-adjacent (`Analytics` domain, `03`)
in that it never writes back to any domain and is always regenerable from
the event log.

### Journey Stage Sequence
Each stage names its owning workflow in `05-MASTER-WORKFLOW-MAP.md`:

1. **Registration & Identity Verification** — `Patient Registration` (05 §1).
2. **Insurance / Consent Capture** — folded into Registration (05 §1);
   Consent domain (`03`) governs ongoing scope.
3. **Appointment Booking & Reminder** — `Appointment & Check-in` (05 §2).
4. **Check-in** — `Appointment & Check-in` (05 §2).
5. **Encounter** (outpatient, emergency, or inpatient admission) —
   `Outpatient Encounter` (05 §3) / `Emergency` (05 §4) / `Admission →
   Inpatient` (05 §5), selected by care setting.
6. **Orders** (lab/imaging/medication) — fanned out to `Pharmacy` (05
   §6), `Laboratory` (05 §7), `Radiology` (05 §8) from the encounter.
7. **Results & Reports** — delivered back into the encounter per the
   owning workflow's "Success State."
8. **Treatment / Care Plan** — recorded in Clinical (`03`), executed via
   Nursing/Pharmacy where applicable (05, Tier 2: Nursing).
9. **Follow-up** — scheduled via `Appointment & Check-in` (05 §2) or
   `Notification Workflow` (05, Tier 2) reminder.
10. **Billing & Payment** — `Billing` (05 §9) and `Insurance & Claims`
    (05 §10) run in parallel once charges are captured.
11. **Feedback / Outcome** — optional patient-reported outcome or
    satisfaction capture via `Patient Mobile App` (05, Tier 2); feeds
    `Analytics` (`03`), never a clinical-record field.

## Alternatives Considered
- **A domain-by-domain patient view (query each module separately and
  merge in the UI)** — rejected; this reintroduces the exact
  identity-duplication risk section 7/8 of the originating prompt warns
  against, and makes the Timeline non-reusable across Patient App, staff
  dashboards, and Analytics.

## Security Impact
Every read of the Patient 360 view is subject to the same purpose-of-use
and active-care-relationship checks defined per-section in `07-MASTER-SECURITY-MAP.md`
— assembling a 360 view does not create a new, looser access path into
the underlying domains.

## Operational Impact
Timeline assembly performance depends on the event backbone (`06`) being
healthy; a lagging event stream degrades Timeline freshness, which must
be surfaced (per `Analytics` domain staleness-indicator rule in `03`),
never hidden.

## Performance Impact
No numbers asserted. REQUIRES MEASUREMENT once implemented.

## Compliance Impact
Consent scope (`Consent` domain, `03`) gates which sections of the 360
view are visible to which external integrations — inherits `08`'s
data-subject-rights controls.

## Failure Modes
A partial assembly failure (e.g., Radiology service down while building a
360 view) must degrade to "this section unavailable," never silently omit
the section without indicating it's missing.

## Dependencies
Depends on `01`, `02`, `03`, `05`. Cross-references every domain and
workflow document rather than duplicating their content.

## Unknowns
UNKNOWN — REQUIRES EVIDENCE whether a unified patient view exists in any
current implementation.

## Validation
Every domain listed in the Patient 360 diagram above has a corresponding
full entry in `03-MASTER-DOMAIN-MAP.md`. Confirmed at time of writing.

## Rollback
N/A — read-only assembled view; nothing to roll back independent of the
underlying domains.

## Definition of Done
A single Patient 360 query can answer "what has happened to this patient,
end to end" without any client needing to separately query more than one
composed endpoint.
