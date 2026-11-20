# 区域订单核对报告（第二轮：仅统计华东）

## 一、变更范围

- 输入文件不变：`orders.csv`、`policy-v1.md`、`policy-v2.md`，未做改写。
- **采用政策版本：`policy-v2.md`（v2，替代 v1）**，去重、状态、金额合法性、退款校验及净金额计算规则与第一轮完全一致（v2 条款 1–5）。
- **本轮唯一变更：统计范围限定为华东区域**。原本通过 v2 条款 1–4 校验、但不属于华东的订单，新增排除原因代码 `out_of_scope` 列入 exceptions；其余排除原因代码及判定顺序保持不变。
- 第一轮产物（`summary.csv`、`exceptions.csv`、`report.md`）保留未覆盖。

## 二、前后合计对比

| 口径 | 有效订单数 | 净金额合计 |
|---|---:|---:|
| 第一轮（全区域，v2） | 4 | 450.50 |
| 第二轮（仅华东，v2） | 2 | 130.50 |
| 差额（范围收缩排除） | 2 | 320.00 |

差额来自第一轮有效但非华东的两条订单：o2（华南，净 200.00）、o6 revision 2（华南，净 120.00），合计 320.00，本轮以 `out_of_scope` 排除。

## 三、本轮区域汇总

- **有效订单数：2 条**
- **净金额合计：130.50**（净金额 = amount − refund，十进制计算，保留两位小数；v2 条款 5）

| region | net_amount | valid_orders |
|---|---:|---:|
| 华东 | 130.50 | 2 |

汇总按区域中文名排序；金额保留两位小数。

### 有效订单明细（华东）

| order_id | region | amount | refund | 净金额 | 依据 |
|---|---|---:|---:|---:|---|
| o1 | 华东 | 100.00 | 20.00 | 80.00 | paid，金额合法，refund ≤ amount（v2 条款 2、3、4） |
| o5 | 华东 | 50.50 | 0.00 | 50.50 | paid，金额合法，refund ≤ amount（v2 条款 2、3、4） |

## 四、排除记录及原因

共排除 6 条记录，明细见 `exceptions-r2.csv`（列顺序：order_id, reason）。判定仍按 v2 条款 1 → 2 → 3 → 4 顺序，每条记录只写第一个适用原因；`out_of_scope` 为范围过滤原因，仅适用于原本通过条款 1–4 校验但非华东的订单。

| order_id | reason | 定位条款与订单说明 |
|---|---|---|
| o2 | out_of_scope | 第一轮有效订单（华南，净 200.00），本轮范围限定华东，排除。 |
| o3 | not_paid | v2 条款 2：status 为 `cancelled`，非 paid，排除。 |
| o4 | invalid_number | v2 条款 3：amount 为 `abc`，非非负合法数字，排除。 |
| o6 | duplicate_older_revision | v2 条款 1：revision 1（amount 120、refund 10）为较旧记录，被 revision 2 取代；order_id 写原始 `o6`，不追加 revision 后缀。 |
| o6 | out_of_scope | v2 条款 1 保留的 revision 2 记录（华南，净 120.00），第一轮有效，本轮范围限定华东，排除。 |
| o7 | refund_exceeds_amount | v2 条款 4：refund 60.00 超过 amount 40.00，排除。 |

> 说明：o6 在 exceptions 中出现两行，分别对应其两条原始记录——旧 revision 记录因去重排除（`duplicate_older_revision`），保留下来的新 revision 记录因非华东排除（`out_of_scope`）。

## 五、关键结论定位

1. 本轮仅华东计入汇总：净金额 130.50，有效订单 2 条（o1、o5）；与第一轮华东口径一致。
2. 范围收缩共移出 2 条华南订单、320.00：o2（200.00）、o6 revision 2（120.00），原因 `out_of_scope`。
3. 其余排除记录与第一轮原因一致：o3 `not_paid`、o4 `invalid_number`、o6 旧记录 `duplicate_older_revision`、o7 `refund_exceeds_amount`。
4. v1 中与 v2 冲突的「保留 revision 最小记录」规则仍未采用，以 v2 条款 1 为准。
