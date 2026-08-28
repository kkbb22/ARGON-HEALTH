# ADR-017 — Infrastructure as Code: OpenTofu (replacing Terraform)

**STATUS:** PROPOSED — not yet independently reviewed/accepted
**EVIDENCE CLASS:** DESIGN (decision), backed by EXTERNAL RESEARCH (see Evidence link below)

> Promoted out of `docs/master/19-MASTER-ARCHITECTURAL-DECISIONS.md` during the
> repository normalization pass. `19` now carries only the short index
> entry; this file is the canonical full text.

**ADR-017 — Infrastructure as Code: OpenTofu (replacing Terraform)**
- Status: **PROPOSED**
- Date: 2026-08-27
- Context: `13`/`14`'s original target named Terraform. The Architecture
  Normalization task explicitly listed "Terraform vs OpenTofu" as a
  drift category to verify with fresh evidence.
- Problem: Which IaC tool should the platform standardize on, given
  Terraform's 2023 relicensing to BSL 1.1 and IBM's 2024 acquisition of
  HashiCorp?
- Options: Terraform (BSL 1.1, IBM-owned), OpenTofu (MPL 2.0, Linux
  Foundation-governed fork).
- Evidence: `docs/evidence/TECHNOLOGY-BASELINE-VERIFICATION.md` §6 (live
  research, 2026-08-27).
- Decision: OpenTofu adopted as the IaC baseline.
- Rationale: OSI-approved MPL 2.0 licensing reduces legal-review friction
  for a healthcare platform expecting ongoing compliance/legal review
  (`08`); native state/plan encryption is a concrete security
  improvement over Terraform's open CLI; HCL syntax and provider
  ecosystem are near-identical, keeping migration risk low; no
  Terraform-exclusive feature (e.g., HCP Terraform Stacks) is required
  by anything in this architecture today.
- Consequences: `13`'s Infrastructure Diagram section and `14`'s
  Observability & Infrastructure table both updated; Terraform state
  language throughout `13`/`17` updated to OpenTofu state.
- Security Impact: Native state encryption directly strengthens the
  Terraform-state DR/security posture already tracked in `17`.
- Operational Impact: Near-zero — CLI and workflow are effectively a
  binary swap (`terraform` → `tofu`).
- Compliance Impact: Improves license-review posture for regulated
  jurisdictions (`08`).
- Revisit Trigger: A specific need for an HCP-Terraform-exclusive
  capability, or evidence of GCP-provider compatibility regression in
  OpenTofu.
- Rollback/Exit Strategy: Both tools read the same state format as of
  this writing; a "dual-engine" fallback (Terraform CLI against the same
  state) remains available without a state migration if ever needed.

