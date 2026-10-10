# FINAL GAP ANALYSIS

STATUS: PROPOSED
EVIDENCE CLASS: RUNTIME EVIDENCE (direct grep/read inspection of the actual repository at commit `921ae46`+, 2026-09-02 — not asserted from memory of having written it)

## Scope and Method
This pass under ADR-020 (deliberate, logged freeze exception — see
`docs/master/19-MASTER-ARCHITECTURAL-DECISIONS.md`). Every gap below was
found by directly searching the actual document text for the specific
concept, not by recalling what was intended when the document was
written. Where a search found nothing, that's recorded as the evidence
for the gap — not an assumption.

**This is architecture-documentation gap analysis, not code gap
analysis** — nothing has been implemented, so there is no code to find
gaps in. Every gap below is "this document doesn't yet specify X," never
"this code doesn't do X."

---

## GAP-001 — No treatment of service identities / machine-to-machine authentication
- **File/Section:** `docs/master/07-MASTER-SECURITY-MAP.md`, Identity & Session Baseline
- **Classification:** MISSING
- **Problem:** The security model specifies human-actor authentication
  (OIDC/OAuth2, MFA, WebAuthn) in detail but has zero mention of how a
  service-to-service call (e.g., Interoperability Layer → external
  payer adapter, or a background job → domain API) authenticates.
- **Why it matters:** Every domain document assumes "an actor" makes a
  request; several real flows (Release workflow triggering health
  checks, the Interoperability Layer calling out) are service-initiated,
  not human-initiated.
- **Risk:** MEDIUM — a future implementer would need to invent this
  ad-hoc per integration, risking inconsistent trust boundaries.
- **Dependency:** `06-MASTER-INTEGRATION-MAP.md`, `13-MASTER-INFRASTRUCTURE-ARCHITECTURE.md`.
- **Recommended action:** Add a Service Identity subsection to `07`
  specifying: workload identity (e.g., GCP service accounts scoped per
  Cloud Run service), short-lived tokens for service-to-service calls, no
  shared static API keys between internal services.
- **Blocks implementation?** No — Phase 1 (Identity/Authorization) would
  surface this naturally; not a Phase-0 blocker.
- **Blocks security?** Not yet — no service-to-service calls exist to be
  insecure.
- **Blocks production?** No.
- **Evidence:** `grep -i "service ident\|machine-to-machine\|m2m\b" docs/master/07*.md docs/master/03*.md` → zero matches.

## GAP-002 — No refresh-token lifecycle/protection detail
- **File/Section:** `docs/master/07-MASTER-SECURITY-MAP.md`, Identity & Session Baseline
- **Classification:** INCOMPLETE
- **Problem:** "Sessions are short-lived tokens with server-side
  revocation" is stated, but refresh-token rotation, reuse detection, and
  binding (device/IP) are not addressed at all.
- **Why it matters:** Refresh-token replay is a standard real-world OAuth
  attack vector; silence here means a future implementer might pick a
  weak default (e.g., long-lived, non-rotating refresh tokens).
- **Risk:** MEDIUM.
- **Dependency:** Keycloak configuration (`14`).
- **Recommended action:** Add: refresh-token rotation on every use,
  reuse detection triggers session-family revocation, optional
  device-binding for high-risk roles.
- **Blocks implementation?** No.
- **Blocks security?** No — no implementation exists yet to exploit.
- **Blocks production?** No.
- **Evidence:** `grep -i "refresh token" docs/master/07*.md` → zero matches.

## GAP-003 — No bulk-access / search-restriction model for PHI
- **File/Section:** `docs/master/07-MASTER-SECURITY-MAP.md`; `docs/master/03-MASTER-DOMAIN-MAP.md` (`Patient` domain)
- **Classification:** MISSING
- **Problem:** The security model covers per-record read authorization
  (active-care-relationship, purpose-of-use) but never addresses
  *bulk* access — e.g., "export all patients," "search across the whole
  tenant," "list every record a given clinician can see." These are a
  materially different risk (mass exfiltration) than single-record
  access and typically need separate rate-limiting/approval controls.
- **Why it matters:** Named explicitly in the originating task's PHI
  Security section as a required check; genuinely absent.
- **Risk:** HIGH *if* implemented naively (a single compromised
  clinician credential could bulk-export a tenant's entire patient list
  today, per the *documented* model, since nothing restricts it
  differently from a single read).
