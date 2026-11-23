# 区域订单核对报告

## 1. 数据与政策范围

- 订单数据：`inputs/orders.csv`，共 8 行记录、7 个不同 `order_id`（`o6` 有 revision 1 与 revision 2 两条记录）。
- 命中政策：`inputs/policy-v1.md`、`inputs/policy-v2.md` 两份政策对同一事项给出相反规则，存在版本冲突：
  - v1 第 1 条规定「按 amount 原额汇总」，即不做退款扣减；
  - v1 第 2 条规定「同一 order_id 只保留 revision **最小**的记录」；
  - v2 第 5 条明确规定净金额 `= amount - refund`；v2 第 1 条规定「保留 revision **最大**的记录」。
- 处理决定：按「政策冲突以版本号较新的政策为准」的要求，**采用 policy v2（`inputs/policy-v2.md`）**，v1 整体被替代（v2 标题即注明「替代v1」，见 `policy-v2.md` 第 1 行）。因此上述 v1 的两条规则均不适用。

## 2. 采用的政策条款（policy-v2.md）

| 条款 | 内容 | 用途 |
| --- | --- | --- |
| 第 1 条 | 同一 order_id 保留 revision 最大的记录，较旧记录排除，原因 `duplicate_older_revision` | 去重 |
| 第 2 条 | 仅统计 status 为 `paid` 的记录，其他排除，原因 `not_paid` | 状态过滤 |
| 第 3 条 | amount 与 refund 必须是非负合法数字，否则排除，原因 `invalid_number` | 数值校验 |
| 第 4 条 | refund 超过 amount 时排除，原因 `refund_exceeds_amount` | 逻辑校验 |
| 第 5 条 | 净金额 = amount − refund，按 region 汇总净金额与有效订单条数；十进制计算；按第 1→4 条顺序检查，每条排除记录只写第一个适用原因 | 计算与汇总 |

## 3. 核对过程

按 policy-v2 第 5 条要求的「条款 1 → 4」顺序逐条判定：

1. **去重（第 1 条）**：`o6` 的两条记录中，revision 2（amount 130、refund 10）为最大 revision，予以保留；revision 1（amount 120、refund 10）被排除，原因 `duplicate_older_revision`。按第 1 条要求，例外文件中的 `order_id` 写被排除记录的原始 id，不追加 revision 后缀，故记为 `o6`。
2. **状态（第 2 条）**：`o3` 状态为 `cancelled`，排除，原因 `not_paid`。
3. **数值（第 3 条）**：`o4` 的 amount 为 `abc`，不是合法数字，排除，原因 `invalid_number`。该记录在第 3 条即被拦截，不再进入第 4 条判断。
4. **退款上限（第 4 条）**：`o7` 的 refund 60 大于 amount 40，排除，原因 `refund_exceeds_amount`。

其余 4 条记录通过全部检查，为有效订单。

### 有效订单明细

| order_id | region | amount | refund | 净金额 |
| --- | --- | --- | --- | --- |
| o1 | 华东 | 100 | 20 | 80.00 |
| o2 | 华南 | 200 | 0 | 200.00 |
| o5 | 华东 | 50.50 | 0 | 50.50 |
| o6（revision 2） | 华南 | 130 | 10 | 120.00 |

### 排除记录明细

| order_id | revision | 命中条款 | reason |
| --- | --- | --- | --- |
| o6 | 1 | policy-v2 第 1 条 | duplicate_older_revision |
| o3 | 1 | policy-v2 第 2 条 | not_paid |
| o4 | 1 | policy-v2 第 3 条 | invalid_number |
| o7 | 1 | policy-v2 第 4 条 | refund_exceeds_amount |

## 4. 汇总结果

按区域中文名（拼音）升序排列：

| region | net_amount | valid_orders |
| --- | --- | --- |
| 华东 | 130.50 | 2 |
| 华南 | 320.00 | 2 |

- 华东：o1 的 80.00 + o5 的 50.50 = 130.50，有效订单 2 条。
- 华南：o2 的 200.00 + o6（revision 2）的 120.00 = 320.00，有效订单 2 条。
- **有效订单数合计：4 条**
- **净金额合计：450.50**

金额均以十进制精确计算并保留两位小数（如 50.50 与 130.50 不含浮点误差）。

## 5. 关键结论与依据定位

- 采用版本：policy v2 —— 依据 `inputs/policy-v2.md` 第 1 行「政策 v2（替代v1）」及任务要求「冲突以版本号较新的政策为准」。
- 净金额口径为 amount − refund，而非 v1 的 amount 原额 —— 依据 `inputs/policy-v2.md` 第 5 条；若误用 v1 第 1 条，o1、o6 的退款 20、10 将不被扣减，合计会虚高。
- `o6` 保留 revision 2、排除 revision 1 —— 依据 `inputs/policy-v2.md` 第 1 条。若沿用 v1 第 2 条保留最小 revision，o6 会取 120 而非 130，华南净额将变为 310.00。
- 合计 450.50 与 4 条有效订单 —— 由 `orders.csv` 中 o1、o2、o5、o6(revision 2) 四行经 policy-v2 第 5 条计算得出；排除项 o3、o4、o6(revision 1)、o7 分别对应 policy-v2 第 2、3、1、4 条。

## 6. 产物说明

- `outputs/summary.csv`：列序 `region,net_amount,valid_orders`，仅含两个区域汇总行。
- `outputs/exceptions.csv`：列序 `order_id,reason`，包含全部 4 条排除记录，`order_id` 为原始 id。
- 本报告：`outputs/report.md`。

输入文件 `orders.csv`、`policy-v1.md`、`policy-v2.md` 均未做任何修改。
