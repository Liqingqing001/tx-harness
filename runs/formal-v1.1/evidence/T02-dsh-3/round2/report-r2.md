# 区域订单核对报告（第二轮：仅统计华东）

## 1. 本轮变更范围

第二轮仅调整**统计范围**：由第一轮的「全部区域」收窄为「仅华东」。其余规则一律沿用第一轮，未做任何改动：

- 政策版本仍为 **policy v2**（`inputs/policy-v2.md`），v1 因版本冲突且已被 v2 明文替代而不适用；
- 去重规则不变（v2 第 1 条，保留 revision 最大的记录）；
- 状态、数值、退款上限校验不变（v2 第 2、3、4 条）；
- 净金额口径不变（v2 第 5 条，净金额 = amount − refund，十进制计算，按条款 1→4 顺序取首个适用原因）；
- 金额两位小数、按区域中文名排序等格式要求不变。

本轮唯一新增的规则是排除原因代码 **`out_of_scope`**：用于「原本能通过第 1–4 条全部检查、但不属于华东」的订单。该代码附于原有四条规则之后判定，因此不会掩盖任何更靠前的排除原因。

## 2. 采用的政策条款（policy-v2.md，延续第一轮）

| 条款 | 内容 | 本轮作用 |
| --- | --- | --- |
| 第 1 条 | 同一 order_id 保留 revision 最大的记录，较旧记录排除，原因 `duplicate_older_revision` | 去重（o6） |
| 第 2 条 | 仅统计 status 为 `paid` 的记录，其他排除，原因 `not_paid` | 状态（o3） |
| 第 3 条 | amount、refund 必须是非负合法数字，否则排除，原因 `invalid_number` | 数值（o4） |
| 第 4 条 | refund 超过 amount 时排除，原因 `refund_exceeds_amount` | 退款（o7） |
| 第 5 条 | 净金额 = amount − refund，按 region 汇总净金额与有效条数；按第 1→4 条顺序检查，每条只写第一个适用原因 | 计算与汇总 |

## 3. 核对过程（按条款顺序判定）

1. **去重（第 1 条）**：`o6` 保留 revision 2（amount 130、refund 10），revision 1（amount 120、refund 10）排除为 `duplicate_older_revision`。按第 1 条要求，例外文件写原始 `order_id`，不追加 revision 后缀。
2. **状态（第 2 条）**：`o3` 为 `cancelled`，排除为 `not_paid`。
3. **数值（第 3 条）**：`o4` 的 amount 为 `abc`，排除为 `invalid_number`（在第 3 条即被拦截，不再进入后续判断）。
4. **退款上限（第 4 条）**：`o7` 的 refund 60 大于 amount 40，排除为 `refund_exceeds_amount`。
5. **范围（新增 `out_of_scope`）**：通过前四条、但 region 不是华东的记录排除为 `out_of_scope`，共 2 条：
   - `o2`（华南，200 − 0 = 200.00）：第一轮为有效订单，本轮因范围收窄被排除；
   - `o6` 的 revision 2（华南，130 − 10 = 120.00）：第一轮为有效订单，本轮同样因范围收窄被排除。

> 说明：`o6` 在 `exceptions-r2.csv` 中出现两次是有意为之——一次对应被去重排除的 revision 1（`duplicate_older_revision`），一次对应范围外被排除的 revision 2（`out_of_scope`）。两条对应不同原始记录，且按第 1 条不得追加 revision 后缀，故 `order_id` 均为 `o6`。

### 有效订单明细（全部为华东）

| order_id | region | amount | refund | 净金额 |
| --- | --- | --- | --- | --- |
| o1 | 华东 | 100 | 20 | 80.00 |
| o5 | 华东 | 50.50 | 0 | 50.50 |

### 排除记录明细（共 6 条）

| 顺序 | order_id | revision | 命中条款 | reason |
| --- | --- | --- | --- | --- |
| 1 | o2 | 1 | 新增范围规则 | out_of_scope |
| 2 | o3 | 1 | policy-v2 第 2 条 | not_paid |
| 3 | o4 | 1 | policy-v2 第 3 条 | invalid_number |
| 4 | o6 | 1 | policy-v2 第 1 条 | duplicate_older_revision |
| 5 | o6 | 2 | 新增范围规则 | out_of_scope |
| 6 | o7 | 1 | policy-v2 第 4 条 | refund_exceeds_amount |

（表内顺序与 `exceptions-r2.csv` 一致，采用输入文件 `orders.csv` 的行顺序，与第一轮的排序规则相同。）

## 4. 汇总结果（本轮）

| region | net_amount | valid_orders |
| --- | --- | --- |
| 华东 | 130.50 | 2 |

- 华东：o1 的 80.00 + o5 的 50.50 = **130.50**，有效订单 **2 条**。
- **有效订单数合计：2 条**
- **净金额合计：130.50**

## 5. 前后合计对比

| 指标 | 第一轮（全部区域） | 第二轮（仅华东） | 变化 |
| --- | --- | --- | --- |
| 区域数 | 2（华东、华南） | 1（华东） | −1 |
| 有效订单数 | 4 | 2 | −2 |
| 净金额合计 | 450.50 | 130.50 | −320.00 |
| 排除记录数 | 4 | 6 | +2 |

分区域对照：

| region | 第一轮净金额 / 单数 | 第二轮净金额 / 单数 | 差异 |
| --- | --- | --- | --- |
| 华东 | 130.50 / 2 | 130.50 / 2 | 无变化 |
| 华南 | 320.00 / 2 | 不统计 | −320.00 |
| 合计 | 450.50 / 4 | 130.50 / 2 | −320.00 / −2 |

差异说明：减少的 320.00 与 2 条订单，恰好是第一轮华南的两条有效订单——`o2`（200.00）与 `o6` revision 2（120.00），本轮转为 `out_of_scope`。华东部分数值与第一轮完全一致，说明本轮收窄范围未影响华东的判定与计算，可交叉验证第一轮结果的正确性。

## 6. 关键结论与依据定位

- 采用版本 policy v2 —— `inputs/policy-v2.md` 第 1 行「政策 v2（替代v1）」；本轮相对第一轮未重新选版。
- 净金额口径 amount − refund —— `policy-v2.md` 第 5 条；故 o1 计 80.00 而非 100。
- `o6` 取 revision 2 —— `policy-v2.md` 第 1 条；其虽通过前四条检查，但 region 为华南，按本轮新增范围规则排除为 `out_of_scope`。
- `o2` 为 `out_of_scope` —— `orders.csv` 中 o2 的 region 为华南，订单本身合规（paid、200、refund 0），仅因范围收窄被排除，故不能标为 `not_paid` 等既有代码。
- 合计 130.50、2 条 —— 由 `orders.csv` 中 o1、o5 两行经 policy-v2 第 5 条计算得出。

## 7. 产物说明

- `outputs/summary-r2.csv`：列序 `region,net_amount,valid_orders`，本轮仅含华东一行。
- `outputs/exceptions-r2.csv`：列序 `order_id,reason`，共 6 条排除记录，含新增的 `out_of_scope`。
- 本报告：`outputs/report-r2.md`。
- 第一轮产物 `summary.csv`、`exceptions.csv`、`report.md` 未改动、未覆盖。
- 输入文件 `orders.csv`、`policy-v1.md`、`policy-v2.md` 均未做任何修改。
