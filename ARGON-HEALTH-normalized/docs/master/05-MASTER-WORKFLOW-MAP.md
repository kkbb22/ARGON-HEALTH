# 05 — MASTER WORKFLOW MAP

**STATUS:** TARGET ARCHITECTURE / PROPOSED
**EVIDENCE CLASS:** DESIGN

## Status
TARGET ARCHITECTURE / PROPOSED.

## Purpose
Document all 30 master workflows named in the originating prompt, each
with a consistent 15-field profile (Trigger, Actor, Preconditions, Steps,
Data, Events, Permissions, External Integrations, Success State, Failure
State, Retry, Audit, Notifications, Rollback, Monitoring), so
implementation has one unambiguous behavioral spec per workflow.

## Scope
30 workflows, tiered like `03-MASTER-DOMAIN-MAP.md`: **Tier 1** (12 slots
covering 15 named workflows via natural pairings) gets full step-by-step
depth. **Tier 2** (15 workflows) gets complete-but-compact profiles,
several cross-referencing the master document that owns their full detail
(Organization Provisioning → `11`; Integration mechanics → `06`; Disaster
Recovery → `17`) to avoid duplicating content across documents.

## Current Assumptions
Every workflow below composes commands/events already defined per-domain
in `03-MASTER-DOMAIN-MAP.md` — no workflow invents a new command that
doesn't trace back to an owning domain.

## Evidence
UNKNOWN — REQUIRES EVIDENCE (see `01`).

---

# TIER 1 — FULL-DEPTH WORKFLOWS

## 1. Patient Registration
- **Trigger:** New patient presents, or self-registers via Patient App.
- **Actor:** Registration staff, or patient (self-service).
- **Preconditions:** Facility active; registration module entitled.
- **Steps:** Capture demographics → MPI identity resolution (check for
  existing record) → capture consent → assign facility-scoped identifier →
  link/merge if candidate match found → create Patient 360 record.
- **Data:** Demographics, ContactInfo, ConsentRecord (Patient domain, `03`).
- **Events:** PatientRegistered, ConsentChanged, (optionally)
  DuplicatesMerged.
- **Permissions:** Registration staff (facility-scoped); patient self-write
  restricted to own record after identity verification.
- **External Integrations:** Optional national ID lookup (`Government
  Integrations` domain, country adapter).
- **Success State:** Patient record active, consent captured, no
  unresolved duplicate flags.
- **Failure State:** MPI flags an ambiguous match — record held in
  "pending identity resolution," not activated.
- **Retry:** Demographic capture is idempotent per submission; ID-lookup
  failures are retried with backoff, falling back to manual entry.
- **Audit:** Every registration and every MPI match decision logged.
- **Notifications:** Welcome/consent-confirmation message if patient has
  an active channel (`Notifications` domain).
- **Rollback:** A wrongly created record is deactivated, never deleted —
  merge/correction workflow applies.
- **Monitoring:** Duplicate-creation rate as a data-quality KPI.

## 2. Appointment & Check-in
- **Trigger:** Booking request (patient app, staff, referral) reaching its
  scheduled date.
- **Actor:** Patient, reception staff.
- **Preconditions:** Patient record exists; provider calendar has an open
  slot.
- **Steps:** Search availability → book slot (locked) → send reminder(s) →
  patient arrives → check-in confirms identity → move to Queue.
- **Data:** Appointment, Slot (Scheduling domain); QueueEntry (Queue
  domain).
- **Events:** AppointmentBooked, ReminderDue, PatientCheckedIn.
- **Permissions:** Patient self-books own appointments; reception books on
  behalf of walk-ins.
- **External Integrations:** SMS/WhatsApp/email reminder channel.
- **Success State:** Patient in queue, linked to a confirmed appointment.
- **Failure State:** Slot double-booked (must be structurally prevented,
  not just detected) or patient no-show.
- **Retry:** Reminder delivery retried per `Notifications` domain rules.
- **Audit:** Booking, rescheduling, cancellation, and check-in all logged.
- **Notifications:** Booking confirmation, reminder(s), no-show follow-up.
- **Rollback:** Cancellation releases the slot back to availability
  immediately.
- **Monitoring:** No-show rate, average wait time from check-in to seen.

