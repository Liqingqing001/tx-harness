# 数据来源与结果说明（T05-doubao-3）

## 1. 实际采用的来源

**最终数据来源：`inputs/backup.csv`（全量记录，2 条）。**

主输入 `inputs/primary.json` 未被采用，其内容未被修改、未被修补、也未与备用文件混用。

## 2. 主输入是否可用

**不可用。**

判断依据（按 `readme.txt` 第 1 条：先检查 `primary.json` 是否为合法 JSON）：

- 用标准 JSON 解析器读取时直接报语法错误：`Unexpected character encountered while parsing value: }. Path 'items[1].units', line 1, position 63`。
- 定位到 `items` 数组的第 2 个元素（`item_id` 为 `b02`）：`"units":}` —— **冒号后没有任何值**，直接跟了右花括号，属于结构性缺失，不是编码或读取问题。
- 文件完整内容（67 字节，无截断迹象）：

```
{"items":[{"item_id":"b01","units":3},{"item_id":"b02","units":}]}
```

- 该错误无法通过“按 schema 容错读取”绕过：缺失的 `units` 数值本身未知，任何补值都属于编造数据，故按 `readme.txt` 规则整体弃用主文件、改用备用文件。

## 3. 备用文件校验

| 检查项 | 结果 |
| --- | --- |
| 列结构 | `item_id,units`，与要求一致 |
| 记录数 | 2 |
| 空值 / 非数字 `units` | 0 行（校验通过） |
| `item_id` 重复 | 无 |

即 `backup.csv` 可完整、干净地承载本次输出，无需任何修复或补值。

## 4. 数据统计

| 指标 | 数值 |
| --- | --- |
| 数据记录数 | **2** 条 |
| units 合计 | **8** |
| item_id 明细 | b01 = 3，b02 = 5（3 + 5 = 8） |

## 5. 交付文件说明

- `items.csv`：列顺序 `item_id,units`，按 `item_id` 升序排列，共 2 行数据（不含表头），UTF-8 纯文本、无 BOM、LF 换行。

```
item_id,units
b01,3
b02,5
```

- 未对任何输入文件执行写入、改名或覆盖；输入目录下三个文件保持原始状态。