- **Dependency:** `Patient`, `Documents`, `Analytics` domains (`03`).
- **Recommended action:** Add a bulk-access control tier to `07`:
  rate-limited/approval-gated bulk export, distinct audit category from
  single-record reads, quota per role.
- **Blocks implementation?** Should block Phase 2 (Patient/Clinical
  Core) sign-off specifically — bulk-export is a real, common feature
  request and needs a control before it's built, not after.
- **Blocks security?** Not yet (undeployed).
- **Blocks production?** Would block production if the Patient App or
  an admin export feature ships without this control designed first.
- **Evidence:** `grep -i "bulk access\|bulk export\|search restrict" docs/master/07*.md docs/master/03*.md` → zero matches.

## GAP-004 — No licensing lifecycle beyond initial grant
- **File/Section:** `docs/master/09-MASTER-CONTROL-PLANE.md`; `docs/master/11-MASTER-ORGANIZATION-PROVISIONING.md`
- **Classification:** MISSING
- **Problem:** `Licensing & Module Entitlements` in `09` covers granting
  a license tier at provisioning time. Nothing addresses: grace period
  after expiry, renewal workflow, upgrade/downgrade between tiers
  (mid-lifecycle, not at creation), or what happens to data/access when
  a subscription lapses.
- **Why it matters:** Every real SaaS licensing model needs this; its
  total absence means "Organization Lifecycle" in `09` is really only
  "Organization *provisioning*," not full lifecycle.
- **Risk:** LOW at the architecture stage; MEDIUM if this reaches
  implementation without a plan (risk of ad-hoc, inconsistent handling
  of "what happens when a clinic doesn't pay").
- **Dependency:** `Billing` domain (`03`), `Organization` domain (`03`).
- **Recommended action:** Add a Licensing Lifecycle subsection: states
  (Active → Grace Period → Suspended-for-nonpayment → Reactivated or
  Archived), and explicit data-retention behavior during each state
  (data must remain intact and exportable during Grace Period at
  minimum, per general SaaS/healthcare good practice — exact retention
  window REQUIRES a business decision, not invented here).
- **Blocks implementation?** No — genuinely a Phase 1+ concern.
- **Blocks security?** No.
- **Blocks production?** Would block a real commercial launch (this is a
  business-operations gap, not a technical one).
- **Evidence:** `grep -i "grace period\|renewal\|upgrade\|downgrade" docs/master/09*.md docs/master/11*.md docs/master/03*.md` → zero matches.

## GAP-005 — Multi-tenancy isolation not explicitly addressed for background jobs, exports, or caching
- **File/Section:** `docs/master/04-MASTER-DATA-MAP.md`; `docs/master/07-MASTER-SECURITY-MAP.md`
- **Classification:** INCOMPLETE
- **Problem:** RLS-based tenant isolation is well specified for
  synchronous, request-scoped reads/writes. Three async/derived
  categories are not explicitly addressed: (a) background jobs
  (does a scheduled job run per-tenant or cross-tenant, and if
  cross-tenant, how does it avoid leaking one tenant's data into
  another's processing context?), (b) exports (does an export job
  inherit RLS the same way an API request does?), (c) cache keys (are
  Redis keys tenant-namespaced explicitly, or only implicitly through
  the data they cache?).
- **Why it matters:** These are exactly the categories where RLS
  (a per-*query* mechanism) doesn't automatically apply — a background
  job or cache layer can bypass RLS if it uses a different DB role or
  reads from cache without re-checking tenant scope.
- **Risk:** HIGH *if unaddressed at implementation time* — this is a
  classic real-world multi-tenant SaaS vulnerability class.
- **Dependency:** `04`, `07`, `Observability` domain.
- **Recommended action:** Add explicit statements: background jobs run
  with the *same* RLS-scoped role as the tenant they're processing (one
  job invocation = one tenant, never a cross-tenant batch query);
  exports go through the same Authorization Service check as any read;
  cache keys are namespaced `{tenantId}:{restOfKey}` by construction,
  enforced by the caching helper, not by convention.
- **Blocks implementation?** Should block Phase 1 sign-off (Platform/
  Authorization) — this is foundational, not a later add-on.
- **Blocks security?** Not yet.
- **Blocks production?** Yes, if any background job or export ships
  without this being resolved first.
