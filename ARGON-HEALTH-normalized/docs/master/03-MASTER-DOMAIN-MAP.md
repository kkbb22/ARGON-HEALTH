# 03 — MASTER DOMAIN MAP

STATUS: PROPOSED
EVIDENCE CLASS: DESIGN

## Status
TARGET ARCHITECTURE / PROPOSED.

## Purpose
Decompose the Application Plane (and the Control Plane, as its own domain)
into bounded domains, each with a consistent 15-field profile, so downstream
implementation work has one unambiguous definition of what each domain owns.

## Scope
39 domains, grouped by function. **Tier 1** domains (the ones most other
domains depend on, or that carry the highest clinical/financial risk) get
full-depth entries. **Tier 2** domains get complete but compact entries —
every field is populated, none are placeholders, but detail is proportional
to blast radius. Depth tiering is a documentation-effort decision, not a
statement that Tier 2 domains matter less.

## Current Assumptions
Every domain owns its own entities and never lets another domain write to
them directly — cross-domain effects happen via commands/events defined
here, never via shared-table writes.

## Evidence
UNKNOWN — REQUIRES EVIDENCE (see `01`).

## Field Legend
Purpose · Responsibilities · Entities · Commands · Queries · Events · APIs ·
Permissions · Dependencies · External Integrations · Data Classification ·
Audit Requirements · Failure Modes · Tests · Compliance Requirements ·
Definition of Done

---

# TIER 1 — FOUNDATIONAL / HIGH BLAST-RADIUS DOMAINS

## PLATFORM
- **Purpose:** Own cross-cutting platform primitives every other domain
  builds on (multi-tenancy context, feature flags, configuration resolution).
- **Responsibilities:** Resolve effective configuration per
  global→country→org→facility→department→module hierarchy; expose tenant
  context to every request; own feature-flag evaluation.
- **Entities:** TenantContext, ConfigurationNode, FeatureFlag, ModuleEntitlement.
- **Commands:** SetConfiguration, ToggleFeatureFlag, GrantModuleEntitlement.
- **Queries:** ResolveEffectiveConfig, GetTenantContext, ListEntitlements.
- **Events:** ConfigurationChanged, FeatureFlagToggled, EntitlementGranted/Revoked.
- **APIs:** Internal only — every other domain calls Platform, Platform calls no one.
- **Permissions:** Control-Plane-operator only for writes; all authenticated
  services may read resolved config for their own tenant.
- **Dependencies:** None (root domain).
- **External Integrations:** None.
- **Data Classification:** Configuration data — internal, not PHI.
- **Audit Requirements:** Every configuration write is audited with actor,
  before/after value, and effective scope.
- **Failure Modes:** Config resolution failure must fail closed (deny/most
  restrictive default), never fail open.
- **Tests:** Hierarchy override precedence (module beats department beats...
  global); ALLOW/DENY entitlement cases.
- **Compliance Requirements:** Non-overridable security policies (see `21`)
  must be structurally impossible to relax via this domain.
- **Definition of Done:** Every other domain's "Dependencies" field names
  Platform explicitly wherever it reads config.

## IDENTITY
- **Purpose:** Authenticate every human and system actor platform-wide.
- **Responsibilities:** Credential lifecycle, MFA/passkey enrollment, session
  issuance, federation with Organization-level SSO where applicable.
- **Entities:** UserAccount, Credential, Session, MFAFactor, FederationLink.
- **Commands:** Register, Authenticate, EnrollMFA, RevokeSession, ResetCredential.
- **Queries:** GetSession, ListActiveSessions, GetMFAStatus.
- **Events:** UserAuthenticated, AuthenticationFailed, SessionRevoked, MFAEnrolled.
- **APIs:** OIDC/OAuth2 token endpoints; internal session-introspection API
  for every downstream domain.
- **Permissions:** Self-service for own credentials; Org Admin for
  provisioning within their org; Control Plane for cross-org identity ops.
- **Dependencies:** Platform (tenant context on every session).
- **External Integrations:** Keycloak (or equivalent OIDC provider) as the
  identity substrate — see `20-IDENTITY` technology decision in `14`.
- **Data Classification:** Credentials — highest sensitivity, never logged
  in plaintext, never in telemetry (`28`).
- **Audit Requirements:** Every authentication attempt (success and
  failure) audited with actor, IP, device fingerprint, outcome.
- **Failure Modes:** Repeated authentication failures trigger lockout with
  rate limiting, not silent retry; MFA bypass must be structurally impossible
  outside a documented break-glass procedure.
- **Tests:** ALLOW valid credential + valid MFA; DENY valid credential +
  missing/invalid MFA where required; DENY session reuse after revocation.
- **Compliance Requirements:** MFA mandatory for any role with PHI access.
- **Definition of Done:** No domain issues its own authentication —
  everything defers to Identity's session introspection.

## ORGANIZATION
- **Purpose:** Model the legal/operational entity that owns one or more
  facilities (clinic, medical center, complex, hospital, hospital network).
- **Responsibilities:** Organization hierarchy, facility registration,
  license-tier tracking, module entitlement ownership.
- **Entities:** Organization, Facility, Department, Unit, LicenseTier.
- **Commands:** CreateOrganization, AddFacility, SetLicenseTier, Suspend, Archive.
- **Queries:** GetOrgHierarchy, ListFacilities, GetLicenseTier.
- **Events:** OrganizationCreated, FacilityAdded, LicenseTierChanged, OrganizationSuspended.
- **APIs:** Control-Plane-facing provisioning API; read API for every
  Application-Plane domain that needs org/facility scope.
- **Permissions:** Control Plane operators for creation/suspension; Org
  Admin for facility/department structure within their own org.
- **Dependencies:** Platform, Identity.
- **External Integrations:** None directly — legal licensing/regulatory
  approval is external to this domain and never auto-implied by a digital
  Organization record (see `11-MASTER-ORGANIZATION-PROVISIONING.md`).
- **Data Classification:** Business/organizational data, not PHI, but
  access-controlling — a compromise here affects every tenant beneath it.
- **Audit Requirements:** Every hierarchy or license-tier change audited
  with reason and approver.
- **Failure Modes:** A partially-created Organization (saga failure
  mid-provisioning) must be resumable or fully compensated — never left in
  an ambiguous half-active state.
- **Tests:** ALLOW facility creation under valid org+license; DENY module
  access beyond entitled license tier.
- **Compliance Requirements:** Data residency constraints per country
  attach at this level (see `06`, `17-MASTER-...` government section).
