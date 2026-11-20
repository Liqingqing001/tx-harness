# 区域订单核对报告（第二轮：仅统计华东）

## 一、采用的政策版本与变更范围

- 政策版本仍采用 **policy-v2.md（政策 v2）**；去重、状态校验、数字合法性、退款超额等计算与异常处理规则与第一轮保持不变，冲突条款仍以较新的 v2 为准。
- **本轮变更范围**：统计区域由全部区域收窄为 **仅华东**；新增排除原因代码 `out_of_scope`，用于在第一轮规则下原本有效、但不属于华东的订单。
- 判定顺序：v2 条款1 → 条款2 → 条款3 → 条款4 → 范围过滤（out_of_scope）；每条排除记录只写第一个适用原因代码。

## 二、前后合计对比

| 口径 | 有效订单数 | 净金额合计 |
| --- | ---: | ---: |
| 第一轮（全部区域） | 4 | 450.50 |
| 第二轮（仅华东） | 2 | 130.50 |

### 第一轮分区域基线

| region | net_amount | valid_orders |
| --- | ---: | ---: |
| 华东 | 130.50 | 2 |
| 华南 | 320.00 | 2 |

## 三、本轮分区域汇总（按区域中文名排序）

| region | net_amount | valid_orders |
| --- | ---: | ---: |
| 华东 | 130.50 | 2 |
| **合计** | **130.50** | **2** |

### 本轮有效订单明细

| order_id | region | 净金额 | 依据 |
| --- | --- | ---: | --- |
| o1 | 华东 | 80.00 | 通过 v2 条款1–4，且属华东范围 |
| o5 | 华东 | 50.50 | 通过 v2 条款1–4，且属华东范围 |

## 四、排除记录及原因

| order_id | reason | 说明（定位政策条款 / 范围规则） |
| --- | --- | --- |
| o2 | out_of_scope | 第二轮范围限定：原可通过 v2 条款1–4，但不属于统计范围（华东），排除 |
| o3 | not_paid | 政策 v2 条款2：status 非 paid，排除 |
| o4 | invalid_number | 政策 v2 条款3：amount/refund 不是非负合法数字，排除 |
| o6 | duplicate_older_revision | 政策 v2 条款1：同一 order_id 仅保留 revision 最大的记录，较旧记录排除 |
| o6 | out_of_scope | 第二轮范围限定：原可通过 v2 条款1–4，但不属于统计范围（华东），排除 |
| o7 | refund_exceeds_amount | 政策 v2 条款4：refund 超过 amount，排除 |

## 五、关键结论定位

- **范围收窄影响**：第一轮华南两笔有效订单在本轮以 `out_of_scope` 排除——**o2**（华南，净 200.00）、**o6**（华南，rev2，净 120.00）；华南净金额 320.00 不再计入合计。
- **o6（华南）**：rev1 依 v2 条款1 以 `duplicate_older_revision` 排除；rev2 通过条款1–4，但因非华东以 `out_of_scope` 排除；例外文件均写原始 order_id `o6`，不追加 revision 后缀。
- **o3（华东）**：status 为 cancelled，依 v2 条款2 以 `not_paid` 排除。
- **o4（华南）**：amount 为 `abc`，依 v2 条款3 以 `invalid_number` 排除。
- **o7（华东）**：refund 60 超过 amount 40，依 v2 条款4 以 `refund_exceeds_amount` 排除。
- 本轮有效订单：**o1、o5**（均为华东）；华东净金额 130.50（o1=80.00，o5=50.50），与第一轮华东口径一致。

> 第一轮产物 summary.csv、exceptions.csv、report.md 予以保留未覆盖；本轮产物为 summary-r2.csv、exceptions-r2.csv、report-r2.md。输入文件 orders.csv、policy-v1.md、policy-v2.md 未被改写。
