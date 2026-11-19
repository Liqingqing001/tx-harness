import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("check_office", ROOT / "scripts/check_office.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class OfficeChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.out = Path(self.temp.name)
    def tearDown(self):
        self.temp.cleanup()
    def write(self, name, text):
        (self.out / name).write_text(text, encoding="utf-8")
    def statuses(self, task, number=1):
        return {c["id"]: c["status"] for c in module.check(task, self.out, number)["checks"]}
    def valid_t03(self):
        for name in ("people", "stock"):
            shutil.copyfile(ROOT / "cases/T03/inputs" / (name + ".csv"), self.out / (name + "-copy.csv"))
        self.write("manifest.csv", "filename,source\nstock-copy.csv,stock.csv\npeople-copy.csv,people.csv\n")
    def test_copy_exact_and_manifest_unordered(self):
        self.valid_t03()
        self.assertEqual(set(self.statuses("T03").values()), {"pass"})
    def test_normalizing_copy_bytes_fails_even_if_csv_values_equal(self):
        self.valid_t03()
        p = self.out / "stock-copy.csv"
        p.write_bytes(p.read_bytes().replace(b"\n", b"\r\n"))
        self.assertEqual(self.statuses("T03")["E02"], "fail")
    def test_duplicate_mapping_not_hidden_by_set(self):
        self.valid_t03()
        self.write("manifest.csv", "filename,source\npeople-copy.csv,people.csv\npeople-copy.csv,people.csv\nstock-copy.csv,stock.csv\n")
        self.assertEqual(self.statuses("T03")["E04"], "fail")
    def test_t04_second_round_requires_only_correct_changes(self):
        self.write("actions-r2.csv", "id,owner,task,due\nA01,小林,核对库存,2026-12-01\nA02,小陈,更新预算,2026-12-04\nA03,小吴,整理纪要,2026-12-03\n")
        self.assertEqual(self.statuses("T04", 2)["E01"], "pass")
        p = self.out / "actions-r2.csv"
        p.write_text(p.read_text(encoding="utf-8").replace("小陈", "小周"), encoding="utf-8")
        self.assertEqual(self.statuses("T04", 2)["E01"], "fail")
    def test_t05_missing_and_extra_rows_fail(self):
        self.assertEqual(self.statuses("T05")["E01"], "fail")
        self.write("items.csv", "item_id,units\nb01,3\nb02,5\n")
        self.assertEqual(self.statuses("T05")["E01"], "pass")
        self.write("items.csv", "item_id,units\nb01,3\nb02,5\nb02,5\n")
        self.assertEqual(self.statuses("T05")["E01"], "fail")
    def test_wrong_header_fails(self):
        self.write("items.csv", "units,item_id\n3,b01\n5,b02\n")
        self.assertEqual(self.statuses("T05")["E01"], "fail")
    def test_partial_checker_does_not_claim_task_success(self):
        self.valid_t03()
        result=module.check("T03", self.out)
        self.assertIn("E05", result["manual_required"])
        self.assertEqual(result["task_success"], "not_determined_by_partial_checker")
if __name__ == "__main__":
    unittest.main()