## 3. Outpatient Encounter
- **Trigger:** Patient called from queue into a clinical room.
- **Actor:** Treating clinician, nursing staff.
- **Preconditions:** Active appointment/queue entry; clinician has an
  active care relationship for this encounter.
- **Steps:** StartEncounter → vitals → history/examination → diagnoses →
  orders (lab/imaging/meds) → notes finalized → treatment/care plan →
  CloseEncounter.
- **Data:** Encounter, ClinicalNote, Diagnosis, Order (Clinical domain).
- **Events:** EncounterStarted, OrderPlaced, NoteFinalized, EncounterClosed.
- **Permissions:** Treating clinician write access; other roles read-only
  unless separately granted.
- **External Integrations:** None directly — orders fan out to
  Pharmacy/Laboratory/Radiology via events.
- **Success State:** Encounter closed with finalized notes and all orders
  placed.
- **Failure State:** Encounter left open past a defined threshold —
  surfaced for follow-up, never auto-closed silently.
- **Retry:** N/A — clinical documentation is not a retryable batch
  operation; amendments are the correction path.
- **Audit:** Full read/write trail per `Clinical` domain audit rules.
- **Notifications:** Follow-up reminder if a care plan requires one.
- **Rollback:** No delete of finalized content — amendment only.
- **Monitoring:** Average encounter duration, open-encounter aging.

## 4. Emergency
- **Trigger:** Patient arrival at ED, walk-in or ambulance.
- **Actor:** ED nursing staff (triage), ED physician.
- **Preconditions:** ED module entitled for the facility.
- **Steps:** Arrival registration (can be provisional if identity unknown)
  → Triage (acuity score) → Vitals/rapid assessment → Physician assessment
  → Orders (lab/imaging/meds) → Reassessment → Disposition decision
  (admit/discharge/transfer) → Documentation.
- **Data:** EDVisit, TriageRecord, Disposition (Emergency domain).
- **Events:** PatientTriaged, DispositionRecorded.
- **Permissions:** ED clinical staff; provisional-identity records get
  restricted access until identity is confirmed.
- **External Integrations:** None mandatory.
- **Success State:** Disposition recorded and downstream workflow
  (Admission, Discharge, or Transfer) triggered.
- **Failure State:** High-acuity triage with no physician acknowledgement
  within the defined window — must auto-escalate.
- **Retry:** N/A for clinical steps; escalation notifications retried
  until acknowledged.
- **Audit:** Triage score, every reassessment, and disposition decision
  logged with actor and timestamp.
- **Notifications:** Escalation alert to charge physician/nurse on
  unacknowledged high-acuity cases.
- **Rollback:** N/A — clinical record, amendment-only correction.
- **Monitoring:** Door-to-triage time, door-to-physician time, LWBS
  (left-without-being-seen) rate.

## 5. Admission → Inpatient
- **Trigger:** Disposition = Admit (from Emergency, Outpatient, or direct
  physician order), or scheduled elective admission.
- **Actor:** Admitting clinician, charge nurse (bed allocation), ward
  nursing staff.
- **Preconditions:** Bed availability in the required ward/unit.
- **Steps:** Admission request → Bed allocation (race-safe lock) → Patient
  arrival/transfer to ward → Nursing assessment → Physician orders → Daily
  review cycle → Discharge planning begins in parallel → Discharge order →
  Summary & follow-up.
- **Data:** Admission, Bed, NursingAssessment, MAR entries (Hospital,
  Nursing, Pharmacy domains).
- **Events:** PatientAdmitted, BedAllocated, MedicationAdministered,
  PatientDischarged.
- **Permissions:** Admitting clinician for admission order; charge nurse
  for bed allocation; administering nurse for MAR with positive-ID check.
- **External Integrations:** Optional HL7 ADT feed.
- **Success State:** Patient discharged with complete summary and
  follow-up plan.
- **Failure State:** Concurrent bed-allocation race (must be structurally
  prevented, see `Hospital` domain in `03`); MAR entry attempted without
  positive patient ID (must hard-block).
- **Retry:** Bed-allocation retries against the next available bed on
  contention, never double-assigns.
- **Audit:** Every admission, transfer, MAR entry, and discharge logged.
- **Notifications:** Family/next-of-kin notification per facility policy;
  discharge instructions to patient.
- **Rollback:** Erroneous admission is corrected via a documented
  transfer/discharge-and-readmit, not a silent record deletion.
