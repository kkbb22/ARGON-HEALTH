# Change Request: Adopt the ARGON Assurance & Verification Kit v1.0

**Status:** PROPOSED — requires approval by the real decision authority. Not self-approved.
**Type:** Process/tooling addition. **Scope impact:** none (no new domain, workflow, or product technology; Architecture Freeze / ACR-1..5 untouched).

## Decision requested
1. Adopt `docs/assurance/` as an assurance layer **subordinate** to `docs/governance/ARGON-SOURCE-OF-TRUTH.md` and approved ADRs.
2. Approve new tooling: one standard-library-only Python script (`scripts/argon_assurance_lint.py`) and, in a later phase, GitHub Actions workflows.

## Conditions before Gate G0 can close
- [ ] Map each of the 67 controls to its authoritative doc/ADR; merge or delete unmapped duplicates (VFY-GOV-001).
- [ ] Resolve naming: kit gates G0–G5 vs existing security gates G-1 / G-7 — rename or document the namespace. **UNKNOWN — REQUIRES EVIDENCE** (not verified against repo).
- [ ] Recalibrate risk tiers: 28 CRITICAL + 35 HIGH of 67 (94%) is not prioritisation; keep CRITICAL for the Plan §6 definition.
- [ ] Name real owners/decision authority (Plan §3).
- [ ] Decide whether the xlsx tracker is kept; the CSVs are the single source, the xlsx is derived.
- [ ] Link ADR-024 (PROPOSED) to the object-storage control as a G1 blocker.

## Phases
- P0 (this change): docs + script + tests only. No CI enabled.
- P1: reconciliation above.
- P2: enable `_deferred-phase-2-ci/` workflows in informational mode; review permissions/branch protection first.
- P3: first real evidence (tenant isolation, authorization, ADR-024).
- P4: enforce gates.

## Truth boundary
A green structural check proves record integrity only. It does not show ARGON is implemented, secure, clinically safe, or compliant. Do not use "compliant/certified/conformant" on the strength of this kit.
