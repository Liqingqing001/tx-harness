读取顺序：先检查 primary.json 是否为合法JSON；若合法则读取items数组；若不合法，使用backup.csv全部记录。
不要修复主文件，不混合两个来源。输出按item_id升序排列，统计units合计。报告如实说明来源和主文件可用性。
