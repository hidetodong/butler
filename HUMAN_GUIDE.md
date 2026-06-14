# Butler 使用指南

> 面向人类用户的操作手册。帮助你在实际项目中正确引用 Butler 规则体系，并获得稳定的 AI 协作结果。

## 1. Butler 是什么

Butler 是一个 Markdown 规则仓库，定义了一套**通用需求开发 SOP**，用于规范 AI 辅助工程开发的协作流程。

它的核心价值：把 AI 从"自由发挥的编码助手"变成"按流程交付的工程协作者"。

### 三个子系统

| 子系统 | 入口 | 用途 |
|---|---|---|
| **Coder** | `Coder/README.md` | 工程开发与 AI 协作 |
| Learner | `Learner/README.md` | 学习事务管理 |
| Composer | `Composer/README.md` | 其他杂项事务 |

本指南重点介绍 **Coder** 子系统。

## 2. 核心工作流（必须理解）

所有非极小任务默认走 **P1-P5 流程**：

```
P1 Analysis → P2 Acceptance → P3 Design → P4 Execute → P5 Verify
  理解问题      定义完成        确认方案      编码实现      验证交付
```

### 每个阶段做什么

| 阶段 | AI 产出 | 你需要做什么 |
|---|---|---|
| **P1 Analysis** | `.ai/CONCEPT.md` — 问题理解 | 确认 AI 理解正确 |
| **P2 Acceptance** | `.ai/AC_LIST.md` — 验收清单 | **必须 ACK 才能继续** |
| **P3 Design** | `.ai/TECH_PLAN.md` — 技术方案 | **必须 ACK 才能继续** |
| **P4 Execute** | 代码 / 配置 / 文档 | 观察进度 |
| **P5 Verify** | `.ai/VERIFY_REPORT.md` — 验证报告 | 确认交付 |

**关键点**：P2 和 P3 结束时，AI 必须等你确认（ACK）后才能进入下一阶段。这是你控制交付质量的核心杠杆。

### 简化路径

如果任务完全不命中以下任何升级信号，可以走简化路径（合并 P1+P2，口头确认 P3）：

- 需求有歧义
- 预计修改 ≥ 3 个文件
- 涉及接口 / API / 数据结构变更
- 涉及认证、权限、支付等关键路径
- 跨模块影响
- 需要在多个方案间取舍

**建议**：除非你非常确定任务很小，否则走完整流程。AI 倾向于高估自己的理解、低估任务复杂度。

### 迭代号与固定需求

每一轮 P1-P5 是一个**迭代**，有一个确定的迭代号 `ITER-NNNN`（单调递增，记在 `.ai/ITERATIONS.md` 台账里）。它的意义是把"这一轮固定了哪些需求、产出了哪套文档"钉死，方便回溯：

- **固定需求**：你在 P2 ACK 验收清单后，这一迭代的范围就**冻结**了。之后小幅改动可以重新 ACK（记一条修订记录）；但影响面明显扩大时，AI 会开**下一个迭代号**承接，而不是把范围悄悄塞进当前迭代。
- **落对应文档**：当前迭代的四件套（CONCEPT / AC_LIST / TECH_PLAN / VERIFY_REPORT）始终在 `.ai/` 固定路径；迭代收口时它们会被快照进 `.ai/iterations/ITER-NNNN/` 冻结归档，并落一份 `deliveries/ITER-NNNN-<slug>.md` 交付总结。
- **你的杠杆**：想开新一轮需求时，直接说"这算新迭代"；想确认当前进度时，让 AI 读 `.ai/ITERATIONS.md` 台账即可。

## 3. 安装（一次性）

在 butler 仓库目录下执行：

```bash
./scripts/setup.sh
```

它会自动完成两件事：

1. 在 `~/.zshrc`（或 `~/.bashrc`）中写入 `BUTLER_PATH` 环境变量
2. 在 `~/.claude/CLAUDE.md` 中写入全局配置，让 Claude Code 在所有项目中都能自动发现 butler

执行完后重启终端（或 `source ~/.zshrc`）。之后你**不需要再告诉 AI butler 在哪**。

## 4. 接入新项目

安装完成后，在任何项目中启动 AI 会话，直接给任务即可：

```
帮我实现用户登录功能
```

AI 会自动走完整个链路：

1. 从全局配置发现 butler 路径 → 读取 `Coder/README.md` 入口
2. 按读取顺序建立规则上下文（identity → logic-protocol → lifecycle …）
3. 检测到当前项目没有 `.ai/` 目录 → 识别为新项目接入 → 自动触发基地车部署
4. 部署完成后，按 P1-P5 流程推进你的任务

部署完成后，项目根目录会生成 CLAUDE.md（内联浓缩规则卡 + 完整规则指针）。后续会话 AI 直接从项目 CLAUDE.md 读取规则，**全局配置不再参与**。

你也可以显式说"部署基地车"来手动触发部署，效果一样。

