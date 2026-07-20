---
状态: ack-frozen
ACK 日期: 2026-07-19
---

# Goal
给 Butler 新增 Pi 宿主适配器：一个 TypeScript 扩展 + setup.sh 安装步骤 + 文档多宿主化，让 Pi 用户享有与 Claude Code / Codex 同等的流程门禁。

# In Scope
- 新建 `plugins/butler-pi/`，放 TypeScript 扩展（`index.ts` + `package.json`）
- 扩展拦截 Pi 的 `write`/`edit` 工具调用，调 Python 判断模块做写前门禁（PreToolUse）和写后提醒（PostToolUse）
- `scripts/setup.sh` 新增 Pi 扩展安装步骤（幂等软链、Pi CLI 不可用时降级警告）
- 文档措辞从"双宿主"升级为"多宿主"：`docs/codex-compatibility.md`、`Coder/README.md`
- CI 验证：新增 `scripts/verify-pi-extension.sh`
- 迁移配方 `migrations/v2.18.0.md`（本次版本号待切版时定）

# Out of Scope
- 拦截 `bash` 工具调用——首版只拦 `write`/`edit`，跟 Codex hook 的 `apply_patch|Edit|Write` 对齐
- Pi plugin marketplace 发布——只做本地软链安装，跟 Codex personal plugin 同级
- 修改 `templates/hooks/rules/` Python 判断模块——不改规则内核
- Pi 的 agent-skills 或 AGENTS.md 模板修改——现有技能和模板已兼容

# Acceptance Checklist
- [ ] AC1：Pi 扩展在已部署 Butler 项目中拦截 `write`/`edit`，阶段产物缺失时拒绝并给出原因
- [ ] AC2：Pi 扩展在阶段产物齐全时正常放行 `write`/`edit`
- [ ] AC3：写 `.ai/MILESTONE.md` 后扩展注入 PRD 切分提醒（PostToolUse advisory，非阻塞）
- [ ] AC4：非 Butler 项目（无 `.ai/` 或无 `BUTLER_PATH`）扩展直接透传，零开销
- [ ] AC5：`.ai/bypass-reason.md` 非空时扩展放行所有写操作（BUTLER_BYPASS 等价机制）
- [ ] AC6：`plugins/butler-pi/index.ts` 结构清晰：事件注册 → 项目检测 → 调 Python → 返回结果
- [ ] AC7：`plugins/butler-pi/package.json` 最小声明（name、version、pi.extensions 入口）
- [ ] AC8：`scripts/setup.sh` 幂等安装 Pi 扩展到 `~/.pi/agent/extensions/`，Pi CLI 不可用时降级警告不阻塞
- [ ] AC9：`docs/codex-compatibility.md` 措辞更新：三层结构增加 Pi 适配层，支持状态增加 Pi 行
- [ ] AC10：`Coder/README.md` 目录结构增加 `plugins/butler-pi/` 条目
- [ ] AC11：`scripts/verify-pi-extension.sh` 可运行：至少检查扩展语法（`npx tsc --noEmit`）和文件存在性
- [ ] AC12：现有 Claude Code / Codex hook 回归：`scripts/verify-ci.sh` 全绿

# Verification Method
- AC1–AC4：手工测试——在已部署 Butler 的测试项目中用 Pi 尝试 `write`/`edit`，验证拦截/放行/提醒/透传四种路径
- AC5：手工测试——创建非空 `.ai/bypass-reason.md` 后验证放行
- AC6–AC7：代码审阅——检查文件结构和内容
- AC8：脚本测试——在无 Pi CLI 和有 Pi CLI 两种环境跑 `setup.sh`，验证幂等和降级
- AC9–AC10：文档审阅——diff 检查措辞变更
- AC11：运行 `bash scripts/verify-pi-extension.sh`
- AC12：运行 `bash scripts/verify-ci.sh`

# External References
- `docs/codex-compatibility.md` — 双宿主兼容架构（本次升级为多宿主措辞）
- `plugins/butler/hooks/hooks.json` — Codex hook 注册格式（Pi 扩展的参考基线）
- `templates/hooks/rules/phase_gate.py` — 阶段产物判断模块（Pi 扩展调用的真源）
- `templates/hooks/rules/prd_split_reminder.py` — PRD 提醒模块

# Open Questions / Risks
- Pi 的 `tool_call` 事件是否在并行工具调用时保证顺序？——不影响：门禁只需检查当前项目状态，不依赖同轮其他工具结果
- Pi 未来版本是否可能改变扩展 API？——风险低，用的是稳定的 `tool_call` 事件，属 Pi 公共 API
