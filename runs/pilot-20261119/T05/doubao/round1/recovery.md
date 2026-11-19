# 数据恢复报告（recovery.md）

## 一、实际采用的来源

- **采用来源：`backup.csv`（备用文件）**，使用其中全部记录。
- 未使用 `primary.json` 中的任何数据；两个来源未混合，主文件未做任何修复或改写。

## 二、主输入是否可用及判断依据

- **主输入 `primary.json` 不可用（非法 JSON）。**
- 判断依据：
  1. 按 `readme.txt` 第 1 条规则，先检查 `primary.json` 是否为合法 JSON。
  2. 使用 JSON 解析器严格解析，返回错误：`Unexpected character encountered while parsing value: }. Path 'items[1].units', line 1, position 63.`
  3. 具体问题：第二条记录 `{"item_id":"b02","units":}` 中 `units` 字段缺少取值，JSON 语法不完整，无法被合法解析。
- 处置方式：依据 `readme.txt` 规则，主文件不合法时改用 `backup.csv` 的全部记录；未对主文件进行修复，也未从中手工提取残缺数据。

## 三、统计结果

| 指标 | 数值 |
|---|---|
| 总件数（记录条数） | 2 |
| units 合计 | 8 |

## 四、输出明细（按 item_id 升序）

| item_id | units |
|---|---|
| b01 | 3 |
| b02 | 5 |

## 五、输入与交付对照

- 输入目录：`D:\新建文件夹\T05-pilot-20261119\doubao\inputs`（仅读取 `primary.json`、`backup.csv`、`readme.txt`，未修改任何输入文件）。
- 交付目录：`D:\新建文件夹\T05-pilot-20261119\doubao\outputs`
  - `items.csv`：列顺序 `item_id,units`，按 `item_id` 升序。
  - `recovery.md`：本报告。
