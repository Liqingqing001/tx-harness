# tx-harness：五款 Harness 竞品评测

作者：Li Qing 李晴（Liqingqing001）

仓库：https://github.com/Liqingqing001/tx-harness

状态：评测体系 v0.2，待试跑校准。没有真实产品分数或排名。

比较对象：Codex、WorkBuddy、DeepSeek Harness（DSH）、元宝专家模式、豆包办公。

## 评测路线
先选核心任务，定义二元检查项；固定输入、配置与预算，多次运行；同时评估交付结果和执行过程；复核异常的原因及评分是否正确；将问题加入回归集。

- [协议与评分](docs/protocol.md)：端到端、过程、可比性及统计口径。
- [参考方法与适配边界](docs/methodology.md)：参考美团方案，不复制其图表或正文。
- [主用例 T02](cases/T02/task.md)：政策冲突、异常订单、多文件交付及第二轮范围修改。
- [二元 Rubric](cases/T02/rubric.json)：检查项、证据与自动/人工分工。
- [T01](cases/T01/task.md)：环境检查，不计入主要竞品排名。
- [运行记录](runs/TEMPLATE.md) / [归因与案例池](docs/case-review.md)
- [报告模板](reports/report-template.md) / [ChangeLog](CHANGELOG.md) / [周报草稿](reports/weekly/2026-11-21-draft.md)

## 首次执行
1. 填写 docs/product-matrix.csv，确认指定模式可用；不可见信息填 unknown。
2. 五款各试跑 T02 一次，试跑不进正式结果；校准任务歧义、时间预算和评分一致性。
3. 冻结协议、输入哈希、Rubric 和版本提交。正式每款做三次独立完整两轮试验，共15次；仅支持这一任务的探索性结论。
4. 按 runs/TEMPLATE.md 留存原始产物、对话和可公开过程证据。
5. 执行 `python scripts/check_t02.py --outputs <产物目录> --round 1`；第二轮改为 `--round 2`。自动验收不替代人工验收。
6. 报告各条检查项、成功次数/有效试验次数、人工介入、时间和可观测覆盖率；归因另列。

测试校验器：`python -m unittest discover -s tests -v`。

主评测不挂载本人的日常自定义 Skill。无法关闭的内置 Skill 如实记录，不宣称纯 Harness 因果排名。不得把标准答案、校验代码、Rubric 或整个仓库当作任务附件，只给 task.md 指定的 inputs 文件与提示。

正式运行前继续补充独立任务族；T02 两轮不是两个独立样本。T03 暂为后续挑战任务，不混入当前分母。

每周六更新仓库、ChangeLog及周报。代码和原创材料采用 MIT；第三方材料遵循原许可。公开证据须脱敏，不上传令牌、个人文件或内部业务数据。
