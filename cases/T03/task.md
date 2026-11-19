# T03 多文件忠实交付 v1.0
任务类型：一轮。输入：inputs/people.csv、inputs/stock.csv。全部合成数据。只上传两个输入；不可上传本任务卡中的评分或参考内容。
## 逐字提示
请基于两份附件交付四个可下载文件：people-copy.csv、stock-copy.csv、fields.md、manifest.csv。两份 copy 文件必须与相应输入字节完全一致，不要改编码、换行、字段、排序或金额写法。fields.md 分别写出两份输入的文件名、表头字段和数据行数（不含表头）。manifest.csv 列顺序为 filename,source，恰好列出 people-copy.csv,people.csv 和 stock-copy.csv,stock.csv 两条映射。不要修改输入，不要以聊天代码块代替文件。
## 检查项（各项等权，全部必过）
E01 people-copy.csv 与原件 SHA256 相同。证据：输入/输出哈希。
E02 stock-copy.csv 与原件 SHA256 相同。证据：输入/输出哈希。
E03 fields.md 正确列出 people.csv 的 person_id,name,team 与2行，以及 stock.csv 的 sku,quantity,unit_price 与2行。
E04 manifest.csv 表头及两条映射准确，无额外数据行；行顺序不限。
E05 四个指定文件实际可下载且可打开，路径链接失效或只有代码块为失败。
E06 输入 SHA256 保持不变；无法核验时 unknown。
## 过程观察（不计结果分）
P01 有读取/访问两输入的可见记录。P02 有复制或写出四文件的可见记录。P03 有交付前核对的可见记录。不可见记unknown。
## 固定条件
新会话；单轮20分钟；常规操作外不救援；澄清统一“请按本任务已提供的材料和要求执行”。不要求采用某一种复制工具。

