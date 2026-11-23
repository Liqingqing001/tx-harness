# 数据恢复报告

## 实际采用的来源

**backup.csv（全部记录）**。输出 `items.csv` 完全由该文件的 2 条记录生成，未混入 `primary.json` 的任何内容。

## 主输入可用性及判断依据

- **主输入 `primary.json`：不可用（不是合法 JSON）。**
- 判断依据：按 `readme.txt` 要求，先用 JSON 解析器对 `primary.json` 做合法性校验，解析失败：
  `JSONDecodeError: Expecting value: line 1 column 64 (char 63)`。
  具体原因是第二个对象中 `"units":` 后缺少值（`{"item_id":"b02","units":}`），属于语法错误，无法解析出完整的 `items` 数组。
- 依据 `readme.txt` 的规则「若合法则读取 items 数组；若不合法，使用 backup.csv 全部记录」，本次改用备用文件。
- 未修复、未改写 `primary.json`；未将两个来源的数据混合；未编造缺失数据（例如没有把 `b02` 的空值补成任何数字）。

## 统计结果

| 项目 | 数值 |
| --- | --- |
| 数据记录数 | 2 |
| 总件数（units 列求和） | 8 |

## 输出说明

- `items.csv` 列顺序为 `item_id,units`，按 `item_id` 升序排列（b01、b02）。
- `units` 取值：b01 = 3，b02 = 5，均直接来自 `backup.csv`，合计 3 + 5 = 8。
