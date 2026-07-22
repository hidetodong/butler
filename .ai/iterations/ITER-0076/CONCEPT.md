> 分流: 完整 | 命中升级信号: 契约变更、跨模块影响、设计取舍、多文件改动 | 2026-07-22

# 一句话

- R1 已能区分“这是哪份需求”，但还不能约束“这份需求允许改哪些包”。R2 建立一张稳定工作区地图，再让每份需求用工作区键声明主要实现、配套可写、只读和排除范围，目录移动时不用重写历史 PRD。

# Goal

- 定义项目级工作区地图、稳定工作区键和需求级四类代码范围，使 monorepo 中的计划与后续实际修改能共享同一边界语言。

# Current Understanding

- 路径不是稳定身份：`apps/web` 可能搬到 `products/web`，历史需求仍应指同一个 workspace key。
- package manifest 的包名通常比目录稳定，应优先作为身份来源；没有 manifest 的目录才显式分配项目内稳定键。
- 需求范围需要区分主实现与配套写入，避免“允许写”退化为整个 monorepo；只读上下文和明确排除还要能机械拒绝写入。
- 单模块范围只能收窄整份需求范围，不能借模块表扩大；越界必须先修改范围事实并重新审查，不能边写边追认。

# Constraints

- R2 只定声明式契约与结果形态；不实现 P4 写入拦截、git diff 对账或自动发现器，这些属于 R8。
- 不按工作区复制或嵌套 PRD；跨包需求仍只有一个 `prd_id`。
- 单包仓库也能用同一模型退化为 `root` 工作区，不强迫伪造 monorepo。
- 工作区键稳定、路径可变；路径变化不得重写历史需求身份。
- 现有 `.ai/project/` 仍是项目知识层，工作区地图落在其中并参与收口折叠。

# Impact Scope

- 新增 `Coder/40_Context_Management/workspace-scope-schema.md`。
- 更新 references schema 的单需求索引职责与 `Coder/README.md` 注册。
- 新增结构合同测试；更新本迭代状态、证据与交付。
- 不改 hook、TECH_PLAN 写入门禁、migration、命令或外部项目。

# Project Type / Active Profiles

- Markdown 规则仓 + Python/Bash 工具 + Claude/Codex/Pi 适配。
- 未命中领域 profile，仅按通用 SOP；危险模式 ON。

# Open Questions

- R8 如何从 TECH_PLAN 与 git diff 机械消费范围、如何处理生成文件和跨项目路径，留给门禁迭代，不阻塞契约定义。
