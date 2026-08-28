# Compliance Traceability Matrix

**STATUS:** ACTIVE (governance register) — expands `docs/master/08`'s
illustrative register into full per-country coverage
**EVIDENCE CLASS:** DESIGN

## Purpose
`docs/master/08-MASTER-COMPLIANCE-MAP.md` defines the compliance
*framework* (Requirement → Control → Implementation → Test → Evidence →
Review, with the mandatory status lifecycle). This document applies that
same framework across all seven required jurisdictions, so no country is
silently missing from the register. It does not redefine the framework —
see `08` for that.

## Hard Rule (inherited from `08`, restated here because it's the rule
most likely to be violated under commercial pressure)
**IMPLEMENTED ≠ COMPLIANT. APPROVED requires an actual external legal or
audit evidence artifact, not an engineering team's own assessment.**
Every cell below stays at its listed status, or lower, until an
independently-obtained evidence artifact justifies moving it up.

## Status Values (same as `08`)
UNKNOWN → DISCOVERED → REQUIRES LEGAL REVIEW → DESIGNED → IMPLEMENTED →
TESTED → EVIDENCED → APPROVED (→ EXPIRED / NON-COMPLIANT)

## Per-Country Register

### Jordan (home jurisdiction)
| Requirement | Control | Status | Owner | Review Date | Evidence |
|---|---|---|---|---|---|
| Personal Data Protection Law No. 24 of 2023 (PDPL) | Consent capture, data-subject rights workflow, breach notification process | DISCOVERED — REQUIRES LEGAL REVIEW | UNKNOWN | UNSET | None — see `argon-compliance-gaps` skill for the detailed gap analysis already done for this jurisdiction |
| Electronic invoicing format & submission | Government Country Adapter (`06`) | DISCOVERED — REQUIRES LEGAL REVIEW | UNKNOWN | UNSET | None |
| National health system integration approval | TBD integration point | UNKNOWN — REQUIRES LEGAL REVIEW | UNKNOWN | UNSET | None |
| Controlled-substance chain-of-custody (pharmacy regulation) | Append-only ledger (`04`) | UNKNOWN — REQUIRES LEGAL REVIEW | UNKNOWN | UNSET | None |

### Saudi Arabia
| Requirement | Control | Status | Owner | Review Date | Evidence |
|---|---|---|---|---|---|
| Personal Data Protection Law (PDPL, KSA) | Same technical controls as Jordan row above; legal text differs | UNKNOWN — REQUIRES LEGAL REVIEW per country (`08`) | UNKNOWN | UNSET | None |
| ZATCA e-invoicing (Fatoora) | Government Country Adapter (`06`) | UNKNOWN — REQUIRES LEGAL REVIEW | UNKNOWN | UNSET | None |
| National health system integration (NPHIES or successor) | TBD integration point | UNKNOWN — REQUIRES LEGAL REVIEW | UNKNOWN | UNSET | None |
| Controlled-substance chain-of-custody | Append-only ledger (`04`) | UNKNOWN — REQUIRES LEGAL REVIEW | UNKNOWN | UNSET | None |

### United Arab Emirates
| Requirement | Control | Status | Owner | Review Date | Evidence |
|---|---|---|---|---|---|
| Federal/Dubai/Abu Dhabi data protection law(s) | Same technical controls as above | UNKNOWN — REQUIRES LEGAL REVIEW per emirate, not just per country | UNKNOWN | UNSET | None |
| E-invoicing / e-billing requirements | Government Country Adapter (`06`) | UNKNOWN — REQUIRES LEGAL REVIEW | UNKNOWN | UNSET | None |
| National health integration (Malaffi / Riayati / NABIDH, depending on emirate) | TBD integration point | UNKNOWN — REQUIRES LEGAL REVIEW | UNKNOWN | UNSET | None |
| Controlled-substance chain-of-custody | Append-only ledger (`04`) | UNKNOWN — REQUIRES LEGAL REVIEW | UNKNOWN | UNSET | None |

### Qatar
| Requirement | Control | Status | Owner | Review Date | Evidence |
|---|---|---|---|---|---|
| Personal data protection law | Same technical controls as above | UNKNOWN — REQUIRES LEGAL REVIEW | UNKNOWN | UNSET | None |
| E-invoicing requirements | Government Country Adapter (`06`) | UNKNOWN — REQUIRES LEGAL REVIEW | UNKNOWN | UNSET | None |
| National health system integration | TBD integration point | UNKNOWN — REQUIRES LEGAL REVIEW | UNKNOWN | UNSET | None |
| Controlled-substance chain-of-custody | Append-only ledger (`04`) | UNKNOWN — REQUIRES LEGAL REVIEW | UNKNOWN | UNSET | None |

