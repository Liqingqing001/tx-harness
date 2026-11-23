# tx-harness：五款 Harness 竞品评测
作者：Li Qing 李晴（Liqingqing001）
仓库：https://github.com/Liqingqing001/tx-harness

截至 11 月 23 日，已归档 56/60 场、85/90 轮正式实验，另有 20 场校准试跑。[最新结果与产品差距](reports/2026-11-23-formal.md) · [逐轮验收](runs/formal-v1.1/2026-11-23-rounds.csv) · [正式逐题初评](runs/formal-v1.1/review-2026-11-23/scorecard.md)

评测对象为 Codex、WorkBuddy、DeepSeek Harness（DSH）、元宝专家模式和豆包工作（独立客户端）。

## 仓库文件树

想了解每款产品能做什么，读[五款产品主要功能调研](reports/2026-11-20-product-functions.md)。

看设计，从 [完整评测方案](docs/evaluation-plan-v1.md) 开始；看五款产品各自的优点和不足，读 [正式实验报告](reports/2026-11-23-formal.md)；核对某个结论，到 [正式实验原件](runs/formal-v1.1/evidence/) 或 [校准试跑原件](runs/pilot-20261119/) 找对应文件。

下面用元宝的一场订单实验展开重复目录。其他产品和轮次可按同样的命名查找。

```text
tx-harness/
├── README.md                       仓库首页与阅读指南
├── CHANGELOG.md                    每次更新了哪些方案、证据或结论
├── LICENSE                         原创代码与材料的许可
├── .gitignore                      指定 Git 应忽略的本地文件
├── docs/                           评测怎么做、怎么打分、怎么判断原因
│   ├── evaluation-plan-v1.md       主方案：任务、控制变量、评分及结论边界
│   ├── protocol.md                 实验协议入口
│   ├── methodology.md              方法来源，以及本项目采用了哪些做法
│   ├── case-review.md              如何根据现场和产物复核问题、判断归因
│   └── product-matrix.csv          记录产品版本、模式、模型和技能的配置表
├── cases/                          给产品的题目、输入及验收条件
│   ├── T01/                        早期订单处理用例，正式排期从 T02 开始
│   ├── T02/                        订单核对：先做全区域汇总，再改为只看华东
│   │   ├── task.md                 任务提示、轮次和完成条件
│   │   ├── inputs/                 给产品的订单表和两版政策
│   │   ├── input-manifest.json     输入文件指纹，用来核对各次使用的材料
│   │   ├── expected/               评审用的参考结果，用于比对产品交付
│   │   └── rubric.json             逐项评分标准及所需证据
│   ├── T03/                        原样复制文件并交付清单
│   ├── T04/                        整理会议待办，再修改指定记录
│   ├── T05/                        主文件损坏时用备用数据恢复
│   └── backlog.md                  候选用例
├── runs/                           每次实验实际发生了什么
│   ├── TEMPLATE.md                 单次运行的记录模板
│   ├── pilot-20261119/             校准试跑原件，按任务、产品、轮次保存
│   │   └── artifact-manifest.json  试跑原件清单与文件指纹
│   └── formal-v1.1/                正式实验的规则、排期和现场证据
│       ├── freeze.md               正式实验采用哪一版协议
│       ├── schedule.csv            60 场的运行编号、顺序、产品及轮数
│       ├── config-preflight.md     运行前配置核对，后续复查也保存在本目录
│       ├── review-amendment-20261119.md  匿名复评规则的修改记录
│       ├── blind-review-sealed.csv 封存的匿名复评结果
│       ├── pilot-adjudication.md   对试跑评分分歧的裁决和理由
│       └── evidence/               正式运行实际交付的文件和检查结果
│           ├── dispatch-notes.md   实际投递顺序及偏离排期的原因
│           └── T02-yuanbao-1/      示例：订单题、元宝、第 1 次独立运行
│               ├── observations.md 这场运行观察到了什么、哪些判断仍待核实
│               ├── round1/         首轮原件与检查结果
│               └── round2/         同一会话收到变更要求后的交付
│                   ├── summary-r2.csv     产品生成的区域汇总
│                   ├── exceptions-r2.csv  产品生成的异常订单明细
│                   ├── report-r2.md       产品对结果与规则的解释
│                   ├── checks.json        评测者的逐项自动检查结果
│                   └── archive.json       归档文件大小和 SHA-256 指纹
├── scripts/                        用来检查产品交付物的程序
│   ├── check_t01.py                检查早期 T01 用例
│   ├── check_t02.py                检查订单汇总和异常明细
│   └── check_office.py             检查 T03–T05 的文件复制、清单或 CSV
├── tests/                          验证评分脚本本身能否识别正确和错误样例
│   ├── test_check_t02.py           订单校验器测试
│   └── test_check_office.py        其他办公任务校验器测试
└── reports/                        根据实验材料写出的分析与周报
    ├── 2026-11-20-product-functions.md   五款产品主要功能、官方资料与实测例子
    ├── 2026-11-20-comparative.md   五款产品的优点、不足及证据
    ├── 2026-11-20-stage.md         阶段发现，含元宝、WorkBuddy 个案复核
    ├── evidence-yuanbao/           元宝应用内预览截图，可与下载文件对照
    ├── pilot-20261119.md           校准试跑报告
    ├── report-template.md          评测报告模板
    └── weekly/                    按日期保存的个人周报及草稿
```

**复核示例。** 要看元宝为什么漏列一条订单，可以依次打开 [第二轮应有的异常清单](cases/T02/expected/exceptions-r2.csv)、[元宝实际交付的清单](runs/formal-v1.1/evidence/T02-yuanbao-1/round2/exceptions-r2.csv)、[元宝自己的解释](runs/formal-v1.1/evidence/T02-yuanbao-1/round2/report-r2.md) 和 [评分脚本的检查结果](runs/formal-v1.1/evidence/T02-yuanbao-1/round2/checks.json)。

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

正式设计：4任务 × 5产品 × 3次 = 60个完整试验，共90轮，执行依据见[正式协议冻结记录](runs/formal-v1.1/freeze.md)。每任务25%，先报告任务完成率，再报告分数与未知项区间。结果、过程、根因分开，无法控制模型和Skill时不宣称纯Harness因果排名。

输入均为合成数据，只给产品对应 inputs/ 和任务提示，不上传评分标准或答案。T03/T04/T05评分条款写在任务卡；输入哈希见各自input-manifest.json。新增自动验收器 scripts/check_office.py 已覆盖 T03 字节/清单及 T04/T05 CSV；报告、下载与过程仍须人工验收。
T02已有CSV验收器：`python scripts/check_t02.py --outputs <产物目录> --round 1`（第二轮用2）。它仅核验CSV，不替代人工验收。
校验器测试：`python -m unittest discover -s tests -v`。

[运行模板](runs/TEMPLATE.md) / [报告模板](reports/report-template.md) / [ChangeLog](CHANGELOG.md) / [周报草稿](reports/weekly/2026-11-21-draft.md)

方案与脚本由AI辅助起草，执行者负责审核、实测和结论。公开证据需脱敏；不得上传账号令牌、私人记录或企业资料。原创代码和材料采用MIT许可，第三方材料遵循其许可。
