# 数据恢复报告

- 读取规则：按照 readme.txt，先检查 primary.json 的 JSON 合法性；不合法则采用 backup.csv 的全部记录，不修复主文件、不混合来源，并按 item_id 升序输出。
- 主输入可用性：不可用。实际 JSON 解析失败；第二个对象（item_id 为 b02）的 units 字段冒号后直接出现右花括号，没有合法 JSON 值，因此整个文件不是合法 JSON。
- 实际采用来源：inputs/backup.csv，使用全部记录，未采用主文件中的任何记录，也未推测缺失值。
- 数据记录数：2 条（不包含表头）。
- 总件数：8（units 列求和：3 + 5 = 8）。
- 输出：items.csv，列顺序为 item_id,units；记录按 item_id 升序排列为 b01、b02。
- 输入保护：未修复或改写 primary.json、backup.csv、readme.txt；处理前后 SHA-256 校验一致。