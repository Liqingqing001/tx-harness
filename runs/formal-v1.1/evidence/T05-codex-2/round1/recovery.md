# 数据恢复报告

- 处理依据：inputs/readme.txt。先验证 primary.json；若 JSON 不合法，则使用 backup.csv 全部记录，不修复主文件、不混合来源，按 item_id 升序输出。
- 主输入可用性：主输入不可用：严格 JSON 解析失败，Expecting value（第 1 行，第 64 列）。第二条记录 b02 的 units 冒号后直接出现右花括号，缺少合法 JSON 值。
- 实际采用来源：inputs/backup.csv，使用全部记录；未从主输入提取或补造数据。
- 数据记录数：2 条（不含表头）。
- 总件数：8 件（units 列求和：3 + 5 = 8）。
- 输出：items.csv，列顺序为 item_id,units，记录按 item_id 升序排列。
- 输入保护：primary.json、backup.csv、readme.txt 均未修改，处理前后 SHA-256 校验一致。
