# ITER-0070 · Pi 宿主适配器

## 本次交付目标

- 给 Butler 新增 Pi 宿主适配器，让 Pi 用户享有与 Claude Code / Codex 同等的流程门禁。
- 不修改规则内核，只做薄壳路由：TypeScript 扩展拦截 `write`/`edit`，调 Python 判断模块。

## 已完成内容

- 新建 `plugins/butler-pi/`：`index.ts` + `package.json`，Pi 扩展入口。
- `tool_call` 事件拦截 `write`/`edit`，调 `butler_gate.py` 做 PreToolUse 门禁（缺产物→拒绝+原因，齐全→放行）。
- `tool_result` 事件调 `butler_advisor.py` 做 PostToolUse 提醒（写 MILESTONE 后注入 PRD 切分提示）。
- 非 Butler 项目（无 `.ai/` 或无 `BUTLER_PATH`）快速退出，零开销透传。
- BYPASS 机制统一走 Python 门禁，与 Claude Code / Codex 一致。
- `scripts/setup.sh` 新增第 3 步：检测 Pi CLI → 幂等软链到 `~/.pi/agent/extensions/`，不可用时降级不阻塞。
- 文档措辞升级：`docs/codex-compatibility.md` 双宿主→多宿主，三层结构增 Pi 适配层。
- `Coder/README.md` 注册 `plugins/butler-pi/` 条目。
- CI：新增 `scripts/verify-pi-extension.sh`，完整 CI 矩阵（147 hooks + Python tests + dual-host）全绿。

## 关键变更 / 用户可感知变化

- Pi 用户在已部署 Butler 的项目中尝试 `write`/`edit` 时，会被门禁拦截或放行，与 Claude Code/Codex 体验一致。
- 写 `.ai/MILESTONE.md` 后自动收到 PRD 切分提醒（非阻塞）。
- 非 Butler 项目完全不受影响，零感知。
- 新机器跑一次 `setup.sh` 即可自动安装 Pi 扩展。

## 高层影响范围

- `plugins/butler-pi/` — 新增 Pi TypeScript 扩展。
- `scripts/setup.sh` — 新增 Pi 扩展安装步骤。
- `docs/codex-compatibility.md` — 多宿主措辞升级。
- `Coder/README.md` — 目录注册。
- `scripts/verify-pi-extension.sh` — 新增 CI 脚本。

## 验证方式与结果摘要

- 全部 12 条 AC 验证通过：7 条自动道（代码审阅 + CI + 脚本）+ 5 条人测（Pi 会话实测拦截/放行/提醒/透传/BYPASS 五路径）。
- Pi 会话实测项目：`anki-cli`（Rust TUI 项目，已部署 Butler）。
- 完整 CI 通过：147 hooks + Python tests + dual-host 矩阵 + verify-pi-extension。

## 已知剩余风险 / 延后事项

- `bash` 写文件不拦截：已知限制，文档已标注，与 Codex hook 对齐（也不拦 shell）。
- Pi 扩展不发布到 plugin marketplace：只做本地软链安装，与 Codex personal plugin 同级。

## 引用

- `.ai/iterations/ITER-0070/AC_LIST.md`
- `.ai/iterations/ITER-0070/CONCEPT.md`
- `.ai/iterations/ITER-0070/TECH_PLAN.md`
- `.ai/iterations/ITER-0070/VERIFY_REPORT.md`
- `plugins/butler-pi/index.ts`
- `plugins/butler-pi/package.json`
