---
方案状态: draft
方案审查日期: —
方案审查方式: —
---

# Goal
支撑 AC1–AC12，实现 Pi 宿主适配器：TypeScript 扩展 + 安装脚本 + 文档 + CI。

# Files / Modules to Change

| 文件 | 操作 | 职责 |
|---|---|---|
| `plugins/butler-pi/index.ts` | 新增 | Pi 扩展入口：注册 `tool_call` 和 `tool_result` 事件，拦截 `write`/`edit`，调 Python 门禁 |
| `plugins/butler-pi/package.json` | 新增 | 最小包声明：name、version、`pi.extensions` 入口 |
| `scripts/setup.sh` | 修改 | 新增第 3 步：检测 Pi CLI、幂等软链扩展到 `~/.pi/agent/extensions/` |
| `docs/codex-compatibility.md` | 修改 | 三层结构增加 Pi 适配层、支持状态表增加 Pi 行、措辞"双宿主"→"多宿主" |
| `Coder/README.md` | 修改 | 目录结构增加 `plugins/butler-pi/`，插件分发说明增加 Pi 安装方式 |
| `scripts/verify-pi-extension.sh` | 新增 | CI 脚本：检查 `index.ts` 语法（`npx tsc --noEmit`）、`package.json` 合法性、文件存在性 |
| `migrations/v2.18.0.md` | 新增 | 切版时产出，含 `[sync-hooks]` → `[add-file]` Pi 扩展安装步骤 |

# Interface / Contract

## 扩展与 Python 门禁的接口

Pi 扩展不重新实现判断逻辑，而是构造跟 Claude Code hook 相同的 JSON 输入，通过 stdin 交给 `butler_gate.py` 和 `butler_advisor.py`。

输入 JSON 格式（与现有 hook 兼容）：
```json
{
  "tool_name": "Write",
  "tool_input": { "file_path": "<目标路径>" },
  "cwd": "<当前工作目录>"
}
```

- PreToolUse：调 `butler_gate.py`，exit 0 = 放行，exit 2 = 拦截（block + reason）
- PostToolUse：调 `butler_advisor.py`，stdout 非空时把 `additionalContext` 注入模型上下文（提醒，不阻塞）

## Pi 工具名映射

Pi 的内置工具名跟 Claude Code 不同：

| Pi 工具 | 传给 Python 的 tool_name |
|---|---|
| `write` | `Write` |
| `edit` | `Edit` |

`read` 和 `bash` 不拦截（跟 Codex hook 只拦 `apply_patch|Edit|Write` 对齐）。

# State / Boundary

- 扩展本身无状态，每次 `tool_call` 事件独立判断
- 项目状态全在 `.ai/` 文件中，由 Python 模块读取
- 扩展在非 Butler 项目直接 return（零开销），不调 Python
- 不修改任何 `.ai/` 文件、不写项目状态
- 不在 Pi 扩展里做 Goal 投影或任何宿主原生能力调用——只做门禁

# Design Decisions

## 决策 1：调 Python 而非重写 TypeScript

**选**：`child_process.execSync` 调 `butler_gate.py` / `butler_advisor.py`
**弃**：用 TypeScript 重写 phase_gate、ledger_status 等判断逻辑

理由：
- DRY：判断模块是 Butler 的真源，Python 版本是唯一实现
- 维护：规则变更时不用同步两套代码
- 风险：`execSync` 每次调用启动 Python 进程有 ~50ms 开销，但 `write`/`edit` 是低频操作，可以忽略

## 决策 2：只拦 `write`/`edit`，不拦 `bash`

理由：
- 对齐：Codex hook 的 matcher 是 `apply_patch|Edit|Write`，也不拦 shell
- 可行：Pi 的 `bash` 工具可能用于 `echo > file` 这种写操作，但拦截 `bash` 太粗暴，会严重影响正常使用
- 诚实：文档里说明 `bash` 不在门禁范围内，Butler 的流程保护从来不是沙箱级安全边界

## 决策 3：用 `tool_result` 事件做 PostToolUse 提醒

Pi 的 `tool_result` 事件在工具执行后、结果返回给模型前触发，可以修改 `content`。跟 Codex 的 `PostToolUse` 的 `additionalContext` 注入不完全一样——Pi 这边只能改工具结果内容，不能直接往上下文注入。做法：在 `tool_result` 返回的 content 里追加提醒文案，模型一样能看到。

## 决策 4：非 Butler 项目检测逻辑

扩展加载时检查 `BUTLER_PATH` 环境变量——没设就整个扩展不注册事件（最快路径）。事件触发时再检查目标路径是否在已部署 Butler 项目内（通过 `.ai/` 目录存在性），双重保险。

# Plan Admission

## AC Coverage
- AC1–AC2（拦截/放行）：`tool_call` 事件 + `butler_gate.py` 覆盖
- AC3（PRD 提醒）：`tool_result` 事件 + `butler_advisor.py` 覆盖
- AC4（非 Butler 透传）：`BUTLER_PATH` 检查 + `.ai/` 检测覆盖
- AC5（BYPASS）：透传给 `butler_gate.py`，其内部已处理 `bypass-reason.md`
- AC6–AC7（扩展结构）：代码审阅覆盖
- AC8（setup.sh）：脚本测试覆盖
- AC9–AC10（文档）：diff 审阅覆盖
- AC11（verify-pi-extension.sh）：CI 运行覆盖
- AC12（回归）：`verify-ci.sh` 覆盖