- **Monitoring:** Length of stay, bed occupancy %, readmission rate.

## 6. Pharmacy (Prescription → Dispense)
- **Trigger:** Clinical order for medication (OrderPlaced event from
  Clinical domain).
- **Actor:** Prescribing clinician, pharmacist, pharmacy technician.
- **Preconditions:** Active encounter or valid outpatient prescription
  context.
- **Steps:** Prescription received → interaction/allergy/dose check →
  pharmacist review → substitution decision (if applicable) → dispense →
  patient counseling → inventory deduction → billing trigger.
- **Data:** Prescription, DispenseRecord, InventoryBatch (Pharmacy
  domain).
- **Events:** PrescriptionCreated, InteractionFlagged,
  MedicationDispensed.
- **Permissions:** Pharmacist for dispense/substitution decisions;
  technician for stock operations only.
- **External Integrations:** Drug terminology source (`Terminology`
  domain).
- **Success State:** Medication dispensed, inventory decremented, charge
  captured.
- **Failure State:** Unresolved interaction/allergy flag — dispense
  blocked by default until a documented override with reason.
- **Retry:** N/A — a blocked dispense requires human resolution, not
  automatic retry.
- **Audit:** Every dispense logged with pharmacist ID, batch/lot, patient
  link; controlled substances get an additional immutable ledger entry.
- **Notifications:** "Ready for pickup" alert to patient where applicable.
- **Rollback:** Dispensing error corrected via a documented return/waste
  entry, never a silent inventory adjustment.
- **Monitoring:** Interaction-override rate, stockout frequency, expiry
  waste rate.

## 7. Laboratory (Order → Result)
- **Trigger:** Lab order placed from Clinical, Emergency, or Hospital
  workflows.
- **Actor:** Ordering clinician, phlebotomist/lab tech, lab
  director/pathologist.
- **Preconditions:** Test catalog entry exists and is active.
- **Steps:** Order placed → specimen collection (barcode-linked) →
  accessioning → analyzer processing → QC check → result validation →
  critical-result check → report to ordering clinician → billing trigger.
- **Data:** LabOrder, Specimen, Accession, Result (Laboratory domain).
- **Events:** LabOrderPlaced, SpecimenCollected, ResultRecorded,
  CriticalResultFlagged.
- **Permissions:** Lab tech for collection/accessioning; pathologist/lab
  director for validation and amendment.
- **External Integrations:** Analyzer interface (HL7 v2/ASTM) via
  Interoperability Layer.
- **Success State:** Result validated and delivered to ordering clinician.
- **Failure State:** Critical result with no acknowledgement within the
  defined window — must escalate automatically, never expire silently.
- **Retry:** Analyzer-interface message failures retried with backoff and
  DLQ after exhaustion.
- **Audit:** Every result view, validation, and amendment logged.
- **Notifications:** Critical-result alert to ordering clinician
  (multi-channel if unacknowledged).
- **Rollback:** Result corrections issued as amendments, original
  preserved.
- **Monitoring:** Turnaround time, critical-result acknowledgement time,
  QC failure rate.

## 8. Radiology (Order → Report)
- **Trigger:** Imaging order placed from Clinical, Emergency, or Hospital
  workflows.
- **Actor:** Ordering clinician, radiology technologist, radiologist.
- **Preconditions:** Modality available; order includes clinical
  indication.
- **Steps:** Order placed → scheduled on modality worklist → patient
  preparation → image acquisition (DICOM) → transfer to PACS →
  radiologist reading → preliminary report (if urgent) → final report →
  critical-finding check → billing trigger.
- **Data:** ImagingOrder, Study/Series/Instance, Report (Radiology
  domain).
- **Events:** ImagingOrderPlaced, StudyAcquired, ReportFinalized,
  CriticalFindingFlagged.
- **Permissions:** Technologist for acquisition; radiologist for report
  finalization and addenda.
- **External Integrations:** DICOM/DICOMweb to PACS via Interoperability
  Layer.
- **Success State:** Final report delivered, critical findings
  acknowledged if any.
- **Failure State:** PACS transfer failure — order stays open, never
  silently marked complete without a confirmed study.
- **Retry:** DICOM transfer retried with backoff; unresolved after N
  attempts routes to a technologist worklist for manual intervention.
