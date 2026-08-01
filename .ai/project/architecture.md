# architecture（模块地图）

> 只摘全貌 + 补成熟度。目录树、读取顺序、各规则一句话职责的**真源在 `Coder/README.md`**（"目录结构" + "规则目录说明" 两节），此处不抄。分层关系真源 `Coder/architecture-overview.md`。

## 三层主干（`Coder/`，所有任务默认走）

三层职责分明、不互窜（这是头号不变量，见 `invariants.md`）：

- **SOP Core**（`00`/`20`/`30`/`40`）——通用主干，任何任务默认加载。
  - `00_System_Prompt` — 协作身份 + 总调度逻辑 + 输出呈现协议（结论先行 / 统一标号 / 表格化 / 说人话）。
  - `20_Workflow_Lifecycle` — P1→P5 状态机 + 四件套 schema + 迭代 / 里程碑 / 版本 / 迁移 / 交付 / 部署规则。**最大一层、骨架所在**。
  - `30_Quality_Gate` — linting / 测试策略 / 复核标准 + P4 常驻底线（纠错契约 `correction-contract`、最小实现纪律 `implementation-discipline`）。
  - `40_Context_Management` — 状态外化、冷启动读序、handoff、知识文件夹契约（`project-digest-schema` 管项目自身全貌 / `references-schema` 管外部参考资料 `.ai/references/` 的索引与渐进读契约 / `prd-split` 管把大 PRD 切成 `prd/` 切片的首切动作 / `prd-update` 管 PRD 改版同步）、角色切换。
- **Domain / Stack Profiles**（`10`）——按项目技术栈**识别后才启用**（vue3 / typescript / build-tooling），不默认前置。
- **Business Extension**（`99`）——业务侧**最高优先级**约束，若存在则压过通用 SOP。当前仓内只有 `.gitkeep`（占位）。

## 扩展模块（按需 / 命令触发，不进冷启动必读）

- `50_Extension_Ideation` — 脑暴 `/ideation`。
- `55_Extension_ConvergenceLoop` — 收敛闭环 `/butler:loop`（P4 纠错的高强度升档）。
- `60_Extension_CodeReview` — 代码复核 `/review`（共享审查流程真源）。
- `62_Extension_Agents` — **帮手名册**：butler 派出去干活的临时子 agent（复核 / 更新说明 / 查过时三帮手 + 通用规矩 G1–G4 唯一真源）。触发式加载、定义不下发到目标项目。
- `65_Extension_Dangerous` — 危险模式 `/butler:dangerous`（实验性无人值守长程自治外壳）。
- `70_Extension_Preference` — 偏好探针 `/butler:preference`（学真人选择、外置存储、反哺 opt-in）。

## 支撑目录（仓库根）

- `plugins/butler/` — Codex 可安装发布包，`skills/` 内 1 个 Router 与 13 个业务工作流是实体真源；`.agents/skills/` 只用相对软链提供 repo discovery。个人 marketplace 安装/刷新由 `scripts/install-codex-plugin.sh` 编排官方 helper 与 CLI。
- `workflows/registry.json` + `scripts/sync-workflow-registry.py` — schema v2 登记不参与候选的 Router 元入口，以及 13 个业务工作流的双宿主名称、路径、风险、隐式策略、触发、优先级/排除/冲突/前置、旧名和分发元数据；生成/校验 57 个窄投影与唯一人读表，正文算法仍留在 `Coder/`。
- `.github/workflows/ci.yml` + `scripts/verify-ci.sh` — PR/main/release tag 的 Ubuntu/macOS 编排层与唯一 local/CI 执行入口；Python/依赖由 `.python-version`、`pyproject.toml`、`uv.lock` 固定，workflow 不复制测试清单。

