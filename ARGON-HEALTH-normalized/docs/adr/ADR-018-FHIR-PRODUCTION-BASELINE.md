# ADR-018 — FHIR Production Baseline Corrected to R4/R4B (was R5)

**STATUS:** PROPOSED — correction, not yet independently reviewed
**EVIDENCE CLASS:** DESIGN (decision), backed by EXTERNAL RESEARCH (see Evidence link below)

> Promoted out of `docs/master/19-MASTER-ARCHITECTURAL-DECISIONS.md` during the
> repository normalization pass. `19` now carries only the short index
> entry; this file is the canonical full text.

**ADR-018 — FHIR production baseline corrected to R4/R4B (was R5)**
- Status: **PROPOSED** (correction, not yet independently reviewed)
- Date: 2026-08-27
- Context: The original `06`/`14` target stated FHIR R5 as the
  production baseline with R4/R4B as a compatibility layer. The
  Architecture Normalization task required re-verifying this against
  current official/authoritative sources rather than carrying it forward
  unverified.
- Problem: Is R5 actually the correct production target for near-term
  real-world interoperability (government systems, payers, external
  labs)?
- Options: R4/R4B as baseline (R5 optional), R5 as baseline (R4/R4B
  compatibility), R6 as baseline (rejected outright — still in ballot).
- Evidence: `docs/evidence/TECHNOLOGY-BASELINE-VERIFICATION.md` §10 (live
  research, 2026-08-27): US Core (the dominant regulatory FHIR baseline)
  remains on R4 and is not planning to move to R5; R5 is independently
  described as having limited real-world adoption; R6 is still in ballot
  (first full ballot dated May 2026), with production-grade adoption not
  expected before late 2027 per HL7's own guidance.
- Decision: FHIR R4/R4B is now the stated production target; R5 is
  transitional/optional (adopted only per specific partner requirement);
  R6 is tracked, not adopted.
- Rationale: Matches the regulatory and ecosystem reality found in fresh
  research rather than an earlier, unverified assumption that R5 was the
  more "current" and therefore preferable choice.
- Consequences: This is a **documentation correction**, not a scope
  change — no domain/workflow document required rewriting beyond the
  `06`/`14` version labels, since the canonical internal clinical model
  (`Clinical` domain, `03`) was never FHIR-native in the first place.
- Security Impact: None identified.
- Operational Impact: None identified at this design stage.
- Compliance Impact: Directly improves alignment with the dominant
  regulatory FHIR baseline (US Core / ONC Cures Act / CMS), reducing
  future integration-conformance risk.
- Revisit Trigger: FHIR R6 reaching final/normative publication.
- Rollback/Exit Strategy: N/A — this is itself the correction of an
  earlier, unverified claim; there is no prior "implementation" to roll
  back.

