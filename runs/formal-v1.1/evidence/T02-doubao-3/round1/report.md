# 区域订单核对报告

## 一、采用的政策版本

- 本次核对采用 **policy-v2.md（政策 v2，替代 v1）**。两份政策存在冲突时，按版本号较新的 v2 执行，v1 不再适用。
- 政策冲突取舍如下：

| 核对事项 | policy-v1.md（已被替代） | policy-v2.md（本次采用） | 依据 |
| --- | --- | --- | --- |
| 同一 order_id 多版本记录 | 条款 2：保留 revision **最小**的记录 | 条款 1：保留 revision **最大**的记录，较旧记录排除，原因 `duplicate_older_revision` | v2 条款 1 |
| 金额口径 | 条款 1：按 amount **原额**汇总 | 条款 5：净金额 = amount − refund，按区域汇总净金额及有效订单条数，十进制计算 | v2 条款 5 |

## 二、核对结论

- **有效订单数：4 条**
- **净金额合计：450.50**（单位与订单原始金额一致，保留两位小数，十进制计算）
- 输入记录共 8 条（含同一 order_id 的重复版本），排除记录 4 条。

### 分区域汇总（按区域中文名排序，详见 summary.csv）

| 区域 | 净金额 net_amount | 有效订单数 valid_orders |
| --- | ---: | ---: |
| 华东 | 130.50 | 2 |
| 华南 | 320.00 | 2 |
| **合计** | **450.50** | **4** |

### 有效订单明细

| order_id | 区域 | amount | refund | 净金额 | 保留依据 |
| --- | --- | ---: | ---: | ---: | --- |
| o1 | 华东 | 100.00 | 20.00 | 80.00 | v2 条款 2（status=paid）、条款 3（数字合法非负）、条款 4（refund ≤ amount） |
| o2 | 华南 | 200.00 | 0.00 | 200.00 | 同上，v2 条款 2、3、4 |
| o5 | 华东 | 50.50 | 0.00 | 50.50 | 同上，v2 条款 2、3、4 |
| o6（revision=2） | 华南 | 130.00 | 10.00 | 120.00 | v2 条款 1（保留 revision 最大记录）；并通过条款 2、3、4 |

- 华东净金额：80.00 + 50.50 = **130.50**（o1、o5）。
- 华南净金额：200.00 + 120.00 = **320.00**（o2、o6 修订版）。

## 三、排除记录及原因（详见 exceptions.csv）

判定顺序严格按 v2 条款 1 → 4 执行，每条排除记录只记录**第一个适用**的原因代码。

| order_id | 排除原因 | 适用条款 | 说明 |
| --- | --- | --- | --- |
| o3 | `not_paid` | v2 条款 2 | status 为 `cancelled`，非 paid，排除。 |
| o4 | `invalid_number` | v2 条款 3 | amount 为 `abc`，不是合法非负数字，排除。 |
| o6 | `duplicate_older_revision` | v2 条款 1 | o6 存在 revision=1（amount 120）与 revision=2（amount 130）两条记录；按条款 1 保留 revision 最大的 revision=2，较旧的 revision=1 记录排除。例外文件中 order_id 写原始 `o6`，不追加 revision 后缀。 |
| o7 | `refund_exceeds_amount` | v2 条款 4 | amount=40、refund=60，refund 超过 amount，排除。 |

> 注：o6 的较旧记录在条款 1 即被排除，不再进入条款 2–4 的后续检查；其保留下来的 revision=2 记录经条款 2、3、4 校验通过，计入华南有效订单。

## 四、口径与计算说明

1. 政策版本冲突一律以版本号较新的 policy-v2.md 为准（v2 文首注明"替代 v1"）。
2. 检查顺序：条款 1（重复旧版本）→ 条款 2（paid 状态）→ 条款 3（合法非负数字）→ 条款 4（refund 不超过 amount）；每条记录仅记录首个命中的原因代码。
3. 净金额 = amount − refund，使用十进制计算；汇总金额保留两位小数。
4. 汇总按区域中文名排序；异常记录按输入文件中的原始出现顺序列入 exceptions.csv。
5. 本次核对仅读取输入文件，未对 orders.csv、policy-v1.md、policy-v2.md 做任何改写。

## 五、交付文件

- `summary.csv`：列顺序 `region,net_amount,valid_orders`
- `exceptions.csv`：列顺序 `order_id,reason`
- `report.md`：本报告
