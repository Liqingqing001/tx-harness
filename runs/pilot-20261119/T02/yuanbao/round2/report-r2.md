# 区域订单核对报告（第二轮 · 仅华东）

## 变更范围

- **采用政策：v2**（`policy-v2.md` 明示“替代v1”），与第一轮一致。
- **唯一变更**：统计范围由全部区域收窄为 **华东**。v2 条款1（按 order_id 取 revision 最大）、条款2（仅 paid）、条款3（金额非负合法数字）、条款4（refund ≤ amount）、条款5（净额 = amount − refund，十进制，按 region 汇总）**规则与执行顺序完全不变**。
- **新增原因代码 `out_of_scope`**：仅用于“已通过 v2 条款1→4 全部校验、但它属于有效订单、只是区域不是华东”的记录。它排在条款4**之后**判定，因此不会掩盖任何数据质量问题——一条记录若同时不合规且非华东，仍只记首个命中的原有代码。
- 列名、列顺序、两位小数、按区域中文名排序等格式要求沿用第一轮。
- 第一轮文件 `summary.csv` / `exceptions.csv` / `report.md` **原样保留，未覆盖**。

## 核对结论

- **有效订单数：2 单**（o1、o5）
- **净金额合计：130.50**
- 汇总表仅剩华东一行（范围收窄后无其他区域可列）。

## 区域汇总（summary-r2.csv）

| region | net_amount | valid_orders |
|---|---:|---:|
| 华东 | 130.50 | 2 |

## 排除记录及原因（exceptions-r2.csv）

按 v2 条款1→4 顺序判定，末位追加 `out_of_scope`；每条仅记首个命中原因。

| order_id | 被排除记录（revision / region / status / amount / refund） | reason | 定位 |
|---|---|---|---|
| o6 | rev1 / 华南 / paid / 120 / 10 | `duplicate_older_revision` | v2 条款1：rev1 < 同单最大 rev2 |
| o3 | rev1 / 华东 / cancelled / 80 / 0 | `not_paid` | v2 条款2：status=cancelled |
| o4 | rev1 / 华南 / paid / abc / 0 | `invalid_number` | v2 条款3：amount=`abc` 非合法数字 |
| o7 | rev1 / 华东 / paid / 40 / 60 | `refund_exceeds_amount` | v2 条款4：refund 60 > amount 40 |
| o2 | rev1 / 华南 / paid / 200 / 0 | `out_of_scope` | 通过条款1→4，但区域非华东 |
| o6 | rev2 / 华南 / paid / 130 / 10 | `out_of_scope` | rev2 已通过条款1→4（净额120.00），因区域非华东剔除 |

> **o6 出现两行的说明**：两行对应**两条不同记录**（rev1 与 rev2），不是重复输出。按 v2 条款1，例外文件的 order_id 写被排除记录的原始 order_id、不追加 revision 后缀，故两行同为 `o6`；区分依据是其命中原因不同（rev1 撞条款1，rev2 撞范围过滤）。若需按订单去重展示，可将这两行合并为 `o6 / duplicate_older_revision;out_of_scope`，但会丢失版本级追溯，本轮未采用。

## 前后合计对比（第一轮 → 第二轮）

| 指标 | 第一轮（全区域） | 第二轮（仅华东） | 差异 | 差异来源 |
|---|---:|---:|---:|---|
| 有效订单数 | 4 | 2 | −2 | o2、o6(rev2) 转 `out_of_scope` |
| 净金额合计 | 450.50 | 130.50 | −320.00 | 华南 320.00 整体移出范围 |
| 华东净金额 | 130.50 | 130.50 | 0.00 | **华东口径下两轮完全一致** |
| 华南净金额 | 320.00 | —（不出表） | −320.00 | 范围收窄，非数据修正 |
| 异常记录条数 | 4 | 6 | +2 | 新增 2 条 `out_of_scope`（o2、o6 rev2） |

**关键结论**：范围收窄**没有改变华东本身的任何数字**——o1（100−20=80.00）、o5（50.50−0=50.50）合计 130.50，与第一轮逐单一致；原有的 4 条质量类排除（o3/not_paid、o4/invalid_number、o6 rev1/duplicate_older_revision、o7/refund_exceeds_amount）原因代码与依据**一条未变**。减少的 320.00 全部来自华南整体出域，属于口径变化，不是新发现的错误。

## 复核口径

- 金额用 `Decimal` 精确十进制运算，输出统一两位小数；订单条数按通过全部校验且落在华东的“记录/订单版本”计数。
- `out_of_scope` 只加在校验链末端，保证“数据质量异常”与“范围外”两类原因可分别统计：本轮质量类 4 条、范围类 2 条。
- 输入文件（`orders.csv`、`policy-v1.md`、`policy-v2.md`）未改写；本轮仅新增 `summary-r2.csv`、`exceptions-r2.csv`、`report-r2.md`。
