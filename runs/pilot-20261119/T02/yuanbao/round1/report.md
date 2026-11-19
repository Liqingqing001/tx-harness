# 区域订单核对报告

## 核对结论

- **采用政策：v2**（`policy-v2.md` 明示“替代v1”）；v1 的“保留最小 revision、按 amount 原额汇总”不再适用。
- **有效订单数：4 单**。
- **净金额合计：450.50**（按 `amount − refund` 十进制计算；v2 条款5）。
- **区域排序**：按中文名排序，华东在前、华南在后。

## 区域汇总

| region | net_amount | valid_orders |
|---|---:|---:|
| 华东 | 130.50 | 2 |
| 华南 | 320.00 | 2 |

## 排除记录及原因

按 v2 条款1→4 顺序判定；每条仅记录首个命中原因。

| order_id | 原始记录（revision / status / amount / refund） | reason | 定位 |
|---|---|---|---|
| o3 | rev1 / cancelled / 80 / 0 | `not_paid` | status=cancelled；适用 v2 条款2 |
| o4 | rev1 / paid / abc / 0 | `invalid_number` | amount=`abc`，非合法数字；适用 v2 条款3 |
| o6 | rev1 / paid / 120 / 10 | `duplicate_older_revision` | revision=1 < 最大 revision=2；适用 v2 条款1 |
| o7 | rev1 / paid / 40 / 60 | `refund_exceeds_amount` | refund=60 > amount=40；适用 v2 条款4 |

## 关键结论与溯源

1. **华东净金额为 130.50，含 o1、o5 两笔有效订单。**
   - o1：100 − 20 = 80.00（v2 条款5）。
   - o5：50.50 − 0 = 50.50（v2 条款5）。
   - 排除：o3 因 `cancelled` 命中 v2 条款2；o7 因退款 60 超过原额 40 命中 v2 条款4。
2. **华南净金额为 320.00，含 o2、o6（rev2）两笔有效订单。**
   - o2：200 − 0 = 200.00（v2 条款5）。
   - o6 先按 v2 条款1保留 rev2（130 − 10 = 120.00），故 rev1 作为 `duplicate_older_revision` 排除；但 rev2 随后在 v2 条款4因 refund=10 ≤ amount=130 通过，故华南有效净额应含 o6 rev2：200+120=320.00。
   - o4 的 amount=`abc`，在 v2 条款3排除。
3. **版本冲突处理**：v2 明确替代 v1，因此 o6 取最大 revision（v2 条款1），且统一扣减 refund（v2 条款5）；若误采 v1，会错误得到华东 230.50、华南 450.00 的原额口径。

## 复核口径

- 金额为 Decimal 精确十进制运算，输出统一保留两位；订单条数按通过全部校验的“记录/订单版本”计数。
- 输入文件未改写；本任务仅新增 `summary.csv`、`exceptions.csv`、`report.md`。