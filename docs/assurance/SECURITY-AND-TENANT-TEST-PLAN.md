# Security and Tenant-Isolation Verification Plan

**Status: PROPOSED test plan.** Execute only against systems you own or are explicitly authorized to test. Use synthetic accounts and synthetic/de-identified records.

Track outcomes against the [verification matrix](VERIFICATION-MATRIX.csv); record approved proof in the [evidence register](EVIDENCE-REGISTER.csv), with open issues linked to the [risk register](RISK-REGISTER.csv). Use the [threat-model template](THREAT-MODEL-TEMPLATE.md) for each major trust-boundary change.

## 1. Establish the tested build and threat model

Record commit/build ID, environment, identity provider, database/schema version, enabled flags, tenant count, roles, test accounts, network boundaries, configuration, and tool versions. Draw trust boundaries for browser/mobile clients, API, job workers, integrations, control plane, clinical data plane, database, object storage, messaging, observability, backup, support/admin paths, and vendor systems. Explicitly identify privileged service accounts and emergency/break-glass paths.

## 2. Required negative-test dimensions

For each resource class (patient, encounter, note, prescription, lab result, imaging metadata/object, invoice/claim, consent, attachment, user, organization, audit record), test:

- unauthenticated request;
- authenticated but wrong role;
- correct role but wrong tenant/organization;
- tampered object identifier and parent-child relationship;
- expired/revoked session or token;
- disabled/suspended user and deprovisioned staff;
- direct API access when the UI hides the function;
- bulk/export/search/report endpoints, background jobs, caches, signed URLs, and object storage;
- privilege elevation attempts and expired/reused break-glass grants;
- concurrent permission revocation during a request/job;
- error responses and logs for unintended sensitive data.

Expected result: default deny; minimum information disclosed; consistent server-side checks; no data leakage in response, export, cache, log, tracing, analytics, notification, or asynchronous worker output. Record exact endpoint/resource, actor, tenant, request correlation ID, expected outcome, observed result, evidence file, reviewer, and defect ID. Never include real PHI or usable credentials in evidence.

## 3. Authorization properties to verify

- Authorization is enforced by trusted server-side layers, not merely the UI.
- Tenant identity comes from validated trusted context; client-supplied tenant IDs are not authoritative by themselves.
- Object-level authorization is checked for every read/write/export path, not only at list endpoints.
- Role + relationship + purpose-of-use + consent conditions are enforced where required by the accepted model.
- Database row-level security, if selected, is enabled and tested under real application DB roles; tests must not accidentally run as a superuser or bypass role policies.
- Privileged/control-plane operations are separated from ordinary clinical-data access.
- Break-glass requires a documented reason, narrow scope, time bound, alert/audit trail, and post-event review.
- Service-to-service identities are scoped, rotatable, and not shared unnecessarily.

## 4. Logging, secrets, and crypto checks

- Assert that telemetry excludes patient names, identifiers, clinical note bodies, tokens, passwords, keys, and sensitive request/response payloads unless specifically justified and protected.
- Confirm secret scanning in source, configuration, artifacts, and deployment logs; rotate exposed secrets, do not merely delete them.
- Verify TLS and storage encryption configuration and key access/rotation procedures against the deployed platform.
- Confirm audit records capture actor, action, subject/resource, tenant, timestamp, purpose/context, outcome, and correlation ID as applicable; privileged users cannot silently rewrite history.
- Test access review, key revocation, token expiry, and incident containment paths.

## 5. Adversarial scenarios

| ID | Scenario | Pass condition |
|---|---|---|
| SEC-TEN-01 | Staff from tenant A requests a known patient ID belonging to B | No clinical data returned; security event recorded where appropriate |
| SEC-TEN-02 | Change tenant ID in body/query/header after authenticating to A | Server derives/validates tenant authority and denies cross-tenant access |
| SEC-TEN-03 | Export/search/report endpoint bypasses detail endpoint checks | No cross-tenant records in aggregate, report, export, or pagination |
| SEC-PRIV-01 | Revoked user reuses an old token/session | Access is denied within the agreed revocation window |
| SEC-BG-01 | Break-glass request lacks reason or exceeds scope/expiry | Request denied; accepted event is fully auditable and alerted |
| SEC-LOG-01 | Trigger errors with synthetic sensitive canary strings | Canary does not appear in ordinary logs/traces/metrics |
| SEC-AUD-01 | Attempt audit alteration/deletion through app/service accounts | Unauthorized change is denied or tampering is detected and alerted |
| SEC-API-01 | API accepts an untrusted role/tenant claim from client input | Claim is rejected/ignored in favour of trusted identity/context |
| SEC-JOB-01 | Background job executes after user permission is revoked | Job re-checks applicable authorization or follows approved snapshot semantics |
| SEC-OBJ-01 | Guess/alter object-storage key or reuse signed URL | Access remains scoped, expires as specified, and is auditable where required |

These are test objectives, not assertions about existing ARGON endpoints. Map each scenario to actual APIs/resources only after implementation exists.

## 6. Defect severity and retest

Any confirmed cross-tenant PHI disclosure or uncontrolled privilege escalation is a release stop. Security findings require severity, exploitability, affected scope, evidence, owner, due date, mitigation, retest, and closure reviewer. A scanner-clean report alone is not a penetration test and does not prove absence of vulnerabilities.
