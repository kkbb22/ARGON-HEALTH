# Release Gates and Stop-the-Line Rules

**Status: PROPOSED.** Adopt through the existing ARGON decision process before treating this as binding governance.

Source registers: [verification matrix](VERIFICATION-MATRIX.csv), [risk register](RISK-REGISTER.csv), [evidence register](EVIDENCE-REGISTER.csv), [release sign-offs](RELEASE-SIGNOFF.csv), and [operational revalidation](OPERATIONAL-REVALIDATION.csv).

## Non-negotiable release stops

Do not release to production if any applicable condition is true:

- an in-scope Critical control is `FAIL`, `BLOCKED`, `NOT_RUN`, or lacks current accepted evidence;
- a critical hazard or critical/high security issue lacks an approved mitigation and verified retest;
- cross-tenant access, privilege escalation, audit-log integrity, patient identity integrity, medication/allergy handling (where in scope), or financial-ledger invariants have an unresolved material defect;
- a required legal, privacy, clinical-safety, or regulatory determination is unresolved for the deployment's actual jurisdiction and intended use;
- backup restore, data migration recovery, or rollback has not been demonstrated for the release's risk profile;
- a material dependency, build artifact, configuration, or database migration is not reproducibly tied to the release candidate;
- the release candidate has not passed its agreed regression, integration, and load tests;
- monitoring, alert routing, incident ownership, and a tested response path are missing;
- required independent sign-offs are absent or expired.

A release gate may report only the scope and build it examined. It does not certify the entire platform forever.

## Gate checklist

### G0 — Baseline integrity

- [ ] Governing source-of-truth and document precedence confirmed.
- [ ] Scope, intended users, non-goals, jurisdictions, hosting regions, and data categories stated.
- [ ] Decision authority and role owners named.
- [ ] Requirements, risks, evidence register, and control IDs stable and unique.
- [ ] Contradictions/open questions logged with owner and due date.

### G1 — Architecture approval

- [ ] Architecture/sequence/data-flow/trust-boundary diagrams reviewed.
- [ ] Domain write ownership, invariants, event semantics, failure paths, and data residency documented.
- [ ] Threat model and clinical hazard analysis reviewed.
- [ ] Security/tenant model includes server-side enforcement and data-store boundaries appropriate to the actual stack.
- [ ] Technology decisions have current evidence, alternatives, operating cost, migration/exit plan, and named approval.
- [ ] Performance/recovery targets are explicitly approved business targets, not unmeasured claims.

### G2 — Implementation verification

- [ ] Build is reproducible from a clean environment and exact revision is recorded.
- [ ] Peer review and automated test suites pass.
- [ ] Static analysis, secrets, dependencies, licences, container/IaC checks are run where applicable.
- [ ] Schema migrations and backward/forward compatibility are tested against realistic volume.
- [ ] Authorization negative tests cover each resource/action and tenant boundary.
- [ ] Independent adversarial/forensic code audit is attached before claiming a phase `IMPLEMENTED`, consistent with existing ARGON rule L15.

### G3 — Staging/pilot safety

- [ ] Test and staging configuration match the production security model.
- [ ] End-to-end workflows tested, including rejection, timeout, duplicate, cancellation, and partial failure.
- [ ] Clinical safety review completed for in-scope clinical functions; hazards have verified controls.
- [ ] Privacy/legal review completed for actual country, controller/processor roles, transfers, retention, and user rights, where applicable.
- [ ] Interoperability contracts tested against real counterpart sandbox/specifications and documented version profiles.
- [ ] Usability/accessibility checks completed with representative users.
- [ ] Restore and rollback drills passed; achieved recovery metrics recorded.
- [ ] No unresolved critical/high issue outside the formally permitted risk-acceptance policy.

### G4 — Production authorization

- [ ] Exact commit/build/image/dependency lock and migration plan identified.
- [ ] All applicable matrix controls through G4 have accepted evidence or approved applicability decisions.
- [ ] No open Critical risk; every High risk is closed or handled with authorized, time-limited acceptance and compensating controls, unless law/clinical policy prohibits acceptance.
- [ ] Data protection/legal and clinical sign-offs are included when scope makes them applicable; inapplicability must have documented specialist rationale.
- [ ] SLOs, dashboards, alert thresholds, on-call owner, incident runbook, and rollback are ready.
- [ ] Backup/restore evidence is recent enough and matches the actual architecture.
- [ ] Data migration validated and reconciled; audit trail retained.
- [ ] Release-signoff record completed by authorized roles.

### G5 — Operational revalidation

- [ ] Monitor SLOs and errors; review alerts and user-reported safety issues.
- [ ] Review access/privilege changes, break-glass use, service accounts, secrets, and audit events.
- [ ] Re-run or review vulnerability/dependency scans and evidence expiry.
- [ ] Conduct scheduled restore/DR drills and record achieved RTO/RPO.
- [ ] Reassess risks after incidents, changes, or jurisdiction/function expansion.
- [ ] Close corrective actions only after a regression test proves the fix.

## Sign-off policy

The included `RELEASE-SIGNOFF.csv` is intentionally empty. A row must refer to one exact release candidate and environment. All roles required for the actual scope must sign. For a genuinely non-applicable sign-off, provide a linked specialist determination instead of silently omitting the field. The included script enforces all sign-off columns for G4 as a conservative default; modify only through an approved governance change.
