# tx-harness：五款 Harness 竞品评测
作者：Li Qing 李晴（Liqingqing001）
仓库：https://github.com/Liqingqing001/tx-harness

当前状态：**评测方案 v1.0 已设计，新增用例待试跑校准，正式实验尚未冻结。没有五款正式成绩或排名。**
已有 T02 部分试跑原件保存在本地，尚未完整发布为公开证据。试跑不得冒充正式结果。

对象：Codex、WorkBuddy、DeepSeek Harness（DSH）、元宝专家模式、豆包客户端“工作／新工作任务”。

## 先看方案
- [完整评测方案](docs/evaluation-plan-v1.md)：研究目标、四类任务、控制变量、评分、归因、证据和交付。
- [协议入口](docs/protocol.md) / [方法来源与适配](docs/methodology.md)
- [归因与案例复核](docs/case-review.md)

## 四套试卷
| 任务 | 关注点 |
|---|---|
| [T02](cases/T02/task.md) | 政策冲突、订单核对、第二轮改范围与保留旧文件 |
| [T03](cases/T03/task.md) | 两文件忠实复制、说明和清单、真实可下载交付 |
| [T04](cases/T04/task.md) | 会议资料中的干扰指令、第二轮定点修改 |
| [T05](cases/T05/task.md) | 损坏JSON与有效备用CSV、异常说明和恢复 |

正式设计：4任务 × 5产品 × 3次 = 60个完整试验，共90轮；试跑后冻结再执行。每任务25%，先报告任务完成率，再报告分数与未知项区间。结果、过程、根因分开，无法控制模型和Skill时不宣称纯Harness因果排名。

输入均为合成数据，只给产品对应 inputs/ 和任务提示，不上传评分标准或答案。T03/T04/T05评分条款写在任务卡；输入哈希见各自input-manifest.json。新增自动验收器 scripts/check_office.py 已覆盖 T03 字节/清单及 T04/T05 CSV；报告、下载与过程仍须人工验收。
T02已有CSV验收器：`python scripts/check_t02.py --outputs <产物目录> --round 1`（第二轮用2）。它仅核验CSV，不替代人工验收。
校验器测试：`python -m unittest discover -s tests -v`。

[运行模板](runs/TEMPLATE.md) / [报告模板](reports/report-template.md) / [ChangeLog](CHANGELOG.md) / [周报草稿](reports/weekly/2026-11-21-draft.md)

方案与脚本由AI辅助起草，执行者负责审核、实测和结论。公开证据需脱敏；不得上传账号令牌、私人记录或企业资料。原创代码和材料采用MIT许可，第三方材料遵循其许可。