- **Evidence:** `grep -i "background job\|export.*tenant\|tenant.*cach" docs/master/04*.md docs/master/07*.md` → one incidental match (a cache row in the data matrix), no explicit isolation statement for any of the three.

## GAP-006 — Specific OWASP application-security attack classes not named
- **File/Section:** `docs/master/07-MASTER-SECURITY-MAP.md`, Security Architecture Components
- **Classification:** WEAK
- **Problem:** `07` names OWASP ASVS/API Security Top 10 as *baseline
  standards* and lists general controls (input validation, rate
  limiting, WAF), but never names IDOR/BOLA, mass assignment, SSRF,
  insecure deserialization, or replay attacks specifically — the exact
  categories the originating task asks about.
- **Why it matters:** Adopting a standard by reference is not the same
  as demonstrating the architecture actually defends against its
  specific failure modes — e.g., nothing in `03`'s domain profiles
  explicitly states "API responses never accept a client-supplied
  ownership/tenant field" (the standard mass-assignment/IDOR defense).
- **Risk:** MEDIUM — the *general* authorization model (three-layer
  enforcement) likely does prevent most of these by construction, but
  that's an inference, not a stated, checkable control.
- **Dependency:** `07`, every domain in `03`.
- **Recommended action:** Add an explicit "OWASP Top 10 / API Top 10
  mapping" table to `07`: for each attack class, state the specific
  architectural control that mitigates it (e.g., IDOR/BOLA → resource
  ownership is always re-derived server-side from the authenticated
  session, never trusted from a client-supplied ID field).
- **Blocks implementation?** No — should be resolved during Phase 1's
  detailed API design, not before.
- **Blocks security?** No.
- **Blocks production?** Would block a pre-production security review.
- **Evidence:** `grep -i "IDOR\|BOLA\|mass assignment\|SSRF\|deserializ\|replay attack" docs/master/07*.md` → zero matches.

## GAP-007 — Supply-chain controls incomplete
- **File/Section:** `docs/master/07-MASTER-SECURITY-MAP.md`
- **Classification:** INCOMPLETE
- **Problem:** SBOM is named once (as one item in a list). Artifact
  signing and license scanning (of third-party dependencies, distinct
  from terminology licensing) are not mentioned at all.
- **Why it matters:** Named explicitly in the originating task's Supply
  Chain section.
- **Risk:** LOW at this stage (no artifacts exist to sign yet).
- **Dependency:** `05` Release workflow, `13`.
- **Recommended action:** Add: container images signed (e.g., Sigstore/
  cosign) before Cloud Run deployment; dependency license scan as a
  Release workflow gate alongside the existing SAST/DAST/dependency-
  scan list.
- **Blocks implementation?** No.
- **Blocks security?** No.
- **Blocks production?** Would block a mature CI/CD launch, not an MVP.
- **Evidence:** `grep -i "sbom\|artifact sign\|license scan" docs/master/07*.md docs/master/13*.md` → one SBOM mention, zero for the other two.

