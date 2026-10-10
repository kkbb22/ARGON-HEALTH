# COMPLIANCE TRACEABILITY MATRIX

STATUS: PROPOSED
EVIDENCE CLASS: DESIGN (LEGAL EVIDENCE required before any status beyond DISCOVERED — none obtained in this pass)

## Purpose
Extend `docs/master/08-MASTER-COMPLIANCE-MAP.md`'s starting register into
a full per-jurisdiction traceability matrix with the columns required by
the governance task: Jurisdiction, Law/Standard, Requirement, Control,
System Component, Implementation, Test, Evidence, Owner, Review Date,
Status.

## Scope
Covers the seven named jurisdictions (Jordan, Saudi Arabia, UAE, Qatar,
Kuwait, Bahrain, Oman) plus the jurisdiction-neutral global security/
accessibility standards already adopted as baselines. **No government
approval, insurer approval, or legal-compliance status is claimed
anywhere in this document** — every row's Status is DISCOVERED or lower
until an actual qualified legal review occurs, per
`docs/master/08-MASTER-COMPLIANCE-MAP.md`'s hard rule that IMPLEMENTED
never converts directly to APPROVED.

## Matrix

| Jurisdiction | Law/Standard | Requirement | Control | System Component | Implementation | Test | Evidence | Owner | Review Date | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| Jordan (home jurisdiction) | Personal Data Protection Law No. 24 of 2023 (PDPL) | Lawful processing, data-subject rights, breach notification | `Consent` domain, `Patient` domain (`03`) | Consent capture/withdrawal, data export/deletion flows | Not started | Not started | None | TBD | Not set | **DISCOVERED — REQUIRES LEGAL REVIEW** |
| Jordan | ISTD e-invoicing requirements | Electronic invoice format, submission, numbering | `Government Integrations` domain, Jordan country adapter (`06`) | Government e-invoicing gateway integration | Not started | Not started | None | TBD | Not set | **DISCOVERED — REQUIRES LEGAL REVIEW** |
| Jordan | Health-sector licensing/regulation (ministry-level) | Facility licensing, clinical record retention rules | `Organization` domain, `11-MASTER-ORGANIZATION-PROVISIONING.md` | Organization Provisioning saga (digital only — see `11`'s explicit non-scope statement) | N/A — digital provisioning ≠ legal licensing (ADR-015) | N/A | None | TBD | Not set | **UNKNOWN — REQUIRES LEGAL REVIEW; explicitly out of this repository's scope to satisfy alone** |
| Saudi Arabia | Personal Data Protection Law (PDPL, SDAIA) | Lawful processing, data localization | `Consent`, `Government Integrations` domains | Country adapter (not yet designed in detail) | Not started | Not started | None | TBD | Not set | **UNKNOWN — REQUIRES LEGAL REVIEW** |
| Saudi Arabia | ZATCA e-invoicing (Fatoora) | Electronic invoice format, real-time reporting | `Government Integrations` domain, KSA country adapter | Not started | Not started | Not started | None | TBD | Not set | **UNKNOWN — REQUIRES LEGAL REVIEW** |
| UAE | Federal Decree-Law on Personal Data Protection | Lawful processing, cross-border transfer rules | `Consent`, `Government Integrations` domains | Country adapter (not yet designed) | Not started | Not started | None | TBD | Not set | **UNKNOWN — REQUIRES LEGAL REVIEW** |
| UAE | Health-sector regulation (DHA/DOH/MOHAP, varies by emirate) | Facility licensing, clinical data handling | `Organization`, `Government Integrations` domains | Not started | Not started | Not started | None | TBD | Not set | **UNKNOWN — REQUIRES LEGAL REVIEW** |
| Qatar | Personal Data Privacy Protection Law | Lawful processing | `Consent`, `Government Integrations` domains | Country adapter (not yet designed) | Not started | Not started | None | TBD | Not set | **UNKNOWN — REQUIRES LEGAL REVIEW** |
| Kuwait | Data protection regulation (sector-specific, evolving) | Lawful processing | `Consent`, `Government Integrations` domains | Country adapter (not yet designed) | Not started | Not started | None | TBD | Not set | **UNKNOWN — REQUIRES LEGAL REVIEW** |
| Bahrain | Personal Data Protection Law (PDPL) | Lawful processing | `Consent`, `Government Integrations` domains | Country adapter (not yet designed) | Not started | Not started | None | TBD | Not set | **UNKNOWN — REQUIRES LEGAL REVIEW** |
| Oman | Personal Data Protection Law | Lawful processing | `Consent`, `Government Integrations` domains | Country adapter (not yet designed) | Not started | Not started | None | TBD | Not set | **UNKNOWN — REQUIRES LEGAL REVIEW** |
| Global (not jurisdiction-specific) | OWASP ASVS 5 / API Security Top 10 | Application security baseline | `07-MASTER-SECURITY-MAP.md` | Three-layer authorization model | Not started | Not started | None | TBD | Not set | **DESIGNED** (baseline adopted; not implemented/tested) |
| Global | ISO/IEC 27001:2022 / 27002:2022 | Information security management system | `07`, `docs/governance/*` | Governance layer (this repository) | Partially — governance documents exist | Not started | This repository's own documents | TBD | Not set | **DESIGNED** |
| Global | ISO 27799:2025 | Health-sector security overlay | `07` | Same as above | Partially | Not started | Same | TBD | Not set | **DESIGNED** |
| Global | WCAG 2.2 AA | Accessibility | `12-MASTER-APPLICATION-ARCHITECTURE.md` | Shared design system (not yet built) | Not started | Not started | None | TBD | Not set | **DESIGNED** |
| Global | PCI DSS (current applicable baseline) | Payment card data handling | `Payments` domain (`03`) | Tokenization-by-design (no raw card storage in ARGON's data plane) | Design only | Not started | None | TBD | Not set | **DESIGNED — REQUIRES an independent PCI scope assessment before any claim, per `docs/governance/TECHNOLOGY-BASELINE.md` Payments section** |

## Rule Enforcement
No row in this matrix may be moved to APPROVED, EVIDENCED, or any
status implying regulatory sign-off by editing this document alone —
that requires an actual qualified legal review or independent audit
whose output becomes the Evidence artifact, per
`docs/master/08-MASTER-COMPLIANCE-MAP.md`'s status lifecycle.

## Alternatives Considered
- **Marking any jurisdiction row DESIGNED or higher based on the country
  adapter architecture pattern being sound** (rejected) — architectural
  soundness (having a place for the logic to live) is not legal
  compliance; conflating the two is exactly the DESIGNED-vs-COMPLIANT
  collapse `docs/master/08` exists to prevent.

## Dependencies
Extends `docs/master/08-MASTER-COMPLIANCE-MAP.md`. Depends on
`docs/master/06`'s Government Country Adapter architecture. Feeds
`docs/governance/ARCHITECTURE-STATUS.md`.

## Unknowns
UNKNOWN for essentially every jurisdiction-specific row — this is the
accurate, honest state of a documentation-only repository with zero
legal review performed. Owner and Review Date columns are uniformly TBD
because no organizational owner has been assigned in this pass.

## Definition of Done
Every jurisdiction named in `docs/master/06`'s Government Country Adapter
list has at least the minimum rows above (data protection, e-invoicing
where applicable, health-sector licensing); expansion beyond this
starting set happens per `docs/master/20-MASTER-IMPLEMENTATION-ROADMAP.md`
Phase 6's per-country trigger, not speculatively.
