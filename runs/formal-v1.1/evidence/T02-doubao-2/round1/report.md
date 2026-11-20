# 区域订单核对报告

## 一、采用的政策版本

- 本次核对采用 **policy-v2.md（政策 v2）**。政策冲突时以版本号较新的政策为准，v2 已整体替代 policy-v1.md（政策 v1）。
- 关键冲突说明：v1 条款2 规定“同一 order_id 只保留 revision 最小的记录”，与 v2 条款1“保留 revision 最大的记录”相冲突；按“版本较新为准”原则，执行 **v2 条款1（保留 revision 最大）**。
- 判定顺序：按 v2 条款1 → 条款2 → 条款3 → 条款4 依次检查，每条排除记录只记录第一个适用的原因代码（v2 条款5）。

## 二、总体结论

- 有效订单数：**4** 笔。
- 净金额合计：**450.50**（净金额 = amount − refund，十进制计算，v2 条款5）。
- 排除记录：**4** 笔（明细见 `exceptions.csv` 及下表）。

## 三、分区域汇总（按区域中文名排序）

| region | net_amount | valid_orders |
| --- | ---: | ---: |
| 华东 | 130.50 | 2 |
| 华南 | 320.00 | 2 |
| **合计** | **450.50** | **4** |

### 有效订单明细

| order_id | region | 净金额 | 依据 |
| --- | --- | ---: | --- |
| o1 | 华东 | 80.00 | 通过 v2 条款1–4 |
| o2 | 华南 | 200.00 | 通过 v2 条款1–4 |
| o5 | 华东 | 50.50 | 通过 v2 条款1–4 |
| o6 | 华南 | 120.00 | 通过 v2 条款1–4 |

## 四、排除记录及原因

| order_id | reason | 说明（定位政策条款） |
| --- | --- | --- |
| o3 | not_paid | 政策 v2 条款2：status 非 paid，排除 |
| o4 | invalid_number | 政策 v2 条款3：amount/refund 不是非负合法数字，排除 |
| o6 | duplicate_older_revision | 政策 v2 条款1：同一 order_id 仅保留 revision 最大的记录，较旧记录排除 |
| o7 | refund_exceeds_amount | 政策 v2 条款4：refund 超过 amount，排除 |

## 五、关键结论定位

- **o6（华南）**：存在 revision 1（120/10）与 revision 2（130/10）两条记录；依 v2 条款1 保留 revision 2，revision 1 以 `duplicate_older_revision` 排除，例外文件仅写原始 order_id `o6`，不追加 revision 后缀。
- **o3（华东）**：status 为 cancelled，依 v2 条款2 以 `not_paid` 排除。
- **o4（华南）**：amount 为 `abc`，非合法数字，依 v2 条款3 以 `invalid_number` 排除。
- **o7（华东）**：refund 60 超过 amount 40，依 v2 条款4 以 `refund_exceeds_amount` 排除。
- 有效订单：**o1、o2、o5、o6（revision 2）**；华东净金额 130.50（o1=80.00，o5=50.50），华南净金额 320.00（o2=200.00，o6 修订后=120.00）。

> 输入文件 orders.csv、policy-v1.md、policy-v2.md 未被改写；全部产物位于 outputs 目录。
