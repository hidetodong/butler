# architecture（模块地图）

> 只摘全貌 + 补成熟度。目录树、读取顺序、各规则一句话职责的**真源在 `Coder/README.md`**（"目录结构" + "规则目录说明" 两节），此处不抄。分层关系真源 `Coder/architecture-overview.md`。

## 三层主干（`Coder/`，所有任务默认走）

三层职责分明、不互窜（这是头号不变量，见 `invariants.md`）：

- **SOP Core**（`00`/`20`/`30`/`40`）——通用主干，任何任务默认加载。
  - `00_System_Prompt` — 协作身份 + 总调度逻辑 + 输出呈现协议（结论先行 / 统一标号 / 表格化 / 说人话）。
  - `20_Workflow_Lifecycle` — P1→P5 状态机 + 四件套 schema + 迭代 / 里程碑 / 版本 / 迁移 / 交付 / 部署规则。**最大一层、骨架所在**。
  - `30_Quality_Gate` — linting / 测试策略 / 复核标准 + P4 常驻底线（纠错契约 `correction-contract`、最小实现纪律 `implementation-discipline`）。
  - `40_Context_Management` — 状态外化、冷启动读序、handoff、知识文件夹契约（`project-digest-schema` 管项目自身全貌 / `references-schema` 管外部参考资料 `.ai/references/` 的索引与渐进读）、角色切换。
- **Domain / Stack Profiles**（`10`）——按项目技术栈**识别后才启用**（vue3 / typescript / build-tooling），不默认前置。
- **Business Extension**（`99`）——业务侧**最高优先级**约束，若存在则压过通用 SOP。当前仓内只有 `.gitkeep`（占位）。

## 扩展模块（按需 / 命令触发，不进冷启动必读）

- `50_Extension_Ideation` — 脑暴 `/ideation`。
- `55_Extension_ConvergenceLoop` — 收敛闭环 `/loop`（P4 纠错的高强度升档）。
- `60_Extension_CodeReview` — 代码复核 `/review`（共享审查流程真源）。
- `62_Extension_Agents` — **帮手名册**：butler 派出去干活的临时子 agent（复核 / 更新说明 / 查过时三帮手 + 通用规矩 G1–G4 唯一真源）。触发式加载、定义不下发到目标项目。
- `65_Extension_Dangerous` — 危险模式 `/dangerous`（实验性无人值守长程自治外壳）。
- `70_Extension_Preference` — 偏好探针 `/preference`（学真人选择、外置存储、反哺 opt-in）。

## 支撑目录（仓库根）

- `templates/` — 部署到目标项目的东西：`CLAUDE.md.template`、浓缩规则卡 `rule-card.md`（强制约束 SSOT）、交付 HTML 模板 `delivery.html.template`、hook 体系（`hooks/` + `settings.hooks-snippet.json`，PreToolUse 机械门禁）。
- `tools/` — butler **驻留**可执行工具（非规则、非部署模板；目标项目按 `$BUTLER` 路径传参调用、不拷副本）。当前只有 `delivery-selftest/`（交付自测人测回传桥，Node 零依赖）。
- 发布元数据 — `VERSION`（版本号机器 SSOT）、`CHANGELOG.md`（人读发布史）、`migrations/`（升级迁移配方）、`deliveries/`（交付总结存档）。
- 其它子系统 — `Learner/`（学习事务）、`Composer/`（杂项事务），与 `Coder/` 并列、本知识文件夹不展开。

## 成熟度（真源里没有的"现状"层）

- **成熟稳定**：三层分层、P1–P5 产物链、四件套 schema、迭代 / 里程碑双层台账、版本 / 迁移 / 交付规则——体系骨架，已跑满两个里程碑。
- **较新、已落地**：知识文件夹契约（MILE-0003，已由 R8/v2.0.0 首次真实 dogfood 落地——butler 自身即文件夹态）、帮手名册（MILE-0003 R1/R4）、说人话三条硬标准（MILE-0003 R7）。
- **最新、契约层未踩过**：`references-schema`（MILE-0004 R1，`.ai/references/` 索引 + 渐进读 + 无损切片契约地基）——只定契约、切分/入口/钉版/同步动作留 R2–R5，正确性待后续真踩上来才完全证伪。
- **实验性**：`/dangerous` 无人值守自治、`/preference` 偏好反哺——护栏齐但真实使用少。
- **欠债**：hook 门禁在 butler 仓自身不 live 运行、`/butler-upgrade` 从未真跑，见 `debt.md`。

## 指针

- 目录 + 读序 + 各规则一句话职责：`Coder/README.md`（真源，不在此重复）。
- 分层与启用关系：`Coder/architecture-overview.md`。
