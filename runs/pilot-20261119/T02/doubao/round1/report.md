# 区域订单核对报告

## 一、采用的政策版本

- 本次核对采用 **policy-v2.md（政策 v2，替代 v1）**。
- 两份政策存在冲突时，以版本号较新的 **v2** 为准。关键冲突点：
  - v1 第 2 条要求"同一 order_id 只保留 revision 最小的记录"；v2 第 1 条要求"同一 order_id 保留 revision 最大的记录"。依据"新版优先"原则，按 **v2 第 1 条**执行（保留最大 revision）。

## 二、总体结论

| 指标 | 数值 |
|---|---|
| 有效订单数 | **4** |
| 净金额合计 | **450.50** |
| 排除记录数 | **4** |

- 净金额口径：净金额 = amount − refund（v2 第 5 条），按十进制计算，金额保留两位小数。
- 明细汇总见 `summary.csv`；排除记录及原因见 `exceptions.csv`。

## 三、分区域汇总（按区域中文名排序）

| region | net_amount | valid_orders |
|---|---:|---:|
| 华东 | 130.50 | 2 |
| 华南 | 320.00 | 2 |

### 华东（净金额 130.50，有效 2 单）

| order_id | amount | refund | 净金额 | 依据 |
|---|---:|---:|---:|---|
| o1 | 100.00 | 20.00 | 80.00 | status=paid（v2 第 2 条），金额合法（第 3 条），refund≤amount（第 4 条） |
| o5 | 50.50 | 0.00 | 50.50 | status=paid（v2 第 2 条），金额合法（第 3 条），refund≤amount（第 4 条） |

### 华南（净金额 320.00，有效 2 单）

| order_id | amount | refund | 净金额 | 依据 |
|---|---:|---:|---:|---|
| o2 | 200.00 | 0.00 | 200.00 | status=paid（v2 第 2 条），金额合法（第 3 条），refund≤amount（第 4 条） |
| o6（revision=2） | 130.00 | 10.00 | 120.00 | 同 order_id 保留最大 revision 记录（v2 第 1 条）；status=paid（第 2 条），金额合法（第 3 条），refund≤amount（第 4 条） |

## 四、排除记录及原因

判定按 v2 第 1→4 条顺序进行，每条排除记录只写第一个适用的原因代码（v2 第 6 条）。

| order_id | 原因代码 | 定位说明 |
|---|---|---|
| o3 | not_paid | status=cancelled，非 paid，命中 v2 第 2 条 |
| o4 | invalid_number | amount=abc 为非合法数字，命中 v2 第 3 条 |
| o6 | duplicate_older_revision | 同一 order_id 存在 revision=1 与 revision=2 两条记录，按 v2 第 1 条保留 revision 最大的记录，排除较旧的 revision=1 记录；原因代码按条款标注，order_id 不追加 revision 后缀 |
| o7 | refund_exceeds_amount | refund=60 > amount=40，命中 v2 第 4 条 |

## 五、口径与备注

- 排除记录明细见 `exceptions.csv`，字段顺序为 `order_id,reason`。
- 汇总明细见 `summary.csv`，字段顺序为 `region,net_amount,valid_orders`。
- 本次核对仅读取输入目录中的 `orders.csv`、`policy-v1.md`、`policy-v2.md`，未改写任何输入文件。
