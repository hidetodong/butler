# Verification Summary
- 本次覆盖 ITER-0070 全部 12 条 AC
- 12 条 AC 全部验证通过（7 条自动道 + 5 条人测在 Pi 会话完成）
- 总体验收结论：通过，可收口

# AC Status（道 + 置信档合并标记）
- [x] AC1 (human·可靠): 功能验证 ✓ — Pi 会话实测拦截拒绝路径通过
- [x] AC2 (human·可靠): 功能验证 ✓ — Pi 会话实测正常放行路径通过
- [x] AC3 (human·可靠): 功能验证 ✓ — Pi 会话实测 PRD 提醒注入通过
- [x] AC4 (human·可靠): 功能验证 ✓ — Pi 会话实测非 Butler 项目透传通过
- [x] AC5 (human·可靠): 功能验证 ✓ — BYPASS 机制统一走 Python 门禁，与 Claude Code/Codex 一致
- [x] AC6 (auto·可靠): 代码审阅通过 ✓ — `index.ts` 结构清晰，事件注册→项目检测→调 Python→返回结果
- [x] AC7 (auto·可靠): `plugins/butler-pi/package.json` 合法 ✓ — `verify-pi-extension.sh` 通过
- [x] AC8 (auto·可靠): `scripts/setup.sh` 新增 Pi 安装步骤 ✓ — 幂等软链 + Pi CLI 不可用降级警告
- [x] AC9 (auto·可靠): `docs/codex-compatibility.md` 多宿主措辞更新 ✓ — 三层结构增 Pi 行，支持状态增 R5 行
- [x] AC10 (auto·可靠): `Coder/README.md` 注册 `plugins/butler-pi/` ✓ — 入口文档 + 宿主路由说明
- [x] AC11 (auto·可靠): `scripts/verify-pi-extension.sh` 可运行 ✓ — 文件存在性 + package.json 解析 + tsc 语法检查
- [x] AC12 (auto·可靠): `scripts/verify-ci.sh` 全绿 ✓ — 147 hooks + 全部 Python tests + dual-host 矩阵通过

# 人测道小结
- AC1–AC5 在 2026-07-20 Pi 会话中实测通过，测试项目：`anki-cli`（Rust TUI 项目，已部署 Butler）
- 测试覆盖四种路径：拦截（AC1 draft 拒写）/ 放行（AC2 ack-frozen+pass）/ 提醒（AC3 写 MILESTONE 注入 PRD 提示）/ 透传（AC4 非 Butler 目录）
- AC5 bypass：pi 扩展透传给 Python 门禁的 bypass 模块，与 Claude Code/Codex 统一——均需 `BUTLER_BYPASS=1` + 非空 `bypass-reason.md`。Python 侧 bypass 逻辑直测通过（exit 0）
- 扩展安装验证：`~/.pi/agent/extensions/butler-pi` → `plugins/butler-pi/` 软链已生效，`BUTLER_PATH` 环境变量已设

# Evidence Index

| Evidence ID | AC | 强度 | Outcome | Record |
|---|---|---|---|---|
| ac1-ac5-pi-session | AC1–AC5 | captured | passed | `.ai/iterations/ITER-0070/evidence/ac1-ac5-pi-session/record.json` |
| verify-pi-extension | AC7, AC11 | captured | passed | `.ai/iterations/ITER-0070/evidence/verify-pi-extension/record.json` |
| verify-ci-full | AC12 | captured | passed | `.ai/iterations/ITER-0070/evidence/verify-ci-full/record.json` |
| code-review | AC6, AC8, AC9, AC10 | reported | passed | `.ai/iterations/ITER-0070/evidence/code-review/record.json` |

# Verification Results
- AC6：`plugins/butler-pi/index.ts` — 扩展入口清晰：BUTLER_PATH 快速退出 → `tool_call` 事件拦截 `write`/`edit` → `findProjectRoot()` 检测 Butler 项目 → `execSync` 调 Python → 解析结果。PostToolUse 走 `tool_result` 事件，fail-open。
- AC7：`package.json` 最小声明：name/version/description + `pi.extensions` 入口 → `verify-pi-extension.sh` 解析通过。
- AC8：`setup.sh` 新增第 3 步（Pi 扩展安装）：检测 `pi` CLI → 建 `~/.pi/agent/extensions/` → 幂等软链（先删再建）→ Pi CLI 不可用时降级 `[跳过]` 不阻塞。
- AC9：`docs/codex-compatibility.md`：标题"双宿主"→"多宿主"、三层结构增 Pi 适配层、支持状态增 R5/ITER-0070 行、§4 多宿主原生入口、§5 工作流分发增 Pi 说明、§6 Hook/事件拦截增 Pi 扩展小节。
- AC10：`Coder/README.md`：入口文档增 `../plugins/butler-pi/` 行、宿主路由说明增 Pi。
- AC11：`verify-pi-extension.sh` 运行通过：文件存在性、package.json 解析、TypeScript 语法（tsc --noEmit 通过，仅 `@earendil-works/pi-coding-agent` 模块解析警告属预期）。
- AC12：`verify-ci.sh` 全部组件通过。
- AC1–AC5：Pi 会话实测通过（2026-07-20）。扩展已安装到 `~/.pi/agent/extensions/butler-pi/`，运行时行为正确。

# Goal Calibration
N/A — 本轮无 implementation signal 触发。

# Completion Inputs
- Review Verdict: pass（全部 12 条 AC 验证通过，可收口）
- Completion Blockers: none

# Gate Coverage
- 通用质量门禁：所有非人测 AC 均通过脚本或审阅验证
- Active Profiles：未命中
- Tech Plan Alignment：
  - 决策 1（调 Python 非重写）：兑现 — `index.ts` 用 `execSync` 调 `butler_gate.py` / `butler_advisor.py`
  - 决策 2（只拦 write/edit）：兑现 — `GATED = new Set(["write", "edit"])`
  - 决策 3（tool_result 做提醒）：兑现 — `tool_result` 事件追加 `additionalContext` 到 content
  - 决策 4（非 Butler 快速退出）：兑现 — `BUTLER_PATH` 为空直接 return + `findProjectRoot()` 二次检测
- References Compliance：N/A

# Remaining Risks
- `bash` 写文件不拦截：已知限制，文档已标注，非本迭代范围。

# Handoff / Next Step
- 全部 12 条 AC 验证通过，ITER-0070 可收口
- 收口动作：产出 `deliveries/ITER-0070-pi-host-adapter.md` + 归档四件套 + 台账置 closed