## GAP-008 — Patient App: no account recovery or device/session management
- **File/Section:** `docs/master/12-MASTER-APPLICATION-ARCHITECTURE.md`
- **Classification:** MISSING
- **Problem:** The Patient App's notes cover booking, results, billing,
  consent — never account recovery (forgotten password/lost-MFA-device
  flow) or device/session management (view active sessions, revoke a
  lost phone's access).
- **Why it matters:** Named explicitly in the originating task's Patient
  Application section; these are baseline expectations for any
  patient-facing account system, doubly so for one gating access to
  health records.
- **Risk:** MEDIUM — account recovery flows are a common real-world
  attack surface (SIM-swap, recovery-email takeover) if under-specified.
- **Dependency:** `Identity` domain (`03`), `07`.
- **Recommended action:** Add both as explicit Patient App
  capabilities, with account recovery specifically requiring
  step-up verification (not a simple email link alone, given the
  sensitivity of what's being protected).
- **Blocks implementation?** Should block Phase 2's Patient App work
  specifically.
- **Blocks security?** No.
- **Blocks production?** Yes, if the Patient App ships without a
  recovery flow design.
- **Evidence:** `grep -i "account recovery\|device management\|session management" docs/master/12*.md docs/master/05*.md` → zero matches.

## GAP-009 — Data governance: no legal-hold or deletion-policy treatment
- **File/Section:** `docs/master/04-MASTER-DATA-MAP.md`; `docs/master/08-MASTER-COMPLIANCE-MAP.md`
- **Classification:** MISSING
- **Problem:** Retention is mentioned as a data-classification concern
  in principle, but there is no explicit treatment of legal hold
  (freezing deletion/retention during litigation or investigation) or a
  deletion policy (what "delete" actually means for a clinical record —
  most jurisdictions restrict or forbid hard-deleting clinical records
  even on patient request, unlike ordinary personal data under GDPR-style
  "right to erasure").
- **Why it matters:** This is a genuine, materially important gap for a
  healthcare platform specifically — the "right to erasure" pattern from
  general data-protection law does *not* apply the same way to clinical
  records in most jurisdictions, and the architecture doesn't yet say
  so explicitly, which risks a future implementer defaulting to a
  generic (and likely wrong, for clinical data) deletion model.
- **Risk:** HIGH if unaddressed before any real deletion feature is
  built — a wrongly "erased" clinical record is a patient-safety and
  legal problem, not just a data-management one.
- **Dependency:** `08`, `docs/compliance/COMPLIANCE-TRACEABILITY-MATRIX.md`, every clinical domain in `03`.
- **Recommended action:** Add an explicit statement: clinical records
  are retained per jurisdiction-specific medical-record-retention law
  (not general data-protection "erasure" law), with anonymization/
  restriction-of-processing as the applicable data-subject-rights
  mechanism instead of deletion — REQUIRES LEGAL VERIFICATION per
  jurisdiction, consistent with `08`'s existing status discipline. Add
  a legal-hold flag that can suspend any scheduled retention/archival
  action.
- **Blocks implementation?** Should block any "delete my data" feature
  specifically, not general implementation.
- **Blocks security?** No.
- **Blocks production?** Yes, if a deletion feature ships without this.
- **Evidence:** `grep -i "legal hold\|deletion polic\|right to erasure" docs/master/04*.md docs/master/08*.md` → zero matches.

## GAP-010 — DR: named catastrophic scenarios not walked through
- **File/Section:** `docs/master/17-MASTER-DISASTER-RECOVERY.md`
- **Classification:** INCOMPLETE
- **Problem:** The DR register is organized per-*component*
  (PostgreSQL, Pub/Sub, Object Storage, etc.) with generic backup/
  restore/RPO/RTO fields. It does not walk through named *scenarios*
  (ransomware, a full regional GCP outage, an identity-provider/
  Keycloak outage) end-to-end across components.
- **Why it matters:** A per-component register can look complete while
  missing scenario-level interactions (e.g., "if Keycloak is down, can
  anyone log in to *initiate* a recovery?" is a cross-component question
  a per-component table doesn't surface).
- **Risk:** MEDIUM.
- **Dependency:** `13`, every Data Plane component.
- **Recommended action:** Add 2-3 named scenario runbooks (ransomware/
  mass-delete, full regional outage, identity-provider outage) that
  reference the existing per-component register rather than duplicating
  it — each answering "what's the actual sequence of actions," not just
  "what's each component's RTO."
- **Blocks implementation?** No.
- **Blocks security?** No.
- **Blocks production?** Would block a real DR drill (the thing `17`
  itself says is the actual bar — "backup is not complete until restore
  is tested").
- **Evidence:** `grep -i "ransomware\|regional failure\|identity outage" docs/master/17*.md` → zero matches.

## GAP-011 — Billing: co-pay/deductible/currency not explicitly named
- **File/Section:** `docs/master/03-MASTER-DOMAIN-MAP.md` (`Billing`, `Insurance` domains)
- **Classification:** WEAK
- **Problem:** "Patient Responsibility" appears in the Revenue Cycle
  sequence, but co-pay, deductible, and multi-currency handling — named
  explicitly in the originating task — aren't broken out as distinct
  concepts, unlike rounding (which *is* explicitly addressed: "DENY
  monetary rounding drift").
- **Why it matters:** Co-pay and deductible are structurally different
  calculations (a flat fee vs. an accumulating threshold) that a generic
  "Patient Responsibility" bucket doesn't distinguish; multi-currency is
  relevant given the multi-country scope (`06`) but only Jordan's home
  currency is implicitly assumed anywhere.
- **Risk:** LOW at architecture stage.
- **Dependency:** `Billing`, `Insurance` domains.
- **Recommended action:** Expand the `Insurance` domain profile to name
  co-pay and deductible as distinct entities/calculations; add a
  currency field to `Invoice`/`Payment` entities explicitly, defaulting
  to JOD, extensible per country adapter.
- **Blocks implementation?** No.
- **Blocks security?** No.
- **Blocks production?** No — refinable during Phase 5 detailed design.
- **Evidence:** `grep -i "co-pay\|copay\|deductible\|currency" docs/master/03*.md` → zero matches (rounding *is* present, confirming this isn't a blanket financial-precision gap, just this specific set of concepts).

## GAP-012 — Control Plane: template cloning/versioning not explicit
- **File/Section:** `docs/master/11-MASTER-ORGANIZATION-PROVISIONING.md`
- **Classification:** INCOMPLETE
- **Problem:** "Preview Before Execution" exists; explicit template
  *cloning* (duplicate an existing org's config as a starting point) and
  template *versioning* (what happens to already-provisioned orgs when
  a template changes) are not addressed.
- **Why it matters:** Named explicitly in the originating task's Control
  Plane section; relevant once more than a handful of organizations
  exist.
- **Risk:** LOW.
- **Dependency:** `09`, `11`.
- **Recommended action:** Add: templates are versioned; an org's
  provisioning record pins the template version used at creation time
  (never silently re-applies a newer template version); cloning is a
  documented saga variant (`CREATE` seeded from an existing org's
  resolved config instead of a blank template).
- **Blocks implementation?** No.
- **Blocks security?** No.
- **Blocks production?** No.
- **Evidence:** `grep -i "dry-run\|preview\|clon" docs/master/11*.md` → Preview present, cloning/versioning absent.

## GAP-013 — Testing: privilege-escalation and break-glass not named as explicit test categories
- **File/Section:** `docs/master/15-MASTER-TESTING-STRATEGY.md`
- **Classification:** WEAK
- **Problem:** Cross-tenant DENY tests are explicit; privilege
  escalation and break-glass are covered only implicitly (as instances
  of the general ALLOW/DENY discipline) rather than named as their own
  required test categories the way cross-tenant is.
- **Why it matters:** Named explicitly in the originating task's Testing
  section; break-glass specifically is a high-consequence,
  low-frequency path that's easy to under-test if it isn't named
  explicitly on the checklist.
- **Risk:** LOW-MEDIUM.
- **Dependency:** `07`, `15`.
- **Recommended action:** Add "privilege escalation" and "break-glass
  invocation + expiry + audit" as named rows in `15`'s Security layer
  description, mirroring how cross-tenant is already named.
- **Blocks implementation?** No.
- **Blocks security?** No.
- **Blocks production?** No.
- **Evidence:** `grep -i "cross-tenant\|privilege escalation\|break-glass" docs/master/15*.md` → cross-tenant present twice, the other two absent.

---

## What Was Checked and Found READY (not a gap — stated for completeness, per the task's own classification requirement)

- **Multi-tenancy core (RLS + three-layer authorization):** `04`, `07` —
  fully specified, consistent, no gap found beyond GAP-005's specific
  async-path carve-out.
- **Clinical identity/duplicate handling (MPI merge/unmerge):** `03`
  `MPI` domain — thorough, includes false-positive-merge hazard
  handling. No gap found.
- **Control Plane provisioning saga (idempotency, compensation,
  rollback):** `11` — thorough beyond the two narrow gaps above (GAP-012).
- **Compliance status discipline (never IMPLEMENTED→APPROVED without
  gates):** `08` — no gap found; this is one of the strongest-enforced
  patterns in the whole repository, verified across three prior audit
  passes.
- **ADR governance (status discipline, non-silent-approval):** `19` —
  no gap found, independently re-verified this pass (19 ADRs, all
  PROPOSED, confirmed via direct grep).

## Dependencies
Feeds `docs/audit/FINAL-GAP-REGISTER.md`,
`docs/audit/DO-NOT-BUILD-YET.md`,
`docs/audit/FINAL-IMPLEMENTATION-READINESS.md`.

## Definition of Done
13 genuine, evidenced gaps found across the categories checked this
pass; zero generic "could be improved" statements; every gap traces to
an actual grep/read result, not an assumption. Categories not
exhaustively re-checked this pass (Pharmacy, Laboratory, Radiology,
Hospital, Country Adapters in detail) are carried into
`FINAL-GAP-REGISTER.md` as OUT OF SCOPE FOR THIS PASS rather than
silently marked clean.
