# 数据恢复与读取报告

## 采用来源

实际采用来源：**backup.csv**

依据 readme.txt 的读取顺序：先检查 `primary.json` 是否为合法 JSON；若不合法，则使用 `backup.csv` 的全部记录，不修复主文件、不混合两个来源。本次严格遵循该规则。

## 主输入可用性

- 主输入 `primary.json`：**不可用**
- 判断依据：文件内容为 `{"items":[{"item_id":"b01","units":3},{"item_id":"b02","units":}]}`，其中第二条记录的 `units` 字段值为空（`"units":` 后缺少数值），不符合 JSON 语法，解析时报错：`Expecting value: line 1 column 48 (char 47)`。
- 处理方式：按 readme 要求未对主文件做任何修复或改写，直接判定为不可用并改用备用文件。

## 数据记录

数据来自 `backup.csv`，按 `item_id` 升序排列：

| item_id | units |
|---------|-------|
| b01     | 3     |
| b02     | 5     |

## 统计结果

- 数据记录数：**2 条**
- units 合计（总件数）：**8**（3 + 5）

## 输出文件

- `items.csv`：列顺序为 `item_id,units`，按 `item_id` 升序排列。
- `recovery.md`：本说明报告。
