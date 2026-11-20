# 区域订单核对报告

## 一、核对依据与采用政策版本

- 输入文件：`orders.csv`、`policy-v1.md`、`policy-v2.md`（均位于 inputs 目录，未做改写）。
- **采用政策版本：`policy-v2.md`（v2，替代 v1）**。政策冲突以版本号较新的政策为准。
- 政策冲突说明：
  - v1 条款 2 规定「同一 order_id 只保留 revision 最小的记录」；v2 条款 1 改为「同一 order_id 先保留 revision 最大的记录，较旧记录排除，原因 `duplicate_older_revision`」。二者冲突，按版本较新原则**采用 v2 条款 1**（保留 revision 最大记录）。
- 核对顺序：按 v2 条款 1 → 2 → 3 → 4 依次检查；每条排除记录只写第一个适用的原因代码（v2 条款 5）。

## 二、汇总结论

- **有效订单数：4 条**
- **净金额合计：450.50**（净金额 = amount − refund，十进制计算，保留两位小数；v2 条款 5）

| region | net_amount | valid_orders |
|---|---:|---:|
| 华东 | 130.50 | 2 |
| 华南 | 320.00 | 2 |

汇总按区域中文名排序；金额保留两位小数。

### 有效订单明细

| order_id | region | amount | refund | 净金额 | 依据 |
|---|---|---:|---:|---:|---|
| o1 | 华东 | 100.00 | 20.00 | 80.00 | paid，金额合法，refund ≤ amount（v2 条款 2、3、4） |
| o2 | 华南 | 200.00 | 0.00 | 200.00 | paid，金额合法，refund ≤ amount（v2 条款 2、3、4） |
| o5 | 华东 | 50.50 | 0.00 | 50.50 | paid，金额合法，refund ≤ amount（v2 条款 2、3、4） |
| o6（revision 2） | 华南 | 130.00 | 10.00 | 120.00 | 同 order_id 保留 revision 最大记录；paid，金额合法，refund ≤ amount（v2 条款 1、2、3、4） |

## 三、排除记录及原因

共排除 4 条记录，明细见 `exceptions.csv`（列顺序：order_id, reason）。

| order_id | reason | 定位条款与订单说明 |
|---|---|---|
| o3 | not_paid | v2 条款 2：status 为 `cancelled`，非 paid，排除。 |
| o4 | invalid_number | v2 条款 3：amount 为 `abc`，非非负合法数字，排除。 |
| o6 | duplicate_older_revision | v2 条款 1：同一 order_id 下 revision 1（amount 120、refund 10）为较旧记录，被 revision 2 记录取代；按条款要求 order_id 写原始 `o6`，不追加 revision 后缀。 |
| o7 | refund_exceeds_amount | v2 条款 4：refund 60.00 超过 amount 40.00，排除。 |

## 四、关键结论定位

1. 区域净金额：华东 130.50（o1、o5），华南 320.00（o2、o6 revision 2）；净金额合计 450.50，有效订单 4 条（v2 条款 5）。
2. o6 存在 revision 1 与 revision 2 两条记录，按 v2 条款 1 仅保留 revision 2；旧记录以 `duplicate_older_revision` 列入 exceptions.csv。
3. 全部排除原因均来自 v2 条款 1–4 的原因代码；v1 中与 v2 冲突的「保留 revision 最小记录」规则未被采用。
