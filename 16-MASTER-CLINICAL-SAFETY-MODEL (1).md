# 16 — MASTER CLINICAL SAFETY MODEL

## Status
TARGET ARCHITECTURE / PROPOSED.

## Purpose
Apply a Hazard → Risk → Mitigation → Verification → Evidence chain to
every clinically significant function, so a design intention (e.g.,
"positive patient ID") is never confused with a verified safety control.

## Scope
Covers the minimum hazard set named in the originating prompt. Each
hazard cross-references the domain/workflow that owns its mitigation
rather than re-describing that mitigation's mechanics.

## Current Assumptions
A mitigation is not "done" until it has a Verification method (from `15`)
and, eventually, Evidence (tracked the same way as `08`'s compliance
evidence) — design intent alone is status DESIGNED, nothing higher.

## Evidence
UNKNOWN — REQUIRES EVIDENCE (see `01`).

## Decision

### Hazard Register

| Hazard | Risk | Mitigation (owning domain/workflow) | Verification (test type, `15`) | Evidence status |
|---|---|---|---|---|
| Wrong Patient | Care/medication delivered to the wrong individual | Positive ID checks at MAR (`Hospital` domain, `03`), MPI ambiguity holds (`MPI` domain, `03`) | Security/E2E — DENY MAR entry on ID mismatch | DESIGNED |
| Wrong Medication | Interaction/allergy-inappropriate drug dispensed | Mandatory interaction/allergy check before dispense (`Pharmacy` domain, `03`; `05` §6) | Security — DENY dispense on unresolved flag | DESIGNED |
| Wrong Dose | Dose outside safe range administered | Dose-check as part of the same Pharmacy interaction-check gate | Unit/Integration — dose-range validation cases | DESIGNED |
| Wrong Procedure | Incorrect or wrong-site surgical procedure performed | Mandatory pre-op verification checklist blocking case start (`Operating Room` domain, `03`; `05` Tier 2 Surgery) | Security — DENY case start without completed checklist | DESIGNED |
| Wrong Result | A result attributed to the wrong patient/specimen | Barcode-linked specimen accessioning (`Laboratory` domain, `03`) | Integration — specimen/order/patient chain-of-custody tests | DESIGNED |
| Duplicate Orders | Redundant or conflicting orders placed | Active-order visibility at order-entry time (`Clinical` domain, `03`, GetActiveOrders query) | Integration — duplicate-order detection tests | DESIGNED |
| Critical Result Miss | A critical lab/imaging finding goes unacknowledged | Mandatory escalation on unacknowledged critical flag (`Laboratory`, `Radiology` domains, `03`; `05` §7–8) | Failure-mode/E2E — escalation-fires test on simulated non-response | DESIGNED |
| Stale Data | A decision made on outdated information presented as current | Staleness indicators on any derived/cached view (`Analytics` domain, `03`; `04` cache rules) | Integration — staleness-indicator presence test | DESIGNED |
| Unavailable Integration | A clinical decision proceeds assuming an unreachable external system's data | Explicit "unavailable" state surfaced rather than silently omitted (`06` Interoperability failure modes) | Failure-mode testing — simulated integration outage | DESIGNED |
| Downtime | Clinical work blocked or corrupted by a platform outage | Plane-independent degradation (`01`), Maintenance workflow graceful-degradation (`05` Tier 2) | Load/Stress/Failure testing — planned and unplanned outage drills | DESIGNED |

## Alternatives Considered
- **Treating clinical safety as a subset of general QA** (rejected) — the
  originating prompt calls for a distinct hazard-tracked model precisely
  because these failure modes carry patient-harm consequences that
  general functional-bug tracking doesn't weight correctly.

## Security Impact
Several mitigations above (Wrong Patient, Wrong Medication, Wrong
Procedure) are simultaneously security-authorization concerns — see the
corresponding DENY test cases, which live in the same Security test layer
defined in `15`.

## Operational Impact
Every hazard's Evidence status must be reviewed on the same cadence as
`08`'s compliance register — clinical safety evidence decays over time
(a mitigation that was tested once, two major releases ago, is not
current evidence).

## Performance Impact
N/A directly — though "Critical Result Miss" and "Downtime" mitigations
have latency-sensitive components tracked in `18`.

## Compliance Impact
Where a final feature is classified in a way that triggers ISO 14971/IEC
62304 applicability (`07` Security Standard Baseline), this hazard
register is a direct input to that risk-management-file requirement —
applicability itself remains UNKNOWN pending that classification.

## Failure Modes
A hazard whose Evidence status is asserted higher than DESIGNED without a
corresponding Verification record on file is a critical documentation
defect — equivalent in severity to a compliance status skip in `08`.

## Dependencies
Depends on `01`, `03`, `05`, `06`, `07`, `15`. Feeds `08` (where
applicable), `20` (roadmap prioritization — hazard mitigation work is
release-gating, not backlog-optional).

## Unknowns
UNKNOWN — REQUIRES EVIDENCE whether any of these mitigations exist or
have been verified in any current implementation.

## Validation
Every hazard's Mitigation column points to a real domain/workflow
citation in `03`/`05`/`06`. Confirmed at time of writing.

## Rollback
N/A — this is a risk-tracking document, not a deployed change.

## Definition of Done
No hazard in this register has an Evidence status above DESIGNED without
a linked Verification artifact; every hazard maps to at least one
Verification test type from `15`.