- `templates/` — 部署到目标项目的两入口模板、强制规则卡 SSOT、交付 HTML 模板和共享 hook 体系；两入口由 `scripts/render-project-entrypoints.py` 统一渲染，施工根由 `templates/hooks/lib/project_root.py` 的单一算法解析（`scripts/resolve-project-root.py` 是 CLI 薄壳），hook rules 由 Claude/Codex dispatcher 共用。
- `scripts/configure-global-install.py` — 全局安装的安全配置边界：统一规划 shell、Claude 配置、`butler.md` 根命令和 `butler/` 命名空间双软链，再以同目录暂存 + 原子替换应用；`setup.sh` 只负责编排与外部 plugin 状态回声，所有中文后缀旁的变量都用显式边界保留真实退出码。
- `tools/` — butler **驻留**可执行工具（非规则、非部署模板；目标项目按 `$BUTLER` 路径传参调用、不拷副本）。包括 `iteration-intake/`（会话结晶后的零写 plan、事务开迭代与回滚）、`project-config/`（严格项目配置 schema、原子读写、legacy 兼容投影与纯迁移计划）、`butler-upgrade/`（manifest 驱动的 dry-run/项目事务升级器）、`verification-evidence/`（自动道真实命令/exit/log/hash 证据）、`delivery-selftest/`（人测回传桥）与 `codex-validators/`（固定的官方 plugin/skill validators）。
- 发布元数据 — `VERSION`（版本号机器 SSOT）、`CHANGELOG.md`（人读发布史）、`migrations/manifest.json`（可执行版本/action 链）+ `migrations/v*.md`（人读配方）、`deliveries/`（交付总结存档）。

## 成熟度（真源里没有的"现状"层）

- **双宿主适配（MILE-0006）**：R1–R4 全部交付——AGENTS 发现、10 skills/plugin、apply_patch hooks、统一 setup、目标双入口部署/升级和隔离回归矩阵。详细边界真源 `docs/codex-compatibility.md`。
- **工程化加固（MILE-0007）**：R1–R5 全部交付——安装器事务安全、机器证据/状态审计、固定工具链与双 OS CI 合同、可执行升级器、工作流注册/分发收敛。远端 required check 与团队/公共 marketplace 仍是明确外部边界，未冒称启用。

- **成熟稳定**：三层分层、P1–P5 产物链、四件套 schema、迭代 / 里程碑双层台账、版本 / 迁移 / 交付规则——体系骨架，已跑满两个里程碑。
- **较新、已落地**：知识文件夹契约（MILE-0003，已由 R8/v2.0.0 首次真实 dogfood 落地——butler 自身即文件夹态）、帮手名册（MILE-0003 R1/R4）、说人话三条硬标准（MILE-0003 R7）。
- **最新、未端到端踩过**：MILE-0004 references/PRD 版本化子系统**六块齐（R1–R6 全落地，随 v2.1.0 发布收官）**——`references-schema`(R1 契约地基 + R6 §9 非回归门) + `prd-split`(R2 切分动作层) + `/milestone` 大 PRD 并进入口(R3) + AC 钉版 `prd_version` 接进 P2/P3/P5(R4，验收对钉住版核而非 live 最新) + `prd-update` 改版同步 `/prd update`(R5 主流程 + R6 §4.2 认亲松边：改名/合并/拆分启发式提候选→确认、绝不自动认、拿不准退回基础态) 均已落地；"绝不切碎/逐字保真/soft 对齐/亮牌不自动/松边不硬认/非回归门 git diff 为空"护栏与钉版的跨改版审计价值靠执行遵从、待真切一份大 PRD + 真跑一次改版才完全兑付。**ITER-0042（触发加固，待 v2.2.0）**：首次实战（Confluence 地址经 MCP 直读当 `/milestone` brief）暴露软触发漏切——MILESTONE 建了但 `references/prd/` 没切；已三层补——注入表按内容类型（非来源）路由 + `milestone §6.4` PRD 分类闸前移为合成前必过 + 新增 PostToolUse advisory 兜 MILESTONE 落盘点。
- **实验性**：`/butler:dangerous` 无人值守自治、`/butler:preference` 偏好反哺——护栏齐但真实使用少。
- **欠债**：hook 门禁在 butler 仓自身不 live 运行、`/butler:upgrade` 从未真跑，见 `debt.md`。

## 指针

- 目录 + 读序 + 各规则一句话职责：`Coder/README.md`（真源，不在此重复）。
- 分层与启用关系：`Coder/architecture-overview.md`。
