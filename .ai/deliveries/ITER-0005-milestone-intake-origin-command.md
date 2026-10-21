# ITER-0005 里程碑录入交互优化：一次性 brief + /milestone 命令

## 本次交付目标
优化里程碑模式的人机录入交互：让用户能在一处一次性讲清想推进的大版本，由模型据此合成里程碑概述（`.ai/MILESTONE.md`）并拆出迭代承接路线图，方便后续逐迭代开发。录入支持对话与文件两通道，操作走"轻量命令 + 语义触发并存"。

## 已完成内容
- **`origin/` 收件箱**：基地车部署时在项目根创建 `.ai/`、`deliveries/`、`origin/` 三类目录。`origin/` 是人类原始概念输入收件箱（用户自管、AI 只读不重塑不归档），与 AI 处理改名注入的 `.ai/references/` 显式区分。
- **两通道 brief 录入 + 合成协议（`milestone-schema.md` §6.4）**：① 对话直接讲清，或 ② 把原始概念文件投到 `origin/` 让模型读取。模型把意图落成 `.ai/MILESTONE.md` 三段（范围评估/理解阐释/拆分路线图），信息缺口显式标"待澄清"而非臆造，产出后 soft 对齐（非硬门）。brief 非权威，合成后 `.ai/MILESTONE.md` 为唯一真源。
- **轻量命令（`milestone-schema.md` §6.5）**：`/milestone` 开启/录入、`/milestone status` 只读看板（范围/路线图进度/含迭代/下一个 planned）；与语义触发等价，open/status 之外仍走语义。
- **SSOT 传播与文档同步**：rule-card（模板经占位符自动继承）、HUMAN_GUIDE（§4 目录树 + §5 用法/命令）、Coder/README（描述 + 命令/目录注册）、lifecycle §P1（`/milestone` 等价入口句）。

## 关键变更 / 使用者可感知变化
- 开里程碑不再靠零散对话边问边拼：一次性说清（对话或 `origin/` 文件）→ 模型生成概述 + 路线图。
- 新增项目部署后根目录多一个 `origin/` 收件箱，用户把原始想法丢进去即可。
- 多了 `/milestone` 与 `/milestone status` 两个可选命令入口（不输命令、用自然语言同样生效）。
- 迭代号仍"开启时绑、不预先占号"：路线图只给主题切片 + 预计跨度，不把全局号钉死。

## 高层影响范围
- 规则层：`Coder/20_Workflow_Lifecycle/{milestone-schema,mcv-deployment,lifecycle}.md`、`Coder/README.md`、`templates/rule-card.md`、`HUMAN_GUIDE.md`。
- 不涉及（零改动护栏）：`iteration-schema.md`、`templates/hooks/**`、`acceptance-schema.md`、其它扩展模块、Composer/Learner。

## 验证方式与结果摘要
- 逐 AC（AC0–AC10）grep 关键句命中各目标文件，11/11 通过。
- AC6 SSOT 单写：`templates/CLAUDE.md.template` 仅 `{{RULE_CARD_CONTENT}}` 占位符、0 处手写里程碑内容。
- AC10 零改动：`git diff --name-only` 确认 iteration-schema/hooks/acceptance 未动；§5.3 不预先占号原文保留；里程碑"不冻结/不被 hook 拦"否定式表述未被破坏。
- 详见 `.ai/iterations/ITER-0005/VERIFY_REPORT.md`。

## 已知剩余风险 / 延后事项
- 命令为语义约定（非真实 slash-command），长上下文识别可能不稳——与现有 `/ideation` 同源同险，靠 rule-card 高注意力登记缓解。
- `origin/` 为部署时创建的空目录（git 不跟踪空目录，首次投放文件即出现）。
- 把 `origin/` 推广为普通迭代 P1 概念等其它录入流的通道，属后续迭代候选，本轮未做。

## 引用
- `.ai/iterations/ITER-0005/CONCEPT.md`
- `.ai/iterations/ITER-0005/AC_LIST.md`
- `.ai/iterations/ITER-0005/TECH_PLAN.md`
- `.ai/iterations/ITER-0005/VERIFY_REPORT.md`
