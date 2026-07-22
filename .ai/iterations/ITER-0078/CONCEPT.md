> 分流: 完整 | 命中升级信号: 新命令、可执行工具、状态写入、跨宿主、批量路由 | 2026-07-22

# 一句话

- R3 只规定收件箱该长什么样，用户仍不能真正扫描 `origin/` 或看到哪些材料变了。R4 交付一个标准库扫描器和 `/butler:inbox` 双宿主入口：机器负责确定性事实，模型负责语义分类，确认后才调用既有 PRD/ideation/milestone 流程。

# Goal

- 让收件箱具备可执行、幂等、跨宿主一致的扫描—分析—确认—路由闭环。

# Current Understanding

- 文件发现、hash、source_id 和 ledger 重写适合确定性工具；“这是新需求还是新版”需要读内容做语义判断，不应伪装成文件名启发式。
- scanner 只维护 Sources 的机械字段，不能写成功 Derivations 或 actual_route。
- 批量路由遇到 `.ai/MILESTONE.md`、CONCEPT/AC/TECH_PLAN 或 ideation 活工作区时，必须逐项延后而非覆盖。
- 新 workflow 必须进 registry，由生成器维护 frontmatter/openai/docs/软链投影；现有“恰好 10 个”合同需整体升级到 11。

# Constraints

- Python 标准库，零新依赖；只写 `.ai/INBOX.md`，绝不写 `origin/`。
- 默认先 plan/preview；真正路由需要用户确认，危险模式用自审门替代但必须留 RUN_LOG。
- 对 ambiguous/duplicate-candidate 不自动定案。
- 不在 scanner 内实现 PRD/里程碑/ideation 算法，只调用现有工作流真源。
- 保留管理区外 INBOX 内容的策略必须明确；不以简单覆盖丢用户注释。

# Impact Scope

- 新增 `Coder/40_Context_Management/inbox-workflow.md`、`tools/inbox/` 与测试。
- 新增 Claude command、Codex skill、registry 项并同步投影/文档/计数。
- 更新 inbox schema 的 canonical managed block 约定。
- 不修改 origin 文件、PRD split/update 算法或 P1–P5 核心状态机。

# Project Type / Active Profiles

- Markdown 规则仓 + Python/Bash 工具 + Claude/Codex/Pi 适配。
- 未命中领域 profile；危险模式 ON。

# Open Questions

- 语义分类由宿主模型完成，CLI 只输出事实 JSON；这是真实能力边界，不阻塞实现。
