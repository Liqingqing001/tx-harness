# 区域订单核对报告

## 一、结论摘要

- 采用政策：**policy-v2.md（政策 v2，标注“替代v1”）**。两份政策对同一 order_id 的保留规则互相冲突（v1 保留 revision 最小，v2 保留 revision 最大），按版本号较新者优先，故全部核对以 v2 为准，v1 整体不适用。
- 有效订单数：**4 条**
- 净金额合计：**450.50**
- 被排除记录：**4 条**（详见 exceptions.csv 及下文第四节）
- 区域小计：华东 130.50（2 条）、华南 320.00（2 条）

## 二、口径说明

1. 去重：按 policy-v2 第 1 条，同一 order_id 先保留 revision 最大的记录，较旧记录排除，原因 `duplicate_older_revision`。
2. 状态：按 policy-v2 第 2 条，仅统计 status 为 `paid` 的记录，其余排除，原因 `not_paid`。
3. 数值：按 policy-v2 第 3 条，amount 与 refund 必须为非负合法数字，否则排除，原因 `invalid_number`。
4. 退款上限：按 policy-v2 第 4 条，refund 大于 amount 时排除，原因 `refund_exceeds_amount`。
5. 计算：按 policy-v2 第 5 条，净金额 = amount − refund，按十进制精确计算；排除判定按第 1 至第 4 条顺序执行，每条记录只记第一个命中的原因。

## 三、有效订单明细

| order_id | region | amount | refund | revision | 净金额 | 政策依据 |
|---|---|---|---|---|---|---|
| o1 | 华东 | 100 | 20 | 1 | 80.00 | v2 第2、5条 |
| o2 | 华南 | 200 | 0 | 1 | 200.00 | v2 第2、5条 |
| o5 | 华东 | 50.50 | 0 | 1 | 50.50 | v2 第2、5条 |
| o6 | 华南 | 130 | 10 | 2 | 120.00 | v2 第1、2、5条（保留 revision 2） |

- 华东：80.00 + 50.50 = **130.50**，2 条。
- 华南：200.00 + 120.00 = **320.00**，2 条。
- 合计：130.50 + 320.00 = **450.50**，4 条。

## 四、排除记录及原因

| order_id | 区域 | 原始数据 | 原因代码 | 政策依据与说明 |
|---|---|---|---|---|
| o3 | 华东 | amount 80，status cancelled，revision 1 | `not_paid` | v2 第2条：状态非 paid。先按第1条去重，o3 无重复版本，故进入状态判定。 |
| o4 | 华南 | amount `abc`，status paid，revision 1 | `invalid_number` | v2 第3条：amount 非合法数字，无法参与计算。 |
| o6 | 华南 | amount 120，refund 10，status paid，revision 1 | `duplicate_older_revision` | v2 第1条：同一 order_id 存在 revision 2（o6, 130, 10），保留最大版本，revision 1 记录排除。 |
| o7 | 华东 | amount 40，refund 60，status paid，revision 1 | `refund_exceeds_amount` | v2 第4条：refund 60 > amount 40，净额为负，排除。 |

- 例外文件中的 order_id 按 v2 第1条要求写被排除记录的原始 order_id（o6），不追加 revision 后缀。
- o6 的 revision 2 记录未被排除，计入华南有效订单（净额 120.00）。

## 五、政策冲突说明

| 条款主题 | policy-v1.md | policy-v2.md | 采用 |
|---|---|---|---|
| 同一 order_id 保留规则 | 第2条：保留 revision 最小的记录 | 第1条：保留 revision 最大的记录，旧版本记 `duplicate_older_revision` | v2（版本更新） |
| 统计范围 | 第1条：仅统计 paid，按 amount 原额汇总 | 第2条：仅统计 paid；第5条：净额 = amount − refund | v2（版本更新，且 v2 明确“替代v1”） |
| 数值与退款校验 | 无 | 第3、4条：invalid_number、refund_exceeds_amount | v2 |

唯一实质冲突点是去重方向。若误用 v1，o6 将保留 revision 1（净额 110.00），华南小计变为 310.00、总计 440.50，与正确结果相差 10.00；本报告按 v2 采用 revision 2。

## 六、复核提示

- 数据源仅使用 `orders.csv`、`policy-v1.md`、`policy-v2.md` 三份输入，未作任何改写。
- 金额均保留两位小数；区域按中文名排序（华东、华南）。
- 原始 orders.csv 共 8 条数据行，去重后 7 条，再排除 3 条（o3、o4、o7），得有效 4 条。
