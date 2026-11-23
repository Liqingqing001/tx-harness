# 数据恢复报告

## 结论

- 实际采用的来源：`backup.csv`（全部记录，未做任何筛选或补值）
- 主输入 `primary.json`：不可用（非法 JSON），已按 readme 规则整份回退到备用文件
- 数据记录数：**2 条**
- units 合计：**8**

## 主输入是否可用及判断依据

判定为不可用。依据如下：

1. 文件内容为单行 67 字节，原文为 `{"items":[{"item_id":"b01","units":3},{"item_id":"b02","units":}]}`，第二个对象的 `units` 键只有键名、没有任何值，因而在 `}` 处断开。
2. 用两个独立解析器分别校验，结论一致：
   - .NET `ConvertFrom-Json`：`Unexpected character encountered while parsing value: }. Path 'items[1].units', line 1, position 63`
   - Python `json.load`：`JSONDecodeError: Expecting value: line 1 column 64 (char 63)`
3. 该错误属于结构层面的语法缺陷，不是编码或读取方式问题；readme 明确规定"不要修复主文件"，因此未尝试补写 `units` 的值，也未改动文件。

需要说明的是，主文件中第一条记录 `b01, units=3` 本身是可读的，按 readme"不混合两个来源"的要求，也未把这半条记录并入结果，整体只取 `backup.csv`。

## 备用文件校验

对 `backup.csv` 逐行检查，未发现异常，可直接作为唯一来源：

- 共 3 行，第 1 行为表头 `item_id,units`，与预期列名逐字符一致
- 2 行数据，每行均为 2 个字段，无多余分隔符
- `units` 均为正整数（3、5），无空值、无小数、无非数字
- `item_id` 无重复（b01、b02）
- 无空行，仅文件末尾存在一个换行符（正常结束标记）

## 输出说明

`items.csv`：

- 列顺序固定为 `item_id,units`
- 按 `item_id` 升序排列（b01 → b02）
- 2 行数据记录，UTF-8 无 BOM 编码，换行符 LF
- 写入后已回读复核：记录数 2、units 求和 8、升序成立、每行 2 列、id 唯一

内容明细：

| item_id | units |
| --- | --- |
| b01 | 3 |
| b02 | 5 |

## 统计口径

- 数据记录数：2 条（不含表头）
- units 列求和：3 + 5 = **8**

两个数字均来自 `backup.csv` 的实际内容，未经任何估算或推断。

## 数据完整性声明

- 未修复、未改写、未覆盖任何输入文件，三个输入文件仅以只读方式读取
- 未在两个来源之间做任何混合、拼接或去重合并
- 备用文件中不存在缺失记录，因此没有产生任何编造或填补的数据

输入文件读取时的状态（会话开始后未发生变化，修改时间仍为 2026-11-19 20:53:57）：

| 文件 | 大小（字节） | SHA256 |
| --- | --- | --- |
| readme.txt | 287 | B06234841AD74CC8464BDA7C79F08AA809FC02E7965EFA2CB906E2393D0CB04D |
| primary.json | 67 | 8B1AC812F43D9F47C5C70A17FA6F3A8EC51B7F18DF6D01552B5E5A5AC9896D9D |
| backup.csv | 26 | D0217D75D6F74762162FA070B230AC379734E3FF249A266C961AD388DB2CA2FE |