# 数据恢复报告

## 采用的来源

`backup.csv`（全部记录）。

## 主输入可用性

**不可用。**

判断依据：对 `primary.json` 仅做了语法层面的解析校验（未修复、未改写该文件）。解析器报错：

```
json.decoder.JSONDecodeError: Expecting value: line 1 column 64 (char 63)
```

文件原始内容为：

```
{"items":[{"item_id":"b01","units":3},{"item_id":"b02","units":}]}
```

在 `"units":` 之后缺少值（`b02` 的数值被截断），属于非法 JSON。按 readme 规则"先检查 primary.json 是否为合法 JSON；若不合法，使用 backup.csv 全部记录"，因此切换到备用文件，且**未混合两个来源**。

## 数据结果

`items.csv` 已按 `item_id` 升序排列，列顺序为 `item_id, units`。

| item_id | units |
| --- | --- |
| b01 | 3 |
| b02 | 5 |

- **数据记录数**：2
- **总件数（units 列求和）**：8

未对任何输入做修复、补全或改写；`b02` 在主文件中缺失的数值未被编造，其值 `5` 来自 `backup.csv` 的原始记录。