- **Definition of Done:** Every Application-Plane record can trace a
  Facility → Organization ownership chain with no orphans.

## PATIENT
- **Purpose:** Own one unified, longitudinal patient identity and view
  across every clinical and financial domain.
- **Responsibilities:** Demographics, identity resolution (MPI), consent
  state, and the assembled Patient 360 timeline.
- **Entities:** Patient, Identifier, Demographics, ContactInfo, ConsentRecord.
- **Commands:** RegisterPatient, UpdateDemographics, RecordConsent, MergeDuplicate.
- **Queries:** GetPatient360, ResolveIdentity, GetConsentStatus.
- **Events:** PatientRegistered, DemographicsUpdated, ConsentChanged, DuplicatesMerged.
- **APIs:** Internal Patient Service API consumed by Clinical, Pharmacy,
  Lab, Radiology, Hospital, Billing — none of which store a second copy of
  patient identity.
- **Permissions:** Registration staff for demographics; patient (via app)
  for consent and self-service updates; clinical roles for read access
  scoped to active care relationship.
- **Dependencies:** Platform, Identity, Organization.
- **External Integrations:** National ID / civil registry lookups where
  available per country adapter (`17`).
- **Data Classification:** PHI — highest sensitivity.
- **Audit Requirements:** Every read of a Patient 360 record is audited
  with actor, purpose-of-use, and accessed sections.
- **Failure Modes:** Duplicate-identity creation is treated as a data-quality
  incident, not a shrug — merge workflow must preserve full history of both
  records, never silently drop one.
- **Tests:** DENY read access without an active care relationship or
  documented purpose-of-use; ALLOW patient self-read of own record.
- **Compliance Requirements:** Consent state gates data sharing with every
  downstream domain and external integration.
- **Definition of Done:** No domain (Pharmacy, Lab, Radiology, Hospital,
  Billing) maintains an independent patient identity table.

## CLINICAL
- **Purpose:** Own the clinical record — encounters, notes, diagnoses,
  orders, medications, procedures — as an auditable, versioned, legally
  defensible record.
- **Responsibilities:** Encounter lifecycle, SOAP/structured notes, problem
  list, allergy list, orders, amendments (never silent overwrites).
- **Entities:** Encounter, ClinicalNote, Diagnosis, Problem, Allergy, Order,
  Medication, Procedure, Amendment.
- **Commands:** StartEncounter, RecordNote, AddDiagnosis, PlaceOrder, Amend,
  CloseEncounter.
- **Queries:** GetEncounterTimeline, GetActiveProblems, GetActiveOrders.
- **Events:** EncounterStarted, NoteFinalized, OrderPlaced, RecordAmended,
  EncounterClosed.
- **APIs:** Internal Clinical Service API; FHIR-mapped read API via
  Interoperability Layer for external consumers.
- **Permissions:** Attending/treating clinician for write within active
  encounter; read scoped to documented care relationship; amendments
  require reason + original-preserving versioning.
- **Dependencies:** Platform, Identity, Organization, Patient, Specialties.
- **External Integrations:** None directly — Pharmacy/Lab/Radiology
  integrate via Order/Result events, not direct table access.
- **Data Classification:** PHI — highest sensitivity, clinical-legal record.
- **Audit Requirements:** Full read/write audit trail; amendments must
  retain the original alongside the correction.
- **Failure Modes:** No silent mutation of a finalized note; a finalized
  record can only be amended, never deleted.
- **Tests:** DENY finalized-note edit without amendment workflow; ALLOW
  amendment with reason captured; DENY cross-encounter order leakage.
- **Compliance Requirements:** Clinical Safety hazards in `16` (wrong
  patient/medication/dose) are primarily mitigated in this domain.
- **Definition of Done:** Every clinical write is traceable to an actor, a
  timestamp, and — for amendments — a reason and the prior version.

## PHARMACY
- **Purpose:** Own the full medication lifecycle from catalog to dispensing.
- **Responsibilities:** Drug master data, interaction/allergy/dose checking,
  prescription and refill handling, dispensing, inventory with expiry/FEFO,
  controlled-substance workflows.
- **Entities:** Drug, Prescription, DispenseRecord, InventoryBatch, Supplier,
  PurchaseOrder.
- **Commands:** PrescribeMedication, CheckInteractions, Dispense, ReceiveStock, Recall.
- **Queries:** GetActivePrescriptions, GetStockLevel, GetExpiringBatches.
- **Events:** PrescriptionCreated, InteractionFlagged, MedicationDispensed,
  StockBelowThreshold, DrugRecalled.
- **APIs:** Internal Pharmacy Service API; consumes Clinical Order events.
- **Permissions:** Prescribing clinician for orders; pharmacist for
  dispense/substitution decisions; pharmacy tech for stock operations only.
- **Dependencies:** Platform, Identity, Organization, Patient, Clinical.
- **External Integrations:** Drug terminology source (`19` Terminology
  domain) — ARGON does not author its own authoritative drug database.
- **Data Classification:** PHI (prescription is patient-linked) + regulated
  controlled-substance data with stricter audit.
- **Audit Requirements:** Every dispense event audited with pharmacist
  identity, batch/lot, and patient link; controlled substances get an
  additional immutable ledger entry.
- **Failure Modes:** Interaction/allergy check failure must block dispense
  by default, never dispense-then-warn; expired-batch dispensing must be
  structurally blocked, not just flagged.
- **Tests:** DENY dispense against a known allergy without documented
  override + reason; ALLOW dispense after cleared interaction check.
- **Compliance Requirements:** Controlled-substance chain-of-custody
  per applicable national regulation (country adapter, `17`).
- **Definition of Done:** No prescription can reach Dispensed state without
  a passed interaction/allergy check recorded against it.

## LABORATORY
- **Purpose:** Own the full lab order-to-result lifecycle (LIS).
- **Responsibilities:** Test catalog/panels, specimen collection and
  accessioning, analyzer result ingestion, QC, critical-result escalation.
- **Entities:** LabOrder, Specimen, Accession, Result, ReferenceRange,
  QCRecord.
- **Commands:** PlaceLabOrder, CollectSpecimen, Accession, RecordResult,
  ValidateResult, FlagCritical.
- **Queries:** GetPendingOrders, GetResultHistory, GetPendingCriticalAcks.
- **Events:** LabOrderPlaced, SpecimenCollected, ResultRecorded,
  CriticalResultFlagged, ResultAmended.
- **APIs:** Internal LIS Service API; HL7 v2 (ORU/ORM) adapter to
  analyzers via Interoperability Layer.
