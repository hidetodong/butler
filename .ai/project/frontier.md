# frontier（当前形态 / 活跃战线 / 下一个瓶颈）

> 变得最快的一层。战线收了就覆盖删除，不叠历史。

## 当前形态

- **版本**：v2.12.0。MILE-0006 R1 / ITER-0051 已交付 Codex 兼容地基：仓根 `AGENTS.md` 原生发现、固定 `.ai/` 冷启动读序、目标项目模板、双宿主架构契约和零依赖结构自检。上一版 v2.11.0 是“说中文、不写翻译腔”的规则增量。
- **里程碑**：MILE-0006「Codex 双宿主兼容层」active；R1 closed，R2–R4 planned；当前无 active 迭代。
- **宿主现状**：Claude Code 能力保持完整；Codex 已能在 Butler 仓根自动读到规则入口并恢复共同状态。目标项目尚不会自动生成 `AGENTS.md`，8 个工作流尚未做成 skills/plugin，Codex hooks 尚未适配 `apply_patch`。
- **共同内核**：`Coder/`、`.ai/` 与 `templates/rule-card.md` 继续作为宿主无关真源；`CLAUDE.md` / `.claude/**` 和 `AGENTS.md` / 后续 `.codex/**` 只做薄适配。

## 活跃战线

- MILE-0006 R2：把 8 个 `/butler:*` 工作流映射为 Codex skills，建立 plugin 骨架、全局安装路径和仓库级 fallback。
- R2 不处理 hooks；现有 Python gate 对 Codex `apply_patch` 输入不兼容，留给 R3。

## 下一个瓶颈

- 用 `plugin-creator` / `skill-creator` 形成不复制规则算法的 8 个薄 skills，并验证显式触发与语义触发。
- 随后的 R3 必须让 Codex PreToolUse/PostToolUse 真正覆盖 `apply_patch`，避免规则“能读但门禁静默失效”。
- R4 才把 `AGENTS.md.template` 接入首次部署、升级和双端回归；v2.12.0 不对既有目标项目自动落双入口。
