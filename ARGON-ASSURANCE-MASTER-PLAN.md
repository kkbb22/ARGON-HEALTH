# ARGON Assurance Master Plan

**Status:** PROPOSED — approval required from the real project decision authority.  
**Evidence class:** ASSURANCE PROCESS DESIGN; no product assurance implied.  
**Precedence:** subordinate to `docs/governance/ARGON-SOURCE-OF-TRUTH.md`, approved ADRs, and the existing master architecture. If a control conflicts with them, open a governed decision/change request.

**Operational registers:** [Verification matrix](VERIFICATION-MATRIX.csv), [risk register](RISK-REGISTER.csv), [evidence register](EVIDENCE-REGISTER.csv), [release sign-offs](RELEASE-SIGNOFF.csv), [operational revalidation](OPERATIONAL-REVALIDATION.csv), and [release gate checklist](RELEASE-GATES.md).

## 1. Assurance objective

For every material product, architecture, security, privacy, clinical-safety, operational, and regulatory claim, maintain a traceable chain:

`Need / hazard / obligation → requirement → design decision → implementation → test → result → evidence artifact → independent review → approval → periodic revalidation`.

No prose assertion, AI-generated review, test badge, line-coverage number, or code merge may substitute for missing evidence.

## 2. What this kit can and cannot prove

This kit can enforce record shape, identity uniqueness, link/evidence integrity, and explicit readiness gates. Once populated, it can make omissions visible and reproducible. It cannot independently prove clinical correctness, the absence of exploitable vulnerabilities, legal compliance, market demand, or safe operation. Those require real implementation, representative tests/data, qualified human review, and sometimes external assessment.

## 3. Roles and separation of duties

Assign named people (not just role labels) in the repository's governed ownership record before Gate G1.

| Role | Accountability | Independence rule |
|---|---|---|
| Decision authority | Accepts ADRs, risk appetite, and phase/release decisions | Cannot self-approve controls merely by authoring them |
| Product/system owner | Scope, user needs, acceptance criteria, roadmap | Must provide evidence of user need/value |
| Architecture owner | Domain/data boundaries, technology rationale, migration path | Another architect reviews material/high-risk decisions |
| Engineering owner | Implementation quality, reproducibility, migrations | Code changes require peer review |
| Security lead | Threat model, identity, authorization, secure SDLC, incident readiness | Critical/high security controls need review independent of implementer |
| Clinical safety lead | Clinical hazards, foreseeable misuse, clinical workflow safety | Must be suitably qualified; not replaced by a generic code review |
| Privacy/legal owner | Data mapping, lawful basis, retention, transfers, jurisdiction review | Local qualified legal/privacy review where applicable |
| QA/verification owner | Traceability, test strategy, results, defect closure | Must challenge evidence, not only report author-reported status |
| Operations owner | SLOs, backup/restore, incident response, capacity, rollback | Must participate in realistic operational drills |
| Release authority | Checks gate package and authorizes environment promotion | Must not waive mandatory legal/clinical/security stops unilaterally |

One person may hold multiple roles in a small team where appropriate, but independent review cannot be represented as independent if the same person implemented and approved the same high-risk control. Record justified role combinations and compensating checks.

## 4. Status models

### Verification matrix statuses

- `NOT_RUN` — no verification result recorded.
- `IN_PROGRESS` — work is underway; no pass claim.
- `PASS` — acceptance criteria passed and an evidence record exists in `REVIEWED` or `ACCEPTED` state.
- `FAIL` — criteria failed; release-gate blocker according to scope/severity.
- `BLOCKED` — verification cannot run because a dependency, environment, owner, or decision is missing.
- `NOT_APPLICABLE` — applicability was explicitly assessed, justified, and approved with evidence; never use it to hide missing work.
- `ACCEPTED_RISK` — a risk exception was formally approved, linked to a live risk record, and remains within its expiry. Critical release controls cannot be waived this way by this checker.

These are assurance statuses and do not replace the architecture lifecycle in `ARCHITECTURE-STATUS.md` or clinical/compliance-specific lifecycles already present.

### Evidence states

- `PLANNED` — expected but not collected.
- `COLLECTED` — captured; not yet reviewed.
- `REVIEWED` — reviewer recorded; suitable for a normal `PASS` record.
- `ACCEPTED` — approved for the stated gate/use and valid until its review/expiry date, suitable for release gates.
- `EXPIRED` — no longer current enough for intended use.
- `REJECTED` — evidence does not support the claim.

Evidence must identify the exact artifact, control(s), environment/build, date, source, result, reviewer, and relevant limitations. Prefer machine-readable output plus a human-readable summary. For high/critical items, include reproducibility instructions, tool/version, configuration, and artifact hash where feasible.

## 5. Gate model

| Gate | Question | Minimum exit condition |
|---|---|---|
| G0 — Baseline integrity | Are the scope, source of truth, owners, and assurance records coherent? | Unique identifiers; authority/owners named; requirements and risk method accepted; known contradictions logged |
| G1 — Design approval | Is the design coherent and risk-informed enough to implement? | Accepted ADRs for in-scope design; threat model; data-flow and trust boundaries; hazard analysis; requirements traceability; unresolved critical design issues closed |
| G2 — Implementation verification | Does the implementation match approved requirements? | Reproducible build; code review; unit/integration/contract tests; migration tests; applicable static/dependency/secret scans; adversarial testing plan and results |
| G3 — Staging safety | Is the release candidate safe enough for a controlled pilot? | Tenant/authorization tests, clinical safety review, privacy/legal applicability review, integration failures, usability checks, recovery/rollback drills, high-risk findings handled |
| G4 — Production release | Is this exact build approved for production? | All applicable controls through G4 have accepted evidence; no open critical risk; high risks treated/accepted under explicit policy; production sign-offs captured; monitoring and rollback ready |
| G5 — Operate and revalidate | Does production remain within approved assumptions? | SLO/error-budget review; incident follow-up; periodic access/risk review; restore/DR drills; evidence expiry review; trigger-based reassessment |

The matrix's `required_gate` is the earliest gate at which a control must be closed. Passing a gate does not mean every future gate passed. Change impact may reopen any control.

## 6. Severity and fail-closed principles

- **Critical:** credible severe patient harm, cross-tenant PHI exposure at scale, privilege escalation to broad clinical records, unrecoverable critical data loss, or a release-blocking legal prohibition. Stop progression; no casual risk acceptance.
- **High:** major privacy/security compromise, clinically meaningful data corruption, core workflow unavailability beyond accepted limits, or material regulatory exposure. Fix or obtain documented, time-bounded acceptance from the authorized risk owner plus compensating controls; legal/clinical obligations may still prohibit acceptance.
- **Medium/Low:** prioritize by likelihood, impact, detectability, exposure, and dependency. Acceptance must still name owner, rationale, expiry, and monitoring.

A risk score does not decide clinical/legal acceptability by arithmetic alone. The relevant qualified owner retains accountability.

## 7. Traceability rules

1. Every in-scope requirement/control has a stable ID, named owner, verification method, measurable acceptance criteria, and gate.
2. Every `PASS` cites evidence that exists in the repository or an approved controlled evidence store with a stable, access-controlled reference. For the included checker, local artifacts are required.
3. Evidence records identify the exact commit/build/environment and data profile tested. Redact secrets and patient identifiers; do not store PHI in the Git repository.
4. Any changed requirement, architecture, dependency, data model, legal scope, clinical workflow, or production incident triggers impact analysis and may reopen related controls.
5. All accepted risks have a named accepting authority, rationale, compensating controls, review date, and expiry. No indefinite waivers.
6. Automated checks are one evidence source, not an independent safety certification.
7. Test data must be synthetic or properly de-identified unless a formal, lawful, access-controlled test-data process is approved.

## 8. Minimum change protocol

For each pull request:

- state intent and affected controls;
- link requirements and ADRs;
- describe threat/hazard/data-migration impact;
- attach tests, scans, and evidence artifacts;
- report failures as failures, not as “known acceptable” without approval;
- require review by appropriate owners;
- update evidence freshness/validity and risk records;
- define rollback/forward-fix approach for production-impacting changes.

## 9. Periodic review triggers

Reassess the affected controls upon: a new or changed clinical function; role/tenant model change; data migration; new external integration; new country or hosting region; material dependency or identity-provider change; severe security/clinical incident; backup/restore failure; threat intelligence relevant to the product; legal/regulatory change; unexplained SLO breach; or expiry of evidence/approval.

## 10. Metrics that expose reality

Track, with defined denominators: proportion of in-scope requirements traced to tests; critical/high controls with current accepted evidence; open critical/high risks; expired evidence count; escaped defects by severity; restore-drill success and achieved RTO/RPO; tenant-isolation negative-test pass rate; vulnerability remediation age; and production SLO/error-budget status. Never use a green average to hide one unresolved critical failure.

## 11. Initial project-specific assumptions to validate

- The target architecture repo is not the implementation repository and presently contains design/planning artifacts only.
- The current live system and its actual deployment/data flows must be confirmed separately; documentation mentions an existing Firebase system and an additive `license_tier`/`enabled_modules` step.
- All countries and obligations must be assessed against actual launch scope, data flows, contracting roles, and intended clinical use. No legal status is inferred from this kit.
- Controls marked in the starter CSV are proposed objectives, not verified findings. All start `NOT_RUN`.

## 12. Definition of done for adopting this kit

- Named owners and a decision authority are accepted in a governed record.
- Existing authoritative docs are mapped to control IDs without duplicate or conflicting sources of truth.
- G0/G1 controls have been reviewed by the project owner; required decisions are approved by the real authority.
- The structural check and its unit tests run in CI.
- Release gate fails on the starter state, then passes only after actual evidence, risk handling, and sign-offs satisfy the configured gate.
