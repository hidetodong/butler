---
title: Codex 双宿主兼容架构
audience: AI / 开发者
scope: Butler 共同内核、Claude Code/Codex 适配层、分阶段支持状态与维护边界
---

# Codex 双宿主兼容架构

Butler 不为 Codex 重写一套规则。兼容方式是保留一个共同内核，再为 Claude Code 和 Codex 分别提供薄入口与运行协议适配。

## 1. 三层结构

| 层 | 内容 | 维护规则 |
|---|---|---|
| 共同内核 | `Coder/`、`.ai/`、`templates/rule-card.md`、`templates/hooks/rules/` 与 `lib/` | 规则算法和状态契约只写在这里 |
| Claude Code 适配层 | `CLAUDE.md`、`.claude/commands/`、部署后的 `.claude/hooks/` 与 settings | 保留现有行为，不为 Codex 改写 |
| Codex 适配层 | `AGENTS.md`、`.agents/skills/`、`plugins/butler/`、后续 `.codex/hooks.json` 或 plugin hooks | 只负责发现、路由、输入输出转换 |

`.ai/` 不属于任何单一宿主。它保存当前目标、验收、方案、验证、台账和跨会话断点；Claude Code 与 Codex 必须读写同一份状态，不能各建副本。

## 2. 单一真源红线

- 强制规则卡只改 `templates/rule-card.md`。`CLAUDE.md.template` 与 `AGENTS.md.template` 都通过 `{{RULE_CARD_CONTENT}}` 注入，不手工抄规则正文。
- P1–P5、迭代、里程碑、PRD、复核和危险模式算法仍在 `Coder/`。commands、skills 和入口文件只能路由到真源。
- Hook 的阶段判断继续复用 `templates/hooks/rules/` 与 `lib/`。宿主差异只放 dispatcher 或输入适配器。
- README、HUMAN_GUIDE 和 Coder 入口只登记能力并回指本文件，不复制整份支持矩阵。

## 3. 支持状态

| 路线 | 能力 | 状态 |
|---|---|---|
| R1 / ITER-0051 | Butler 仓根 `AGENTS.md` 自动发现、`.ai/` 冷启动读序、目标项目模板与兼容架构 | v2.12.0 已交付 |
| R2 / ITER-0052 | 8 个 Butler 工作流迁为 Codex skills，并打包成可安装 plugin | v2.13.0 已交付 |
| R3 | Codex PreToolUse/PostToolUse 配置、`apply_patch` 输入适配、拒绝与提醒端到端验证 | 计划中 |
| R4 | setup、首次部署、既有升级、迁移配方和 Claude/Codex 双端回归矩阵 | 计划中 |

因此，v2.13.0 可以说“Codex 能原生发现 Butler 仓库规则，并通过 plugin 使用 8 个工作流入口”，仍不能说“Butler 已在 Codex 中全面兼容”。机械门禁和目标项目自动生成 `AGENTS.md` 仍要等 R3/R4。

## 4. Codex 原生入口

Codex 会在开始工作前读取仓库级 `AGENTS.md`，并允许在更深目录放置更具体的覆盖文件。Butler 的根入口保持短小：只放常驻约束、验证命令和读序，复杂规则继续按指针读取。这也避免撞上 Codex 项目指令的默认大小预算。

- 官方说明：[Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md.md)
- Butler 仓入口：`AGENTS.md`
- 目标项目模板：`templates/AGENTS.md.template`

不把 `CLAUDE.md` 配成 Codex fallback 作为正式方案：fallback 是个人机器设置，不能随仓保证。原生 `AGENTS.md` 才是团队可版本化的契约。

## 5. 工作流与分发方向

Codex 官方把可重复工作流放在 skills 中，再用 plugin 做可安装分发。Butler 的发布真源是 `plugins/butler/skills/`；`.agents/skills/` 的 8 个相对软链让仓内开发态也能发现同一批 skill，不产生第二份正文。

8 个入口是 `$butler-prd`、`$butler-review`、`$butler-milestone`、`$butler-upgrade`、`$butler-ideation`、`$butler-preference`、`$butler-loop` 和 `$butler-dangerous`。前 6 个允许语义触发；后两个高风险入口在 `agents/openai.yaml` 禁止隐式调用，必须显式点名。所有入口都从 `BUTLER_PATH` 读取 `Coder/` 真源。

- 官方说明：[Customization](https://learn.chatgpt.com/docs/customization/overview.md)、[Build skills](https://learn.chatgpt.com/docs/build-skills)
- 安装/刷新：`bash scripts/install-codex-plugin.sh`；它使用官方 creator/cachebuster/validator 与 `codex plugin add`，安装后新开 Codex thread 生效。
- 结构回归：`bash scripts/verify-codex-workflows.sh`。
- 不创建 custom prompts；官方已把它们标为弃用路线。

## 6. Hook 当前边界

Codex 支持 `PreToolUse`、`PostToolUse` 等生命周期事件，项目配置从受信任仓库的 `.codex/hooks.json` 或 `.codex/config.toml` 加载；非托管 hook 还需要用户检查并信任。事件名字相近不代表现有 Butler hook 已可直接使用。

当前 `templates/hooks/butler_gate.py` 和 `butler_advisor.py` 仍按 Claude Code 输入编写：

- 只接受 `Edit`、`Write`、`MultiEdit`。
- 从 `tool_input.file_path` 找目标文件。
- 修改内容按 `content`、`old_string/new_string` 或 `edits` 读取。

Codex 的主要写文件调用是 `apply_patch`。即使 matcher 用 `Edit|Write` 能触发该调用，当前 dispatcher 也会因内部工具名和 patch 结构不同而直接放行。所以在 R3 完成前，**Codex 写文件没有 Butler 机械阶段门禁**；只能依赖 `AGENTS.md` 规则纪律，不能把它报告成 hook 绿。

- 官方说明：[Hooks](https://learn.chatgpt.com/docs/hooks.md)
- R3 必须验证：单文件 patch、多文件 patch、创建/删除/移动、拒绝信息、PostToolUse 提醒和 hook trust。

## 7. 安全边界

Butler 的流程规则不能覆盖 Codex 自身的 sandbox、审批、hook trust、项目 trust 或企业管理策略。`/butler:dangerous` 的“无人值守”只改变 Butler 的 P2/P3 决策方式，不等于绕过宿主权限；权限不足时必须如实停下。

## 8. 维护检查

修改 Codex 入口、目标模板或本文后运行：

```bash
bash scripts/verify-codex-foundation.sh
bash scripts/verify-codex-workflows.sh
```

修改共享 hook 判断模块时，还要运行：

```bash
python3 -m pytest templates/hooks/tests -q
```

两个宿主出现差异时，先判断它属于“规则算法”还是“宿主协议”。前者回共同内核，后者留在对应适配层；不要用复制正文解决协议差异。
