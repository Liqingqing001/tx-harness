# T05 数据恢复报告

## 结论摘要

| 项目 | 结果 |
| --- | --- |
| 实际采用来源 | `backup.csv`（全部记录） |
| 主输入 `primary.json` 是否可用 | 不可用（非法 JSON，解析失败） |
| 数据记录数 | 2 |
| 总件数（units 求和） | 8 |
| 是否修复或改写输入 | 否 |
| 是否混合两个来源 | 否 |

## 主输入可用性判定

`readme.txt` 规定的读取顺序是：先检查 `primary.json` 是否为合法 JSON，合法则读取 `items` 数组；不合法则使用 `backup.csv` 的全部记录，且不得修复主文件、不得混合两个来源。

对 `primary.json` 做 JSON 解析校验，结果如下：

- 文件大小 67 字节，内容为单行 `{"items":[{"item_id":"b01","units":3},{"item_id":"b02","units":}]}`
- 解析报错：`Unexpected character encountered while parsing value: }. Path 'items[1].units', line 1, position 63.`
- 失败原因：数组第二个元素中，`"units"` 键后面直接出现了 `}`，缺少对应的数值，导致整体不是合法 JSON。

因此按 readme 规则第 2 条，判定主输入不可用，改由 `backup.csv` 提供全部记录。整个过程未对 `primary.json` 做任何修补，也未把主文件中可读出的 `b01=3` 与备用文件拼合使用。

需要说明的是：主文件即便允许容错读取，第二个条目的 `units` 也是缺失的，本报告没有根据推测为其补值；`b02` 的 5 件完全来自 `backup.csv`。

## 数据记录清单

`backup.csv` 共 1 个表头行加 2 个数据行，表头为 `item_id,units`。输出按 `item_id` 升序排列：

| item_id | units |
| --- | --- |
| b01 | 3 |
| b02 | 5 |

- 记录数：2
- 总件数：3 + 5 = 8

## 校验结果

- `item_id` 无重复，排序后与原始顺序一致。
- `units` 两行均为非负整数，无空值、无千分位分隔符或其他非数值字符。
- 输出 `items.csv` 的列顺序为 `item_id,units`，与要求一致，数据行与 `backup.csv` 逐条对应。

## 输入完整性

输入文件仅被读取，未发生任何写入或修改，处理前后 SHA256 一致：

| 文件 | 大小(字节) | SHA256 |
| --- | --- | --- |
| primary.json | 67 | 8B1AC812F43D9F47C5C70A17FA6F3A8EC51B7F18DF6D01552B5E5A5AC9896D9D |
| backup.csv | 26 | D0217D75D6F74762162FA070B230AC379734E3FF249A266C961AD388DB2CA2FE |
| readme.txt | 287 | B06234841AD74CC8464BDA7C79F08AA809FC02E7965EFA2CB906E2393D0CB04D |