- **Audit:** Study access and report finalization/addenda logged.
- **Notifications:** Critical-finding alert to ordering clinician.
- **Rollback:** Addendum issued for report corrections; original
  preserved.
- **Monitoring:** Report turnaround time, critical-finding acknowledgement
  time.

## 9. Billing (Charge → Payment)
- **Trigger:** Any chargeable clinical/operational event (encounter close,
  dispense, lab result, procedure).
- **Actor:** Billing staff, patient (self-service payment).
- **Preconditions:** Price list/contract exists for the charge item.
- **Steps:** Charge captured (event-driven) → priced against
  contract/price list → discounts/taxes applied → invoice generated →
  insurance portion routed to Insurance workflow → patient portion
  collected → payment reconciled → statement issued if balance remains.
- **Data:** ChargeItem, Invoice, Payment, PatientAccount (Billing domain).
- **Events:** ChargeCaptured, InvoiceIssued, PaymentReceived,
  AccountReconciled.
- **Permissions:** Billing staff for invoice/charge operations; finance
  role for corrections (credit note only, never in-place edit).
- **External Integrations:** Payment gateway; government e-invoicing
  adapter (see `06`).
- **Success State:** Invoice fully reconciled (paid + insurance-settled +
  any adjustment).
- **Failure State:** Payment gateway timeout — must not double-charge;
  idempotency key required.
- **Retry:** Gateway retries via idempotency key; e-invoicing submission
  retried with backoff, escalated to manual review after exhaustion.
- **Audit:** Every charge, invoice, payment, and credit note logged;
  posted records corrected only via reversing entries.
- **Notifications:** Invoice/receipt delivery, payment reminders for
  outstanding balances.
- **Rollback:** Correction via credit note + new charge — never an
  in-place edit of a posted record.
- **Monitoring:** Days-in-AR, collection rate, aging buckets.

## 10. Insurance & Claims (Eligibility → Remittance)
- **Trigger:** Chargeable event with an active insurance coverage on file.
- **Actor:** Registration/billing staff, payer (via adapter).
- **Preconditions:** Coverage record exists on the Patient's account.
- **Steps:** Eligibility check → (if required) prior authorization →
  service rendered → charge capture → coding attached → claim assembled →
  claim submitted → adjudication → remittance posted → denial handling/
  appeal if applicable → reconciliation.
- **Data:** Coverage, Authorization, Claim, Remittance (Insurance/Claims
  domains).
- **Events:** EligibilityChecked, ClaimSubmitted, ClaimAdjudicated,
  RemittancePosted.
- **Permissions:** Billing/coding staff for claim assembly and
  submission; finance for remittance reconciliation.
- **External Integrations:** Per-payer adapter via Payer Adapter
  Framework/Interoperability Layer.
- **Success State:** Claim paid and reconciled against the invoice.
- **Failure State:** Claim denied — routes to a denial-management queue
  with reason captured, not dropped.
- **Retry:** Resubmission after correcting the denial reason; payer
  gateway outage queues submission for retry rather than failing silently.
- **Audit:** Full claim lifecycle logged including verbatim payer
  responses for dispute resolution.
- **Notifications:** Denial alert to billing staff; patient-responsibility
  notice once adjudication is final.
- **Rollback:** Appeal workflow for disputed denials; no silent write-off
  without an approval step.
- **Monitoring:** Denial rate by reason, days-to-adjudication, appeal
  success rate.

## 11. Incident (Platform Incident Response)
- **Trigger:** Automated alert (Observability domain) or manually
  declared incident.
- **Actor:** On-call platform-ops/SRE, Control Plane operator for
  high-severity incidents.
- **Preconditions:** Incident-management tooling active in Control Plane.
- **Steps:** Declare incident → assign severity → assemble
  responders → mitigate → verify recovery → resolve → postmortem →
  compliance-evidence update if applicable.
- **Data:** Incident record (Control Plane domain).
- **Events:** IncidentDeclared, IncidentResolved.
- **Permissions:** Platform-ops for declaration/mitigation; Control Plane
  operator role for platform-wide mitigating actions (e.g., emergency
  suspension), gated by step-up MFA for the highest-severity actions (see
  `27` in the originating prompt).
