# 区域订单核对报告（第二轮：仅华东）

## 一、变更范围

| 项目 | 第一轮 | 第二轮 |
|---|---|---|
| 政策版本 | policy-v2.md（替代 v1） | 不变，仍为 policy-v2.md |
| 统计区域 | 全部区域 | **仅华东** |
| 去重规则 | 同一 order_id 保留 revision 最大（v2 第1条） | 不变 |
| 状态规则 | 仅 status = paid（v2 第2条） | 不变 |
| 数字规则 | amount、refund 必须为非负合法数字（v2 第3条） | 不变 |
| 退款规则 | refund ≤ amount（v2 第4条） | 不变 |
| 净额计算 | 净金额 = amount − refund，十进制（v2 第5条） | 不变 |
| 排除原因代码 | duplicate_older_revision / not_paid / invalid_number / refund_exceeds_amount | 新增 **out_of_scope** |

新增规则：**out_of_scope** — 通过 v2 第1—4条、原本有效但 region 不属于华东的订单予以排除。判定位置在 v2 第1—4条之后，因此原有排除原因及其优先级保持不变。

## 二、前后合计对比

| 指标 | 第一轮（全部区域） | 第二轮（仅华东） | 变化 |
|---|---:|---:|---:|
| 有效订单数 | 4 | 2 | −2 |
| 净金额合计 | 450.50 | 130.50 | −320.00 |
| 其中华东 | 130.50 / 2 条 | 130.50 / 2 条 | 0 / 0 |
| 其中华南 | 320.00 / 2 条 | —（全部 out_of_scope） | −320.00 / −2 条 |

华东口径本身未发生变化；合计的减少全部来自 o2 与 o6（revision 2）因区域范围被排除。

## 三、第二轮核对结果

- **有效订单数：2**
- **净金额合计：130.50**
- 区域汇总（按区域中文名排序）：

| region | net_amount | valid_orders |
|---|---:|---:|
| 华东 | 130.50 | 2 |

有效订单明细（净额 = amount − refund，v2 第5条）：

| order_id | region | amount | refund | 净额 |
|---|---|---:|---:|---:|
| o1 | 华东 | 100.00 | 20.00 | 80.00 |
| o5 | 华东 | 50.50 | 0.00 | 50.50 |

## 四、排除记录及原因

检查按 v2 第1条至第4条顺序执行，随后执行第二轮新增的 out_of_scope；每条排除记录只记录第一个适用的原因代码。

| order_id | reason | 依据条款 | 定位说明 |
|---|---|---|---|
| o6 | duplicate_older_revision | v2 第1条 | o6 的 revision 1（amount 120、refund 10）为较旧记录，被保留的 revision 2 排除；例外中 order_id 不追加 revision 后缀 |
| o3 | not_paid | v2 第2条 | 订单 o3 的 status = cancelled |
| o4 | invalid_number | v2 第3条 | 订单 o4 的 amount = abc，不是合法非负数字 |
| o7 | refund_exceeds_amount | v2 第4条 | 订单 o7 的 amount = 40、refund = 60，refund 超过 amount |
| o2 | out_of_scope | 第二轮新增规则 | 订单 o2（华南，净额 200.00）原本有效，但不属于华东 |
| o6 | out_of_scope | 第二轮新增规则 | 订单 o6 的 revision 2（华南，净额 120.00）原本有效，但不属于华东 |

**关于 o6 出现两次**：这是两条不同的订单记录。revision 1 在 v2 第1条去重时被排除（duplicate_older_revision）；revision 2 是该 order_id 唯一保留的记录，通过 v2 第1—4条后，因 region = 华南 在第二轮被排除（out_of_scope）。两者原因不同、对应记录不同，故分别列示。

## 五、计算说明

1. 去重优先：先按 v2 第1条处理同一 order_id 的多版本记录，o6 的 revision 1 不参与后续判定。
2. 顺序判定：对剩余记录依次执行 v2 第2—4条，命中即排除，避免同一记录写入多个原因。
3. 区域过滤：最后对原本有效的记录执行 out_of_scope，仅保留 region = 华东 者。
4. 净额与汇总：以十进制计算净额并保留两位小数，按 region 中文名排序。
5. 第一轮文件 `summary.csv`、`exceptions.csv`、`report.md` 全部保留、未覆盖；三份输入文件亦未作修改。