- **Permissions:** Ordering clinician for orders; lab tech for
  collection/accessioning; pathologist/lab director for result validation
  and amendment.
- **Dependencies:** Platform, Identity, Organization, Patient, Clinical.
- **External Integrations:** Analyzer interfaces (HL7 v2 / ASTM where
  justified) via Interoperability Layer only — never direct analyzer-to-
  database connections.
- **Data Classification:** PHI, with a subset (genetic, reproductive,
  infectious-disease results) carrying elevated sensitivity handling.
- **Audit Requirements:** Every result view/amendment audited; delta checks
  and critical flags logged with acknowledgement timestamp.
- **Failure Modes:** A critical result with no acknowledgement within a
  defined window must escalate, not silently expire; specimen mislabeling
  must be structurally prevented via barcode-linked accessioning, not
  manual re-entry.
- **Tests:** DENY result release without QC pass where QC is required;
  ALLOW critical-result escalation to fire even if the ordering clinician
  is offline.
- **Compliance Requirements:** Westgard/QC rule evidence retained for
  accreditation review (status DESIGNED until evidenced — see `08`).
- **Definition of Done:** Every result traces specimen → accession → order
  → patient with no manual re-linking step.

## RADIOLOGY
- **Purpose:** Own the imaging order-to-report lifecycle (RIS) and DICOM
  interchange boundary.
- **Responsibilities:** Imaging orders, modality worklist, study/series/
  instance tracking, reading worklist, preliminary/final report, critical
  findings acknowledgement.
- **Entities:** ImagingOrder, Study, Series, Instance, Report, Addendum.
- **Commands:** PlaceImagingOrder, ScheduleStudy, AcquireImages,
  FinalizeReport, FlagCriticalFinding.
- **Queries:** GetReadingWorklist, GetStudyStatus, GetReportHistory.
- **Events:** ImagingOrderPlaced, StudyAcquired, ReportFinalized,
  CriticalFindingFlagged, AddendumIssued.
- **APIs:** Internal RIS Service API; DICOM/DICOMweb + FHIR
  ImagingStudy/DiagnosticReport via Interoperability Layer.
- **Permissions:** Ordering clinician for orders; technologist for
  acquisition; radiologist for report finalization and addenda.
- **Dependencies:** Platform, Identity, Organization, Patient, Clinical.
- **External Integrations:** PACS via DICOM/DICOMweb — image binaries never
  transit or land in PostgreSQL (see `01`, `23`).
- **Data Classification:** PHI; imaging binaries classified separately from
  the structured report for storage-tier purposes.
- **Audit Requirements:** Every study access and report finalization
  audited; critical findings require documented acknowledgement.
- **Failure Modes:** PACS unreachable must not silently mark a study
  "complete" — order stays open until acquisition is confirmed.
- **Tests:** DENY report finalization without a linked completed study;
  ALLOW addendum after finalization without altering the original report.
- **Compliance Requirements:** DICOM conformance statement required before
  claiming PACS interoperability (status: TARGET, not evidenced).
- **Definition of Done:** No radiology report exists without a traceable
  Study/Series/Instance chain.

## HOSPITAL
- **Purpose:** Own inpatient operations — admission through discharge —
  across ADT, beds, ICU, OR, and nursing.
- **Responsibilities:** Bed management with race-condition-safe allocation,
  ADT transitions, nursing medication administration, transfer/discharge
  planning.
- **Entities:** Admission, Bed, Ward, Transfer, Discharge, MAR (Medication
  Administration Record).
- **Commands:** Admit, AllocateBed, Transfer, AdministerMedication, Discharge.
- **Queries:** GetBedOccupancy, GetActiveAdmissions, GetPendingDischarges.
- **Events:** PatientAdmitted, BedAllocated, PatientTransferred,
  MedicationAdministered, PatientDischarged.
- **APIs:** Internal Hospital Ops Service API; HL7 v2 ADT via
  Interoperability Layer for external systems.
- **Permissions:** Admitting clinician/nurse for admission; charge nurse
  for bed allocation; administering nurse for MAR entries with
  wrong-patient-prevention checks (barcode/positive ID).
- **Dependencies:** Platform, Identity, Organization, Patient, Clinical,
  Pharmacy (for MAR).
- **External Integrations:** None mandatory; ADT feed optional per `06`.
- **Data Classification:** PHI, inpatient-specific.
- **Audit Requirements:** Every bed allocation and medication
  administration event audited with actor and patient-identity
  verification method used.
- **Failure Modes:** Concurrent bed-allocation requests must resolve via a
  single authoritative lock, never a race that double-books a bed; MAR
  entry must hard-block on patient-ID mismatch, not just warn.
- **Tests:** DENY double-allocation of the same bed under concurrent
  requests; DENY MAR entry without positive patient identification.
- **Compliance Requirements:** Wrong-patient and wrong-medication hazards
  from `16-MASTER-CLINICAL-SAFETY-MODEL.md` are primarily mitigated here.
- **Definition of Done:** Bed state and MAR entries are provably race-safe
  under load testing (see `15-MASTER-TESTING-STRATEGY.md`).

## BILLING
- **Purpose:** Own charge capture through invoicing and payment
  reconciliation as an immutable financial ledger.
- **Responsibilities:** Price lists/contracts, charge capture from clinical
  events, invoicing, payments, refunds, statements, aging.
- **Entities:** ChargeItem, Invoice, Payment, CreditNote, PatientAccount.
- **Commands:** CaptureCharge, GenerateInvoice, RecordPayment, IssueCreditNote.
- **Queries:** GetPatientBalance, GetInvoiceHistory, GetAgingReport.
- **Events:** ChargeCaptured, InvoiceIssued, PaymentReceived,
  CreditNoteIssued, AccountReconciled.
- **APIs:** Internal Billing Service API; e-invoicing government adapter
  via Interoperability Layer (`17`).
- **Permissions:** Billing staff for charge/invoice operations; finance
  role for credit notes and corrections; no direct edit of a posted
  financial record.
- **Dependencies:** Platform, Identity, Organization, Patient, Clinical
  (charge triggers), Insurance.
- **External Integrations:** Government e-invoicing (country adapter),
  payment gateways.
- **Data Classification:** Financial PII, regulated by tax/e-invoicing law
  per country.
- **Audit Requirements:** Every posted financial record change is via a
  reversing/correcting entry, never an in-place edit; full audit trail
  required for tax authority review.
- **Failure Modes:** Financial values must use exact/decimal
  representation — floating point is a defect, not a style choice (see
  `01`, `14`).