- **External Integrations:** Paging/alerting channel.
- **Success State:** Incident resolved, postmortem published, any
  compliance-evidence gap logged.
- **Failure State:** Incident reopens after premature resolution —
  tracked as a distinct recurrence, not silently merged into the closed
  record.
- **Retry:** N/A — human-driven response workflow.
- **Audit:** Full timeline logged: detection, actions taken, actor,
  resolution.
- **Notifications:** Stakeholder updates per severity-based communication
  plan.
- **Rollback:** Mitigating actions (e.g., a config rollback) follow the
  Rollback workflow (Tier 2, below).
- **Monitoring:** MTTD, MTTR, recurrence rate.

## 12. Release (Deployment / Release Workflow)
- **Trigger:** A release candidate is ready for rollout (see `31` in the
  originating prompt — never "update everyone immediately").
- **Actor:** Release manager (Control Plane), automated release pipeline.
- **Preconditions:** Compatibility validation passed.
- **Steps:** Compatibility validation → canary deployment → monitor →
  Wave 1 → monitor → Wave 2 → monitor → Wave 3 → 100% → post-release
  validation.
- **Data:** ReleaseWave record (Control Plane domain).
- **Events:** ReleaseWaveStarted, ReleaseWaveCompleted, ReleaseRolledBack.
- **Permissions:** Release-manager role in Control Plane; automatic
  pause/rollback triggers do not require human permission to fire.
- **External Integrations:** CI/CD pipeline.
- **Success State:** 100% rollout with post-release validation passed.
- **Failure State:** Any wave's health signal breaches a defined
  threshold — automatic pause, then rollback if not resolved within a
  defined window.
- **Retry:** A paused release can resume only after the triggering
  condition is explicitly cleared, not automatically.
- **Audit:** Every wave transition and every pause/rollback logged with
  the triggering signal.
- **Notifications:** Release status broadcast to platform-ops.
- **Rollback:** Full rollback procedure defined per component in
  `17-MASTER-DISASTER-RECOVERY.md`.
- **Monitoring:** Per-wave error rate, latency, and business-KPI deltas
  against pre-release baseline.

---

# TIER 2 — SUPPORTING WORKFLOWS
*(complete but compact; several cross-reference the master document that
owns their full mechanics)*

## Organization Creation
Full mechanics owned by `11-MASTER-ORGANIZATION-PROVISIONING.md`. Summary:
Trigger — Control Plane operator initiates provisioning. Actor — Control
Plane operator. Preconditions — country profile and template selected.
Steps — the CREATE→VALIDATE→...→ACTIVATE saga defined in `11`. Data —
Organization, Facility (`03`). Events — OrganizationCreated. Permissions —
Control Plane operator only. External Integrations — none at this stage
(legal licensing is external and separate). Success — organization
ACTIVE. Failure — saga failure triggers compensation, not partial state.
Retry — step-level retry within the saga. Audit — every step logged.
Notifications — admin invite on activation. Rollback — full saga
compensation. Monitoring — provisioning success rate, time-to-activate.

## Hospital Provisioning
Specific instance of Organization Creation with facility type = Hospital,
triggering the fuller structure (campus/buildings/departments/units/
wards/beds/ICU/ED/OR) enumerated in the originating prompt section 5 and
detailed in `11`. Same field profile as Organization Creation above,
scoped to hospital-tier module entitlements.

## Clinic Provisioning
Specific instance of Organization Creation with facility type = Clinic —
the minimal-structure path (no wards/beds/ICU/OR). Same field profile as
Organization Creation, lighter module set.

