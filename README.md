# 五款 Harness 竞品评测

作者：Li Qing 李晴（Liqingqing001）

仓库：https://github.com/Liqingqing001/harness-benchmark

[评测协议](docs/protocol.md) · [首个用例](cases/T01/task.md) · [ChangeLog](CHANGELOG.md) · [周报草稿](reports/weekly/2026-11-21-draft.md)

状态：准备阶段，尚无产品实测数据或排名。对象：Codex、Workbuddy、DSH、元宝专家模式、豆包办公。DSH 指 DeepSeek Harness，官方入口：https://www.deepseek.com/harness/。

## 开始顺序
1. 确认五款产品入口、版本、套餐、可用工具、模型是否可选、是否支持自定义 Skill。填写 docs/product-matrix.csv。
2. 冻结 docs/protocol.md 和 cases/T01 下的任务与输入，提交 Git；之后修改需升版本。
3. 每款先跑 T01 一次作为试跑，检查证据采集和验收方法，不纳入正式排名。
4. 正式评测采用三个任务，每款每任务三个独立新会话，共 45 次；资源不足时先完成 15 次并标为探索性结果。随机交错运行产品，保存顺序。
5. 填写每次运行记录，核验证据后打分，形成报告和周报。

目录：docs 为方案；cases 为用例和输入；runs 为脱敏现场；scripts 为验收代码；reports 为报告与周报。所有正式结果须指向公开证据及对应 Git 提交。

## 开源提交
本项目公开仓库已创建：https://github.com/Liqingqing001/harness-benchmark 。发布前移除个人信息、账号令牌、内部材料及未获授权的截图。不要上传真实客户资料或产品私有配置。按所用素材许可决定可公开范围，并补充合适的代码许可证。

每周六更新 CHANGELOG、周报及仓库。公告末尾也提到周六/日，按较严格的周六执行。下一次为 2026-11-21。邮件收件人以公告列出的四个地址为准；本项目没有自动发信或设定定时任务。
