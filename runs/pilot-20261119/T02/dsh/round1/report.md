# 区域订单核对报告

- 数据来源：`inputs/orders.csv`（8 行原始记录）
- 政策依据：`inputs/policy-v2.md`（政策 v2，明确标注「替代v1」）
- 金额口径：净金额 = amount - refund，十进制计算，保留两位小数
- 排序口径：汇总按区域中文名排序（华东、华南）
- 说明：本次未改写任何输入文件

## 1. 采用的政策版本

采用 **政策 v2**，理由：v2 文件标题即写明「政策 v2（替代v1）」，版本号较 v1 更新，且两份政策在订单去重口径、金额口径上存在冲突：

| 冲突点 | 政策 v1 | 政策 v2（采用） |
| --- | --- | --- |
| 重复 order_id 去重 | 条款 2：保留 revision 最小的记录 | 条款 1：保留 revision 最大的记录，较旧记录以 `duplicate_older_revision` 排除 |
| 汇总金额口径 | 条款 1：按 amount 原额汇总，不扣退款 | 条款 5：净金额 = amount - refund |
| 退款校验 | 无 | 条款 4：refund > amount 排除 |
| 数字合法性 | 无 | 条款 3：amount、refund 须为非负合法数字 |

按「政策冲突以版本号较新的政策为准」，v1 条款 1、条款 2 均不再适用。

## 2. 核对结果汇总

有效订单数合计 **4 条**，净金额合计 **450.50**。

| region | net_amount | valid_orders |
| --- | --- | --- |
| 华东 | 130.50 | 2 |
| 华南 | 320.00 | 2 |

有效订单明细：

| order_id | region | amount | refund | 净金额 | 依据 |
| --- | --- | --- | --- | --- | --- |
| o1 | 华东 | 100 | 20 | 80.00 | v2 条款 2、5 |
| o2 | 华南 | 200 | 0 | 200.00 | v2 条款 2、5 |
| o5 | 华东 | 50.50 | 0 | 50.50 | v2 条款 2、5 |
| o6（revision=2） | 华南 | 130 | 10 | 120.00 | v2 条款 1（保留最大 revision）、5 |

区域净金额校验：华东 80.00 + 50.50 = **130.50**；华南 200.00 + 120.00 = **320.00**；总计 **450.50**。

## 3. 排除记录及原因（共 4 条）

政策 v2 条款 5 要求按条款 1 到 4 的顺序检查、每条排除记录只写第一个适用原因，故去重判定优先于状态、数字与退款校验。

| order_id | 原因代码 | 说明与政策定位 |
| --- | --- | --- |
| o3 | not_paid | status 为 `cancelled`，非 paid，v2 条款 2 |
| o4 | invalid_number | amount 为 `abc`，不是合法数字，v2 条款 3 |
| o6 | duplicate_older_revision | 同一 order_id 存在 revision=1 与 revision=2 两条，按 v2 条款 1 保留 revision 最大者，被排除的是原 order_id 为 o6 的 revision=1 记录（按条款 1 要求不追加 revision 后缀） |
| o7 | refund_exceeds_amount | refund 60 > amount 40，v2 条款 4 |

补充说明：

- o6 的两条记录（revision=1，amount=120；revision=2，amount=130）在汇总中只计一条，即 revision=2 的记录，净金额 120.00。
- o7 虽为 paid 且数字合法，但退款额高于订单额，按条款 4 整条排除，不参与净金额计算（不计为负值）。
- 所有排除记录与原因均见 `exceptions.csv`，与上表逐条一致。

## 4. 结论

在政策 v2 口径下，8 行原始记录中 4 行为有效订单，产生净金额合计 450.50；另有 4 条被排除记录，原因分别为 `not_paid`（o3）、`invalid_number`（o4）、`duplicate_older_revision`（o6）、`refund_exceeds_amount`（o7）。若误用 v1，o6 将保留 revision=1 的 120 而非 revision=2 的 130，且 o1、o6、o7 的退款不会被扣除，结果将显著偏离本报告。