### Kuwait
| Requirement | Control | Status | Owner | Review Date | Evidence |
|---|---|---|---|---|---|
| Personal data protection law | Same technical controls as above | UNKNOWN — REQUIRES LEGAL REVIEW | UNKNOWN | UNSET | None |
| E-invoicing requirements | Government Country Adapter (`06`) | UNKNOWN — REQUIRES LEGAL REVIEW | UNKNOWN | UNSET | None |
| National health system integration | TBD integration point | UNKNOWN — REQUIRES LEGAL REVIEW | UNKNOWN | UNSET | None |
| Controlled-substance chain-of-custody | Append-only ledger (`04`) | UNKNOWN — REQUIRES LEGAL REVIEW | UNKNOWN | UNSET | None |

### Bahrain
| Requirement | Control | Status | Owner | Review Date | Evidence |
|---|---|---|---|---|---|
| Personal Data Protection Law (PDPL, Bahrain) | Same technical controls as above | UNKNOWN — REQUIRES LEGAL REVIEW | UNKNOWN | UNSET | None |
| E-invoicing requirements | Government Country Adapter (`06`) | UNKNOWN — REQUIRES LEGAL REVIEW | UNKNOWN | UNSET | None |
| National health system integration | TBD integration point | UNKNOWN — REQUIRES LEGAL REVIEW | UNKNOWN | UNSET | None |
| Controlled-substance chain-of-custody | Append-only ledger (`04`) | UNKNOWN — REQUIRES LEGAL REVIEW | UNKNOWN | UNSET | None |

### Oman
| Requirement | Control | Status | Owner | Review Date | Evidence |
|---|---|---|---|---|---|
| Personal data protection law | Same technical controls as above | UNKNOWN — REQUIRES LEGAL REVIEW | UNKNOWN | UNSET | None |
| E-invoicing requirements | Government Country Adapter (`06`) | UNKNOWN — REQUIRES LEGAL REVIEW | UNKNOWN | UNSET | None |
| National health system integration | TBD integration point | UNKNOWN — REQUIRES LEGAL REVIEW | UNKNOWN | UNSET | None |
| Controlled-substance chain-of-custody | Append-only ledger (`04`) | UNKNOWN — REQUIRES LEGAL REVIEW | UNKNOWN | UNSET | None |

## Global (Not Jurisdiction-Specific)
| Requirement | Control | Status | Owner | Review Date | Evidence |
|---|---|---|---|---|---|
| Application security baseline (OWASP ASVS 5 / API Security Top 10) | `07-MASTER-SECURITY-MAP.md` | DESIGNED | UNKNOWN | UNSET | None yet |
| Information security management (ISO/IEC 27001/27002:2022) | `07` | DESIGNED (target framework) | UNKNOWN | UNSET | None yet |
| Health-sector security overlay (ISO 27799) | `07` | DESIGNED (target framework) | UNKNOWN | UNSET | None yet |
| FHIR conformance (R4/R4B, ADR-018) | `06` | UNKNOWN — REQUIRES EVIDENCE of a published conformance statement/Implementation Guide | UNKNOWN | UNSET | None |
| DICOM/PACS conformance | `06` | UNKNOWN — REQUIRES EVIDENCE of an actual conformance statement | UNKNOWN | UNSET | None |
| Payment card handling (if payments module touches cards directly) | Tokenization, no raw card storage (`03` Payments domain) | Mitigated by design — REQUIRES independent PCI DSS scope assessment before any claim | UNKNOWN | UNSET | None |
| Accessibility (WCAG 2.2 AA) | `12`, `15` | DESIGNED (target adopted) | UNKNOWN | UNSET | None yet |

## What This Matrix Deliberately Does Not Do
- It does **not** assert that any row is legally correct — every
  per-country row is at DISCOVERED or UNKNOWN precisely because no
  licensed local counsel has reviewed it yet. Rows here mirror the
  detailed jurisdiction-specific gap analysis already captured in the
  `argon-compliance-gaps` skill for Jordan; the other six countries have
  **not** had that same depth of analysis done and their rows reflect
  that honestly (UNKNOWN, not DISCOVERED).
- It does **not** invent government agency names, portal names, or
  submission formats where the actual current name isn't independently
  confirmed — several rows above say "TBD integration point" or name an
  informally-known system rather than fabricate specificity that hasn't
  been verified.
- It does **not** claim any certification, government approval, or
  insurer approval anywhere in this file.

## Next Step
Per-country legal review is genuinely external work — outside what any
document-normalization pass can produce. The next authorized action for
this matrix is commissioning that review (licensed local counsel, one
country at a time, starting with Jordan since the platform's operator is
based there), not writing more architecture text.
