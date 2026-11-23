"""Inspect exported bytes and the CSV records a strict row-count check sees."""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path


def inspect(path):
    raw = path.read_bytes()
    rows = list(csv.reader(io.StringIO(raw.decode("utf-8-sig"), newline="")))
    return {"file": path.name, "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw), "utf8_bom": raw.startswith(b"\xef\xbb\xbf"),
            "cr_cr_lf_sequences": raw.count(b"\r\r\n"),
            "csv_field_counts_including_header": [len(row) for row in rows],
            "nonempty_data_rows": sum(bool(row) for row in rows[1:]),
            "blank_records": sum(not row for row in rows),
            "A02": [r for r in rows if r[:1] == ["A02"]]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    body = json.dumps(inspect(args.file), ensure_ascii=False, indent=2)
    if args.out:
        args.out.write_text(body, "utf-8")
    else:
        print(body)
