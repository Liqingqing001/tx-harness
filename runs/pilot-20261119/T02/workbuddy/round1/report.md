# 区域订单核对报告

## 一、核对口径

- 采用政策：**v2**（`policy-v2.md`，标题注明“替代 v1”）。政策冲突以版本号较新的 v2 为准，v1 不再适用。
- 计算规则（v2 条款5）：净金额 = amount − refund，按十进制计算；按 region 汇总净金额与有效订单条数。
- 排除检查顺序（v2 条款1→4）：同一 order_id 保留 revision 最大记录 → 仅 paid → 数字合法且非负 → refund 不超过 amount；每条排除记录只记第一个适用原因。

## 二、关键结论

- **有效订单数：4 单**
- **净金额合计：450.50**
- **采用的政策版本：v2**（覆盖 policy-v1.md）

### 分区域汇总（按区域中文名排序）

| region | net_amount | valid_orders |
| --- | --- | --- |
| 华东 | 130.50 | 2 |
| 华南 | 320.00 | 2 |
| **合计** | **450.50** | **4** |

### 有效订单明细（定位到订单编号）

| order_id | region | amount | refund | 净金额 |
| --- | --- | --- | --- | --- |
| o1 | 华东 | 100.00 | 20.00 | 80.00 |
| o2 | 华南 | 200.00 | 0.00 | 200.00 |
| o5 | 华东 | 50.50 | 0.00 | 50.50 |
| o6 | 华南 | 130.00 | 10.00 | 120.00 |

## 三、排除记录及原因

排除记录与原因同时列于 `exceptions.csv`（列顺序 order_id, reason）。下列每条结论均定位到政策条款与订单编号：

- `o3` — `not_paid`：v2 条款2：仅统计 status 为 paid 的记录，其他状态排除。
- `o4` — `invalid_number`：v2 条款3：amount 与 refund 必须是非负合法数字，否则排除。
- `o6` — `duplicate_older_revision`：v2 条款1：同一 order_id 仅保留 revision 最大的记录，较旧记录排除；例外中的 order_id 写原始编号、不追加 revision 后缀。 本条为 o6 的 revision=1（amount=120）被排除；其 revision=2（amount=130）为保留记录并计入有效订单。
- `o7` — `refund_exceeds_amount`：v2 条款4：refund 超过 amount 时排除。

## 四、说明

- 订单 o6 在输入中有两条：revision=1 与 revision=2。按 v2 条款1排除 revision=1，保留 revision=2 并计入华南净金额 120（=130−10）；因此 o6 既出现在 exceptions.csv（旧版本记录），也计入有效订单。
- 订单 o4 的 amount 为 `abc`，非合法数字，按 v2 条款3排除。
- 所有金额保留两位小数；输入文件未被修改。
