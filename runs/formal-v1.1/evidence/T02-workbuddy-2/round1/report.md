# 区域订单核对报告

## 一、采用的政策版本

| 项目 | 内容 |
|---|---|
| 采用版本 | **policy-v2.md（v2）** |
| 依据 | v2 标题明确"替代v1"；v1 与 v2 冲突时按版本号较新者为准 |
| v1 被覆盖的冲突点 | v1 第2条"保留 revision 最小"与 v2 第1条"保留 revision 最大"冲突 → 采用 v2；v1"按 amount 原额汇总"与 v2 第5条"净金额 = amount − refund"冲突 → 采用 v2 |

## 二、核对结果

- **有效订单数：4**
- **净金额合计：450.50**
- 区域汇总（按区域中文名排序：华东 < 华南）：

| region | net_amount | valid_orders |
|---|---:|---:|
| 华东 | 130.50 | 2 |
| 华南 | 320.00 | 2 |
| **合计** | **450.50** | **4** |

有效订单明细（净额 = amount − refund，v2 第5条）：

| order_id | region | amount | refund | 净额 |
|---|---|---:|---:|---:|
| o1 | 华东 | 100.00 | 20.00 | 80.00 |
| o2 | 华南 | 200.00 | 0.00 | 200.00 |
| o5 | 华东 | 50.50 | 0.00 | 50.50 |
| o6（revision 2） | 华南 | 130.00 | 10.00 | 120.00 |

## 三、排除记录及原因

检查按 v2 第1条至第4条顺序执行；每条排除记录只记录第一个适用的原因代码（v2 第5条）。

| order_id | reason | 依据条款 | 定位说明 |
|---|---|---|---|
| o6 | duplicate_older_revision | v2 第1条 | 该 order_id 存在 revision 1（amount 120、refund 10）与 revision 2（amount 130、refund 10）；保留最大 revision 2，排除旧记录。按条款要求，例外中的 order_id 写原始编号，不追加 revision 后缀 |
| o3 | not_paid | v2 第2条 | 订单 o3 的 status = cancelled，非 paid |
| o4 | invalid_number | v2 第3条 | 订单 o4 的 amount = abc，不是合法非负数字 |
| o7 | refund_exceeds_amount | v2 第4条 | 订单 o7 的 amount = 40、refund = 60，refund 超过 amount |

## 四、计算说明

1. 去重优先：先按 v2 第1条处理同一 order_id 的多版本记录，o6 的 revision 1 被排除，不参与后续条款判断。
2. 顺序判定：对剩余记录依次执行 v2 第2—4条，命中即排除，避免同一记录写入多个原因。
3. 净额与汇总：对通过全部检查的 4 条订单按 v2 第5条以十进制计算净额，按 region 汇总条数与净额；金额统一保留两位小数。
4. 输入文件 `orders.csv`、`policy-v1.md`、`policy-v2.md` 均未作修改。
