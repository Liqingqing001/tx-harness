import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("check_t02", ROOT / "scripts/check_t02.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class CheckerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.out = Path(self.tmp.name)
        for f in (ROOT / "cases/T02/expected").glob("*.csv"):
            shutil.copy(f, self.out / f.name)

    def status(self, round=1):
        return [c["status"] for c in m.check(self.out, round)["checks"]]

    def test_both_reference_rounds(self):
        self.assertEqual(self.status(), ["pass", "pass"])
        self.assertEqual(self.status(2), ["pass", "pass"])
        self.assertEqual(m.check(self.out, 2)["task_success"], "not_determined_by_csv_checker")

    def test_wrong_amount(self):
        f = self.out / "summary.csv"
        f.write_text(f.read_text(encoding="utf-8").replace("130.50", "150.50"), encoding="utf-8")
        self.assertEqual(self.status()[0], "fail")

    def test_duplicate_region(self):
        with (self.out / "summary.csv").open("a", encoding="utf-8") as f:
            f.write("华东,130.50,2\n")
        self.assertEqual(self.status()[0], "fail")

    def test_missing_exception(self):
        f = self.out / "exceptions-r2.csv"
        f.write_text(f.read_text(encoding="utf-8").replace("o6,out_of_scope\n", ""), encoding="utf-8")
        self.assertEqual(self.status(2)[1], "fail")

    def test_missing_file(self):
        (self.out / "summary.csv").unlink()
        self.assertEqual(self.status()[0], "fail")

    def test_reordered_exceptions_are_valid(self):
        f = self.out / "exceptions.csv"
        lines = f.read_text(encoding="utf-8").splitlines()
        f.write_text("\n".join([lines[0]] + list(reversed(lines[1:]))) + "\n", encoding="utf-8")
        self.assertEqual(self.status()[1], "pass")

    def test_nan_rejected(self):
        f = self.out / "summary.csv"
        f.write_text(f.read_text(encoding="utf-8").replace("130.50", "NaN"), encoding="utf-8")
        self.assertEqual(self.status()[0], "fail")

if __name__ == "__main__":
    unittest.main()
