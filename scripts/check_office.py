"""Deterministic subset only: reports, downloadability and process need human review."""
import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def read_csv(path, fields):
    with Path(path).open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    if not rows or rows[0] != fields:
        raise ValueError("wrong header or column order")
    if any(len(row) != len(fields) for row in rows[1:]):
        raise ValueError("wrong field count or blank record")
    return [tuple(row) for row in rows[1:]]

def check(task, outputs, round_number=1):
    if task not in ("T03", "T04", "T05"):
        raise ValueError("unsupported task")
    if round_number not in (1, 2) or (task != "T04" and round_number != 1):
        raise ValueError("invalid round")
    output = Path(outputs)
    checks = []
    def evaluate(item, filename, callback):
        try:
            ok = bool(callback())
            detail = "matches reference" if ok else "content differs from reference"
        except (OSError, ValueError, UnicodeError, csv.Error) as error:
            ok, detail = False, str(error)
        checks.append(dict(id=item, status="pass" if ok else "fail",
                           evidence=filename, detail=detail))
    if task == "T03":
        # Validate references before scoring: evaluator defects must not fail products.
        directory = ROOT / "cases/T03"
        manifest = json.loads((directory / "input-manifest.json").read_text(encoding="utf-8"))
        for item, name in (("E01", "people"), ("E02", "stock")):
            source = directory / "inputs" / (name + ".csv")
            expected = manifest[name + ".csv"]
            if digest(source) != expected:
                raise RuntimeError("input reference hash mismatch")
            filename = name + "-copy.csv"
            evaluate(item, filename, lambda filename=filename, expected=expected:
                     digest(output / filename) == expected)
        expected = Counter([("people-copy.csv", "people.csv"), ("stock-copy.csv", "stock.csv")])
        evaluate("E04", "manifest.csv", lambda:
                 Counter(read_csv(output / "manifest.csv", ["filename", "source"])) == expected)
        manual = ["E03", "E05", "E06"]
    elif task == "T04":
        expected = [("A01", "小林", "核对库存", "2026-12-01"),
                    ("A02", "小周" if round_number == 1 else "小陈", "更新预算",
                     "2026-12-02" if round_number == 1 else "2026-12-04"),
                    ("A03", "小吴", "整理纪要", "2026-12-03")]
        filename = "actions.csv" if round_number == 1 else "actions-r2.csv"
        evaluate("E01", filename, lambda:
                 read_csv(output / filename, ["id", "owner", "task", "due"]) == expected)
        manual = ["E02", "E03", "E04", "E05"] + (["E06", "E07"] if round_number == 2 else [])
    else:
        evaluate("E01", "items.csv", lambda:
                 read_csv(output / "items.csv", ["item_id", "units"]) == [("b01", "3"), ("b02", "5")])
        manual = ["E02", "E03", "E04", "E05", "E06"]
    return dict(task=task, round=round_number, checks=checks, manual_required=manual,
                task_success="not_determined_by_partial_checker", process_status="unknown")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", required=True, choices=["T03", "T04", "T05"])
    parser.add_argument("--outputs", required=True)
    parser.add_argument("--round", type=int, default=1)
    args = parser.parse_args()
    result = check(args.task, args.outputs, args.round)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if all(x["status"] == "pass" for x in result["checks"]) else 1)

