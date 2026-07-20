> 分流: 完整 | 命中升级信号: 多文件改动, 跨模块影响, 设计取舍 | 2026-07-19

# 一句话
Butler 已经有 Claude Code 和 Codex 两个宿主适配器，现在 Pi 也能发现 and 加载 Butler 的 skills 和 AGENTS.md，唯独缺一个写操作流程门禁。本迭代给 Pi 写一个 TypeScript 扩展，用 Pi 的 `tool_call` 事件拦截 `write`/`edit`，调 Butler 现有的 Python 判断模块做阶段产物检查，让 Pi 成为第三个完整支持的宿主。

# Goal
- 给 Butler 新增 Pi 宿主适配器，使 Pi 用户部署 Butler 后享有与 Claude Code / Codex 同等的流程门禁保护
- 不能复制规则、不双写判断逻辑：Pi 扩展只做薄薄的路由层，复用 `templates/hooks/rules/` 下已有的 Python rule modules

# Current Understanding

## Pi 已经能做什么
- Skills：Pi 遵循 Agent Skills 标准，`.agents/skills/` 下的 8 个 Butler skill 已自动发现
- AGENTS.md：Pi 启动时读取项目根 `AGENTS.md`，Butler 的冷启动读序、规则卡等已经生效
- `.ai/` 状态层：Pi 有 `read`/`write`/`edit`/`bash` 工具，跟 Claude Code/Codex 一样读写同一份 `.ai/`
- Butler 驻留工具：goal-assurance、verification-evidence 等 Python 工具通过 `bash` 调用

## Pi 缺什么
Pi 没有 Codex 的 `hooks.json` 机制，所以 Butler 的 PreToolUse（写前查阶段产物）和 PostToolUse（写后追加提醒）在 Pi 上不存在。Pi 的等价机制是 **TypeScript 扩展** 的 `tool_call` 事件——可以拦截工具调用并返回 `{ block: true }`。

## 方案概要
1. 新建 `plugins/butler-pi/`，放一个 TypeScript 扩展
2. 扩展在 `tool_call` 事件中拦截 `write`/`edit`，判断目标路径是否属于已部署 Butler 项目
3. 命中则 `exec` 调 Python 判断模块（`butler_gate.py`），拒绝时返回 `{ block: true }`
4. PostToolUse 提醒同样复用 `butler_advisor.py`
5. `scripts/setup.sh` 新增安装步骤，把扩展软链到 `~/.pi/agent/extensions/`
6. 更新相关文档（双宿主 → 多宿主措辞）

# Constraints
- 不改 Butler 规则内核：`Coder/` 和 `templates/hooks/rules/` 一字不动
- 不复制判断逻辑：Pi 扩展调 Python，不把 phase_gate 等逻辑用 TypeScript 重写
- 安装方式跟 Codex plugin 一致：软链到 Pi 的 extensions 目录，`setup.sh` 统一管理
- Pi 扩展在非 Butler 项目零开销：没检测到 `.ai/` + `BUTLER_PATH` 就直接透传

# Impact Scope

## 会影响
- `plugins/butler-pi/`：新增目录，含 `index.ts` + `package.json`
- `scripts/setup.sh`：新增 Pi 扩展安装步骤（检测 Pi CLI 是否存在、幂等软链）
- `docs/codex-compatibility.md`：措辞从"双宿主"升级为"多宿主"，增加 Pi 适配层说明
- `Coder/README.md`：目录结构里增加 `plugins/butler-pi/` 条目
- `templates/AGENTS.md.template`：可能需要微调（Pi 的 AGENTS.md 目前跟 Codex 共用同一模板）
- 可能新增 CI 验证脚本：`scripts/verify-pi-extension.sh`

## 不影响
- `Coder/` 全部规则文件
- `templates/hooks/rules/` Python 判断模块
- `.ai/` 状态层契约
- 已有的 Claude Code / Codex 适配器
- `templates/rule-card.md`

# Project Type / Active Profiles
- 本仓是 Butler 规则仓库自身，编辑的是规则基础设施
- 未命中特定 Domain/Stack Profile，按通用 SOP 推进

# Open Questions
- Pi 的 `tool_call` 事件是否覆盖所有写路径？Pi 目前四个内置工具是 `read`/`write`/`edit`/`bash`，`bash` 理论上也能写文件（`echo >`、`mv` 等）。是否也要拦截 `bash`？——倾向首版只拦 `write`/`edit`，`bash` 透传（跟 Codex hook 的 matcher `apply_patch|Edit|Write` 对齐，Codex 也不拦 shell）
- Pi 扩展是否需要 `BUTLER_BYPASS` 等价机制？——需要，读 `.ai/bypass-reason.md` 非空则放行，跟现有逻辑一致
- 安装时 Pi CLI 不可用要不要报错？——跟 Codex 一样降级警告、不阻塞 setup.sh