### 部署后的目录结构

```
你的项目/
├── .ai/
│   ├── CONCEPT.md          # P1 产物 = 当前迭代工作区
│   ├── AC_LIST.md           # P2 产物 = 当前迭代工作区
│   ├── TECH_PLAN.md         # P3 产物 = 当前迭代工作区
│   ├── VERIFY_REPORT.md     # P5 产物 = 当前迭代工作区
│   ├── ITERATIONS.md        # 迭代台账（迭代号/状态/所属 milestone/交付链接）
│   ├── iterations/          # 各迭代收口快照（ITER-NNNN/，按需产生）
│   ├── MILESTONES.md        # 里程碑台账（大版本，按需产生）
│   ├── MILESTONE.md         # 当前里程碑工作区：范围评估/理解阐释/拆分路线图（按需产生）
│   ├── milestones/          # 各里程碑收口快照（MILE-NNNN/，按需产生）
│   ├── local-constraints.md # 本地化约束
│   ├── 00_IDEATION.md       # 脑暴产物（/ideation 模式）
│   ├── 01_CHANGELOG.md      # 技术决策日志
│   ├── 02_SESSION_HANDOFF.md # 跨会话恢复入口
│   ├── 03_BUG_LOG.md        # RCA 报告
│   ├── task-state.md        # 运行时状态
│   └── references/          # 外部参考资料（按需创建）
└── deliveries/              # 交付总结归档
    ├── ITER-NNNN-<slug>.md  #   迭代交付（小版本），平铺即时间线
    └── milestones/          #   里程碑交付（大版本），MILE-NNNN-<slug>.md
```

## 5. 扩展模式

Butler 提供若干可选扩展模式，通过指令或语义触发，默认不启用：

| 模式 | 触发方式 | 用途 |
|---|---|---|
| **Ideation** | `/ideation` 或 "脑暴"、"完善需求"、"想不清楚"、"还没想好" | 需求脑暴与完善 |
| **收敛闭环** | `/loop` 或 "死磕"、"必须变绿" | 高强度纠错升档（死磕到绿 + 定量熔断）；底线由常驻纠错收口契约保证 |
| **Review** | `/review` 或 "看看写得怎么样"、"代码审查" | 代码审计 |
| **Dangerous** ⚠️ | `/dangerous` 或 "放手做"、"自己跑完"、"别等我确认" | 实验性无人值守长程自治：自动拆迭代连续推进、P2/P3 ACK 由自审门替代，附审计/回滚/P5 强制审查护栏。仅在可隔离、可回滚环境用 |
| **Preference** ⚠️ | `/preference on`/`off`(隐私总关) · `reback on`/`off` · `distill` | 实验性偏好探针：采集你的设计取舍、蒸馏跨项目通识，在**有监督**工作里改进提议。采集经一次同意默认开、反哺 opt-in，详见下方 |

### 里程碑（大版本）

迭代之上还可套一层**里程碑** `MILE-NNNN`，作为"大可交付版本"。当一批需求跨多个迭代、需要先整体圈定范围再拆分推进时，AI 会提议开里程碑：先写一份范围评估 + 理解阐释 + 拆分路线图（`.ai/MILESTONE.md`），与你 soft 对齐后，期间开启的迭代自动归属它；大版本收口时聚合各迭代产出一份版本级交付（`deliveries/milestones/MILE-NNNN-<slug>.md`）。里程碑是可选、松耦合的：不影响你按迭代推进的习惯，迭代历史在 `deliveries/` 根仍是一条连续时间线。

### `/preference` 偏好探针（实验性）

让 AI 在长期协作中**学习你的设计风格**，并在你**在场**时用它给出更合你意的提议。

**它怎么工作**

1. **采集**（经一次同意后默认开）：AI 在你做关键决策时（选项选择、打回方案、直接纠正）把你的**取舍倾向**记成信号。首次会问你一次是否同意，答应后就默认在 butler 项目里自动攒，随时可 `/preference off` 全关。
2. **蒸馏**（默认开）：在迭代/里程碑收口或你说 `/preference distill` 时，把信号归纳成偏好。**一条偏好要在 ≥2 个不同项目里一致出现，才会晋级为"跨项目通识"**——单项目重复不算，避免把局部口味当普适。
3. **反哺**（默认关，`/preference reback on` 才开）：开启后，AI 只在**有监督**工作里（P2/P3 提案、选项排序）参考你的风格，把你常选的前置或设默认——你随时能否决。

**关键边界**

