# ARGON HEALTH — Assurance & Verification Kit

**Purpose:** a repository-ready assurance layer for the ARGON target architecture. It connects requirements, risks, verification methods, evidence, independent review, and release authorization.

> **Critical truth boundary:** this kit does not make ARGON implemented, secure, clinically safe, legally compliant, or production-ready. The public ARGON-HEALTH repository describes a proposed target architecture and says it contains architecture/planning artifacts, not application code or deployed infrastructure. This kit is a set of controls to be adopted and then populated with real evidence.

## What is included

- `docs/assurance/ARGON-ASSURANCE-MASTER-PLAN.md` — operating model and assurance lifecycle.
- `docs/assurance/VERIFICATION-MATRIX.csv` — 67 control objectives across governance, architecture, appsec, tenancy, privacy, clinical safety, data, integrations, testing, operations, and releases.
- `docs/assurance/RISK-REGISTER.csv` — initial risk hypotheses to validate; not a claim that these are confirmed defects.
- `docs/assurance/EVIDENCE-REGISTER.csv` — evidence inventory. It starts empty on purpose.
- `docs/assurance/RELEASE-SIGNOFF.csv` — release sign-offs tied to the exact commit, artifact digest, config, migration and rollback plan. It starts empty on purpose.
- `docs/assurance/OPERATIONAL-REVALIDATION.csv` — recurring production continuation reviews; it starts empty on purpose.
- `docs/assurance/ACCEPTANCE-TEST-CATALOG.csv` — 20 high-value cross-system acceptance scenarios.
- Focused playbooks for security/tenant isolation, clinical/data safety, resilience, release gates, and threat modelling.
- `scripts/argon_assurance_lint.py` — standard-library-only CSV integrity, evidence integrity, and fail-closed release-gate checker.
- `tests/` — tests of the checker, not tests of the ARGON product.
- `.github/workflows/` — continuous assurance-pack checks and a manual release-readiness gate.
- `.github/pull_request_template.md` and issue template — evidence-first change review and defect intake.
- `SECURITY.md` — private vulnerability reporting starter policy.

## Install into ARGON-HEALTH

Copy these paths into a clean clone of `kkbb22/ARGON-HEALTH`, preserving existing files. This kit does **not** replace `docs/governance/ARGON-SOURCE-OF-TRUTH.md`, the existing architecture status board, clinical safety model, compliance matrix, or ADR governance. Where a conflict appears, resolve it through the existing source-of-truth/ADR process instead of silently choosing this kit.

Linux/macOS from the extracted kit directory:

```bash
cp -n README.md /path/to/ARGON-HEALTH/ARGON-ASSURANCE-KIT-README.md
mkdir -p /path/to/ARGON-HEALTH/docs/assurance /path/to/ARGON-HEALTH/scripts /path/to/ARGON-HEALTH/tests /path/to/ARGON-HEALTH/.github/workflows /path/to/ARGON-HEALTH/.github/ISSUE_TEMPLATE
cp -n docs/assurance/* /path/to/ARGON-HEALTH/docs/assurance/
cp -n scripts/argon_assurance_lint.py /path/to/ARGON-HEALTH/scripts/
cp -n tests/test_argon_assurance_lint.py /path/to/ARGON-HEALTH/tests/
# Merge these into existing .github files; do not overwrite current workflows.
cp -n .github/pull_request_template.md /path/to/ARGON-HEALTH/.github/
cp -n .github/workflows/argon-assurance.yml /path/to/ARGON-HEALTH/.github/workflows/
cp -n .github/workflows/argon-release-gate.yml /path/to/ARGON-HEALTH/.github/workflows/
mkdir -p /path/to/ARGON-HEALTH/.github/ISSUE_TEMPLATE
cp -n .github/ISSUE_TEMPLATE/assurance-defect.yml /path/to/ARGON-HEALTH/.github/ISSUE_TEMPLATE/
cp -n SECURITY.md /path/to/ARGON-HEALTH/
cd /path/to/ARGON-HEALTH
python3 scripts/argon_assurance_lint.py --root .
python3 -m unittest discover -s tests -v
```

If `.github/workflows/` or `tests/` already exist, **merge** their contents; do not overwrite existing project workflows or tests. Review every workflow's permissions and branch protections before enabling it.

PowerShell users can copy the same folders using `Copy-Item` with `-Recurse`; merge pre-existing `.github` files manually.

## Run checks

Structural/integrity check (does not claim the product passes):

```bash
python scripts/argon_assurance_lint.py --root .
```

Generate JSON output:

```bash
python scripts/argon_assurance_lint.py --root . --json-out /tmp/argon-assurance-report.json
```

Evaluate a readiness gate (expected to FAIL until real records/evidence/reviews are supplied):

```bash
python scripts/argon_assurance_lint.py --root . --gate G1
python scripts/argon_assurance_lint.py --root . --gate G4
```

`G4` is the proposed production-release gate and requires controls due through G4 to be complete, evidence to be accepted, critical risks to be closed and high risks closed or explicitly accepted under a time-bounded policy, and a complete production sign-off record. A green **structural** check is not a green product assurance result.

## First actions after installing

1. Name the actual decision authority and owners for security, clinical safety, privacy/legal, quality, and operations.
2. Reconcile each control against existing ARGON docs; merge duplicates and add exact links to authoritative requirements.
3. Mark controls `IN_PROGRESS` only when work is actually underway. Do not mark `PASS` until evidence is recorded and reviewed.
4. Start with tenant isolation and authorization, then clinical data integrity, auditability, backup/restore, and one end-to-end workflow.
5. Do not enter production with open critical risks or missing legal/clinical review where applicable.

## Standards are references, not badges

Use current versions of relevant guidance as references (e.g., OWASP ASVS for application-security verification, NIST SSDF for secure development, and medical-device lifecycle/risk standards only if the intended use/classification makes them applicable). Confirm version, scope, licensing, applicability, and legal interpretation with the responsible specialists. Do not write “compliant”, “certified”, or “conformant” based on a checklist alone.
