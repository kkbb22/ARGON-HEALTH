# ARGON Threat Model — Template

**State:** NOT REVIEWED until completed and approved. Never populate with patient-identifying data, secrets, tokens, or live credentials.

Map each threat and abuse case to the [verification matrix](VERIFICATION-MATRIX.csv) and record accepted test artifacts in the [evidence register](EVIDENCE-REGISTER.csv).

## Metadata

- System/subsystem:
- Revision/commit/environment:
- Owner and reviewers:
- Date / next review / trigger:
- Intended uses and out-of-scope uses:
- Data classes and jurisdictions:
- Relevant ADRs and verification controls:

## Assets and security objectives

| Asset | Confidentiality objective | Integrity objective | Availability objective | Owner |
|---|---|---|---|---|
| Patient/clinical data | | | | |
| Identity/session/authorization | | | | |
| Audit and evidence records | | | | |
| Financial/claims data | | | | |
| Integration credentials/messages | | | | |
| Backups/object storage | | | | |

## Data flows and trust boundaries

Attach/update diagrams. Include client, API, identity, service, database, object store, async workers/queues, integrations, analytics/telemetry, admin/control plane, backup, support, and third-party processors as applicable. Mark trust boundary crossing, identities, data classes, encryption, authorization decision point, and failure modes.

## Threat list

| Threat ID | Actor/capability | Entry point | Threat/event | Impact | Existing control | Verification evidence | Residual risk/owner |
|---|---|---|---|---|---|---|---|
| TM-001 | | | | | | | |

Consider spoofing, tampering, repudiation, information disclosure, denial of service, and elevation of privilege; also insider misuse, compromised vendor credentials, malicious/defective dependency, configuration drift, backup theft, tenant confusion, and AI/tool misuse if AI features exist.

## Abuse cases and negative tests

For each material threat, give a reproducible test case, safe test data, expected deny/fail-safe outcome, evidence path, and retest trigger. Map results to the verification matrix. Do not write only generic statements such as “use RBAC”.

## Decisions and acceptance

- Unmitigated critical/high threats:
- Compensating controls and limitations:
- Risk acceptor (if allowed), expiry, and monitoring:
- Security review decision:
- Required actions / owner / deadline:
- Re-review triggers:
