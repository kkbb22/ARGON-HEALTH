import csv
import importlib.util
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

if __name__ == '__main__':
    unittest.main()