- **Tests:** DENY in-place edit of a posted invoice; ALLOW correction only
  via credit note + new charge; DENY monetary rounding drift under
  repeated operations.
- **Compliance Requirements:** Country-specific e-invoicing format
  validation (`17-MASTER...` government section).
- **Definition of Done:** Every posted charge is traceable to the clinical
  or operational event that generated it.

## INSURANCE
- **Purpose:** Own payer relationships without hardcoding any insurer into
  Clinical or Billing.
- **Responsibilities:** Eligibility/coverage/benefits checks,
  authorization, claim submission and lifecycle, remittance
  reconciliation.
- **Entities:** Payer, Coverage, Authorization, Claim, Remittance.
- **Commands:** CheckEligibility, RequestAuthorization, SubmitClaim,
  ReconcileRemittance, FileAppeal.
- **Queries:** GetCoverageStatus, GetClaimStatus, GetDenialReasons.
- **Events:** EligibilityChecked, AuthorizationGranted/Denied,
  ClaimSubmitted, ClaimAdjudicated, RemittancePosted.
- **APIs:** Internal Insurance Service API; Payer Adapter Framework
  (per-payer plugins) via Interoperability Layer.
- **Permissions:** Registration/billing staff for eligibility checks;
  billing staff for claim submission; finance for remittance
  reconciliation.
- **Dependencies:** Platform, Identity, Organization, Patient, Billing.
- **External Integrations:** Individual payer gateways behind the Payer
  Adapter Framework — no payer-specific logic in Clinical Core.
- **Data Classification:** PHI + financial data (coverage details linked
  to patient).
- **Audit Requirements:** Every eligibility/authorization/claim action
  audited with payer response captured verbatim for dispute resolution.
- **Failure Modes:** Payer gateway outage must queue submissions for
  retry, never silently drop a claim.
- **Tests:** DENY claim submission without a prior eligibility check on
  file; ALLOW resubmission after denial with amended data.
- **Compliance Requirements:** Payer-specific data handling per contract;
  see `17` for national payer/government scheme adapters.
- **Definition of Done:** Adding a new payer requires only a new adapter
  plugin, zero changes to Clinical Core or Billing Core.

## CONTROL PLANE
- **Purpose:** Own the platform-management surface described in `09-MASTER-CONTROL-PLANE.md`,
  distinct from every clinical/operational domain above.
- **Responsibilities:** Organization lifecycle orchestration, licensing,
  release management, global security/compliance operations, incident
  management.
- **Entities:** ProvisioningJob, LicenseGrant, ReleaseWave, Incident,
  ComplianceEvidence.
- **Commands:** ProvisionOrganization, GrantLicense, StartReleaseWave,
  PauseRelease, RollbackRelease, DeclareIncident.
- **Queries:** GetProvisioningStatus, GetActiveIncidents, GetReleaseHealth.
- **Events:** ProvisioningStepCompleted, ReleaseWaveStarted,
  ReleaseRolledBack, IncidentDeclared, IncidentResolved.
- **APIs:** Control-Plane-operator-only API surface — structurally
  separate from every Application-Plane API (see `27`).
- **Permissions:** Platform operator role, distinct from any clinical
  role; high-risk operations require step-up MFA + documented reason
  (see `27`).
- **Dependencies:** Platform (this domain effectively owns Platform's
  write side).
- **External Integrations:** None directly.
- **Data Classification:** Platform-operational data — not PHI, but
  compromise here can affect every tenant, so treated as maximum-blast-
  radius regardless of classification.
- **Audit Requirements:** Every Control Plane action is audited at the
  highest fidelity in the platform — actor, reason, before/after, approver
  where applicable.
- **Failure Modes:** A stuck provisioning saga must be resumable or
  compensable — never left corrupting partial state (see `11`).
- **Tests:** DENY Control-Plane-operator access to any PHI field by
  default; ALLOW only via documented, audited, time-boxed break-glass.
- **Compliance Requirements:** This domain is the evidence source for
  most of `08-MASTER-COMPLIANCE-MAP.md`'s platform-level controls.
- **Definition of Done:** No Application-Plane domain can perform a
  Control-Plane action (suspend a tenant, change licensing) through any
  path other than this domain's audited command surface.

---

# TIER 2 — SUPPORTING DOMAINS
*(complete profile, compact depth — full expansion is triggered when a
domain moves toward implementation; see the staged-trigger principle in
`19-MASTER-ARCHITECTURAL-DECISIONS.md`)*

## MEMBERSHIP
Purpose: link a UserAccount to an Organization/Facility with a role.
Responsibilities: invite, assign role, deactivate membership. Entities:
Membership, RoleAssignment. Commands: Invite, AssignRole, Deactivate.
Queries: GetMembershipsForUser, GetMembersForFacility. Events:
MemberInvited, RoleAssigned, MemberDeactivated. APIs: internal only.
Permissions: Org Admin manages memberships within own org. Dependencies:
Identity, Organization. External Integrations: none. Data Classification:
internal/organizational. Audit: every role change audited. Failure Modes:
orphaned membership (user deleted, membership remains) must be prevented
via cascade rules. Tests: DENY role assignment above assigner's own
privilege level. Compliance: least-privilege default on invite. DoD: every
active session's role set is fully explained by current Membership records.

## AUTHORIZATION
Purpose: evaluate every access decision platform-wide (RBAC + ABAC +
purpose-of-use). Responsibilities: policy evaluation, break-glass handling.
Entities: Policy, Role, Permission, BreakGlassGrant. Commands:
DefinePolicy, GrantBreakGlass. Queries: Evaluate(actor, resource, action,
context). Events: AccessDenied, BreakGlassInvoked. APIs: internal
Authorization Service, called by every domain before every sensitive
operation. Permissions: policy authoring restricted to Control Plane
security operators. Dependencies: Identity, Membership, Platform. External
Integrations: none. Data Classification: internal. Audit: every DENY and
every break-glass invocation logged. Failure Modes: evaluator failure must
fail closed. Tests: exhaustive ALLOW/DENY matrix per role×resource×action.
Compliance: enforced at application + database RLS, never UI-only (`20`).
DoD: no domain implements its own ad-hoc permission check outside this
service.

