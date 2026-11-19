# 运行记录 v0.2

状态：模板，无产品实测。

## 环境
run_id / 产品 / 入口 / 客户端版本 / 套餐 / 指定模式 / 模型与推理预算 / Skill清单与是否实际加载 / 工具权限 / 记忆设置 / unknown项：
任务版本 / 协议提交SHA / 输入SHA256 / 随机或交错顺序 / 开始结束时间（Asia/Shanghai）/ 各轮时限：
有效运行？如否写故障证据并保留补跑关联。产品失败不得按无效排除。

## 证据目录
inputs-manifest.json、transcript.md、events.jsonl、outputs/round1/、outputs/round2/、evidence/、grading.json、case-review.md。
只归档本次任务所需的脱敏材料。第一轮完成时立即保存产物快照，第二轮后核验第一轮仍可访问。
events.jsonl 每行：timestamp、round、event_type、tool_or_skill、visible_input、visible_output、status、artifact、evidence_ref。不可见值写unknown，不推测。

## 验收
每轮执行 scripts/check_t02.py，保存JSON输出；补齐人工E项及过程P项。
每项记录 id / pass|fail|unknown|not_applicable / evidence_ref / 理由 / 现象置信度 / 评审人。
明确列出每轮结果分、必过项、整任务成功/失败/未决、过程可观测率、过程通过率和分母。
人工介入：类型、内容、次数、时间；预设权限确认与额外纠正分开。额外纠正后的成功标assisted。

## 归因与评分复核
每个失败关联 docs/case-review.md 的Case记录。原因置信度与现象置信度分开。
初评 / 独立复评或本人隔时复评 / 分歧 / 裁决 / Rubric版本：
