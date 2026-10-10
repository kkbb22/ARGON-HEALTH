# Operations, Performance, Backup, and Resilience Assurance

**Status: PROPOSED.** Targets are hypotheses until approved by business owners and demonstrated in measured tests.

Map resilience objectives to the [verification matrix](VERIFICATION-MATRIX.csv), store drill outputs in the [evidence register](EVIDENCE-REGISTER.csv), and use the [release gate checklist](RELEASE-GATES.md) before a production transition.

## 1. Make service objectives explicit

For each critical user journey, define SLI/SLO, measurement window, availability and latency thresholds, excluded conditions, error-budget policy, alert owner, and customer/patient impact. Do not use one global uptime target to hide failures in login, patient lookup, result delivery, prescribing, billing, or audit logging.

Approve business-derived RTO (maximum tolerable service restoration time) and RPO (maximum tolerable data-loss window) per data/workflow tier. Record rationale and owner. Do not copy arbitrary values from the architecture and present them as measured.

## 2. Mandatory tests

- baseline, expected peak, burst, stress, and soak/load tests using representative synthetic data;
- database saturation, connection-pool exhaustion, slow queries, lock contention, queue backlog, storage exhaustion, and rate-limit behaviour;
- dependency timeouts, retries, circuit breakers, partial failures, duplicate delivery, and recovery after dependencies return;
- process/node/region failure to the extent the deployed design claims to tolerate it;
- backup integrity, point-in-time recovery if promised, full restore into an isolated environment, record-count/integrity reconciliation, and measured restoration time;
- data migration rehearsal on a production-like copy with rollback/roll-forward procedure and reconciliation;
- failed release rollback, configuration rollback, secret/key rotation, credential revocation, and disaster-recovery exercise;
- audit/monitoring continuity during partial outage and protection against PHI leaking into telemetry.

## 3. Evidence format

Every drill/test records: release/commit; environment topology; test-data volume/profile; workload generator and version; duration; start/end UTC; SLI results; errors; resource saturation; deviations from production; recovery steps; actual RTO/RPO; data reconciliation; screenshots/logs/results with secrets/PHI removed; reviewer; and remediation tickets.

## 4. Resilience acceptance

Pass criteria must be approved before the test run. Do not change thresholds after seeing results without recording a revised test decision and rerun. A restore is successful only when data and application workflows are usable and integrity checks pass, not merely when a backup job reports success.

## 5. Operational readiness

Before production, identify on-call ownership, severity definitions, escalation tree, incident commander, clinical-safety escalation for patient-impacting incidents, privacy/security breach process, customer communication owner, status-page/communications approach if used, and post-incident review deadlines. Maintain concise, tested runbooks for the most likely high-impact incidents.
