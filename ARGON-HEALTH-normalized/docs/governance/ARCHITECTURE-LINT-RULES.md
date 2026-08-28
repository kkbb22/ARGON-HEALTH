# Architecture Lint Rules

**STATUS:** ACTIVE (governance policy)
**EVIDENCE CLASS:** DESIGN

## Purpose
A checklist of structural rules every future domain, workflow, API, or
infrastructure addition to ARGON must satisfy. These are lint rules for
architecture documents and, later, for actual code review — not a claim
that any of them have been mechanically enforced yet.

## How to read this file
Each rule lists **Source** — the master document that already
establishes it — so this file is an index, not a duplicate. A rule with
no Source is new to this normalization pass.

| # | Rule | Source |
|---|---|---|
| L1 | No domain without an owner. | `03-MASTER-DOMAIN-MAP` (owner is a required field per domain profile) |
| L2 | No workflow without a documented failure path. | `05-MASTER-WORKFLOW-MAP` (Failure is a required field per workflow) |
| L3 | No sensitive action without explicit authorization. | `07-MASTER-SECURITY-MAP` (three-layer enforcement) |
| L4 | No clinical mutation without an audit trail. | `16-MASTER-CLINICAL-SAFETY-MODEL`, `07` |
| L5 | No external integration bypasses the Interoperability Layer. | `06-MASTER-INTEGRATION-MAP` (ADR-006) |
| L6 | No country-specific logic inside Global Core. | `06` (Government Country Adapter pattern) |
| L7 | No duplicate patient identity model across domains. | `10-MASTER-PATIENT-JOURNEY` (single MPI/identity) |
| L8 | No PHI in standard telemetry (logs, metrics, traces). | `18-MASTER-NON-FUNCTIONAL-REQUIREMENTS`; `argon-governance` skill, Core Principle 1 |
| L9 | No financial value stored or computed as floating point. | `04-MASTER-DATA-MAP`, `MASTER-ARGON-BLUEPRINT` §3 |
| L10 | No DICOM or other large binary payload stored in the transactional (PostgreSQL) database. | `04` (ADR-005) |
| L11 | No production infrastructure change applied without review. | NEW — see "Definition of Done" gap below |
| L12 | No compliance status claim skips its evidence gate (IMPLEMENTED ≠ APPROVED). | `08-MASTER-COMPLIANCE-MAP` (ADR-009) |
| L13 | No certification claim without external evidence. | `08`, this repository's own Zero-Fabrication rule |
| L14 | No standard-conformance claim (FHIR, DICOM, WCAG, etc.) without evidence of actual conformance testing. | NEW — no conformance-test register exists yet; tracked as a gap |
| L15 | No messaging domain code imports a broker SDK directly — always via the messaging abstraction. | `06` (ADR-016) |
| L16 | No IaC tool assumption goes unqualified after ADR-017 — say OpenTofu, not "Terraform," unless explicitly discussing history. | `docs/adr/ADR-017-INFRASTRUCTURE-AS-CODE.md`; enforced in this pass, see `docs/audit/ARCHITECTURE-CONSISTENCY-AUDIT.md` |
| L17 | No FHIR version assumption goes unqualified after ADR-018 — R4/R4B is production baseline, R5 is conditional, R6 is deferred. | `docs/adr/ADR-018-FHIR-PRODUCTION-BASELINE.md`; enforced in this pass |
| L18 | Every ADR that changes a prior decision must reference the ADR or master-document statement it supersedes — never a silent edit. | `docs/governance/ARGON-SOURCE-OF-TRUTH.md` §2 |
| L19 | A Control Plane / platform-operator role never gets standing PHI access — only time-boxed, audited, break-glass elevation. | `07` (ADR-008) |
| L20 | No numeric performance, RTO/RPO, or scale claim ("supports X million users") without measured evidence. | `17`, `18` (ADR-012, ADR-013) |

## Gaps Identified While Compiling This List
- **L11** (no production infra change without review) has no dedicated
  enforcement document yet — `docs/master/13-MASTER-INFRASTRUCTURE-ARCHITECTURE.md`
  covers the target topology but not a change-review gate. Recommend an
  ADR, or a new governance document (e.g. "CHANGE-CONTROL.md" under
  `docs/governance/`) in a future pass.
- **L14** (standard-conformance claims need evidence) has no register.
  Recommend folding into `docs/compliance/COMPLIANCE-TRACEABILITY-MATRIX.md`
  as a "Standard Conformance" section in a future pass, rather than a
  new document.

## Enforcement Status
These are **documentation-level rules today** — none are mechanically
enforced by a linter, CI check, or code review process, because no code
exists yet. When Foundation Implementation begins, L1–L20 above are the
starting checklist for that implementation's own CI/lint tooling and PR
review checklist.
