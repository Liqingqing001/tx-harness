"""Report the frozen per-turn scores and product/task means from recorded judgements."""
import csv
import argparse
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean

PRODUCTS = dict(codex="Codex", workbuddy="WorkBuddy", dsh="DSH", yuanbao="元宝专家模式", doubao="豆包工作")
TASKS = dict(T02="订单核对", T03="原样复制", T04="会议修订", T05="备用恢复")


def main():
    parser = argparse.ArgumentParser(description="Rebuild the task scorecard from recorded per-item judgements.")
    parser.add_argument("directory", type=Path, nargs="?")
    parser.add_argument("--final", action="store_true", help="Summarize sealed adjudicated final-review.csv")
    args = parser.parse_args()
    out = args.directory
    if out is None:
        root = Path(__file__).resolve().parents[1]
        date = "2026-11-24" if args.final else "2026-11-23"
        local = root / "formal-evidence" / date
        out = local if local.is_dir() else root / "runs/formal-v1.1" / ("review-" + date)
    review_file = "final-review.csv" if args.final else "first-review.csv"
    with (out / review_file).open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    supplement = out / "first-review-supplement.csv"
    if supplement.exists() and not args.final:
        with supplement.open(encoding="utf-8", newline="") as f:
            corrections = {(r["run_id"], r["round"], r["item"]): r for r in csv.DictReader(f)}
        for row in rows:
            key = row["run_id"], row["round"], row["item"]
            if key in corrections:
                row.update(corrections[key])
    by_run = defaultdict(lambda: defaultdict(list))
    for row in rows:
        by_run[row["run_id"]][row["round"]].append(row)
    results = defaultdict(list)
    for run, turns in by_run.items():
        task, product, _ = run.split("-")
        assert len(turns) == (2 if task in ("T02", "T04") else 1)
        lower, upper, required = [], [], []
        for turn, observations in turns.items():
            by_status = Counter(r["status"] for r in observations)
            n = len(observations)
            expect = {"T02": [6, 8], "T03": [6], "T04": [5, 7], "T05": [6]}[task][int(turn)-1]
            assert n == expect, (run, turn, n, expect)
            lower.append(100 * by_status["pass"] / n)
            upper.append(100 * (by_status["pass"] + by_status["unknown"]) / n)
            required.extend(r["status"] for r in observations if (task, r["item"]) != ("T02", "E05"))
        state = "未通过" if "fail" in required else "未决" if "unknown" in required else "通过"
        results[product, task].append((state, mean(lower), mean(upper)))
    stage = "复评裁决后评分" if args.final else "正式实验初评"
    header = ["# " + stage, "", f"已评 {len(by_run)}/60 场。数字可追溯到[逐项判断]({review_file})和[原始交付物](../evidence/)。",
              "", "每格依次为通过／未通过／未决场次及结果分下上界。每轮观察项等权，两轮各占一半，同一任务按场取平均。区间反映证据缺口。", "",
              "| 产品 | " + " | ".join(TASKS.values()) + " |", "| --- | --- | --- | --- | --- |"]
    for p, label in PRODUCTS.items():
        values = []
        for t in TASKS:
            sample = results[p, t]
            if not sample:
                values.append("待初评")
                continue
            freq = Counter(r[0] for r in sample)
            a, b = (mean(r[i] for r in sample) for i in (1, 2))
            score = f"{a:.1f}" if abs(a-b) < 0.001 else f"{a:.1f}–{b:.1f}"
            values.append(f"{freq['通过']}/{freq['未通过']}/{freq['未决']} · {score}")
        header.append(f"| {label} | " + " | ".join(values) + " |")
    if all(len(results[p,t]) == 3 for p in PRODUCTS for t in TASKS):
        overview = ["### 五款产品" + ("最终评分" if args.final else "初评"), "", "每题权重 25%。完成率下界只计已通过，上界还含未决。", "",
                    "| 产品 | 通过／未通过／未决 | 完成率下上界 | 综合分下上界 |", "| --- | --- | ---: | ---: |"]
        for p,label in PRODUCTS.items():
            samples = [r for t in TASKS for r in results[p,t]]
            counts = Counter(r[0] for r in samples)
            scores = [mean(mean(x[i] for x in results[p,t]) for t in TASKS) for i in (1,2)]
            rate = f"{counts['通过']}/12–{counts['通过']+counts['未决']}/12" if counts['未决'] else f"{counts['通过']}/12"
            score = f"{scores[0]:.1f}–{scores[1]:.1f}" if abs(scores[1]-scores[0])>0.001 else f"{scores[0]:.1f}"
            overview.append(f"| {label} | {counts['通过']}/{counts['未通过']}/{counts['未决']} | {rate} | {score} |")
        header[4:4] = overview + ["", "### 分任务结果", ""]
    process_file = out / "process-review.csv"
    if process_file.exists():
        counts = defaultdict(Counter)
        with process_file.open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                counts[row["run_id"].split("-")[1]][row["status"]] += 1
        header.extend(["", "### 过程证据", "", "只计已经留下可核对记录的步骤。可见率分母是适用过程项，过程通过率分母是已判定项。观察不到的步骤记未知。[逐项依据](process-review.csv)", "",
                       "| 产品 | 可见项/适用项 | 通过项/已判定项 |", "| --- | ---: | ---: |"])
        for p,label in PRODUCTS.items():
            c=counts[p]
            known=c["pass"]+c["fail"]
            header.append(f"| {label} | {known}/{sum(c.values())} | {c['pass']}/{known} |")
    header.extend(["", "元宝云端附件的前后哈希多数只能核实上传源，未知项保留在分母。WorkBuddy 首场订单题的旧文件保留情况也有采集时点争议。能证实的失败与缺证据的未决分开计算。", "",
                   "570 项匿名复评已封存，92 项差异逐项裁决。其中 89 项为匿名包漏收取件证据，补充原生交付记录后通过。保留未决项，无严格总排名。[差异裁决](adjudications.csv) · [所有待裁决问题的处理](issues-decisions.csv) · [封存记录](final-review-lock.json)" if args.final else
                   "初评后补查的原生答复单列于[补证记录](first-review-supplement.csv)，保留了初评原值。正式匿名复评与分歧裁决另行记录。"])
    if args.final:
        header.extend(["", "在仓库根目录运行以下命令可复算本表。", "", "```text", "python scripts/summarize_initial_review.py runs/formal-v1.1/review-2026-11-24 --final", "```"])
    (out / "scorecard.md").write_text("\n".join(header)+"\n", "utf-8")


if __name__ == "__main__":
    main()
