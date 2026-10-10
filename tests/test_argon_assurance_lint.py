import csv
import datetime as dt
import hashlib
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'argon_assurance_lint.py'
spec = importlib.util.spec_from_file_location('argon_assurance_lint', SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)

class AssuranceLintTests(unittest.TestCase):
    def test_starter_pack_registers_are_structurally_valid(self):
        root = SCRIPT.parents[1]
        report = module.validate(root)
        self.assertTrue(report.passed, '\n'.join(report.errors))
        self.assertGreaterEqual(len(report.info), 4)

    def test_duplicate_control_ids_are_rejected(self):
        rows = [{'control_id':'VFY-SEC-001','__line__':'2'}, {'control_id':'VFY-SEC-001','__line__':'3'}]
        report = module.Report()
        module.unique_ids(rows, 'control_id', 'test', report)
        self.assertTrue(any('duplicate' in e for e in report.errors))

    def test_starter_pack_must_not_pass_production_gate(self):
        root = SCRIPT.parents[1]
        report = module.validate(root, 'G4')
        self.assertFalse(report.passed)
        self.assertTrue(any('Gate G4:' in e for e in report.errors))

    def test_evidence_paths_cannot_escape_repository(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            report = module.Report()
            result = module.artifact_path(root, '../outside.txt', report, 'test evidence', required=True)
            self.assertIsNone(result)
            self.assertTrue(any('escapes repository root' in e for e in report.errors))

    def test_accepted_evidence_requires_distinct_creator_and_reviewer(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / 'docs/assurance').mkdir(parents=True)
            (root / 'docs/assurance/evidence.txt').write_text('controlled synthetic evidence', encoding='utf-8')
            def put_csv(rel, headers, rows):
                with (root/rel).open('w', newline='', encoding='utf-8') as f:
                    w=csv.DictWriter(f, fieldnames=headers); w.writeheader(); w.writerows(rows)
            # Use empty but schema-correct risk and signoff registers.
            put_csv(module.MATRIX, module.MATRIX_FIELDS, [{
                'control_id':'VFY-SEC-001','domain':'Security','title':'Example','requirement':'Requirement',
                'verification_method':'Test','acceptance_criteria':'Must pass','risk_tier':'HIGH','required_gate':'G1',
                'owner_role':'Security lead','frequency':'Each change','status':'PASS','evidence_id':'EVD-001','notes':''}])
            put_csv(module.EVIDENCE, module.EVIDENCE_FIELDS, [{
                'evidence_id':'EVD-001','control_id':'VFY-SEC-001','artifact_path':'docs/assurance/evidence.txt',
                'artifact_sha256':__import__('hashlib').sha256(b'controlled synthetic evidence').hexdigest(),'evidence_type':'test','created_by':'Same Person','reviewed_by':'Same Person',
                'approved_by':'Approver','created_utc':'2026-10-10T00:00:00Z','valid_until':'2027-10-10','status':'ACCEPTED','notes':'test'}])
            put_csv(module.RISKS, module.RISK_FIELDS, [])
            put_csv(module.SIGNOFFS, module.SIGNOFF_FIELDS, [])
            put_csv(module.REVALIDATION, module.REVALIDATION_FIELDS, [])
            report = module.validate(root)
            self.assertTrue(any('creator and reviewer must differ' in e for e in report.errors))

# ---------------------------------------------------------------------------
# Synthetic fixtures for the G4/G5 hardening tests (P0).
# Everything below is artificial: no patient data, secrets or production data.
# Column lists are taken from the checker and extended with the P0 binding
# columns, so the same fixtures also run against the pre-fix checker (the extra
# columns are simply ignored there), which is how the bypasses were reproduced.
# ---------------------------------------------------------------------------
TODAY = dt.date(2026, 10, 10)
EVIDENCE_EXTRA = ['release_id', 'environment', 'commit_sha', 'artifact_digest']
SIGNOFF_EXTRA = ['release_artifact_path']
REVALIDATION_EXTRA = ['release_id']

def _cols(base, extra):
    return list(base) + [c for c in extra if c not in base]

def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def _git(root, *args):
    return subprocess.run(['git', '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                           '-c', 'commit.gpgsign=false', *args], cwd=root, check=True,
                          capture_output=True, text=True).stdout.strip()

ROLLBACK_SECTIONS = ['Trigger Conditions', 'Rollback Steps', 'Data and Migration Handling',
                     'Verification After Rollback', 'Owner and Escalation']

def rollback_text(release_id, commit, environment='production', drop=None):
    lines = ['# Rollback plan (synthetic)', '', f'release_id: {release_id}', f'environment: {environment}',
             f'commit_sha: {commit}', '']
    for name in ROLLBACK_SECTIONS:
        if name == drop:
            continue
        lines += [f'## {name}', f'Synthetic content for "{name}".', '']
    return '\n'.join(lines)

class Fixture:
    """A throw-away git repo plus schema-correct assurance registers that pass G4 and G5."""
    RELEASE = 'REL-2026-001'

    def __init__(self, td):
        self.root = Path(td)
        _git(self.root, 'init', '-q')
        (self.root / 'seed.txt').write_text('seed', encoding='utf-8')
        _git(self.root, 'add', '.')
        _git(self.root, 'commit', '-q', '-m', 'first')
        self.other_commit = _git(self.root, 'rev-parse', 'HEAD')
        (self.root / 'seed.txt').write_text('seed 2', encoding='utf-8')
        _git(self.root, 'commit', '-q', '-am', 'second')
        self.commit = _git(self.root, 'rev-parse', 'HEAD')
        self.manifest_rel = f'docs/releases/{self.RELEASE}/release-manifest.json'
        self.rollback_rel = f'docs/releases/{self.RELEASE}/rollback-plan.md'
        self.files = {}
        self.set_manifest()
        self.files[self.rollback_rel] = rollback_text(self.RELEASE, self.commit)
        self.matrix = [self._control('VFY-OPS-003', 'G3', 'HIGH'), self._control('VFY-REL-001', 'G4', 'HIGH'),
                       self._control('VFY-REL-002', 'G4', 'CRITICAL'), self._control('VFY-GOV-009', 'G5', 'HIGH')]
        self.evidence = [self._evidence('EVD-OPS3', 'VFY-OPS-003'), self._evidence('EVD-REL1', 'VFY-REL-001'),
                         self._evidence('EVD-REL2', 'VFY-REL-002'), self._evidence('EVD-RISK', 'VFY-REL-002'),
                         self._evidence('EVD-GOV9', 'VFY-GOV-009', created='2026-10-02T09:00:00Z')]
        self.risks = [{'risk_id': 'RISK-001', 'title': 'Synthetic risk', 'domain': 'Security',
                       'scenario': 'Synthetic', 'impact': 'Synthetic', 'likelihood': 'Low',
                       'inherent_severity': 'CRITICAL', 'mitigation': 'Synthetic', 'owner_role': 'Security lead',
                       'status': 'CLOSED', 'linked_controls': 'VFY-REL-002', 'accepted_by': '', 'expires_on': '',
                       'acceptance_evidence_id': '', 'closure_evidence_id': 'EVD-RISK', 'notes': 'synthetic'}]
        self.signoffs = [{'release_id': self.RELEASE, 'environment': 'production', 'gate': 'G4', 'decision': 'APPROVE',
                          'decision_owner': 'Owner A', 'commit_sha': self.commit, 'artifact_digest': '',
                          'configuration_version': 'cfg-1', 'migration_version': 'mig-1', 'scope': 'synthetic scope',
                          'rollback_plan_path': self.rollback_rel, 'release_artifact_path': self.manifest_rel,
                          'qa_signoff': 'QA B', 'security_signoff': 'Security C', 'clinical_signoff': 'Clinical D',
                          'privacy_legal_signoff': 'Legal E', 'operations_signoff': 'Ops F',
                          'recorded_utc': '2026-09-01T10:00:00Z', 'valid_until': '2027-03-01', 'notes': 'synthetic'}]
        self.reval = [{'period_id': 'P-2026-09B', 'environment': 'production', 'period_start': '2026-09-15',
                       'period_end': '2026-10-01', 'decision': 'CONTINUE', 'operations_reviewer': 'Ops G',
                       'security_reviewer': 'Security H', 'clinical_reviewer': 'Clinical I',
                       'privacy_legal_reviewer': 'Legal J', 'evidence_id': 'EVD-GOV9', 'next_review': '2026-12-01',
                       'notes': 'synthetic', 'release_id': self.RELEASE}]
        self.sync_digest()

    def set_manifest(self, release_id=None, commit=None):
        self.files[self.manifest_rel] = json.dumps({'release_id': release_id or self.RELEASE,
                                                    'commit_sha': commit or self.commit,
                                                    'environment': 'production'}, indent=2)

    def sync_digest(self):
        self.signoffs[0]['artifact_digest'] = _sha(self.files[self.manifest_rel].encode('utf-8'))
        for ev in self.evidence:
            if ev['release_id'] == self.RELEASE:
                ev['artifact_digest'] = self.signoffs[0]['artifact_digest']

    @staticmethod
    def _control(cid, gate, tier):
        return {'control_id': cid, 'domain': 'Synthetic', 'title': cid, 'requirement': 'Synthetic requirement',
                'verification_method': 'Synthetic test', 'acceptance_criteria': 'Synthetic criteria',
                'risk_tier': tier, 'required_gate': gate, 'owner_role': 'Owner', 'frequency': 'Each release',
                'status': 'PASS', 'evidence_id': {'VFY-OPS-003': 'EVD-OPS3', 'VFY-REL-001': 'EVD-REL1',
                                                  'VFY-REL-002': 'EVD-REL2', 'VFY-GOV-009': 'EVD-GOV9'}[cid],
                'notes': ''}

    def _evidence(self, eid, control, created='2026-08-25T09:00:00Z'):
        rel = f'docs/evidence-files/{eid}.txt'
        self.files[rel] = f'synthetic evidence {eid}'
        return {'evidence_id': eid, 'control_id': control, 'artifact_path': rel,
                'artifact_sha256': _sha(self.files[rel].encode('utf-8')), 'evidence_type': 'test',
                'created_by': 'Creator', 'reviewed_by': 'Reviewer', 'approved_by': 'Approver',
                'created_utc': created, 'valid_until': '2027-06-30', 'status': 'ACCEPTED', 'notes': 'synthetic',
                'release_id': self.RELEASE, 'environment': 'production', 'commit_sha': self.commit,
                'artifact_digest': ''}

    def ev(self, eid):
        return next(e for e in self.evidence if e['evidence_id'] == eid)

    def write(self):
        (self.root / 'docs/assurance').mkdir(parents=True, exist_ok=True)
        for rel, text in self.files.items():
            p = self.root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(text.encode('utf-8'))
        # Evidence hashes follow the (possibly mutated) artifact content unless a test pinned a wrong one.
        for path, fields, rows in [
            (module.MATRIX, module.MATRIX_FIELDS, self.matrix),
            (module.EVIDENCE, _cols(module.EVIDENCE_FIELDS, EVIDENCE_EXTRA), self.evidence),
            (module.RISKS, module.RISK_FIELDS, self.risks),
            (module.SIGNOFFS, _cols(module.SIGNOFF_FIELDS, SIGNOFF_EXTRA), self.signoffs),
            (module.REVALIDATION, _cols(module.REVALIDATION_FIELDS, REVALIDATION_EXTRA), self.reval)]:
            with (self.root / path).open('w', newline='', encoding='utf-8') as f:
                w = csv.DictWriter(f, fieldnames=fields)
                w.writeheader()
                w.writerows(rows)

    def validate(self, gate=None):
        self.write()
        return module.validate(self.root, gate, today=TODAY)

def build(td, mutate=None):
    fx = Fixture(td)
    if mutate:
        mutate(fx)
    return fx

class GateHardeningTests(unittest.TestCase):
    def check_fail(self, mutate, gate, reason, subtest=None):
        """The mutation must make `gate` fail, for the stated reason (and the unmutated fixture must pass)."""
        with tempfile.TemporaryDirectory() as td:
            base = build(td)
            self.assertTrue(base.validate(gate).passed, 'baseline fixture must pass')
        with tempfile.TemporaryDirectory() as td:
            fx = build(td, mutate)
            report = fx.validate(gate)
            self.assertFalse(report.passed, f'{gate} wrongly passed; expected failure containing {reason!r}')
            self.assertTrue(any(reason in e for e in report.errors),
                            f'expected an error containing {reason!r}, got:\n' + '\n'.join(report.errors))

    # ----- positive cases (the hardening must not reject everything) -----
    def test_positive_structural_g4_and_g5_pass_on_complete_synthetic_data(self):
        with tempfile.TemporaryDirectory() as td:
            fx = build(td)
            for gate in (None, 'G4', 'G5'):
                report = fx.validate(gate)
                self.assertTrue(report.passed, f'{gate}: ' + '\n'.join(report.errors))

    def test_positive_g5_requires_g4_first_and_g4_pass_does_not_imply_g5(self):
        with tempfile.TemporaryDirectory() as td:
            fx = build(td)
            fx.reval = []
            self.assertTrue(fx.validate('G4').passed)
            r5 = fx.validate('G5')
            self.assertFalse(r5.passed)
            self.assertTrue(any('Gate G5' in e for e in r5.errors))

    # ----- A. G4 -----
    def test_g4_rejects_malformed_commit_sha(self):
        for bad in ['abc123', 'z' * 40, 'a' * 39, 'a' * 41, 'HEAD', self.sha_with_suffix()]:
            with self.subTest(bad=bad):
                self.check_fail(lambda fx, b=bad: fx.signoffs[0].update(commit_sha=b), 'G4',
                                'commit_sha must be a full 40- or 64-character hexadecimal')

    @staticmethod
    def sha_with_suffix():
        return 'a' * 40 + ' extra'

    def test_g4_rejects_well_formed_sha_that_is_not_a_repository_commit(self):
        self.check_fail(lambda fx: fx.signoffs[0].update(commit_sha='ab' * 20), 'G4',
                        'commit_sha does not resolve to a commit')

    def test_g4_rejects_malformed_artifact_digest(self):
        for bad in ['xyz', 'a' * 63, 'a' * 65, 'sha256:' + 'a' * 64, 'g' * 64]:
            with self.subTest(bad=bad):
                self.check_fail(lambda fx, b=bad: fx.signoffs[0].update(artifact_digest=b), 'G4',
                                'artifact_digest must be exactly 64 hexadecimal')

    def test_g4_rejects_digest_that_does_not_match_real_release_artifact(self):
        self.check_fail(lambda fx: fx.signoffs[0].update(artifact_digest='0' * 64), 'G4',
                        'does not match the SHA-256 of release_artifact_path')

        def tamper(fx):
            fx.files[fx.manifest_rel] = fx.files[fx.manifest_rel] + '\n'   # digest was computed before this edit
        self.check_fail(tamper, 'G4', 'does not match the SHA-256 of release_artifact_path')

    def test_g4_requires_a_release_artifact_path(self):
        self.check_fail(lambda fx: fx.signoffs[0].update(release_artifact_path=''), 'G4',
                        'release_artifact_path is required')

    def test_g4_rejects_digest_of_an_unrelated_file(self):
        def unrelated(fx):
            fx.files['docs/unrelated.txt'] = 'any file at all'
            fx.signoffs[0].update(release_artifact_path='docs/unrelated.txt',
                                  artifact_digest=_sha(b'any file at all'))
        self.check_fail(unrelated, 'G4', 'release manifest')

        def other_release_manifest(fx):
            fx.set_manifest(release_id='REL-OTHER')
            fx.sync_digest()
        self.check_fail(other_release_manifest, 'G4', 'release manifest')

        def other_commit_manifest(fx):
            fx.set_manifest(commit=fx.other_commit)
            fx.sync_digest()
        self.check_fail(other_commit_manifest, 'G4', 'release manifest')

    def test_g4_rejects_generic_or_unstructured_rollback_plan(self):
        def generic(fx):
            fx.files['docs/governance/generic-policy.md'] = '# Rollback policy\n\nRoll back when things go wrong.\n'
            fx.signoffs[0].update(rollback_plan_path='docs/governance/generic-policy.md')
        self.check_fail(generic, 'G4', 'rollback plan')

        def any_existing_file(fx):
            fx.signoffs[0].update(rollback_plan_path='seed.txt')
        self.check_fail(any_existing_file, 'G4', 'rollback plan')

        for section in ROLLBACK_SECTIONS:
            with self.subTest(missing=section):
                def drop(fx, s=section):
                    fx.files[fx.rollback_rel] = rollback_text(fx.RELEASE, fx.commit, drop=s)
                self.check_fail(drop, 'G4', 'missing required section')

        def placeholder(fx):
            fx.files[fx.rollback_rel] = rollback_text(fx.RELEASE, fx.commit).replace(
                'Synthetic content for "Rollback Steps".', 'TBD')
        self.check_fail(placeholder, 'G4', 'placeholder')

    def test_g4_rejects_rollback_plan_for_another_release_or_commit(self):
        def other_release(fx):
            fx.files[fx.rollback_rel] = rollback_text('REL-OTHER', fx.commit)
        self.check_fail(other_release, 'G4', 'rollback plan')

        def other_commit(fx):
            fx.files[fx.rollback_rel] = rollback_text(fx.RELEASE, fx.other_commit)
        self.check_fail(other_commit, 'G4', 'rollback plan')

    def test_g4_rejects_valid_hash_evidence_that_is_not_bound_to_this_release(self):
        cases = {
            'release_id': ('REL-OTHER', 'is not bound to release'),
            'environment': ('staging', 'is not bound to environment'),
            'commit_sha': (None, 'is not bound to commit'),
            'artifact_digest': ('f' * 64, 'is not bound to artifact_digest'),
        }
        for field, (value, reason) in cases.items():
            with self.subTest(field=field):
                def mutate(fx, f=field, v=value):
                    fx.ev('EVD-REL1')[f] = v if v is not None else fx.other_commit
                self.check_fail(mutate, 'G4', reason)

    def test_g4_rejects_evidence_with_missing_release_binding(self):
        def unbound(fx):
            for f in EVIDENCE_EXTRA:
                fx.ev('EVD-REL2')[f] = ''
        self.check_fail(unbound, 'G4', 'lacks release binding')

    def test_g4_rollback_drill_needs_accepted_release_bound_evidence(self):
        # A rollback plan file alone never proves a drill: VFY-OPS-003 must carry accepted, bound evidence.
        def no_drill(fx):
            fx.matrix[0].update(status='NOT_RUN', evidence_id='')
        self.check_fail(no_drill, 'G4', 'VFY-OPS-003')

        def drill_for_other_release(fx):
            fx.ev('EVD-OPS3')['release_id'] = 'REL-OTHER'
        self.check_fail(drill_for_other_release, 'G4', 'is not bound to release')

        def drill_not_accepted(fx):
            fx.ev('EVD-OPS3')['status'] = 'REVIEWED'
        self.check_fail(drill_not_accepted, 'G4', 'requires ACCEPTED evidence')

    def test_g4_rejects_evidence_for_a_different_control(self):
        def wrong_control(fx):
            fx.matrix[1]['evidence_id'] = 'EVD-REL2'   # evidence belongs to VFY-REL-002, not VFY-REL-001
        self.check_fail(wrong_control, 'G4', 'belongs to control')

    def test_g4_rejects_expired_evidence_and_evidence_created_after_approval(self):
        self.check_fail(lambda fx: fx.ev('EVD-REL1').update(valid_until='2026-10-09'), 'G4', 'evidence expired')
        self.check_fail(lambda fx: fx.ev('EVD-REL1').update(created_utc='2026-09-02T00:00:00Z'), 'G4',
                        'created after the approval was recorded')
        self.check_fail(lambda fx: fx.ev('EVD-REL1').update(valid_until='2026-08-31'), 'G4',
                        'not valid at the time the approval was recorded')

    def test_g4_keeps_independent_signoff_requirements_and_expiry(self):
        self.check_fail(lambda fx: fx.signoffs[0].update(qa_signoff='Owner A'), 'G4', 'distinct')
        self.check_fail(lambda fx: fx.signoffs[0].update(clinical_signoff=''), 'G4', 'missing')
        self.check_fail(lambda fx: fx.signoffs[0].update(valid_until='2026-10-09'), 'G4', 'expired')
        self.check_fail(lambda fx: fx.signoffs[0].update(valid_until='2027-03-01T00:00:00Z'), 'G4', 'invalid valid_until')
        self.check_fail(lambda fx: fx.signoffs[0].update(recorded_utc='2026-11-01T00:00:00Z'), 'G4',
                        'recorded_utc is in the future')

    # ----- B. G5 -----
    def test_g5_requires_prior_g4_production_approval_for_the_same_release(self):
        self.check_fail(lambda fx: fx.signoffs.clear(), 'G5', 'no valid production G4 approval')
        self.check_fail(lambda fx: fx.reval[0].update(release_id='REL-OTHER'), 'G5',
                        'no valid production G4 approval')
        self.check_fail(lambda fx: fx.signoffs[0].update(environment='staging'), 'G5',
                        'no valid production G4 approval')
        self.check_fail(lambda fx: fx.signoffs[0].update(decision='REJECT'), 'G5',
                        'no valid production G4 approval')

    def test_g5_g4_approval_must_precede_and_cover_the_period_start(self):
        self.check_fail(lambda fx: fx.signoffs[0].update(recorded_utc='2026-09-20T00:00:00Z'), 'G5',
                        'recorded after period_start')
        self.check_fail(lambda fx: fx.signoffs[0].update(valid_until='2026-09-10'), 'G5',
                        'not valid at period_start')

    def test_g5_ignores_nonconforming_g4_rows_instead_of_trusting_them(self):
        self.check_fail(lambda fx: fx.signoffs[0].update(commit_sha='abc'), 'G5',
                        'commit_sha must be a full 40- or 64-character hexadecimal')

    def test_g5_rejects_invalid_dates(self):
        for field in ('period_start', 'period_end', 'next_review'):
            for bad in ['2026-9-15', '2026-09-15T00:00:00Z', '20260915', '2026-02-30', '2026-09-15 extra', 'soon']:
                with self.subTest(field=field, bad=bad):
                    self.check_fail(lambda fx, f=field, b=bad: fx.reval[0].update({f: b}), 'G5',
                                    f'{field} must be YYYY-MM-DD')

    def test_g5_rejects_inverted_or_future_period_and_bad_next_review(self):
        self.check_fail(lambda fx: fx.reval[0].update(period_start='2026-10-05', period_end='2026-10-01'), 'G5',
                        'period_start is after period_end')
        self.check_fail(lambda fx: fx.reval[0].update(period_end='2026-10-11'), 'G5', 'period_end is in the future')
        self.check_fail(lambda fx: fx.reval[0].update(next_review='2026-09-30'), 'G5',
                        'next_review must be after period_end')
        self.check_fail(lambda fx: fx.reval[0].update(next_review='2026-10-09', period_end='2026-10-01'), 'G5',
                        'next_review is in the past')

    def test_g5_evidence_must_match_release_environment_and_a_g5_control(self):
        self.check_fail(lambda fx: fx.ev('EVD-GOV9').update(release_id='REL-OTHER'), 'G5', 'is not bound to release')
        self.check_fail(lambda fx: fx.ev('EVD-GOV9').update(environment='staging'), 'G5', 'is not bound to environment')
        self.check_fail(lambda fx: fx.ev('EVD-GOV9').update(commit_sha='ab' * 20), 'G5', 'is not bound to commit')
        self.check_fail(lambda fx: fx.ev('EVD-GOV9').update(control_id='VFY-REL-001'), 'G5', 'is not a G5 control')
        self.check_fail(lambda fx: fx.ev('EVD-GOV9').update(created_utc='2026-09-01T00:00:00Z'), 'G5',
                        'created before period_start')
        self.check_fail(lambda fx: fx.ev('EVD-GOV9').update(valid_until='2026-10-01'), 'G5', 'evidence expired')

    def test_g5_still_requires_independent_reviewers(self):
        self.check_fail(lambda fx: fx.reval[0].update(security_reviewer='Ops G'), 'G5', 'independent')

    # ----- C. risk register / evidence integrity -----
    def test_empty_risk_register_is_rejected_even_without_a_gate(self):
        with tempfile.TemporaryDirectory() as td:
            fx = build(td, lambda f: f.risks.clear())
            report = fx.validate()
            self.assertFalse(report.passed)
            self.assertTrue(any('risk register is empty' in e for e in report.errors))

    def test_risk_closure_evidence_must_be_linked_to_that_risk(self):
        def unrelated(fx):
            fx.risks[0]['closure_evidence_id'] = 'EVD-OPS3'    # ACCEPTED, but about VFY-OPS-003
        self.check_fail(unrelated, 'G4', 'not linked to the risk')

        def no_linked_controls(fx):
            fx.risks[0]['linked_controls'] = ''
        self.check_fail(no_linked_controls, 'G4', 'requires linked_controls')

    def test_risk_closure_evidence_must_be_current(self):
        self.check_fail(lambda fx: fx.ev('EVD-RISK').update(valid_until='2026-10-01'), 'G4', 'evidence expired')
        self.check_fail(lambda fx: fx.ev('EVD-RISK').update(status='REVIEWED'), 'G4',
                        'CLOSED risk requires closure_evidence_id linked to ACCEPTED evidence')

    def test_accepted_risk_needs_valid_acceptance_evidence_and_strict_dates(self):
        def accepted(fx):
            fx.risks[0].update(inherent_severity='HIGH', status='ACCEPTED', accepted_by='Owner K',
                               acceptance_evidence_id='EVD-RISK', expires_on='2027-01-01', closure_evidence_id='')
        with tempfile.TemporaryDirectory() as td:
            self.assertTrue(build(td, accepted).validate('G4').passed)
        self.check_fail(lambda fx: (accepted(fx), fx.risks[0].update(expires_on='2027-01-01xyz')), 'G4',
                        'expires_on in YYYY-MM-DD form')
        self.check_fail(lambda fx: (accepted(fx), fx.risks[0].update(expires_on='2026-10-09')), 'G4',
                        'accepted risk expired')
        self.check_fail(lambda fx: (accepted(fx), fx.risks[0].update(acceptance_evidence_id='EVD-OPS3')), 'G4',
                        'not linked to the risk')

    def test_dates_must_be_full_iso_dates_not_a_prefix_of_longer_text(self):
        self.assertIsNone(module.date_value('2026-10-10T12:00:00Z'))
        self.assertIsNone(module.date_value('2026-10-10 extra'))
        self.assertIsNone(module.date_value('2026-1-1'))
        self.assertEqual(module.date_value('2026-10-10'), dt.date(2026, 10, 10))
        self.check_fail(lambda fx: fx.ev('EVD-REL1').update(valid_until='2027-06-30T00:00:00Z'), None,
                        'valid_until must be YYYY-MM-DD')

    # ----- scope honesty / starter pack -----
    def test_starter_pack_still_fails_every_readiness_gate_it_is_asked_about(self):
        root = SCRIPT.parents[1]
        for gate in ('G4', 'G5'):
            report = module.validate(root, gate)
            self.assertFalse(report.passed, gate)
            self.assertTrue(any(f'Gate {gate}:' in e for e in report.errors), gate)

    def test_structural_pass_is_never_presented_as_product_verification(self):
        report = module.validate(SCRIPT.parents[1])
        self.assertTrue(report.passed)
        self.assertTrue(any('does NOT prove the product' in w for w in report.warnings))
        self.assertIn('not verification of the ARGON product', report.as_dict()['scope_warning'])
        with tempfile.TemporaryDirectory() as td:
            g4 = build(td).validate('G4')
            self.assertTrue(any('applies only to the recorded scope' in m for m in g4.info))
            self.assertTrue(any('rollback' in m and 'does not prove' in m for m in g4.info))


if __name__ == '__main__':
    unittest.main()