## MPI
Purpose: Master Patient Index — deduplicate and resolve patient identity
across facilities. Responsibilities: probabilistic matching, merge/unmerge,
identifier cross-referencing. Entities: MPIRecord, IdentifierCrossRef,
MergeHistory. Commands: ResolveIdentity, Merge, Unmerge. Queries:
FindCandidateMatches. Events: PotentialDuplicateFlagged, RecordsMerged.
APIs: internal, called by Patient domain. Permissions: registration
supervisor for merge approval. Dependencies: Patient, Platform. External
Integrations: national ID registries where available. Data Classification:
PHI. Audit: every merge/unmerge fully logged with both source records
preserved. Failure Modes: false-positive merge is the primary hazard —
merge requires human confirmation above a match-confidence threshold.
Tests: DENY auto-merge above ambiguity threshold; ALLOW manual override
with reason. Compliance: identity-resolution errors treated as clinical
safety incidents (`16`). DoD: zero silent auto-merges in production.

## CONSENT
Purpose: track what a patient has agreed to share and with whom.
Responsibilities: consent capture, versioning, withdrawal, scope
enforcement. Entities: ConsentRecord, ConsentScope, WithdrawalRecord.
Commands: CaptureConsent, WithdrawConsent. Queries: GetActiveConsentScopes.
Events: ConsentGranted, ConsentWithdrawn. APIs: internal, checked by every
domain and by Interoperability Layer before any external share. Permissions:
patient (self), guardian (documented relationship). Dependencies: Patient,
Identity. External Integrations: none directly. Data Classification: PHI.
Audit: every consent check and every override logged. Failure Modes:
missing consent record must default to most restrictive sharing, not
permissive. Tests: DENY external share without matching active consent
scope. Compliance: core to `08` data-subject-rights controls. DoD: every
external data share can point to the consent record that authorized it.

## SPECIALTIES
Purpose: extend Clinical Core per medical specialty without forking it.
Responsibilities: specialty-specific templates, fields, and CDS rules
layered on Clinical Core entities. Entities: SpecialtyProfile,
SpecialtyTemplate. Commands: RegisterSpecialtyExtension. Queries:
GetSpecialtyTemplate. Events: SpecialtyExtensionRegistered. APIs: plugin
interface consumed by Clinical. Permissions: clinical configuration admin.
Dependencies: Clinical. External Integrations: none. Data Classification:
inherits Clinical (PHI). Audit: extension registration audited. Failure
Modes: a specialty extension must never bypass Clinical Core's
amendment/versioning rules. Tests: DENY specialty extension that writes
directly to core tables outside Clinical's command surface. Compliance:
inherits Clinical. DoD: a new specialty can be added without modifying
Clinical Core code.

## SCHEDULING
Purpose: manage appointment booking and provider calendars.
Responsibilities: slot management, booking, rescheduling, reminders
trigger. Entities: Appointment, ProviderCalendar, Slot. Commands: Book,
Reschedule, Cancel. Queries: GetAvailableSlots, GetProviderSchedule.
Events: AppointmentBooked, AppointmentCancelled, ReminderDue. APIs:
internal + patient-app-facing booking API. Permissions: reception staff,
patient self-service (own appointments only). Dependencies: Patient,
Organization. External Integrations: notification channel (SMS/WhatsApp/
email) via Communications domain. Data Classification: PHI-adjacent
(links patient to visit intent). Audit: booking changes logged. Failure
Modes: double-booking must be prevented via the same locking discipline as
Hospital bed allocation. Tests: DENY concurrent double-booking of one slot.
Compliance: n/a beyond general PHI handling. DoD: no slot can be held by
two confirmed appointments simultaneously.

## QUEUE
Purpose: manage real-time patient flow within a facility (check-in to
seen). Responsibilities: queue state, position, wait-time estimation.
Entities: QueueEntry, QueueState. Commands: CheckIn, CallNext, Skip.
Queries: GetQueueStatus. Events: PatientCheckedIn, PatientCalled,
PatientSkipped. APIs: internal + display-board feed. Permissions:
reception/nursing staff. Dependencies: Scheduling, Patient. External
Integrations: none. Data Classification: PHI-adjacent (presence data).
Audit: check-in/call events logged. Failure Modes: queue state must
recover cleanly from a mid-day service restart. Tests: ALLOW queue state
reconstruction from event log after restart. Compliance: n/a. DoD: queue
position is always derivable from the event log alone.

## EMERGENCY
Purpose: own ED-specific workflow (triage through disposition).
Responsibilities: triage acuity, rapid vitals capture, disposition
decision. Entities: EDVisit, TriageRecord, Disposition. Commands:
Triage, RecordVitals, Disposition. Queries: GetEDBoard. Events:
PatientTriaged, DispositionRecorded. APIs: internal, feeds Hospital Ops on
admission disposition. Permissions: ED nursing/physician staff.
Dependencies: Clinical, Hospital, Patient. External Integrations: none.
Data Classification: PHI. Audit: triage and disposition decisions logged
with acuity score. Failure Modes: unacknowledged high-acuity triage must
escalate automatically. Tests: DENY silent timeout on high-acuity
unacknowledged case. Compliance: clinical safety hazard domain (`16`).
DoD: every ED visit has a traceable triage→disposition chain.

## ICU
Purpose: own critical-care-specific monitoring and orders context.
Responsibilities: acuity tracking, continuous-order context, ICU bed
state. Entities: ICUStay, AcuityScore. Commands: AdmitToICU,
UpdateAcuity, TransferOut. Queries: GetICUCensus. Events: ICUAdmitted,
AcuityUpdated, ICUTransferredOut. APIs: internal, extends Hospital Ops.
Permissions: ICU clinical staff. Dependencies: Hospital, Clinical.
External Integrations: bedside monitor integration is TARGET/PROPOSED,
not designed in this pass. Data Classification: PHI, high acuity. Audit:
acuity changes logged. Failure Modes: ICU bed state must share the same
race-safe allocation lock as general Hospital beds. Tests: same
concurrency tests as Hospital, ICU-scoped. Compliance: inherits Hospital.
DoD: ICU bed state is never tracked separately from the general Bed
entity's state machine.

## OPERATING ROOM
Purpose: own surgical scheduling and intra-op record. Responsibilities: OR
booking, case scheduling, intra-op documentation, post-op handoff.
Entities: ORCase, SurgicalSchedule, IntraOpRecord. Commands: ScheduleCase,
StartCase, CompleteCase. Queries: GetORSchedule. Events: CaseScheduled,
CaseStarted, CaseCompleted. APIs: internal, extends Hospital Ops.
Permissions: surgical scheduling staff, surgical team. Dependencies:
Hospital, Clinical, Patient. External Integrations: none. Data
Classification: PHI. Audit: case timeline fully logged (time-in, time-out,
team). Failure Modes: wrong-site/wrong-procedure hazard — case must
require a documented site/procedure verification step before start. Tests:
DENY case start without verification checklist complete. Compliance:
clinical safety hazard domain (`16`). DoD: every completed case has a full
verification-checklist record attached.

