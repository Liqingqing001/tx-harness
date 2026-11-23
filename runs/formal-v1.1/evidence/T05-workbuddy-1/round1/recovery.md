# 数据恢复说明

## 实际采用的来源
- 采用来源：`backup.csv` 的全部记录（未混合使用 primary.json）。
- 输出文件：`items.csv`，列顺序为 `item_id,units`，按 `item_id` 升序排列。

## 主输入可用性判断
- 主输入：`primary.json`。
- 判断结果：**不可用**。
- 判断依据：按 `readme.txt` 要求先对 `primary.json` 进行 JSON 合法性检查，解析失败并抛出 `JSONDecodeError: Expecting value: line 1 column 64 (char 63)`。文件中 `b02` 记录的 `"units":` 后缺少合法值（紧接 `}`），因此不是合法 JSON，其 `items` 数组不可读取。
- 处理方式：未修复、未改写主文件；未从主文件提取任何记录；未混合两个来源的数据。

## 统计结果
- 数据记录数：**2** 条（b01、b02）。
- 总件数（units 列求和）：**8**（3 + 5）。

## 来源内容说明
- `backup.csv` 原始记录：`b01,3`；`b02,5`。输出按 `item_id` 升序排列即为上述顺序。
- 未编造缺失数据；`items.csv` 中每条记录均直接来自备用文件。
