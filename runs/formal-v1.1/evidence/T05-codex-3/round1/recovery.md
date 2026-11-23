# 数据恢复报告

- 实际采用的来源：inputs/backup.csv，采用全部记录。
- 主输入可用性：inputs/primary.json 不可用，未通过 JSON 语法解析。
- 判断依据：b02 的 units 字段冒号后直接出现右花括号，缺少 JSON 值。实际解析错误：Expecting value（第 1 行，第 64 列）。
- 处理规则：依照 readme.txt，主输入不是合法 JSON 时使用备用文件全部记录；未修复主输入，未混合两个来源，未编造缺失数据。
- 输出：items.csv，列顺序为 item_id,units，按 item_id 升序排列。
- 数据记录数：2 条（不含表头）。
- 总件数：8（units 列求和：3 + 5 = 8）。
- 输入保护：三个输入文件均未改写，处理前后 SHA-256 校验一致。