## NURSING
Purpose: own nursing assessment and care-plan execution.
Responsibilities: nursing assessments, care plan tasks, MAR execution
(shared with Pharmacy/Hospital). Entities: NursingAssessment, CarePlanTask.
Commands: RecordAssessment, CompleteCareTask. Queries: GetCarePlan.
Events: AssessmentRecorded, CareTaskCompleted. APIs: internal. Permissions:
nursing staff. Dependencies: Clinical, Hospital, Pharmacy. External
Integrations: none. Data Classification: PHI. Audit: assessments and task
completions logged. Failure Modes: overdue care tasks must surface, not
silently lapse. Tests: ALLOW overdue-task alerting under load. Compliance:
n/a beyond general PHI. DoD: every care plan task has a closed-loop
completion or escalation record.

## INVENTORY
Purpose: track stock across Pharmacy and general facility supplies.
Responsibilities: stock levels, batch/lot/expiry, reorder thresholds.
Entities: InventoryItem, StockLevel, Batch. Commands: ReceiveStock,
AdjustStock, IssueStock. Queries: GetStockLevel, GetExpiringSoon. Events:
StockReceived, StockAdjusted, ThresholdBreached. APIs: internal, shared
substrate for Pharmacy's InventoryBatch. Permissions: inventory/pharmacy
staff. Dependencies: Platform, Organization. External Integrations:
supplier systems (optional, future). Data Classification: operational,
not PHI. Audit: every adjustment logged with reason. Failure Modes: stock
count drift must be reconcilable via an audit trail, not just a running
total. Tests: DENY negative stock without an explicit backorder state.
Compliance: n/a. DoD: stock level is always reconstructable from the
event log.

## PROCUREMENT
Purpose: manage purchasing from suppliers. Responsibilities: purchase
orders, receiving, returns. Entities: PurchaseOrder, Supplier,
ReceivingRecord. Commands: CreatePO, ReceiveGoods, ReturnGoods. Queries:
GetOpenPOs. Events: POCreated, GoodsReceived, GoodsReturned. APIs:
internal. Permissions: procurement staff. Dependencies: Inventory,
Organization. External Integrations: supplier portals (future). Data
Classification: operational/financial. Audit: PO lifecycle logged. Failure
Modes: receiving quantity mismatch must block auto-close of a PO. Tests:
DENY PO auto-close on quantity mismatch. Compliance: n/a beyond financial
controls. DoD: every received item traces to an open PO line.

## PAYMENTS
Purpose: process patient and payer payments. Responsibilities: payment
capture, refunds, gateway integration. Entities: PaymentTransaction,
RefundTransaction. Commands: CapturePayment, IssueRefund. Queries:
GetPaymentHistory. Events: PaymentCaptured, RefundIssued,
PaymentFailed. APIs: internal + payment gateway adapter. Permissions:
billing staff, patient (self-service payment). Dependencies: Billing.
External Integrations: payment gateway providers. Data Classification:
financial PII — card data never stored directly, tokenized via gateway.
Audit: every transaction logged, reconciled daily against gateway
statements. Failure Modes: gateway timeout must not double-charge — use
idempotency keys. Tests: DENY duplicate charge on retried request with
same idempotency key. Compliance: PCI DSS scope minimization via
tokenization. DoD: zero raw card data touches ARGON's own data plane.

## CLAIMS
Purpose: own the claim submission-to-adjudication sub-lifecycle within
Insurance. Responsibilities: claim assembly, coding attachment,
submission, status tracking. Entities: Claim, ClaimLine, DenialReason.
Commands: AssembleClaim, SubmitClaim, TrackStatus. Queries: GetClaimStatus,
GetDenialsByReason. Events: ClaimAssembled, ClaimSubmitted, ClaimDenied,
ClaimPaid. APIs: internal, part of Insurance's API surface. Permissions:
billing/coding staff. Dependencies: Insurance, Billing, Clinical (coding
source). External Integrations: payer adapters. Data Classification: PHI +
financial. Audit: full claim lifecycle logged. Failure Modes: coding
mismatch between clinical record and claim must block submission, not
just warn. Tests: DENY submission with unresolved coding discrepancy.
Compliance: coding accuracy required by payer contracts. DoD: every claim
line traces to a specific clinical charge item.

## REVENUE CYCLE
Purpose: model the end-to-end financial workflow, registration through
patient responsibility. Responsibilities: orchestrate the sequence across
Insurance, Billing, Claims (this domain owns the sequence, not the
sub-domains' internals). Entities: RevenueCycleCase (an orchestration
record, not a data owner). Commands: AdvanceRevenueCycleStage. Queries:
GetCaseStage. Events: StageAdvanced, StageFailed. APIs: internal
orchestrator. Permissions: revenue-cycle/billing supervisors. Dependencies:
Insurance, Billing, Claims, Scheduling. External Integrations: inherited
from sub-domains. Data Classification: inherits sub-domains. Audit: stage
transitions logged. Failure Modes: a stalled case must surface on an aging
report, not disappear. Tests: ALLOW stage-failure visibility on the
revenue-cycle dashboard. Compliance: n/a beyond sub-domains. DoD: every
case's current stage is queryable without joining every sub-domain
manually.

## DOCUMENTS
Purpose: own file/document storage and retrieval across the platform.
Responsibilities: upload, versioning, access-controlled retrieval, e-
signature where applicable. Entities: Document, DocumentVersion,
SignatureRecord. Commands: Upload, Sign, Retrieve. Queries: GetDocument,
ListVersions. Events: DocumentUploaded, DocumentSigned. APIs: internal,
consumed by every domain needing attachments. Permissions: scoped to the
owning record's access rules (inherits from Patient/Clinical/Billing
context). Dependencies: Object Storage (Data Plane), Consent. External
Integrations: e-signature provider (optional). Data Classification: varies
by content — PHI if clinical, financial if billing-linked. Audit: every
retrieval logged. Failure Modes: orphaned document (owning record
deleted) must be handled by retention policy, not silent deletion.
Tests: DENY retrieval outside the owning record's access scope.
Compliance: retention periods per `08`. DoD: every document has exactly
one owning domain record.