- **只学你亲手的选择，不学模型自己的**。`/dangerous` 无人值守模式**完全不碰偏好**：既不参考、也不把模型的自主决策记成你的偏好。偏好是"人在回路"的东西，模型自己跑的时候用不上它。
- **反哺只是参考，不是命令**。偏好永远压不过你当下的明确指令；你这次怎么说就怎么来，AI 还会把这次"偏好让位于指令"记下来修正自己。
- **数据存在 butler 仓库之外**（默认 `~/.butler/preferences/`，可用 `BUTLER_PREF` 指定），跨项目共用、与规则仓库解耦。只记决策倾向的抽象，**不记业务数据或敏感内容**。
- **不碰你的迭代**。探针是旁路观察者，从不写 `.ai/`、不卡流程，坏了也不影响迭代。
- 想看它学到了什么，让 AI 读 `~/.butler/preferences/profile.md` 的"通识层"即可。（首次采集会自动初始化外置存储；也可手动跑 `./scripts/preference-init.sh`。）

## 6. 常见问题与对策

### AI 跳过了 P1-P5 直接写代码

**原因**：AI 把任务判定为"极小"走了简化路径，或者根本没读规则。

**对策**：
- 确认 CLAUDE.md / .cursorrules 已正确配置
- 明确要求："请按 P1 开始分析"
- 如果 AI 跳过，直接打断："回到 P1，先产出 CONCEPT.md"

### AI 读了规则但执行不稳定

**原因**：规则文件太多，AI 在长上下文下 instruction-following 退化。

**对策**：
- 在 CLAUDE.md 中内联最关键的约束（而不是只写文件路径引用）
- 分阶段提醒："我们现在在 P2，请产出 AC_LIST.md"
- 每个阶段结束时显式 ACK，强化 AI 对流程的感知

### 基地车部署失败或不完整

**原因**：AI 没有先执行侦察（Scouting），直接开始创建文件。

**对策**：
- 明确要求："先侦察项目环境，再展开基地车"
- 检查 AI 是否先读了 `mcv-deployment.md`

### 跨会话丢失上下文

**原因**：上一个会话没有产出 `02_SESSION_HANDOFF.md`。

**对策**：
- 在结束会话前告诉 AI："请生成 02_SESSION_HANDOFF.md"
- 新会话开始时："请读取 .ai/02_SESSION_HANDOFF.md 恢复上下文"

## 7. 获得稳定结果的核心原则

1. **规则必须自动注入**：靠 CLAUDE.md 或等价机制，不要靠手动每次粘贴。
2. **核心约束内联到注入文件**：最关键的 3-5 条规则直接写在 CLAUDE.md 里，不要只留文件路径。
3. **按阶段推进**：不要一次性把任务和所有上下文倒给 AI。先 P1，确认后 P2，确认后 P3...
4. **显式 ACK 是你最强的杠杆**：P2 和 P3 的 ACK 机制保证 AI 不会跑偏。用好它。
5. **及时打断**：发现 AI 偏离流程时立即纠正，不要等它做完再返工。
6. **长任务分段交接**：超过一个会话能完成的任务，务必让 AI 生成 handoff 文件。

## 8. 规则体系速查

```
Coder/
├── 00_System_Prompt/          # 身份与总调度
│   ├── identity.md            # 角色定义与工程哲学
│   └── logic-protocol.md      # 读取协议、模块激活、流程总调度
├── 10_Domain_Stack_Profiles/  # 技术栈规则（按需启用）
├── 20_Workflow_Lifecycle/     # 核心工作流
│   ├── lifecycle.md           # P1-P5 状态机（最重要）
│   ├── concept-schema.md      # P1 产物模板
│   ├── acceptance-schema.md   # P2 产物模板
│   ├── tech-plan-schema.md    # P3 产物模板
│   ├── verify-schema.md       # P5 产物模板
│   ├── iteration-schema.md    # 迭代号/台账/锁定纪律
│   ├── milestone-schema.md    # 里程碑（大版本）号/台账/路线图/版本级交付
│   ├── delivery-summary.md    # 交付总结规范
│   ├── mcv-deployment.md      # 基地车部署协议
│   ├── mcv-update.md          # 基地车升级协议
│   ├── progressive-handoff.md # 渐进式交接
│   └── maintenance-boundaries.md # 维护边界
├── 30_Quality_Gate/           # 质量门禁
│   ├── linting.md             # 提交前自检清单
│   ├── testing-strategy.md    # 测试分层与验收映射
│   ├── review-standard.md     # 通用审计准则
│   └── correction-contract.md # 纠错收口契约（P4 常驻底线）
├── 40_Context_Management/     # 上下文治理（长任务必读）
│   ├── context-persistence.md # 状态外化与阶段结晶
│   ├── handoff-spec.md        # 02_SESSION_HANDOFF.md 格式契约
│   └── role-switch.md         # Architect/Coder/Reviewer 角色切换
├── 50_Extension_Ideation/     # 脑暴扩展
├── 55_Extension_ConvergenceLoop/ # 收敛闭环扩展（/loop 升档）
├── 60_Extension_CodeReview/   # 代码审查扩展
├── 65_Extension_Dangerous/    # 无人值守长程自治扩展（实验性）
├── 70_Extension_Preference/   # 偏好探针扩展（实验性，外置存储）
└── 99_Business_Extension/     # 业务约束（最高优先级）
```
