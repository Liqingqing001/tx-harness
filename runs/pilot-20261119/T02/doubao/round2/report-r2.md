# 区域订单核对报告（第二轮 r2）

## 一、本轮变更范围

- **统计范围收窄为仅华东区域**；其他计算、去重与异常处理规则保持第一轮不变，仍采用 **policy-v2.md（政策 v2，替代 v1）**，冲突条款以新版 v2 为准。
- 新增排除原因代码 **`out_of_scope`**：用于在第一轮规则（v2 第 1→4 条）下原本判定为有效、但区域不属于华东的订单。
- 判定顺序：先按 v2 第 1→4 条完成去重、状态、金额合法性与退款金额校验；通过校验后，区域非华东的记录再以 `out_of_scope` 排除。
- 本轮交付文件：`summary-r2.csv`、`exceptions-r2.csv`、`report-r2.md`；第一轮文件（`summary.csv`、`exceptions.csv`、`report.md`）原样保留，未覆盖。

## 二、前后合计对比

| 指标 | 第一轮（全区域） | 第二轮（仅华东） | 差额（范围外） |
|---|---:|---:|---:|
| 有效订单数 | 4 | **2** | 2（o2、o6） |
| 净金额合计 | 450.50 | **130.50** | 320.00（o2、o6） |
| 排除记录数 | 4 | **6** | 新增 2 条 `out_of_scope` |

- 勾稽关系：130.50（华东）+ 320.00（范围外华南）= 450.50（第一轮合计）。
- 净金额口径：净金额 = amount − refund（v2 第 5 条），按十进制计算，金额保留两位小数。

## 三、分区域汇总（按区域中文名排序）

| region | net_amount | valid_orders |
|---|---:|---:|
| 华东 | 130.50 | 2 |

### 华东（净金额 130.50，有效 2 单）

| order_id | amount | refund | 净金额 | 依据 |
|---|---:|---:|---:|---|
| o1 | 100.00 | 20.00 | 80.00 | status=paid（v2 第 2 条），金额合法（第 3 条），refund≤amount（第 4 条），区域为华东（本轮范围） |
| o5 | 50.50 | 0.00 | 50.50 | status=paid（v2 第 2 条），金额合法（第 3 条），refund≤amount（第 4 条），区域为华东（本轮范围） |

## 四、排除记录及原因

判定按 v2 第 1→4 条顺序进行，每条排除记录只写第一个适用的原因代码（v2 第 6 条）；通过校验但区域非华东的记录标注 `out_of_scope`。

| order_id | 原因代码 | 定位说明 |
|---|---|---|
| o2 | out_of_scope | 第一轮规则下有效（华南，净金额 200.00），本轮仅统计华东，命中新增范围规则 |
| o3 | not_paid | status=cancelled，非 paid，命中 v2 第 2 条 |
| o4 | invalid_number | amount=abc 为非合法数字，命中 v2 第 3 条 |
| o6 | duplicate_older_revision | 同一 order_id 存在 revision=1 与 revision=2 两条记录，按 v2 第 1 条保留 revision 最大的记录，排除较旧的 revision=1 记录；order_id 不追加 revision 后缀 |
| o6 | out_of_scope | 保留的 revision=2 记录属华南（净金额 120.00），第一轮规则下有效，本轮仅统计华东，命中新增范围规则 |
| o7 | refund_exceeds_amount | refund=60 > amount=40，命中 v2 第 4 条 |

## 五、口径与备注

- 排除记录明细见 `exceptions-r2.csv`，字段顺序为 `order_id,reason`。
- 汇总明细见 `summary-r2.csv`，字段顺序为 `region,net_amount,valid_orders`。
- 第一轮文件保留未改；本次核对未改写任何输入文件。
