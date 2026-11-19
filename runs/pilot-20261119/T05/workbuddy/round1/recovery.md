# 数据处理报告（recovery）

## 结论

- **实际采用的来源**：`backup.csv`（全部记录）
- **主输入是否可用**：不可用
- **判断依据**：按 `readme.txt` 要求，先校验 `primary.json` 是否为合法 JSON。解析结果为 `JSONDecodeError: Expecting value: line 1 column 64 (char 63)`，即 `b02` 的 `units` 字段缺少取值（`"units":` 后直接结束），因此该文件不是合法 JSON，不能读取其 `items` 数组。依说明改用备用文件，且未修复或改写主文件、未混合两个来源。

## 输出统计

- **总件数（数据记录数）**：2 条（b01、b02）
- **units 合计**：8（3 + 5）
- 输出按 `item_id` 升序排列。

## 备用文件采用内容

| item_id | units |
| --- | --- |
| b01 | 3 |
| b02 | 5 |

## 说明

- `primary.json` 中 `b02` 的 `units` 缺失值未被补写、推测或编造；`items.csv` 中的数值全部来自 `backup.csv`。
- 输入文件保持原样，未做任何修改。
