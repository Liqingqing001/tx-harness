# 区域订单核对报告（第二轮：仅统计华东）

## 一、本轮结论

- 统计范围：**仅华东区域**；华南订单一律不计入汇总。
- 采用政策：**policy-v2.md（政策 v2）**，与第一轮一致；v1 因去重规则冲突仍不适用。
- 有效订单数：**2 条**（o1、o5，均为华东）
- 净金额合计：**130.50**
- 被排除记录：**6 条**，其中新增 `out_of_scope` 2 条（o2、o6 revision 2）

## 二、变更范围

本轮相对第一轮（`summary.csv`、`exceptions.csv`、`report.md`）只做一项变更：

1. **统计口径收窄为华东**：新增排除原因代码 `out_of_scope`，用于“按政策 v2 第1—4条原本有效、但不属于华东”的订单。该判定放在原有第1—4条检查之后执行，因此不影响既有排除原因的判定顺序。

保持不变的部分：

- 政策版本仍为 v2（v2 标注“替代v1”，版本更新，冲突以 v2 为准）。
- 去重规则（v2 第1条：同一 order_id 保留 revision 最大者，较旧记录记 `duplicate_older_revision`）。
- 状态规则（v2 第2条：仅 paid，其余记 `not_paid`）。
- 数值规则（v2 第3条：非负合法数字，否则 `invalid_number`；v2 第4条：refund > amount 记 `refund_exceeds_amount`）。
- 净金额公式（v2 第5条：amount − refund，十进制计算，两位小数）。
- 列名与格式：`region,net_amount,valid_orders` 与 `order_id,reason` 均沿用第一轮。
- 第一轮三份文件保留未覆盖。

## 三、有效订单明细（华东）

| order_id | region | amount | refund | revision | 净金额 | 政策依据 |
|---|---|---|---|---|---|---|
| o1 | 华东 | 100 | 20 | 1 | 80.00 | v2 第2、5条 |
| o5 | 华东 | 50.50 | 0 | 1 | 50.50 | v2 第2、5条 |

- 华东小计：80.00 + 50.50 = **130.50**，**2 条**。
- 本轮合计：**130.50**，**2 条**。

## 四、排除记录及原因（6 条）

| order_id | 区域 | 原始数据 | 原因代码 | 说明与政策依据 |
|---|---|---|---|---|
| o2 | 华南 | amount 200，refund 0，status paid，revision 1 | `out_of_scope` | 按 v2 第1—4条本为有效记录（净额 200.00），但不属于华东，按本轮范围排除。 |
| o3 | 华东 | amount 80，status cancelled，revision 1 | `not_paid` | v2 第2条：状态非 paid。 |
| o4 | 华南 | amount `abc`，status paid，revision 1 | `invalid_number` | v2 第3条：amount 非合法数字；数值校验先于范围判定，故不记 `out_of_scope`。 |
| o6 | 华南 | amount 120，refund 10，status paid，revision 1 | `duplicate_older_revision` | v2 第1条：同一 order_id 存在 revision 2，保留最大版本，rev1 排除。 |
| o6 | 华南 | amount 130，refund 10，status paid，revision 2 | `out_of_scope` | rev2 为去重后保留记录，按 v2 第1—4条本有效（净额 120.00），但不属于华东，按本轮范围排除。 |
| o7 | 华东 | amount 40，refund 60，status paid，revision 1 | `refund_exceeds_amount` | v2 第4条：refund 60 > amount 40；金额校验先于范围判定。 |

补充说明：

- **o6 在例外文件中出现两行**：revision 1 因去重被排除（`duplicate_older_revision`），revision 2 虽通过去重与金额校验，但属华南、被本轮范围排除（`out_of_scope`）。两条记录对应同一 order_id 的不同 revision，故 `order_id` 列相同。
- 例外文件仍按 v2 第1条只写原始 order_id，不追加 revision 后缀。
- 判定顺序为：去重 → 状态 → 数值 → 退款上限 → 范围；每条记录只写第一个适用原因，因此 o4 记 `invalid_number` 而非 `out_of_scope`。

## 五、前后合计对比

| 项目 | 第一轮（全区域） | 第二轮（仅华东） | 变化 |
|---|---|---|---|
| 有效订单数 | 4 | 2 | −2 |
| 净金额合计 | 450.50 | 130.50 | −320.00 |
| 华东小计 | 130.50（2 条） | 130.50（2 条） | 不变 |
| 华南小计 | 320.00（2 条） | 0.00（0 条） | −320.00 |
| 例外记录数 | 4 | 6 | +2（新增 `out_of_scope`：o2、o6 rev2） |

- 减少的 320.00 与 2 条有效订单，全部来自华南：o2（200.00）与 o6 revision 2（120.00）。
- 华东自身数据与第一轮一致，未受范围调整影响。

## 六、复核提示

- 数据源仍为 `orders.csv`、`policy-v1.md`、`policy-v2.md` 三份附件，未改写输入文件。
- 金额保留两位小数；本轮仅一个区域，排序无歧义。
- 原始 orders.csv 共 8 条数据行，去重后 7 条；排除 o3、o4、o7 及范围外的 o2、o6，得有效华东订单 2 条。