## Assumptions
1. Pi 的 `tool_call` 事件参数中 `path` 字段对应目标文件路径（Pi write 工具的参数）——已验证，Pi 的 write 工具参数是 `{ path, content }`
2. Pi 的 `edit` 工具参数中 `path` 字段同样对应目标文件路径——已验证，Pi 的 edit 工具参数是 `{ path, edits[] }`
3. Pi 扩展中 `process.env.BUTLER_PATH` 可访问——已验证，Pi 扩展运行在 Node.js 环境，可直接读环境变量
4. `execSync` 在 Pi 扩展中可用——已验证，Pi 扩展允许使用 Node.js 内置模块

## Alternatives / Trade-offs

**替代方案 A：纯 TypeScript 重写判断逻辑**
- 优势：无进程启动开销、类型安全
- 代价：规则双写、每次规则变更要同步两处、容易漂移
- 结论：弃用。DRY 是 Butler 的核心原则（"不维护两套规则算法"）

**替代方案 B：Pi skill 而非 extension**
- 优势：更简单，用户手动调用
- 代价：skill 是被动调用（用户触发），不是自动拦截。门禁必须是无感的自动行为，skill 做不到
- 结论：弃用。门禁必须是自动事件拦截，不能用 skill

## Failure Modes
1. Python 未安装或 `butler_gate.py` 不可用 → `execSync` 抛异常 → 扩展 fail-closed，返回 block
2. `BUTLER_PATH` 指向错误路径 → 跟 1 一样，`execSync` 失败 → fail-closed
3. Pi 的 `edit` 工具参数格式变化 → `event.input.path` 为空 → 扩展跳过不处理（fail-open，因为无法判断目标）
4. 扩展本身有语法错误 → Pi 加载扩展时失败 → Pi 会报告扩展加载错误，不影响其他功能

## Impact / Scope Challenge
- 是否真的需要新增迁移配方？——需要。v2.18.0 切版时部署了 Butler 的项目要知道怎么装 Pi 扩展
- 是否真的需要 verify-pi-extension.sh？——CI 覆盖需要。但可以最小化（只做语法检查和文件存在性）
- 是否可以用更简单的方式实现门禁而不写 TypeScript 扩展？——不能。Pi 没有 hooks.json 等价物，扩展是唯一的事件拦截机制

## Verification Blind Spots
- 无法自动测试 Pi 扩展在真实 Pi 环境中的行为——CI 里没有 Pi CLI。verify-pi-extension.sh 只做静态检查，手工测试覆盖运行时行为（见 AC1–AC5 的 Verification Method）
- `bash` 工具写的文件不被拦截——已知限制，文档里诚实说明
- Pi 未来增加新写工具（如在 Pi 扩展中注册的自定义工具）——不被拦截，新工具需要更新本扩展的白名单

## Verdict
**pass** — 方案覆盖全部 12 条 AC，关键决策（调 Python）守 DRY 原则，失败模式 fail-closed，没有已知 Must Fix。

# Execution Steps

- [ ] T1 新建 `plugins/butler-pi/package.json` → AC7
- [ ] T2 新建 `plugins/butler-pi/index.ts`：扩展骨架 + BUTLER_PATH 检测 + 事件注册 → AC6
- [ ] T3 实现 PreToolUse 拦截：构造 JSON → execSync 调 butler_gate.py → 解析 exit code → AC1, AC2, AC4, AC5
- [ ] T4 实现 PostToolUse 提醒：tool_result 事件 → execSync 调 butler_advisor.py → 追加提醒 → AC3
- [ ] T5 修改 `scripts/setup.sh`：新增 Pi 扩展安装步骤（检测 CLI、幂等软链、降级警告）→ AC8
- [ ] T6 修改 `docs/codex-compatibility.md`：三层结构增加 Pi 行、支持状态表增加 Pi 行、措辞双宿主→多宿主 → AC9
- [ ] T7 修改 `Coder/README.md`：目录结构增加 `plugins/butler-pi/`、分发说明增加 Pi 安装 → AC10
- [ ] T8 [P] 新建 `scripts/verify-pi-extension.sh`：TypeScript 语法检查 + 文件存在性 → AC11
- [ ] T9 运行 `scripts/verify-ci.sh` 确认全绿 → AC12
- [ ] T10 手工端到端测试：在测试项目中验证拦截/放行/提醒/透传/BYPASS 四种路径 → AC1–AC5

# Verification Plan
- AC1–AC5：手工测试（T10），用 Pi 在已部署 Butler 的测试项目中实际执行 write/edit
- AC6–AC7：代码审阅 T1–T4 产物
- AC8：在无 Pi CLI 和有 Pi CLI 环境分别跑 `setup.sh`，验证幂等与降级
- AC9–AC10：文档 diff 审阅 T6–T7
- AC11：运行 `bash scripts/verify-pi-extension.sh`
- AC12：运行 `bash scripts/verify-ci.sh`

# Risks / Open Questions
- Pi 扩展 API 稳定性：`tool_call` 和 `tool_result` 是 Pi 文档中的公共事件，版本兼容风险低
- `bash` 写文件不被拦截：首版已知限制，文档里标注。后续版本如需加强，可在 Pi 扩展中解析 `bash` 命令（但复杂度高、易误拦）
