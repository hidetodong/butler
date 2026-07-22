分流: 完整 | 命中升级信号: 多文件改动、契约变更、关键路径、跨模块影响、设计取舍 | 2026-07-22

# 一句话目标

把已经声明的 PRD 工作区范围变成可发现、可计划、能检查真实改动、并由双宿主 hook 在写入前拦截的机器边界，再用完整链路和真实 apps 样本证明 MILE-0009 可收口。

> ⚠️ 危险模式：本产物由模型自主推进（ITER-0082，2026-07-22），施工授权上限为 Butler 仓。

# Context

- R1–R7 已交付需求集合、范围声明、收件箱、迁移、首切/status 和 update 事务；R8 只补最后的执行消费者与版本级回归。
- `workspace-scope-schema.md` 已规定稳定键、四类范围和扩张纪律，但明确写着自动发现、计划映射、diff 对账、生成文件归属与 hook 门禁尚未实现。
- 真实 `WorkCode.nosync/apps` 是多包 npm 仓，仍保留扁平 PRD、非标准 queued 里程碑和五份 closed AC，适合做兼容样本；本轮只读原仓，在临时副本中验证迁移，不把危险模式当仓外授权。

# Problem

- 现在只能“声明允许改哪些包”，工具无法回答地图是否来自真实 manifest、TECH_PLAN 是否越界、Git 改动是否落在允许范围，hook 也不会拦 read-only/excluded/未声明包。
- 根级共享配置、生成文件和嵌套工作区没有确定归属时，简单的最长路径匹配会误放行或误拦截。
- 仅有各工具专项测试不足以证明“收件箱 → 多 PRD → 钉版 → 迁移/update → 范围执行”这一整条版本目标成立。

# Goal

- 提供一个标准库范围工具，共享一套解析器给 CLI 与 hook；发现默认零写，所有歧义 fail-closed。
- 让 P3 显式列出本迭代计划写入的 workspace，验证工具和 hook 都从 AC 的 `prd_refs` 解析同一批钉版范围。
- 用临时多包 fixture 覆盖发现、计划、实际 diff、生成/共享路径、双宿主写入和完整 MILE-0009 链路；用真实 apps 只读快照证明迁移指南面对旧布局/历史引用仍成立。

# In Scope

- workspace 自动发现与现有地图校验；显式共享/生成路径归属。
- TECH_PLAN 工作区写计划合同、Git diff/显式路径对账、PreToolUse 范围规则。
- Claude/Codex 共同内核接线、部署/升级副本同步说明、专项与端到端 CI。
- apps 原仓只读取证，临时副本执行 inspect/plan/apply/verify/rollback 和历史引用核对。

# Out of Scope

- 不写 apps 原仓，不自动接受范围扩张，不自动改 PRD/AC/TECH_PLAN。
- 不实现 shell 命令级拦截；hook 只覆盖宿主送入的 Edit/Write/MultiEdit/apply_patch。
- 不把没有 PRD 引用的普通迭代强制套用虚假工作区范围。
- 不切版本、不提交、不推送。

# Constraints

- 项目根、宿主授权和需求范围三层取交集；任何一层拒绝都不能被另两层放行。
- 新 parser 必须零第三方依赖、拒绝 symlink 逃逸、重复键、重叠归属和未知字段；输出稳定 JSON。
- hook 只读且 fail-closed；没有 `prd_refs` 时受控 N/A，不影响现有非 PRD 工作流。
- 当前工作树承载 R1–R7 未提交改动，无法提供干净 Git 回滚点；R8 必须保持窄文件面、禁止破坏性 Git 操作，并在交付披露这一事实。

# Impact

- 规则：workspace scope、TECH_PLAN/VERIFY/README 与部署说明。
- 工具：新增 `tools/workspace-scope/`，CI 接入。
- 宿主：新增共享 hook rule；Claude 部署副本与 Codex 驻留 wrapper 自动复用同一实现。
- 验证：范围专项、hook 集成、MILE-0009 e2e、apps 只读/临时副本 dogfood。

# Open Questions / Risks

- apps 现状含非标准 queued 里程碑；迁移工具必须保留历史 bytes 或明确报告，不得借 dogfood 顺手规范化用户项目。
- shell 写入不经过当前 hook；CLI 的 diff 检查是交付门，不能宣称宿主层覆盖所有写通道。
- 极大 monorepo 的 manifest 扫描成本需通过声明 patterns 限界，禁止递归 node_modules。
