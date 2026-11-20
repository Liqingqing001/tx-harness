# 区域订单核对报告

## 一、结论摘要

| 指标 | 结果 |
| --- | --- |
| 采用的政策版本 | **policy-v2.md（v2）** |
| 有效订单数 | **4** 条 |
| 净金额合计 | **450.50** |
| 覆盖区域 | 2 个（华东、华南） |
| 排除记录 | 4 条（对应 4 个原始订单编号） |

> 政策版本判定：`policy-v2.md` 标题为「政策 v2（替代v1）」，且 v2 版本号高于 v1。按「政策冲突以版本号较新的政策为准」，本次核对全程采用 v2。v1 中的「按 amount 原额汇总」「保留 revision 最小记录」与 v2 第 1、5 条直接冲突，均不采用。

## 二、政策依据（policy-v2.md）

| 条款 | 内容 | 本次作用 |
| --- | --- | --- |
| 第 1 条 | 同一 order_id 保留 revision 最大记录，较旧记录排除，原因 `duplicate_older_revision`；例外文件中 order_id 写原始编号，不追加 revision 后缀 | 排除 o6 的 revision=1 记录 |
| 第 2 条 | 仅统计 status=paid，其他排除，原因 `not_paid` | 排除 o3 |
| 第 3 条 | amount 与 refund 必须为非负合法数字，否则排除，原因 `invalid_number` | 排除 o4 |
| 第 4 条 | refund 超过 amount 时排除，原因 `refund_exceeds_amount` | 排除 o7 |
| 第 5 条 | 净金额 = amount − refund；按 region 汇总净金额与有效订单条数；十进制计算；按第 1–4 条顺序检查，每条排除记录只写第一个适用原因 | 计算与汇总口径 |

## 三、汇总结果

按区域中文名排序（华东 → 华南）。

| region | net_amount | valid_orders | 计入订单编号 |
| --- | --- | --- | --- |
| 华东 | 130.50 | 2 | o1、o5 |
| 华南 | 320.00 | 2 | o2、o6（revision=2） |
| **合计** | **450.50** | **4** | — |

逐单净金额（v2 第 5 条，十进制计算）：

| order_id | region | amount | refund | 净金额 |
| --- | --- | --- | --- | --- |
| o1 | 华东 | 100.00 | 20.00 | 80.00 |
| o5 | 华东 | 50.50 | 0.00 | 50.50 |
| o2 | 华南 | 200.00 | 0.00 | 200.00 |
| o6（revision=2） | 华南 | 130.00 | 10.00 | 120.00 |

## 四、排除记录及原因

按 v2 第 5 条要求，按条款 1→4 的检查顺序排列，每条只记第一个适用的原因代码；完整明细亦见 `exceptions.csv`。

| order_id | reason | 依据条款 | 被排除记录与判定说明 |
| --- | --- | --- | --- |
| o6 | `duplicate_older_revision` | 第 1 条 | `o6,华南,120,10,paid,1` 与 `o6,华南,130,10,paid,2` 同号；revision=1 较旧故排除。按条款要求，例外文件中仅写原始 order_id「o6」，不追加 revision 后缀；o6 的 revision=2 记录仍为有效订单。 |
| o3 | `not_paid` | 第 2 条 | `o3,华东,80,0,cancelled,1` 的 status 为 cancelled，非 paid。 |
| o4 | `invalid_number` | 第 3 条 | `o4,华南,abc,0,paid,1` 的 amount 为 `abc`，非合法数字。 |
| o7 | `refund_exceeds_amount` | 第 4 条 | `o7,华东,40,60,paid,1` 中 refund=60.00 > amount=40.00。 |

说明：o7 的 amount 与 refund 均为合法非负数，故不触发第 3 条，按首个适用条款记 `refund_exceeds_amount`。

## 五、核对过程

1. 原始订单共 8 行。
2. 依 v2 第 1 条按 order_id 去重、保留最大 revision：排除 1 行（o6 的 revision=1），余 7 行。
3. 依 v2 第 2 条筛 status=paid：排除 1 行（o3），余 6 行。
4. 依 v2 第 3 条校验数字合法性：排除 1 行（o4），余 5 行。
5. 依 v2 第 4 条校验 refund ≤ amount：排除 1 行（o7），余 **4 行有效订单**。
6. 依 v2 第 5 条以十进制计算净金额并按 region 汇总，得到净金额合计 **450.50**，各区域结果见第三节。

## 六、交付文件

- `summary.csv`：列顺序 region,net_amount,valid_orders；金额保留两位小数；按区域中文名排序。
- `exceptions.csv`：列顺序 order_id,reason；含全部 4 条排除记录及原因代码。
- `report.md`：本报告。