## ICU
Extends Admission → Inpatient (Tier 1, #5) with ICU-specific acuity
tracking. Trigger — ICU admission order. Actor — ICU clinical staff.
Preconditions — ICU bed available (same race-safe lock as general Hospital
beds). Steps — AdmitToICU → continuous acuity updates → orders → transfer
out when stable. Data/Events/Permissions — per `ICU` domain in `03`.
External Integrations — bedside monitor integration is TARGET, not
designed in this pass. Success — safe transfer out or discharge. Failure —
acuity deterioration without an escalation path triggered. Retry — N/A.
Audit — every acuity change logged. Notifications — deterioration alert to
attending. Rollback — N/A (clinical, amendment-only). Monitoring — ICU
LOS, mortality-adjusted outcome tracking (facility-defined).

## Surgery
Trigger — OR case scheduled. Actor — surgical scheduling staff, surgical
team. Preconditions — OR slot available, pre-op clearance complete. Steps
— ScheduleCase → pre-op verification checklist → StartCase →
intra-op documentation → CompleteCase → post-op handoff. Data/Events —
`Operating Room` domain in `03`. Permissions — surgical team, scoped to
assigned case. External Integrations — none. Success — case completed
with full intra-op record and handoff. Failure — verification checklist
incomplete — case start blocked (wrong-site/wrong-procedure hazard, see
`16`). Retry — N/A. Audit — full case timeline logged. Notifications —
family update per facility policy. Rollback — N/A (clinical). Monitoring
— on-time case start rate, checklist-completion rate.

## Nursing
Trigger — active care plan or standing order. Actor — nursing staff.
Preconditions — active admission or encounter. Steps — RecordAssessment →
CompleteCareTask (including MAR execution, shared with Pharmacy/Hospital)
→ escalate if overdue. Data/Events — `Nursing` domain in `03`. Permissions
— assigned nursing staff. External Integrations — none. Success — care
plan tasks closed on schedule. Failure — overdue task with no
escalation — treated as a process defect. Retry — N/A. Audit — every
assessment/task logged. Notifications — overdue-task alert. Rollback —
N/A. Monitoring — task-completion-on-time rate.

## Revenue Cycle
Orchestration layer over Billing (#9) and Insurance & Claims (#10) — see
the `Revenue Cycle` domain profile in `03` for the full field set; this
entry exists only to confirm the workflow sequence: Registration →
Eligibility → Authorization → Service → Charge Capture → Coding → Claim →
Submission → Adjudication → Denial/Appeal → Remittance → Reconciliation →
Patient Responsibility. No new commands beyond what Billing/Insurance
already define.

## Government E-Invoicing
Full mechanics owned by `06-MASTER-INTEGRATION-MAP.md` (government-adapter
section) and the `Government Integrations` domain in `03`. Summary:
Trigger — invoice finalized (Billing #9). Steps — format per country
adapter → submit → await acceptance/rejection → remediate rejections.
Success — accepted submission. Failure — rejection surfaced for manual
remediation, never silently retried forever. Compliance status: REQUIRES
LEGAL VERIFICATION per country before any compliance claim.

## Patient Mobile App
Trigger — patient opens the app. Actor — patient. Preconditions —
registered account, active consent. Steps — authenticate → view
appointments/results/prescriptions/bills → book/reschedule → message
care team → pay bill → manage consent/notification preferences. Data —
read-mostly views into Patient, Scheduling, Clinical (results only, per
release rules), Billing. Events — consumed, not generated, except
patient-initiated commands (BookAppointment, SendMessage, CapturePayment).
Permissions — strictly self-scoped. External Integrations — payment
gateway, notification channels. Success — self-service action completed.
Failure — action blocked by consent/permission scope, surfaced with a
clear reason. Retry — standard API retry semantics. Audit — every
self-service action logged like any other actor. Notifications — in-app +
push. Rollback — cancel/reschedule are first-class actions, not
"rollback" per se. Monitoring — app engagement, self-service completion
rate.

## Doctor Workflow
Cross-cutting summary of a clinician's day across Scheduling, Outpatient
Encounter (#3), Orders, and results review — not a new domain, a
navigational summary. Trigger — start of clinical session. Actor —
clinician. Preconditions — active credentials, assigned schedule. Steps —
review day's schedule → see patients (Outpatient Encounter, #3 per
patient) → review pending results (Lab #7 / Radiology #8 callbacks) →
close open items. Data/Events — composed from Scheduling + Clinical +
Laboratory + Radiology, no new entities. Permissions — clinician,
self-scoped to assigned patients. External Integrations — none new.
Success — day's schedule and pending-results queue both cleared or
explicitly deferred. Failure — pending critical result unacknowledged
past threshold (see Laboratory #7 escalation). Retry — N/A. Audit —
inherits from composed workflows. Notifications — daily digest option.
Rollback — N/A. Monitoring — pending-item aging per clinician.

## Notification Workflow
Full mechanics owned by the `Notifications` domain in `03`. Summary:
Trigger — any domain event configured to notify (reminders, critical
results, billing alerts). Steps — template resolution → consent check at
send-time → channel delivery → status tracking. Success — delivered.
Failure — delivery failure logged and, for critical categories, escalated
to an alternate channel. Retry — channel-appropriate backoff. Rollback —
consent withdrawal halts future sends immediately.

## Integration Workflow
Full mechanics owned by `06-MASTER-INTEGRATION-MAP.md`. Summary: Trigger —
inbound or outbound message crossing the Interoperability Layer. Steps —
validate against profile → translate → apply/emit → acknowledge. Success
— accepted and applied/delivered. Failure — malformed message quarantined,
never partially applied. Retry — per-integration backoff/DLQ policy.
Monitoring — per-integration error rate and latency.

## Maintenance Workflow
Trigger — scheduled or emergency maintenance window. Actor — Control
Plane operator. Preconditions — maintenance-mode capability exists per
Organization/Facility (`03` Organization domain: Suspend/Maintenance
states). Steps — announce → enter maintenance mode (Application Plane
degrades gracefully, Control Plane stays available) → perform work →
verify → exit maintenance mode. Success — clean exit with health checks
passed. Failure — health check fails post-maintenance — stay in
maintenance mode, do not exit prematurely. Retry — re-run failed
health-check step. Audit — full window logged. Notifications — advance
notice to affected tenants. Rollback — pre-maintenance state restore
procedure defined per component. Monitoring — maintenance-window
duration vs. planned.

## Release Rollback Workflow
Trigger — a Release workflow (#12) breaches its automatic rollback
condition, or a manual rollback is declared. Actor — Control Plane
operator / automated pipeline. Steps — halt further wave progression →
revert to last-known-good version → verify → declare resolved or escalate
to Incident (#11) if reversion itself fails. Success — reverted and
verified healthy. Failure — rollback itself fails — this immediately
becomes a Tier-1 Incident (#11), not a repeated rollback attempt in a
loop. Audit — full sequence logged including the original triggering
signal. Monitoring — rollback frequency as a release-quality signal.

## Disaster Recovery Workflow
Full mechanics owned by `17-MASTER-DISASTER-RECOVERY.md` and the
`Disaster Recovery` domain in `03`. Summary: Trigger — declared data-loss
or project-level outage incident. Steps — assess scope → select
recovery point → restore from tested backup → verify integrity → resume
service → postmortem. Success — service resumed within defined RTO, data
loss within defined RPO. Failure — restore itself fails validation — this
is the highest-severity Incident (#11) category, escalated accordingly.
Audit — full recovery timeline logged, feeding compliance evidence (`08`).

---

## Alternatives Considered
A flat, unstructured workflow list (no tiering, no field consistency) was
rejected for the same reason given in `03`: it would make it impossible to
mechanically check "does every workflow have a defined failure state?"

## Security Impact
Every workflow's "Permissions" field must match the owning domain's
permission model in `03` and the consolidated view in `07-MASTER-SECURITY-MAP.md`.

## Operational Impact
Tier 1 workflows are the primary input to `15-MASTER-TESTING-STRATEGY.md`'s
end-to-end test scenarios.

## Performance Impact
No numbers asserted. Turnaround/latency targets referenced above (e.g.,
lab TAT, report TAT) are placeholders for future SLO definition — REQUIRES
MEASUREMENT.

## Compliance Impact
Government E-Invoicing and Disaster Recovery workflows carry the highest
compliance load — both are explicitly cross-referenced rather than
duplicated to keep a single source of truth for their compliance status.

## Failure Modes
Any workflow above without a distinct Success/Failure state pair is a
documentation defect — none should be missing one; verified at time of
writing.

## Dependencies
Depends on `01`, `02`, `03`, `04`. Feeds `06`, `07`, `11`, `15`, `17`.

## Unknowns
UNKNOWN — REQUIRES EVIDENCE whether any of these workflows has a partial
real-world implementation already.

## Validation
Every command/event referenced above traces to a domain entry in `03`.
Confirmed consistent at time of writing.

## Rollback
N/A at design stage for the document itself; individual workflows define
their own rollback behavior above.

## Definition of Done
All 30 named workflows from the originating prompt are represented (12
Tier-1 slots covering 15 named workflows via natural pairing, 15 Tier-2
entries covering the remaining 15), each with all 15 required fields
populated.
