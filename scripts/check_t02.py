"""T02 CSV checks only. Exit 1 on failed CSV checks; manual items remain unknown."""
import argparse
from collections import Counter
import csv
from decimal import Decimal
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

def rows(path, fields):
    with Path(path).open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != fields:
            raise ValueError("incorrect column names/order")
        result = list(reader)
    if any(None in row or any(v is None for v in row.values()) for row in result):
        raise ValueError("malformed CSV row")
    return result

def summary(path):
    data = rows(path, ["region", "net_amount", "valid_orders"])
    regions = [r["region"] for r in data]
    if regions != sorted(set(regions)):
        raise ValueError("duplicate region or incorrect sort order")
    result = {}
    for row in data:
        if not re.fullmatch(r"[0-9]+\.[0-9]{2}", row["net_amount"]):
            raise ValueError("amount requires two decimal places")
        if not re.fullmatch(r"[0-9]+", row["valid_orders"]):
            raise ValueError("invalid order count")
        result[row["region"]] = (Decimal(row["net_amount"]), int(row["valid_orders"]))
    return result

def exceptions(path):
    return Counter((r["order_id"], r["reason"]) for r in rows(path, ["order_id", "reason"]))

def check(outputs, round_number):
    if round_number not in (1, 2):
        raise ValueError("round must be 1 or 2")
    outputs = Path(outputs)
    suffix = "" if round_number == 1 else "-r2"
    reference = ROOT / "cases/T02/expected"
    result = []
    for item, filename, parser in [("E01", "summary", summary), ("E02", "exceptions", exceptions)]:
        filename += suffix + ".csv"
        # Reference faults are evaluator errors, never product failures.
        expected = parser(reference / filename)
        try:
            actual = parser(outputs / filename)
            passed = actual == expected
            detail = "matches reference" if passed else "content differs from reference"
        except (OSError, ValueError, csv.Error) as error:
            passed, detail = False, str(error)
        result.append({"id": item, "status": "pass" if passed else "fail", "evidence": filename, "detail": detail})
    return {"round": round_number, "checks": result,
            "manual_required": ["E03", "E04", "E05", "E08"] + (["E06", "E07"] if round_number == 2 else []),
            "process_status": "unknown", "task_success": "not_determined_by_csv_checker"}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--outputs", required=True)
    ap.add_argument("--round", type=int, choices=[1, 2], required=True)
    args = ap.parse_args()
    result = check(args.outputs, args.round)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if all(c["status"] == "pass" for c in result["checks"]) else 1)
