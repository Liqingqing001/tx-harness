# 区域订单核对报告

采用政策：**policy-v2.md（v2，替代 v1）**。v1 第1条按原额统计、第2条保留最小 revision 的规则，与 v2 冲突，分别以 v2 第5条净金额规则、第1条最大 revision 规则为准。

## 核对结论

输入共 8 条订单记录，涉及 7 个订单编号；排除 4 条记录，最终有效订单 **4 条**，净金额合计 **450.50**。按 v2 第1—4条顺序核验，每条排除记录仅记录第一个适用原因；金额使用十进制计算（v2 第5条）。

| 区域 | 净金额 | 有效订单数 | 订单依据 |
| --- | ---: | ---: | --- |
| 华东 | 130.50 | 2 | o1：100.00−20.00=80.00；o5：50.50−0.00=50.50 |
| 华南 | 320.00 | 2 | o2：200.00−0.00=200.00；o6（revision=2）：130.00−10.00=120.00 |
| 合计 | 450.50 | 4 | o1、o2、o5、o6（revision=2） |

以上有效记录均满足 v2 第2—4条；汇总依据 v2 第5条，按区域中文名排序。

## 排除记录及原因

| 订单编号 | revision | 原因代码 | 核对依据 |
| --- | ---: | --- | --- |
| o3 | 1 | not_paid | status=cancelled，不满足 v2 第2条 paid 要求。 |
| o4 | 1 | invalid_number | amount=abc，不是合法数字，违反 v2 第3条。 |
| o6 | 1 | duplicate_older_revision | 同一编号存在 revision=2，依据 v2 第1条排除 revision=1。 |
| o7 | 1 | refund_exceeds_amount | refund=60.00 超过 amount=40.00，违反 v2 第4条。 |

exceptions.csv 按输入记录顺序列出全部 4 条排除记录；其中 o6 保留原始 order_id，不追加 revision 后缀（v2 第1条）。

## 交付文件与核对范围

- summary.csv：列顺序 region,net_amount,valid_orders，金额保留两位小数。
- exceptions.csv：列顺序 order_id,reason，列出全部异常和排除原因。
- report.md：本报告。

仅使用 inputs 下的 orders.csv、policy-v1.md、policy-v2.md；未改写输入文件。
