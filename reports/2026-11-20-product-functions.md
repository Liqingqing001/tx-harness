# 五款 Harness 产品主要功能调研报告

调研日期为 2026 年 11 月 20 日。本文所说的 Harness，是用户从布置任务到拿到结果所经过的产品层，包括工作区、附件、工具、权限和交付界面。

**五款产品都能接收业务材料，并在订单核对任务中交付 CSV 和 Markdown。选用哪款，首先看工作从哪里开始、最后交给谁。** 改代码并审查差异，可以从 Codex 入手。把日常办公步骤交给助手连续执行，可以看 WorkBuddy。需要自定义插件、检查工具调用，可以看 DSH。手里有几份附件、希望在对话里读完并导出结果，可以看元宝专家模式。需要围绕一组材料制作表格、文稿或演示，再与飞书协作，可以看豆包工作。这些使用场景有重叠。[本项目五款产品的交付记录](https://github.com/Liqingqing001/tx-harness/blob/main/reports/2026-11-20-comparative.md)

## 五款产品分别能做什么

### Codex 桌面端 · 修改项目并审查差异

给它一个项目目录，可以让它读代码、改文件、运行命令和测试，再逐项查看改动。同一项目里的多项开发任务可以用不同的 Git 工作树并行处理。反复使用的工作步骤可以封装为技能，也可以配置自动化。它对开发者特别有用的一点，是交付后还能检查具体改了哪几行。[OpenAI 桌面端功能说明](https://openai.com/index/introducing-the-codex-app/)

**本项目用到的功能。** Codex 从本地材料核对订单。第二轮缩小统计范围后，它保留第一轮文件，另行写出新版明细和说明，方便前后对照。这个样本验证了本地文件的读取、修改与交付。并行开发和定时自动化属于官方资料覆盖的能力。[Codex 第二轮交付](https://github.com/Liqingqing001/tx-harness/blob/main/runs/formal-v1.1/evidence/T02-codex-2/round2/report-r2.md)

### WorkBuddy · 把多步办公任务交给助手

可以用自然语言布置任务，让它拆分步骤、读取授权目录，整理表格、生成文档并交付文件。任务可按项目分组，专家、技能和连接器可用来复用业务流程或接入其他服务。目录权限和连接器配置会影响它能拿到哪些材料。[腾讯云 WorkBuddy 产品说明](https://cloud.tencent.com/product/workbuddy)

**本项目用到的功能。** 它能一次交付订单明细和配套报告。会议任务试跑暴露了多文件交付的一个问题：改完的待办表里负责人正确，简报回顾变更时却写错了原负责人。对需要留痕的工作，应把表格和说明放在一起验收。[订单交付](https://github.com/Liqingqing001/tx-harness/blob/main/runs/formal-v1.1/evidence/T02-workbuddy-2/round2/report-r2.md) · [会议试跑裁决](https://github.com/Liqingqing001/tx-harness/blob/main/runs/formal-v1.1/pilot-adjudication.md)

### DeepSeek Harness（DSH）· 工作区、插件与执行记录

DSH 是开源的桌面工作台。用户可以在工作区里处理代码、文档和表格，通过插件扩充工具，也可用“创造模式”制作插件。官方提供开发者工具查看执行时间线和工具调用。对需要调查某一步读了什么、调用了什么工具的团队，这个入口值得关注。[DeepSeek 产品说明](https://deepseek.com/harness/) · [官方开源仓库](https://github.com/deepseek-ai/deepseek-harness)

**本项目用到的功能。** DSH 在工作区读取输入、写出新版订单结果和异常说明，并列出变动文件。现有归档可以复核交付内容。本次没有归档完整内部调用记录，因此无法从这份材料还原每一步的工具参数。[DSH 第二轮交付](https://github.com/Liqingqing001/tx-harness/blob/main/runs/formal-v1.1/evidence/T02-dsh-2/round2/report-r2.md)

### 腾讯元宝桌面端专家模式 · 在对话里分析附件并导出

专家模式面向复杂问题的分析和推理。本次使用的是元宝桌面客户端里的“专家模式”。用户在对话中上传材料、补充或修改要求，再通过结果卡片预览和下载文件。对临时收到几份材料、希望直接拿到分析结果的用户，这条操作路径较短。[元宝官方专家模式活动说明](https://apps.apple.com/cn/app/id6480446430?eventid=6808534521) · [桌面端预览与下载记录](https://github.com/Liqingqing001/tx-harness/blob/main/reports/2026-11-20-stage.md)

**本项目用到的功能。** 元宝读入订单材料，两次独立运行都算对变更后的总额。第一次交付的异常表只有 5 条，应有 6 条。它在说明中写明，同一订单号已经有一条异常，因此省略了新版记录。第二次交付列全了记录。这个例子能定位到用户拿到的异常清单和采用的合并口径，内部由模型、技能还是写表工具作出该决定仍待验证。[第一次的处理说明](https://github.com/Liqingqing001/tx-harness/blob/main/runs/formal-v1.1/evidence/T02-yuanbao-1/round2/report-r2.md) · [第二次的处理说明](https://github.com/Liqingqing001/tx-harness/blob/main/runs/formal-v1.1/evidence/T02-yuanbao-2/round2/report-r2.md)

### 豆包工作独立客户端 · 处理办公材料并衔接协作

围绕同一项工作，可以让它查资料、写文档、分析表格、制作可视化或演示稿，也可以继续指定要修改的部分。官方还介绍了与飞书文档协同的用法。能读取哪些组织资料、把成果交给谁，取决于登录身份和授权范围。本项目调查的入口是豆包工作独立客户端。[飞书发布的豆包工作功能介绍](https://www.feishu.cn/content/article/7677519271848610746)

**本项目用到的功能。** 豆包工作在本地电脑模式下处理输入，交付订单表格与说明，第二轮按新范围更新。文件复制试跑还观察到调用表格技能。现有证据覆盖本地办公文件流程，飞书组织协作和演示稿制作有待另行验证。[豆包工作第二轮交付](https://github.com/Liqingqing001/tx-harness/blob/main/runs/formal-v1.1/evidence/T02-doubao-2/round2/report-r2.md) · [试跑与正式实验汇总](https://github.com/Liqingqing001/tx-harness/blob/main/reports/2026-11-20-comparative.md)

## 怎么理解这份调研

官方资料回答“产品提供哪些入口”，留存的文件回答“这一次实际交付了什么”。五款产品的订单任务都遇到了同一个范围变更，结果都从 4 单、450.50 调整为 2 单、130.50。对这几个数，可以用原件复核。对稳定性，当前可比较的正式样本是每款两次独立订单任务；文档中的会议整理和文件复制属于校准试跑。不同产品使用的模型、内置技能和权限存在差异，因此一次漏行或一次说明写错，只足以说明当次交付出了什么问题。判断是哪一层造成，还需要能区分这些原因的对照或内部记录。[评测方案](https://github.com/Liqingqing001/tx-harness/blob/main/docs/evaluation-plan-v1.md) · [综合报告与证据](https://github.com/Liqingqing001/tx-harness/blob/main/reports/2026-11-20-comparative.md)
