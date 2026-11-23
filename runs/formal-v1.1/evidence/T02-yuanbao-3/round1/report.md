# 区域订单核对报告

## 核对结论

- **采用政策：v2（替代 v1）**。v2 标题明确替代 v1，故按“最大 revision 去重 → paid 过滤 → 数值校验 → 退款校验 → 计算净额”执行；不采用 v1 的“最小 revision、amount 原额汇总”。
- **有效订单数：4 单**；**净金额合计：450.50**。
- 净金额口径为 `amount − refund`，使用 Decimal 十进制计算，并按 v2 第5条按区域汇总。

| 区域 | 净金额 | 有效订单数 |
|---|---:|---:|
| 华东 | 130.50 | 2 |
| 华南 | 320.00 | 2 |

## 关键结论与订单定位

- **华东：净金额 130.50，有效 2 单。** 有效记录：o1（revision 1，80.00）、o5（revision 1，50.50）。
- **华南：净金额 320.00，有效 2 单。** 有效记录：o2（revision 1，200.00）、o6（revision 2，120.00）。
- **两区各贡献 2 单，华南金额略高**：最大单笔为华南 o2（200.00）；华东由 o1（80.00）与 o5（50.50）构成。华东 o7 的 60.00 退款不能作为负收入冲抵，而应在 refund>amount 时整单排除（v2 第4条）。
- **华南有效 2 单、净额 320.00**：o2 贡献 200.00；o6 先按 v2 第1条保留 revision 2，再以 130−10 得 120.00。o4 因 `abc` 无法参与金额计算，o6 的 revision 1 不重复计入。

## 排除记录及原因

| 订单编号 | 被排除的原始记录 | 原因代码 | 首个命中条款 |
|---|---|---|---|
| o6 | revision 1 | `duplicate_older_revision` | v2 第1条：同一 order_id 仅保留最大 revision；按原始编号输出 |
| o3 | revision 1 | `not_paid` | v2 第2条：仅统计 status=paid |
| o4 | revision 1 | `invalid_number` | v2 第3条：amount/refund 须为非负合法数字 |
| o7 | revision 1 | `refund_exceeds_amount` | v2 第4条：refund 不得超过 amount |

**顺序判定说明：** o6 的 revision 1 在 v2 第1条即排除，因此不再进入第2—4条；其余三条均在最新版本上判定，且每条只记录首个适用原因。

## 核对边界与勾稽

- 原始 8 行 = 有效 4 行 + 排除 4 行，覆盖完整，无未分类记录。
- `exceptions.csv` 仅含规定列 `order_id,reason`；`duplicate_older_revision` 按要求保留原始订单号 o6，不写 o6_1。
- 输入文件未改写；脚本仅从 `/data/inputs/orders.csv`、`policy-v1.md`、`policy-v2.md` 读取，结果写入工作目录。
- 金额为最终展示值两位小数；计算过程未做二进制浮点累加。
