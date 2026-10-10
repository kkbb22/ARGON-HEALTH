# G4 / G5 Gate Rules (P0 hardening of the checker)

**Status: PROPOSED.** Same status as ADR-025 and [the release gates](RELEASE-GATES.md); nothing here is binding until adopted through the ARGON decision process.

These rules describe what `scripts/argon_assurance_lint.py` enforces for gates G4 and G5. They tighten how the registers are checked; they do not change the target architecture, scope, workflows or data ownership. A passing run is a statement about the **register bookkeeping for the recorded release and period only**. It is not verification of the ARGON product and does not prove that a rollback, restore or recovery actually worked.

## Register columns added (backward compatible)

Older registers without these columns still load. The structural check passes, and G4/G5 fail closed because the values are empty.

| Register | New column | Meaning |
|---|---|---|
| `RELEASE-SIGNOFF.csv` | `release_artifact_path` | Repository-relative release manifest (JSON). `artifact_digest` must be the SHA-256 of exactly this file. |
| `EVIDENCE-REGISTER.csv` | `release_id`, `environment`, `commit_sha`, `artifact_digest` | The release the evidence was produced for. Required for the evidence listed under "Release-bound evidence". |
| `OPERATIONAL-REVALIDATION.csv` | `release_id` | The release whose production operation is being revalidated. |

## G4 — Production authorization

A production `APPROVE` row passes only if all of the following hold:

1. **`commit_sha`** is a full 40-character (or 64-character, SHA-256 repositories) hexadecimal id, and `git rev-parse --verify <sha>^{commit}` resolves it to a commit in the repository being checked. Abbreviations and free text are rejected. A shallow clone or missing `git` fails closed.
2. **`artifact_digest`** is exactly 64 hexadecimal characters (no `sha256:` prefix).
3. **`release_artifact_path`** names a file whose SHA-256 equals `artifact_digest`, and that file is a JSON release manifest declaring `release_id` and `commit_sha` equal to the sign-off row (and `environment`, if present). A digest of an unrelated file is rejected.
4. **`rollback_plan_path`** is a dedicated Markdown file for this release (see the structure below). A generic policy file, or any file that merely exists, is rejected.
5. **Release-bound evidence:** see below.
6. All sign-off columns are filled, `recorded_utc` is a timezone-aware ISO-8601 timestamp that is not in the future, `valid_until` is a real `YYYY-MM-DD` date that has not passed, and the decision owner and the five signers are distinct (unchanged conservative default).
7. The existing gate rules still apply: every control due by G4 has `ACCEPTED` evidence (or an approved N/A / non-critical accepted risk), no open Critical risk, and High risks are closed or validly accepted.

### Rollback plan structure

The file must contain these header lines (each on its own line) matching the sign-off row, and these level-2 headings, each with real content (empty or `TBD`/`TODO`/`UNKNOWN`/`N/A` bodies are rejected):

```markdown
release_id: <release_id>
environment: production
commit_sha: <full commit sha>

## Trigger Conditions
## Rollback Steps
## Data and Migration Handling
## Verification After Rollback
## Owner and Escalation
```

**Checking this file proves only that a dedicated, structured plan exists.** That the rollback works is shown by `VFY-OPS-003` (rollback/forward-fix drill), which G4 requires to be `ACCEPTED` and release-bound.

### Release-bound evidence

For every control with `required_gate = G4`, plus `VFY-OPS-003`, the linked evidence record must have `release_id`, `environment`, `commit_sha` and `artifact_digest` equal to the approved sign-off. At G4 it must also have been created no later than `recorded_utc` and be valid on that date (approvers cannot have relied on evidence that did not exist yet). Evidence expiry is checked at every gate.

## G5 — Operational revalidation

G5 is a continuing operational gate. It requires, and never replaces, the original G4 approval.

A `CONTINUE` row for `environment=production` passes only if:

1. **A prior G4 production approval exists for the same `release_id`**, fully valid under the G4 rules above, recorded on or before `period_start`, and with `valid_until` on or after `period_start` (historical validity; it need not still be unexpired today).
2. `period_start`, `period_end` and `next_review` are real `YYYY-MM-DD` dates. Trailing text, timestamps, and non-dates are rejected.
3. `period_start` is not after `period_end`; `period_end` is not in the future; `next_review` is after `period_end` and not in the past.
4. The linked evidence is `ACCEPTED`, unexpired, belongs to a control whose `required_gate` is `G5`, is bound to the same release, environment, commit and artifact digest, and was created on or after `period_start`.
5. The four reviewers are independent (unchanged conservative default).
6. The G4-due controls' evidence is still bound to the approved release.

## Risk and evidence integrity

- An empty risk register is rejected. (Retiring baseline risks needs an explicit governance decision; deleting them is not one.)
- A `CLOSED` risk needs `linked_controls`, and its closure evidence must be `ACCEPTED`, unexpired, and about one of those controls. An `ACCEPTED` risk's acceptance evidence follows the same rule.
- All dates use the full `YYYY-MM-DD` form; text is never truncated to ten characters to make it parse.
- Existing protections stay: duplicate-id rejection, repository-relative evidence paths, SHA-256 mismatch detection, distinct creator/reviewer.

## Choosing a release

By default every production approval (G4) or continuation row (G5) in the registers must hold. With several releases recorded, pass `--release-id <id>` to evaluate one candidate.

## Not decided by the existing documents (kept UNKNOWN)

The P0 checker applies the conservative defaults above where the documents are silent. These remain **open policy questions for the project owner**:

1. Whether evidence for controls due **before** G4 (G0–G3, other than `VFY-OPS-003`) must also be release-bound.
2. What happens when a G4 approval expires **during** a G5 period (only validity at `period_start` is checked).
3. A maximum period length or required revalidation cadence (none is enforced).
4. Revocation or supersession of an approval (e.g. a later `REJECT` row) — not modelled.
5. How the release manifest is produced and signed in CI, and whether a container-image digest must be recorded in it.
6. A frozen baseline of risk and control ids, so that deleting **individual** rows is detectable (only the fully empty risk register is rejected today).
7. Whether the "evidence created before approval" and "G5 evidence created on or after `period_start`" rules match the intended evidence lifecycle.