## NOTIFICATIONS
Purpose: deliver outbound alerts (SMS/WhatsApp/email/push).
Responsibilities: template management, delivery, opt-in/consent
enforcement, delivery-status tracking. Entities: NotificationTemplate,
NotificationJob, DeliveryStatus. Commands: SendNotification,
UpdatePreferences. Queries: GetDeliveryStatus. Events:
NotificationQueued, NotificationDelivered, NotificationFailed. APIs:
internal, consumed by Scheduling/Pharmacy/Lab/Billing for reminders and
alerts. Permissions: system-triggered; patient controls own opt-in.
Dependencies: Consent, Patient. External Integrations: SMS/WhatsApp/email
gateways. Data Classification: PHI-adjacent (message content may
reference care). Audit: delivery attempts logged. Failure Modes: consent
withdrawal must stop future sends immediately, not at next batch cycle.
Tests: DENY send after opt-out event, even if queued before it. Compliance:
opt-in required per `08`. DoD: every send checks current consent state at
send-time, not queue-time.

## COMMUNICATIONS
Purpose: own two-way patient/staff messaging beyond one-way notifications.
Responsibilities: secure messaging threads, staff-to-staff clinical
communication. Entities: MessageThread, Message. Commands: SendMessage,
CloseThread. Queries: GetThread. Events: MessageSent, ThreadClosed. APIs:
internal + patient-app messaging API. Permissions: scoped to thread
participants only. Dependencies: Identity, Patient, Consent. External
Integrations: none. Data Classification: PHI if clinical content is
discussed. Audit: message access logged. Failure Modes: thread visibility
must not leak across unrelated care teams. Tests: DENY read access to a
thread by a non-participant. Compliance: same as Documents/Clinical. DoD:
every thread's participant list is the sole source of access truth.

## INTEROPERABILITY
Purpose: own the technical boundary layer described in `01`/`02` — FHIR,
HL7, DICOM, IHE — as the single external-facing contract point.
Responsibilities: protocol translation, validation, versioning of external
contracts. Entities: FHIRResourceMapping, HL7MessageSpec, IHETransaction.
Commands: TranslateInbound, TranslateOutbound, ValidateAgainstProfile.
Queries: GetSupportedProfiles. Events: InboundMessageReceived,
OutboundMessageSent, ValidationFailed. APIs: FHIR REST API, HL7 v2
listener, DICOMweb endpoint. Permissions: system-level, not user-facing.
Dependencies: every Application-Plane domain it fronts. External
Integrations: this domain is entirely external integrations by
definition. Data Classification: PHI in transit — encryption and
minimum-necessary-field rules apply. Audit: every external message
logged with correlation ID. Failure Modes: malformed inbound message must
be quarantined, never partially applied to internal state. Tests: DENY
partial-apply of a message that fails mid-validation. Compliance: FHIR/
HL7/DICOM conformance is TARGET, not evidenced (`08`). DoD: no
Application-Plane domain has its own bespoke external protocol handling.

## TERMINOLOGY
Purpose: own coding systems (SNOMED CT, ICD, LOINC, UCUM, ATC, local codes)
as a shared service. Responsibilities: CodeSystem/ValueSet/ConceptMap
management, validation, translation, versioning. Entities: CodeSystem,
ValueSet, ConceptMap. Commands: ImportCodeSystem, PublishValueSet.
Queries: ValidateCode, TranslateCode. Events: CodeSystemVersionPublished.
APIs: internal terminology service, consumed platform-wide. Permissions:
terminology admin for imports. Dependencies: none (foundational service).
External Integrations: licensed terminology providers — ARGON does not
redistribute proprietary datasets without valid rights (see `19`
Terminology in original prompt, section 19). Data Classification: 
reference data, not PHI. Audit: import/publish events logged. Failure
Modes: an unversioned code change must never silently alter historical
record interpretation. Tests: DENY use of an unpublished/draft code
version in a finalized clinical record. Compliance: licensing terms per
provider (REQUIRES LEGAL VERIFICATION). DoD: every clinical code
reference is pinned to a specific CodeSystem version.

## GOVERNMENT INTEGRATIONS
Purpose: isolate every country-specific regulatory/government integration
behind a Country Adapter so Global Core never contains country-specific
logic. Responsibilities: per-country e-invoicing, national health system
submission, local payer/government scheme integration. Entities:
CountryAdapter, GovernmentSubmission. Commands: SubmitToGovernmentSystem.
Queries: GetSubmissionStatus. Events: SubmissionAccepted,
SubmissionRejected. APIs: per-country adapter plugin interface via
Interoperability Layer. Permissions: system-level, country-scoped.
Dependencies: Interoperability, Billing (for e-invoicing), Organization
(country attribute). External Integrations: government APIs — by
definition. Data Classification: varies; often includes PHI + financial.
Audit: every submission logged with government response. Failure Modes:
a rejected submission must surface for manual remediation, never retry
silently forever. Tests: DENY deployment of a country adapter without a
documented regulatory requirement mapping. Compliance: REQUIRES LEGAL
VERIFICATION per country before any claim of compliance. DoD: adding a
country requires only a new adapter, zero changes to Global Core domains.

## COMPLIANCE
Purpose: own the compliance-requirement tracking system described fully
in `08-MASTER-COMPLIANCE-MAP.md`. Responsibilities: requirement→control→
evidence tracking, status lifecycle (UNKNOWN through
APPROVED/EXPIRED/NON-COMPLIANT). Entities: ComplianceRequirement, Control,
Evidence. Commands: RecordEvidence, UpdateStatus. Queries: GetComplianceStatus.
Events: StatusChanged, EvidenceExpired. APIs: internal. Permissions:
compliance officer role. Dependencies: Audit, Control Plane. External
Integrations: none. Data Classification: internal/governance. Audit: every
status change logged with evidence reference. Failure Modes: status must
never jump directly from IMPLEMENTED to APPROVED without a TESTED/
EVIDENCED step (see `33` rule in the original prompt). Tests: DENY status
transition that skips a required intermediate state. Compliance: this
domain IS the compliance system — see `08` for full detail. DoD: no
compliance claim exists in any other document without a corresponding
record here.

## AUDIT
Purpose: own the platform-wide, tamper-evident audit log every other
domain writes to. Responsibilities: append-only event capture, retention,
tamper-evidence. Entities: AuditEvent. Commands: RecordAuditEvent
(internal-only, called by every domain). Queries: SearchAuditLog. Events:
n/a (Audit is itself the event sink). APIs: internal write API for all
domains; read API restricted to compliance/security roles. Permissions:
write from any domain; read restricted and itself audited (meta-audit).
Dependencies: none (foundational, alongside Platform). External
Integrations: none. Data Classification: contains fragments of whatever
it's logging — treated at the sensitivity of its most sensitive entries.
Audit Requirements: this domain's own access is meta-audited. Failure
Modes: audit-write failure must block the originating operation in
high-risk domains (Clinical, Billing, Control Plane), not fail silently.
Tests: DENY a high-risk write from completing if its audit record fails
to persist. Compliance: retention periods per `08`. DoD: every write
command in every other domain's profile above has a corresponding
AuditEvent type.

## ANALYTICS
Purpose: own read-optimized reporting fed by events, never a second
source of truth. Responsibilities: operational/clinical/financial
dashboards, KPI computation. Entities: AnalyticsView (materialized,
derived only). Commands: none (read-only domain, populated by event
consumers). Queries: GetDashboard, GetKPI. Events: consumes events from
every other domain; emits none. APIs: internal dashboard API. Permissions:
role-scoped per dashboard (clinical dashboards ≠ financial dashboards ≠
operational dashboards). Dependencies: every domain, via events only —
never direct database reads of OLTP tables. Data Classification: derived
— inherits sensitivity of source domains. Audit: dashboard access logged
for PHI-containing views. Failure Modes: analytics lag must be visible
(a staleness indicator), never presented as real-time when it isn't.
Tests: DENY analytics write path to any OLTP table. Compliance: same as
source domains. DoD: every analytics view can be regenerated from the
event log alone.

## AI
Purpose: own AI/ML-assisted features (CDS, forecasting) as advisory,
never autonomous-clinical-decision, without explicit design review.
Responsibilities: model serving, CDS Hooks integration, safety guardrails.
Entities: ModelVersion, Recommendation, GuardrailPolicy. Commands:
RequestRecommendation. Queries: GetModelVersion. Events:
RecommendationIssued, GuardrailTriggered. APIs: CDS Hooks-compliant
internal API. Permissions: clinician-facing only, always presented as
advisory with source/confidence. Dependencies: Clinical, Terminology,
Analytics. External Integrations: model providers (future, unspecified).
Data Classification: PHI when model input includes patient data. Audit:
every recommendation issued is logged with model version and input
summary. Failure Modes: a recommendation must never auto-apply to the
clinical record — clinician action is always required. Tests: DENY any
code path where an AI recommendation writes directly to Clinical without
clinician confirmation. Compliance: IEC 62304/ISO 14971 applicability is
UNKNOWN — REQUIRES EVIDENCE based on final feature classification (`21`).
DoD: every AI-influenced clinical action has a human-confirmation step in
its event trail.

## OBSERVABILITY
Purpose: own platform telemetry (metrics/logs/traces) per `28`.
Responsibilities: instrumentation standards, PHI-scrubbing before
telemetry export, alerting thresholds. Entities: MetricDefinition,
TraceSpan, AlertRule. Commands: DefineAlertRule. Queries: GetServiceHealth.
Events: AlertFired, AlertResolved. APIs: OpenTelemetry-compatible
internal API. Permissions: SRE/platform-ops role for alert configuration.
Dependencies: every domain emits telemetry through this one path.
External Integrations: none mandatory. Data Classification: must be
PHI-free by construction — this domain's core responsibility is ensuring
that. Audit: alert-rule changes logged. Failure Modes: a domain emitting
raw PHI into a log line is treated as a security incident, not a bug
ticket. Tests: DENY any telemetry payload containing a recognized PHI
field pattern (automated scrubbing test). Compliance: this domain is a
control for `21`/`28`. DoD: zero PHI findings in a telemetry-content
audit sample.

## DISASTER RECOVERY
Purpose: own backup, restore-testing, and failover per `17-MASTER-DISASTER-RECOVERY.md`.
Responsibilities: backup scheduling, restore drills, RTO/RPO tracking per
stateful component. Entities: BackupJob, RestoreDrillResult,
RecoveryRunbook. Commands: TriggerBackup, RunRestoreDrill. Queries:
GetLastSuccessfulRestore. Events: BackupCompleted, RestoreDrillPassed/Failed.
APIs: internal, Control-Plane-operated. Permissions: platform-ops/SRE
role. Dependencies: Data Plane (all stateful components), Control Plane.
External Integrations: none. Data Classification: backups inherit the
classification of what they contain (often PHI) — encrypted at rest,
access-audited. Audit: every backup and restore action logged. Failure
Modes: "backup exists" is not equivalent to "backup is restorable" — this
domain's core mandate. Tests: DENY marking DR-ready without a passed
restore drill within the defined interval. Compliance: RTO/RPO targets
per component defined in `17`. DoD: every stateful component listed in
`02` Data Plane has a documented, tested restore procedure with a
non-expired drill result.

---

## Alternatives Considered
A shallower "one paragraph per domain, no fixed fields" format was
rejected — it would fail the field-completeness requirement in the
originating prompt (section 6) and make cross-domain audits (does every
domain have an audit story? a failure-mode story?) impossible to check
mechanically.

## Security Impact
This map is the primary input to `07-MASTER-SECURITY-MAP.md`'s per-domain
permission model.

## Operational Impact
Domain boundaries here should map 1:1 to eventual code module boundaries
(see `38` repository architecture in the originating prompt, formalized in
future `13-MASTER-INFRASTRUCTURE-ARCHITECTURE.md`).

## Performance Impact
N/A — inventory/design document.

## Compliance Impact
Every domain's "Compliance Requirements" field is a pointer, not a
compliance claim — actual status lives only in `08-MASTER-COMPLIANCE-MAP.md`.

## Failure Modes
A domain whose "Failure Modes" field is empty is a defect in this
document — none should be empty above; if a future edit adds a domain
without this field populated, treat it as blocking.

## Dependencies
Depends on `01`, `02`. Feeds `05` (workflows reference these commands/
events), `07` (security map assigns permissions per domain), `15`
(testing strategy references the ALLOW/DENY test hints above).

## Unknowns
UNKNOWN — REQUIRES EVIDENCE whether any of these 39 domains has a partial
real-world implementation already.

## Validation
Cross-check against `02-MASTER-SYSTEM-MAP.md`: every domain listed there
must appear here, and vice versa. Confirmed consistent as of this
document's creation.

## Rollback
N/A at design stage.

## Definition of Done
All 39 domains have all 15 fields populated with real content (verified
above — Tier 1: 12 domains full depth; Tier 2: 27 domains compact-complete
depth). Full expansion of any Tier 2 domain into Tier 1 depth is triggered
on request or when that domain enters active implementation.
